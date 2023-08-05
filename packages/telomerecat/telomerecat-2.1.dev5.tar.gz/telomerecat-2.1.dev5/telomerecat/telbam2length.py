import sys
import textwrap
import time
import os
import re
import random
import parabam
import pdb

import numpy as np

from shutil import copy
from itertools import izip
from collections import namedtuple

#from scipy.stats import beta as beta_dist
import telomerecat.simulator as simulator
from _version import __version__

######################################################################
##
##      Create a length estimate given a set of TELBAMS 
##
##      Author: jhrf
##
######################################################################

class QCLogic(object):

    def __init__(self,qual_mean,qual_sd,phred_offset,max_qual,min_qual):
        self._phred_offset = phred_offset
        self._qual_mean = qual_mean
        self._qual_sd = qual_sd
        self._max_qual = max_qual
        self._min_qual = min_qual
        self._error_thresh = 10

    def get_beta_thresh(self,thresh):
        pass
#        alpha,beta = self.get_beta_dist_fit()
#        return beta_dist.ppf(thresh,alpha,beta)

    def get_beta_dist_fit(self):
        dist_max = self._max_qual - self._min_qual
        dist_min = 0

        qual_mean_adjust = (self._qual_mean - self._min_qual) / (self._max_qual - self._min_qual)
        qual_var_adjust = ( (self._qual_sd**2) / ((self._max_qual - self._min_qual)**2))

        core = ( ((qual_mean_adjust*(1-qual_mean_adjust)) / qual_var_adjust) -1 )

        alpha = qual_mean_adjust * core
        beta = (1-qual_mean_adjust) * core

        return alpha, beta

    def get_error_thresh(self,thresh=0):
        def thresh_workings(thresh):
            return (self._qual_mean - (self._qual_sd*thresh)) - self._phred_offset
        return thresh_workings(thresh)

    def get_read_qc_status(self,read):
        return self.get_read_qc_score(read) > self._error_thresh

    def get_read_qc_score(self,read):
        read_score = np.mean([ord(q) - self._phred_offset for q in read.qual])
        return read_score

class ReadLogic(object):

    def __init__(self,phred_offset=35,qc_logic=None,
                    error_profiles=None,
                    error_thresh=10,read_len=100):

        self._SimpleRead = namedtuple("SimpleRead",
                                      "seq qual complete five_prime "+
                                            "pattern read_status "+
                                            "mima_loci qc_pass")
        self._phred_offset = phred_offset

        self._compliments = {"A":"T","T":"A",
                             "C":"G","G":"C",
                             "N":"N"}

        self._read_len = read_len

        self._error_profiles = error_profiles
        self._error_thresh = error_thresh

        self._complete_decision = self.__complete_decision__
        if qc_logic is not None:
            self._qc_logic = qc_logic
        else:
            self._qc_logic = QCLogic(0, 1, 0, 1, 0)

        self._templates = self.__get_compare_templates__(["TTAGGG","CCCTAA"])

    def __is_complete__(self,seq,qual,pattern):
        if pattern:
            mismatch_loci,fuse_loci = self.__get_mismatch_loci__(seq,pattern)
            return self._complete_decision(seq,qual,mismatch_loci,pattern),mismatch_loci
        return False,range(len(seq))

    def __complete_decision__(self,seq,qual,mismatch_loci,pattern,N=50):
        mismatch_loci_count = len(mismatch_loci)

        if mismatch_loci_count == 0:
            return True
        else:
            mismatch_loci_score = \
                        np.mean([ord(qual[i])-self._phred_offset for i in mismatch_loci])
            return mismatch_loci_score < 15 and mismatch_loci_count < 15

    def __get_random_score__(self,qual,N):
        random_quals = random.sample(qual,N)
        return sum(random_quals)

    def __get_loci_score__(self,loci,qual):
        qual_ints = []
        for i in loci:
            qual_ints.append( ord(qual[i]) - self._phred_offset )

        if len(qual_ints) > 0:
            return int((sum(qual_ints)))
        return 0

    def __check_error_profile__(self,mismatch_loci,qual,pattern):
        if self._error_profiles is not None:
            score = self.__error_profile_score__(mismatch_loci, qual)
            if score < 400:
                return self._error_profiles[pattern][len(mismatch_loci),score]
        return False

    def __error_profile_score__(self,mismatch_loci,qual):
        return np.mean([ord(qual[loci]) - self._phred_offset \
                                for loci in mismatch_loci])

    def __get_pattern__(self,seq):
        cta,tag = "CCCTAA","TTAGGG"
        pattern = None
        if cta in seq or tag in seq:   
            if seq.count(cta) > seq.count(tag):
                pattern = cta
            elif seq.count(tag) > seq.count(cta):
                pattern = tag
        return pattern

    def __get_compare_templates__(self,patterns):
        templates = {}

        for pattern in patterns:
            templates[pattern] = {}

            overshoot = (self._read_len / len(pattern)) + 1
            for i in xrange(len(pattern)):
                reference = pattern[len(pattern)-i:] \
                     + (pattern * overshoot)
                reference = reference[:self._read_len]

                templates[pattern][i] = reference

        return templates

    def confident_mima_debug(self,simple_reads):
        read_status_complete = [len(read.mima_loci) == 0 for read in simple_reads]

        if any(read_status_complete) and not all(read_status_complete):
            for read in simple_reads:
                if len(read.mima_loci) > 10:
                    print "-"
                    avg_read_score = np.mean([ord(q) - 33 for q in read.qual])
                    avg_mima_score = np.mean([ord(read.qual[i]) - 33 for i in read.mima_loci])

                    print read.seq,"%.1f" % (avg_mima_score,),avg_read_score,len(read.mima_loci)
                    print "".join(["1" if i in read.mima_loci else "0" for i in xrange(len(read.seq))])
                    print read.qual,read.five_prime


    def get_read_type(self,read1,read2):
        # READ TYPE
        simple_reads = self.get_simple_reads( (read1,read2,) )
        qc_pass = [read.qc_pass for read in simple_reads]

        is_complete = [read.complete for read in simple_reads]

        read_type = "F3"
        pat_counts = {}
        if all(qc_pass):
            for read in simple_reads:
                if read.pattern is None:
                    continue
                pat_count = read.seq.count(read.pattern)
                pat_counts["%s_count" % read.pattern] = pat_count

            if all(is_complete):
                read_type =  "F1"
            elif any(is_complete):
                read_type = self.__check_orientation__(simple_reads)
        return read_type,pat_counts

    def __check_orientation__(self, simple_reads):
        #This function is only called when at least 
        #one read was completely telomeric 
        pattern_is_none = []
        for read in simple_reads:
            if read.pattern is None or read.seq.count(read.pattern) < 2:
                pattern_is_none.append(True)
            else:
                pattern_is_none.append(False)

        prefix = ""
        if any(pattern_is_none):
            prefix = "alt_"

        for read in simple_reads:
            if read.complete:
                if read.five_prime:
                    return prefix+"F2"
                else:
                    return prefix+"F4"

    def get_simple_reads(self,reads):
        simple_reads = []
        for read in reads:
            seq,qual = self.__flip_and_compliment__(read)
            #seq,qual = self.__trim_seq__(seq, qual)
            pattern = self.__get_pattern__(seq)

            complete,mima_loci = self.__is_complete__(seq,qual,pattern)
            five_prime = self.__get_five_prime__(pattern)
                
            simple_read = self._SimpleRead(
                seq,
                qual,
                complete,
                five_prime,
                pattern,
                self.__get_read_status__(complete,seq,pattern),
                mima_loci,
                self._qc_logic.get_read_qc_status(read))

            simple_reads.append(simple_read)
        return simple_reads

    def __get_read_status__(self,complete,seq,pattern):
        if complete:
            return "full"
        elif pattern is not None and seq.count(pattern) > 3:
            return "partial"
        else:
            return "non"

    def __trim_seq__(self,seq,qual):
        lo_qual_offset = self.__lo_qual_offset__(seq, qual)

        #print seq[:lo_qual_offset],qual[:lo_qual_offset]
        return seq[:lo_qual_offset],qual[:lo_qual_offset]

    def __lo_qual_offset__(self,seq,qual):
        offset = 0
        for q in qual:
            if ord(q) - self._phred_offset > 3:
                offset += 1
            else:
                break
        return offset 

    def __get_hash_offset__(self,qual):
        offset = len(qual)
        for q in reversed(qual):
            if q == "#":
                offset -= 1
            else:
                break
        return offset

    def __get_five_prime__(self,pattern):
        if pattern == None:
            return None
        else:
            return pattern == "CCCTAA"

    def __flip_and_compliment__(self,read):
        if read.is_reverse:
            compliments = self._compliments
            seq_compliment = map(lambda base: compliments[base],read.seq)
            seq_compliment = "".join(seq_compliment)
            return(seq_compliment[::-1],read.qual[::-1])
        else:
            return (read.seq,read.qual)

    def simple_read_to_mmloci(self,simple_read):
        return self.__get_mismatch_loci__(simple_read.seq, 
                                          simple_read.pattern)

    def __get_mismatch_loci__(self,seq,pattern):
        simple_mima_loci = self.__get_simple_mmloci__(seq,pattern)
        if len(simple_mima_loci) == 0:
            return [],[]

        segments = re.split("(%s)" % (pattern,), seq)
        segments = self.__join_segments__(segments, pattern)
        mima_loci,fuse_loci = self.__get_damage_loci__(segments,pattern)
        return_loci = [m for m in mima_loci if m in simple_mima_loci]
        return_loci.extend(fuse_loci)
       
        return sorted(return_loci),fuse_loci

    def __get_simple_mmloci__(self,seq,pattern):
        
        best_mima_loci = []
        best_mima_score = len(seq)+1

        for offset,ref in self._templates[pattern].items():
            cur_mima_loci = []
            cur_mima_score = 0
            for i,(s,r) in enumerate(izip(seq,ref)):
                if s != r:
                    cur_mima_loci.append(i)
                    cur_mima_score += 1

                if cur_mima_score > best_mima_score:
                    break
            if cur_mima_score < best_mima_score:
                best_mima_score = cur_mima_score
                best_mima_loci = cur_mima_loci
        return best_mima_loci

    def __get_damage_loci__(self,segments,pattern):
        mmloci = []
        fuse_loci = []
        prev_was_tel = False
        offset = 0

        for segment in segments:
            if pattern in segment:
                if prev_was_tel:
                    fuse_loci.append(offset)
                else:
                    prev_was_tel = True
            else:
                mmloci.extend(xrange(offset,offset+len(segment)))
                prev_was_tel = False
            offset += len(segment)
        return mmloci,fuse_loci
            
    def __join_segments__(self,fragments,pattern):
        segments = []
        current_segment = ""
        prev_was_pattern = False
        for frag in fragments:

            if frag == "":
                continue

            elif current_segment == "":
                current_segment = frag
                prev_was_pattern = (frag == pattern)

            elif frag == pattern:
                if prev_was_pattern:
                    current_segment = current_segment + frag
                else:
                    new_segment = frag
                    count = 0
                    for c,p in izip(reversed(current_segment),reversed(pattern)):
                        if c == p:
                            new_segment = c + new_segment
                            count += 1
                        else:
                            break

                    not_matched = current_segment[:(len(current_segment) - count)]
                    if not_matched != "":
                        segments.append(not_matched)
                    current_segment = new_segment
                    prev_was_pattern = True

            else:
                new_segment = current_segment
                count = 0
                for c,p in izip(frag, pattern):
                    if c == p:
                        new_segment = new_segment + c
                        count += 1
                    else:
                        break
                segments.append(new_segment)
                if count == len(frag):
                    current_segment = ""
                else:
                    current_segment = frag[count:]

                prev_was_pattern = False

        if current_segment != "":
            segments.append(current_segment)
        
        return segments

class VitalStatsFinder(object):

    def __init__(self,temp_dir,total_procs,task_size):
        self._temp_dir = temp_dir
        self._total_procs = total_procs
        self._task_size = task_size

    def __csv_to_dict__(self,stats_path):
        insert_dat = np.genfromtxt(stats_path,delimiter=",",
                                names=True,dtype=("S256",float,float,
                                                         float,float,
                                                         float,float,
                                                         float,float,
                                                         float,float))

        ins_N = int(insert_dat['N'])
        if ins_N == 0:
            insert_mean = -1
            insert_sd = -1
        else:
            ins_sum = int(insert_dat['sum'])
            ins_power_2 = int(insert_dat['power_2'])

            insert_mean,insert_sd = \
                        self.__get_mean_and_sd__(ins_sum, ins_power_2, ins_N)
    
        min_qual = int(insert_dat['min_qual'])
        qual_mean,qual_sd = self.__get_mean_and_sd__(insert_dat["qual_sum"],
                                                    insert_dat["qual_power_2"],
                                                    insert_dat["qual_N"])

        return {"insert_mean":insert_mean, 
                "insert_sd": insert_sd,
                "min_qual":min_qual,
                "max_qual":int(insert_dat['max_qual']),
                "read_len":int(insert_dat['read_len']),
                "qual_mean":qual_mean,
                "qual_sd":qual_sd,
                "effective_min_qual":insert_dat['effective_min_qual']}

    def __get_mean_and_sd__(self,x_sum,x_power_2,x_N):
        x_mean = x_sum / x_N
        x_sd = np.sqrt( (x_N * x_power_2) - x_sum**2) / x_N

        return x_mean,x_sd

    def __run_read_count_engine__(self,sample_path,vital_stats):

        read_len = vital_stats["read_len"]
        phred_offset = vital_stats["phred_offset"]
        matrix_size = 40

        structures = {"tga_read_counts":{"data":np.zeros((read_len,matrix_size)),
                                     "store_method":"cumu"},
                      "cta_read_counts":{"data":np.zeros((read_len,matrix_size)),
                                     "store_method":"cumu"},
                     "random_counts":{"data":np.zeros((read_len,matrix_size)),
                                      "store_method":"cumu"}}

        readlogic = ReadLogic(qc_logic=vital_stats["qc_logic"],
                                phred_offset=phred_offset)

        def engine(reads,master,constant):
            results = {}
            simple_reads = readlogic.get_simple_reads(reads)
            read_types = [read.complete for read in simple_reads]

            for read in simple_reads:
                if read.qc_pass and read.pattern and not read.complete:

                    mismatch_loci,fuse_loci = readlogic.__get_mismatch_loci__(\
                            read.seq,read.pattern)
                    mismatch_qual = readlogic.__error_profile_score__\
                                            (mismatch_loci,read.qual)

                    if len(mismatch_loci) > 0 and mismatch_qual < 420:                    
                        
                        read_counts = np.zeros((read_len,matrix_size))
                        read_counts[len(mismatch_loci),mismatch_qual] = 1
                        if read.pattern == "TTAGGG":
                            results["tga_read_counts"] = {"result":read_counts}
                        elif read.pattern == "CCCTAA":
                            results["cta_read_counts"] = {"result":read_counts}


                    random_loci = random.sample(xrange(len(read.seq)), 
                                   random.randint(1,len(read.seq)-1))
                    random_score = readlogic.__error_profile_score__(random_loci, 
                                                               read.qual)
                    if random_score < 400:
                        random_counts = np.zeros((read_len,matrix_size))
                        random_counts[len(random_loci),random_score] += 1
                        results["random_counts"] = {"result":random_counts}

            return results

        stat_interface = parabam.command.stat.Interface(self._temp_dir)
        out_paths = stat_interface.run(
            input_bams= [sample_path],
            total_procs = self._total_procs,
            task_size = 10000,
            user_constants = {},
            user_engine = engine,
            pair_process=True,
            user_struc_blueprint = structures,
            keep_in_temp=True)

        return out_paths[sample_path]

    def __path_to_profile__(self,read_counts_path,
                                random_counts_path,lo=0,hi=20):

        read_counts = np.genfromtxt(read_counts_path,comments="#",delimiter=",")
        random_counts = np.genfromtxt(random_counts_path,comments="#",delimiter=",")
        read_counts[0,0] = 0

        normalised = read_counts - random_counts
        normalised = normalised * (normalised > 0)

        log_read_counts = np.log(normalised+1)

        ################
        # SIGNAL CHECK #
        ################

        #non_zero_vals =  self.__filter_zero_values__(log_read_counts[:hi,0:hi])
        #mean_zero_vals = non_zero_vals.mean()
        #sd_zero_vals = non_zero_vals.std()
        #cutoff = mean_zero_vals + (sd_zero_vals*1)
        #error_profile = (log_read_counts > (cutoff)) * 1

        error_profile = log_read_counts * 0
        error_profile[:20,:20] = 1

        return error_profile * 1

    # def __patch_profile__(self,error_profile):

    # def __patch_profile__(self,error_profile):
    #     for x in xrange(error_profile.shape[0]):
    #         error_profile[x,(40*x)/3:] = 0
    #     return error_profile
    
    def __filter_zero_values__(self,observations):
        filtered_list = observations.flatten()
        return np.array([x for x in filtered_list if x > 0])

    def get_vital_stats(self,sample_path):

        vital_stats_csv = self.__run_vital_engine__(sample_path)
        vital_stats = self.__csv_to_dict__(vital_stats_csv)
        vital_stats["phred_offset"] = vital_stats["min_qual"]
        vital_stats["qc_logic"] = QCLogic(vital_stats["qual_mean"],
                                           vital_stats["qual_sd"],
                                           vital_stats["phred_offset"],
                                           vital_stats["max_qual"],
                                           vital_stats["min_qual"])

        tga_read_count_path,cta_read_count_path,random_path = \
                        self.__run_read_count_engine__(sample_path, vital_stats)

        tga_profile = self.__path_to_profile__(tga_read_count_path,random_path)
        cta_profile = self.__path_to_profile__(cta_read_count_path,random_path)

        vital_stats["random_path"] = random_path
        vital_stats["tga_read_count_path"] = tga_read_count_path
        vital_stats["cta_read_count_path"] = cta_read_count_path

        vital_stats["error_profiles"] = {"TTAGGG":tga_profile,"CCCTAA":cta_profile}

        return vital_stats

    def __run_vital_engine__(self,sample_path):
        def engine(read,constants,master):
            stats = {}

            byte_vals = map(ord,read.qual)
            min_qual = min(byte_vals)
            max_qual = max(byte_vals)

            stripped = [b for b in byte_vals if b != min_qual]
            if len(stripped) > 0:
                effective_min_qual = min(stripped)
            else:
                effective_min_qual = 999
            
            if read.is_read1 and read.is_proper_pair:
                    insert_size = abs(read.template_length)
                    stats["sum"] = {"result":insert_size}
                    stats["power_2"] = {"result":insert_size**2}
                    stats["N"] = {"result":1}
                        
            qual_mean = np.mean(byte_vals)
            stats["qual_sum"] = {"result":qual_mean}
            stats["qual_power_2"] = {"result":qual_mean**2}
            stats["qual_N"] = {"result":1}

            stats["read_len"] = {"result": len(read.seq)}
            stats["min_qual"] = {"result":min_qual}
            stats["max_qual"] = {"result":max_qual}
            stats["effective_min_qual"] = {"result":effective_min_qual}

            return stats

        structures = {}

        structures["sum"] = {"data":0,"store_method":"cumu"}
        structures["power_2"] = {"data":0,"store_method":"cumu"}
        structures["N"] = {"data":0,"store_method":"cumu"}
        structures["read_len"] = {"data":0,"store_method":"max"}

        structures["min_qual"] = {"data":999,"store_method":"min"}
        structures["max_qual"] = {"data":0,"store_method":"max"}
        structures["effective_min_qual"] = {"data":999,"store_method":"min"}

        structures["qual_sum"] = {"data":0,"store_method":"cumu"}
        structures["qual_power_2"] = {"data":0,"store_method":"cumu"}    
        structures["qual_N"] = {"data":0,"store_method":"cumu"}    

        stat_interface = parabam.command.stat.Interface(self._temp_dir)
        out_paths = stat_interface.run(
            input_bams= [sample_path],
            total_procs = self._total_procs,
            task_size = 10000,
            user_constants = {},
            user_engine = engine,
            user_struc_blueprint = structures,
            keep_in_temp=True)

        return out_paths["global"][0]

class Interface(parabam.core.Interface):
    def __init__(self,temp_dir):
        super(Interface,self).__init__(temp_dir)
        self._compliments = {"A":"T","T":"A","C":"G","G":"C","N":"N"}

    def run_cmd(self,parser):
        cmd_args = parser.parse_args()
        self.run(input_paths = cmd_args.input,
            total_procs = cmd_args.p,
            task_size = cmd_args.s,
            reader_n = cmd_args.f,
            verbose = cmd_args.v,
            inserts_path=cmd_args.insert,
            output = cmd_args.out,
            announce=True)

    def run(self,input_paths,total_procs,task_size,verbose,output,reader_n,
        inserts_path=None,alig_params=None,announce=False,keep_in_temp=False):
        
        if not verbose:
            announce = False
        self.verbose = verbose
        program_name = "telomerecat telbam2length"
        self.__introduce__(program_name,announce)

        names = map(lambda b: self.__get_basename__(b),input_paths)
        names = map(lambda nm: nm.replace("_telbam",""),names)

        output_csv_path = self.__create_output_file__(output)
        vital_stats_finder = VitalStatsFinder(self._temp_dir, 
                                        total_procs,
                                        task_size)
        
        insert_length_generator = self.__get_insert_generator__(inserts_path)

        self.__output__(" Results will be written to the following file:\n",1)
        self.__output__("\t./%s\n\n" % (os.path.basename(output_csv_path,)))

        for sample_path,sample_name, in izip(input_paths,names):
            sample_intro = " Estimating telomere length of sample: %s\n" \
                                                            % (sample_name)

            self.__output__(sample_intro,1)
            self.__output__("\t- Estimation started %s\n" \
                                    % (self.__get_date_time__(),),2)

            self.__output__("\t- Finding read error rates and insert size\n",2)
            vital_stats = vital_stats_finder.get_vital_stats(sample_path)
            self.__check_vital_stats_insert_size__(inserts_path,
                                                    insert_length_generator,
                                                    vital_stats)

            read_type_counts = self.__get_read_types__(sample_path,
                                  vital_stats,total_procs,
                                  task_size,reader_n,
                                  keep_in_temp)

            simulation_results = self.__run_simulation__(vital_stats,
                                                         read_type_counts,
                                                         total_procs)

            read_type_counts.update(simulation_results)

            self.__write_to_csv__(read_type_counts,output_csv_path,sample_name)

            self.__output__("\t- Estimation finished %s\n\n" \
                                            % (self.__get_date_time__(),),2)
        
        self.__goodbye__(program_name,announce)
        if keep_in_temp:
            return output_csv_path
        else:
            self.__copy_out_of_temp__([output_csv_path])
            return os.path.join(".",os.path.split(output_csv_path)[1])

    def __get_insert_generator__(self,inserts_path):
        if inserts_path:
            with open(inserts_path,"r") as inserts_file:
                for line in inserts_file:
                    yield map(float,line.split(","))

    def __check_vital_stats_insert_size__(self,inserts_path,
                                        insert_length_generator,vital_stats):
        if inserts_path:
            insert_mean,insert_sd = insert_length_generator.next()
            vital_stats["insert_mean"] = insert_mean
            vital_stats["insert_sd"] = insert_sd
            self.__output__("\t\t+ Using user defined insert size: %d,%d\n" \
                                                    % (insert_mean,insert_sd),2)
        elif vital_stats["insert_mean"] == -1:
            default_mean,default_sd = 350,25
            vital_stats["insert_mean"] = 350
            vital_stats["insert_sd"] = 25
            self.__output__("\t\t+ Failed to estimate insert size. Using default: %d,%d\n"\
                                                % (default_mean,default_sd),2)

    def __get_read_types__(self,sample_path,vital_stats,total_procs,task_size,
                                          reader_n,keep_in_temp):
        self.__output__("\t- Categorising reads into telomeric read types\n",2)
        read_type_counts = self.__run_read_type_engine__(sample_path,
                                        vital_stats,task_size,
                                        total_procs,
                                        reader_n)

        self.__output__("\t\t+ F1:%d | F2a:%d | F2b+F4:%d\n" % \
                                                (read_type_counts["F1"],
                                                 read_type_counts["F2a"],
                                                  read_type_counts["F2b_F4"],),2)
        return read_type_counts

    def __create_output_file__(self,output):
        if output:
            unqiue_file_ID = output
        else:
            unqiue_file_ID = "telomerecat_length_%d-%s.csv" % (time.time(),
                                                               __version__,)

        output_csv_path = os.path.join(self._temp_dir,unqiue_file_ID)
        with open(output_csv_path,"w") as total:
            header =\
             "Sample,F1,F2a,F2b_F4,Uncertainty,Insert_mean,Insert_sd,Length\n"
            total.write(header)
        return output_csv_path

    def __output__(self,outstr,level=-1):
        if self.verbose and (self.verbose >= level or level == -1):
            sys.stdout.write(outstr)
            sys.stdout.flush()

    def __write_to_csv__(self,read_type_counts,output_csv_path,name):
        with open(output_csv_path,"a") as counts:
            counts.write("%s,%d,%d,%d,%.3f,%.3f,%.3f,%d\n" %\
                (name,
                read_type_counts["F1"],
                read_type_counts["F2a"],
                read_type_counts["F2b_F4"],
                read_type_counts["uncertainty"],
                read_type_counts["insert_mean"],
                read_type_counts["insert_sd"],
                read_type_counts["length"]))

    def __run_simulation__(self,vital_stats,read_type_counts,total_procs):
        self.__output__("\t- Using read counts to estimate length\n",2)
        total_F2 = read_type_counts["F2a"]
        total_f1 = read_type_counts["F1"]
        read_length = vital_stats["read_len"]
        insert_mean = vital_stats["insert_mean"]
        insert_sd =   vital_stats["insert_sd"]

        len_mean,len_std = simulator.run_simulator_par(insert_mean,insert_sd,
                                        total_f1,total_F2,
                                         total_procs,read_length,N=16)

        self.__output__("\t\t+ Length: %d\n" % (len_mean,),2)

        return {"insert_mean":insert_mean,
                "insert_sd":insert_sd,
                "length":len_mean,
                "uncertainty":len_std}
        
    def __run_read_type_engine__(self,sample_path,vital_stats,
                                        task_size,total_procs,reader_n):

        read_logic = ReadLogic(
                error_profiles=vital_stats["error_profiles"],
                phred_offset=vital_stats["phred_offset"],
                read_len = vital_stats["read_len"],
                qc_logic = vital_stats["qc_logic"])

        def engine(reads,constants,parent):
            results = {}
            read_type,pat_counts = read_logic.get_read_type(*reads)
            results[read_type] = {"result":1}
            return results

        structures = {"F1":{"data":0,"store_method":"cumu"},
                      "F2":{"data":0,"store_method":"cumu"},
                      "F4":{"data":0,"store_method":"cumu"},
                      "alt_F4":{"data":0,"store_method":"cumu"},
                      "alt_F2":{"data":0,"store_method":"cumu"},
                      "F3":{"data":0,"store_method":"cumu"},
                      "TTAGGG_count":{"data":0,"store_method":"cumu"},
                      "CCCTAA_count":{"data":0,"store_method":"cumu"},
                      }

        interface = parabam.command.stat.Interface(self._temp_dir)
        output_files = interface.run(input_bams=[sample_path],
                            total_procs = total_procs,
                            reader_n = reader_n,
                            task_size = 10000,
                            user_constants = {},
                            user_engine = engine,
                            user_struc_blueprint = structures,
                            keep_in_temp = True,
                            pair_process = True)

        return self.__parabam_results_to_dict__(output_files["global"][0])

    def __parabam_results_to_dict__(self,csv_path):
        results_array = np.genfromtxt(csv_path,
                                    delimiter=",",
                                    names=True,
                                    comments="#",
                                    dtype=("S256",float,float,float,
                                                    float,float,float,
                                                        float,float))

        called_F2 = results_array["F2"].tolist()
        total_F4 = results_array["F4"].tolist()
        total_F1 = results_array["F1"].tolist()

        total_F2a = called_F2 - total_F4 #Find the F2a by removing the
                                          #probablistic amount of F2bs
                                          #For each F4 we assume an F2b thus

        total_F2b_F4 = total_F4 * 2 #Reflect the removal of F2b from F2a
                                     #by inflating the F4 count
        
        #tga_count = results_array["TTAGGG_count"].tolist()
        #cta_count = results_array["CCCTAA_count"].tolist()
        #total_F2a = (cta_count - tga_count) / 33.333
        #total_F1 = cta_count / 16.666

        return {"F1":int(total_F1),"F2b_F4":int(total_F2b_F4),
                "F2a":int(total_F2a),
                "F2a_F2b":int(called_F2)}

    def __copy_out_of_temp__(self,file_paths,copy_path="."):
        map(lambda fil: copy(fil,copy_path),file_paths)

    def get_parser(self):
        parser = self.default_parser()
        parser.description = textwrap.dedent(
        '''\
        telomerecat telbam2length v%s
        ----------------------------------------------------------------------

            The telbam2length command allows the user to genereate a telomere
            length estimate from a previously generated TELBAM file.

            Example useage:

            telomerecat telbam2length /path/to/some_telbam.bam

            This will generate a .csv file with an telomere length estimate
            for the `some_telbam.bam` file.

        ----------------------------------------------------------------------
        ''' % (__version__,))

        parser.add_argument('input',metavar='TELBAM(S)', nargs='+',
            help="The telbam(s) that we wish to analyse")
        parser.add_argument('--out',metavar='CSV',type=str,nargs='?',default=None,
            help='Specify output path for length estimation CSV.\n'+\
                'Automatically generated if left blank [Default: None]')
        parser.add_argument('--insert',metavar='CSV',nargs='?',type=str,default=None,
            help="A file specifying the insert length mean and std for\n"+\
                 "each input sample. If not present telomerecat will\n"+\
                 "automatically estimate insert length of sample [Default: None]")
        parser.add_argument('-v',choices=[0,1,2],default=0,type=int,
            help="Verbosity. The amount of information output by the program:\n"\
            "\t0: Silent [Default]\n"\
            "\t1: Output\n"\
            "\t2: Detailed Output")

        return parser

if __name__ == "__main__":
    print "Do not run this script directly. Type `telomerecat` for help."
