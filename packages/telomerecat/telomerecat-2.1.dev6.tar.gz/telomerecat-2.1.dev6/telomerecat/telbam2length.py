import sys
import textwrap
import time
import os
import re
import random
import parabam
import pdb

import numpy as np
import pandas as pd

from shutil import copy
from numpy import genfromtxt,mean,sqrt,\
                  rot90,tril,log,zeros,std
from numpy import round as np_round
from itertools import izip,combinations
from collections import namedtuple,Counter

from sklearn import mixture
from pprint import pprint as ppr

import simulator

######################################################################
##
##      Create a length estimate given a set of TELBAMS 
##
##      Author: jhrf
##
######################################################################

class PatternLogic(object):

    def get_non_telo_patterns(self,seq,pattern):
        patterns = Counter()

        for pattern in self.pattern_generator(seq,pattern):
            patterns[pattern] += 1

        return patterns 

    def pattern_generator(self,seq,pattern):
        patterns = re.split("%s" % \
                        (pattern,), seq)

        qual_offset = 0
        for pattern in patterns:
            if pattern == '':
                continue
            #elif len(pattern) >= 6:
            offset = 0
            while pattern[offset:offset+7]:
                trim_seq = pattern[offset:offset+7]
                if offset == 0:
                    yield self.__modify_pattern__(trim_seq,pattern)
                elif offset > 0 and len(trim_seq) >= 6:
                    yield trim_seq
                offset += len(trim_seq)
        return

    def get_error_patterns(self,pattern_path):
        pattern_dict = self.__path_to_pattern_dict__(pattern_path)
        error_patterns = []

        compliments = {"A":"T","C":"G",
                   "G":"C","T":"A",
                   "N":"N"}

        for pattern,count in pattern_dict.items():
            pattern_compliment = "".join([compliments[p] for p in pattern])
            pattern_compliment = pattern_compliment[::-1]

            try:
                compliment_count = pattern_dict[pattern_compliment]
                ratio = count / float(compliment_count)
            except KeyError:
                compliment_count = 0
                ratio = float("Inf")

            if ratio > 2.5 and (count+compliment_count) > 200:
                error_patterns.append(pattern)
                #print pattern,ratio,count+compliment_count

        return error_patterns


    def __path_to_pattern_dict__(self,pattern_path):

        pattern_dict = {}
        with open(pattern_path,"r") as pattern_file:
            for line in pattern_file:
                pattern,count = line.strip().split(",")
                count = int(np.round(float(count)))
                pattern_dict[pattern] = count
        return pattern_dict

    def __modify_pattern__(self,pattern,parent_pattern):
        print_pattern = pattern
        if len(pattern) < 4:
            if parent_pattern == "TTAGGG":
                print_pattern = "TTAGGG" + pattern
            else:
                print_pattern = pattern + "CCCTAA"
        return print_pattern

class QCLogic(object):

    def __init__(self,vital_stats):
        self._phred_offset = vital_stats["phred_offset"]
        self._qual_mean = vital_stats["qual_mean"]
        self._qual_sd =  vital_stats["qual_sd"]
        self._max_qual =  vital_stats["max_qual"]
        self._min_qual = vital_stats["min_qual"]
        self._error_thresh = 15 #self.get_beta_thresh(0.01)

    def get_beta_thresh(self,thresh):
        alpha,beta = self.get_beta_dist_fit()
        return (self._max_qual - self._min_qual) *\
                         (beta_dist.ppf(thresh,alpha,beta))

    def get_beta_dist_fit(self):
        dist_max = self._max_qual - self._min_qual
        dist_min = 0

        qual_mean_adjust = (self._qual_mean - self._min_qual) / (self._max_qual - self._min_qual)
        qual_var_adjust = ( (self._qual_sd**2) / ((self._max_qual - self._min_qual)**2))

        core = ( ((qual_mean_adjust*(1-qual_mean_adjust)) / qual_var_adjust) - 1 )

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
        read_score = self.get_qual_qc_score(read.qual)
        return read_score

    def get_qual_qc_score(self,qual):
        qual_score = np.mean([ord(q) - self._phred_offset for q in qual])
        return qual_score

    def get_qual_qc_status(self,qual):
        return self.get_qual_qc_score(qual) > self._error_thresh

class SimpleReadFactory(object):

    def __init__(self,vital_stats=None,conduct_tests = True,
                    test_weights = None):
        self._SimpleRead = namedtuple("SimpleRead","seq qual" +
                                      " five_prime pattern mima_loci"+
                                      " test_data read_score complete")

        self._conduct_tests = conduct_tests
        
        if vital_stats is not None:
            if conduct_tests:
                #self._error_patterns = vital_stats["error_patterns"]
                self._qc_logic = vital_stats["qc_logic"]
                #self._error_profiles = vital_stats["error_profiles"]

            self._read_len = vital_stats["read_len"]
            self._phred_offset = vital_stats["phred_offset"]
            self._max_qual = vital_stats["max_qual"] - vital_stats["phred_offset"]
            
        else:
            self._read_len = 100
            self._phred_offset = 33

        self._templates = self.__get_compare_templates__(["TTAGGG","CCCTAA"])
        self._compliments = {"A":"T","T":"A",
                             "C":"G","G":"C",
                             "N":"N"}

        self._complete_thresh = 700

        if test_weights is None:    
            self._weights = {'column_score': 6.6083,
                     'cumulative_qual': -3.783,
                      'first_pattern': -3.3225,
                       'highest_qual_deviation': -9.3971,
                        'inverse_mima_count': 19.456,
                         'mima_count': -12.8864,
                          'pattern_count': 15.0844,
                           'signif_poor_mima': 9.2827,
                            'trim_thresh': 21.2162}
        else:
            self._weights = test_weights

    def get_simple_read(self,read):
        seq,qual = self.__flip_and_compliment__(read)
        seq,qual = self.__trim_seq__(seq,qual)
        pattern = self.__get_pattern__(seq)

        mima_loci,frameshift_loci,pattern = self.__get_mima_loci__(seq,qual,pattern) #complete
        
        test_data,read_score,is_complete = {},0,False 
        if self._conduct_tests:
            if len(mima_loci) == 0:
                read_score = (self._complete_thresh + 1)
                is_complete = True
            else:
                test_data = self.__run_tests__(seq, 
                                                qual, 
                                                pattern, 
                                                mima_loci, 
                                                frameshift_loci)

                read_score = self.__test_data_to_score__(test_data)
                is_complete = self.__complete_logic__(read_score)
            
        simple_read = self._SimpleRead(
            seq,
            qual,
            self.__get_five_prime__(pattern),
            pattern,
            mima_loci,
            test_data,
            read_score,
            is_complete)

        return simple_read

    def __trim_seq__(self,seq,qual):
        cutoff = 0
        for q in qual:
            qual_byte = ord(q) - self._phred_offset
            if qual_byte <= self._weights["trim_thresh"]:
                break
            cutoff += 1

        return seq[:cutoff],qual[:cutoff]

    def __test_data_to_score__(self,test_data):
        score = 0
        weights = self._weights
        for test_name,test_result in test_data.items():
            if test_name in weights:
                weight = self._weights[test_name]
            else:
                weight = 1

            score += test_result * weight

        return score

    def __complete_logic__(self,read_score):

        is_complete = False
        if read_score >= self._complete_thresh:
            is_complete = True

        return is_complete

    def __get_five_prime__(self,pattern):
        if pattern is None:
            return None
        else:
            return pattern == "CCCTAA"

    def __run_tests__(self,seq,qual,pattern,mima_loci,frameshift_loci):
        if len(mima_loci) == 0:
            #This read is a genuine complete read
            return {}
        else:
            test_dict = {}

            #self.__error_seq_ratio__(seq,pattern,mima_loci,test_dict)
            #self.__gc_range__(seq,test_dict)
            #self.__recurrant_deviation_count__(seq,pattern,test_dict)
            #self.__check_error_profile__(mima_loci,qual,pattern,test_dict) 
            #self.__average_mima_loci__(seq,mima_loci,test_dict)
            #self.__non_cannon_count(seq,pattern,test_dict)
            #self.__qc_score__(qual,test_dict)
            #self.__frameshift_count__(frameshift_loci,test_dict)
            #self.__mima_gaps__(seq,mima_loci,test_dict)

            self.__significantly_poor_mima_loci__(qual, mima_loci, test_dict)
            self.__mima_count__(mima_loci,test_dict)
            self.__inverse_mima_count__(seq,mima_loci,test_dict)
            self.__pattern_count__(seq,pattern,test_dict)
            self.__highest_qual_deviation__(mima_loci,qual,test_dict)
            self.__cumulative_qual__(mima_loci,qual,test_dict)
            self.__first_pattern__(seq,pattern,test_dict)
            self.__column_score__(seq,mima_loci,test_dict)

            return test_dict

    def __first_pattern__(self,seq,pattern,test_dict):
        if pattern in seq:
            test_dict["first_pattern"] = seq.find(pattern)
        else:
            test_dict["first_pattern"] = len(seq)

    def __column_score__(self,seq,mima_loci,test_dict):

        comparison_vector = []
        for i,s in enumerate(seq):
            if i in mima_loci:
                comparison_vector.append(1)
            else:
                comparison_vector.append(0)

        pattern_div = len(seq)/6 
        comparison_vector = comparison_vector[:pattern_div*6]
        comparison_matrix = np.array(comparison_vector).reshape(pattern_div,6)
        test_dict["column_score"] = (np.max(comparison_matrix.sum(0)) \
                                     - np.median(comparison_matrix.sum(0))) * 4

    def __cumulative_qual__(self,mima_loci,qual,test_dict):
        qual_sum = 0
        for i in mima_loci:
            qual_sum += (ord(qual[i]) - (self._phred_offset+1))
        test_dict["cumulative_qual"] = qual_sum / float(26)

    def __mima_gaps__(self,seq,mima_loci,test_dict):
        gap_score = 0
        last = -1

        for locus in mima_loci:
            if last == -1:
                last = locus
                continue
            else:
                gap_score += (locus - last)
            last = locus

        test_dict["mima_gaps"] = gap_score

    def __error_seq_ratio__(self,seq,pattern,mima_loci,test_dict):
        pattern_logic = PatternLogic()

        non_error_seq = 1
        error_seq = 1

        for pattern in pattern_logic.pattern_generator(seq,pattern):
            if pattern in self._error_patterns:
                error_seq += 1
            else:
                non_error_seq += 1

        test_dict["error_seq_ratio"] = error_seq / float(non_error_seq)

    def __frameshift_count__(self,frameshift_loci,test_dict):
        test_dict["frameshisft_count"] = len(frameshift_loci)

    def __qc_score__(self,qual,test_dict):
        test_dict["qc_score"] = self._qc_logic.get_qual_qc_score(qual) 

    def __non_cannon_count(self,seq,pattern,test_dict):

        def pattern_generator(pattern):
            for x,y in combinations(range(0,len(pattern)),2):
                pattern_split = list(pattern)
                pattern_split[x] = "."
                pattern_split[y] = "."
                yield "".join(pattern_split)

        pseudo_telomere_patterns = []

        for regex_command in pattern_generator(pattern):
            regex_results = re.findall(regex_command,seq)
            regex_results = [result for result in regex_results if result != pattern]
            pseudo_telomere_patterns.extend(regex_results)

        psuedo_telomere_count = 0
        pseudo_telomere_patterns = list(set(pseudo_telomere_patterns))
        for psuedo_pattern in pseudo_telomere_patterns:
            psuedo_telomere_count += seq.count(psuedo_pattern)

        telomere_count = seq.count(pattern)

        test_dict["non_cannon_count"] = psuedo_telomere_count * 4

    def __highest_qual_deviation__(self,mima_loci,qual,test_dict):
        mima_scores = []
        for i in mima_loci:
            mima_scores.append( ord(qual[i]) - self._phred_offset )
        test_dict["highest_qual_deviation"] = (max(mima_scores) / float(self._max_qual)) * 100

    def __mima_count__(self,mima_loci,test_dict):
        test_dict["mima_count"] = len(mima_loci)

    def __inverse_mima_count__(self,seq,mima_loci,test_dict):
        if len(mima_loci) < len(seq) * .25:
            test_dict["inverse_mima_count"] = len(seq) - len(mima_loci)
        else:
            test_dict["inverse_mima_count"] = 0

    def __pattern_count__(self,seq,pattern,test_dict):
        pattern_count = seq.count(pattern)
        test_dict["pattern_count"] = pattern_count * 6.25

    def __average_mima_loci__(self,seq,mima_loci,test_dict):
        test_dict["lo_qual_area"] = np.mean(mima_loci)

    def __recurrant_deviation_count__(self,seq,pattern,test_dict):

        pattern_logic = PatternLogic()

        seen = []
        recurrant_count = 0

        for pattern in pattern_logic.pattern_generator(seq,pattern):
            if pattern not in seen:
                seq_count = seq.count(pattern)
                if seq_count > 1:
                    recurrant_count += seq_count
                    seen.append(pattern)

        test_dict["recurrant_deviation_count"] = recurrant_count

    def __all_mima_lo_qual__(self,qual,mima_loci,test_dict):

        all_mima_lo_qual = True
        for i in mima_loci:
            if (ord(qual[i])-self._phred_offset) > 15:
                all_mima_lo_qual = False
                break

        test_dict["mima_lo_qual"] = all_mima_lo_qual

    def __gc_range__(self,seq,test_dict):

        def get_gc_content(seq):
            gc_count = sum([1 for s in seq if s == "G" or s == "C"])
            gc_perc  = (gc_count / float(len(seq))) * 100
            return np.round(gc_perc,2)

        gc_content = get_gc_content(seq)
        test_dict["gc_content"] = 50 - (abs(50-gc_content))

    def __significantly_poor_mima_loci__(self,qual,mima_loci,test_dict,N=50):
        qual_bytes = [ord(q) - self._phred_offset for q in qual]

        random_scores = []
        for n in xrange(N):
            random_scores.append(\
                self.__get_random_score__(qual_bytes,len(mima_loci)))

        random_mean = np.mean(random_scores)
        random_std = np.std(random_scores)

        loci_score = self.__get_loci_score__(mima_loci,qual)

        dif = random_mean - loci_score
        if dif < 0:
            dif = 0

        test_dict["signif_poor_mima"] = dif * 4

    def __get_random_score__(self,qual,N):
        random_quals = random.sample(qual,N)
        return np.mean(random_quals)

    def __get_loci_score__(self,loci,qual):        
        loci_vals = [ord(qual[i])-self._phred_offset for i in loci] 
        loci_score = np.mean(loci_vals)
        return int(loci_score)

    def __check_error_profile__(self,mima_loci,qual,pattern,test_dict):
        loci_score = self.__get_loci_score__(mima_loci, qual)

        error_result = 0

        if loci_score < 400:
            error_result = \
              int(self._error_profiles[pattern][len(mima_loci),loci_score])
        else:
            error_result = 0

        test_dict["error_profile"] = error_result*100

    def __get_compare_templates__(self,patterns):
        templates = {}
        #TODO: Doesn't properly handle reads longer than 180bp
        for pattern in patterns:
            templates[pattern] = {}
            for i in xrange(len(pattern)):
                templates[pattern][i] = (pattern[ len(pattern)- i:] )\
                                        + (pattern*30)[:self._read_len]
        return templates

    def __get_pattern__(self,seq):
        cta,tag = "CCCTAA","TTAGGG"
        pattern = None
        if cta in seq or tag in seq:   
            if seq.count(cta) > seq.count(tag):
                pattern = cta
            else:
                pattern = tag
        return pattern

    def __flip_and_compliment__(self,read):
        if read.is_reverse:
            compliments = self._compliments
            seq_compliment = map(lambda base: compliments[base],read.seq)
            seq_compliment = "".join(seq_compliment)
            return(seq_compliment[::-1],read.qual[::-1])
        else:
            return (read.seq,read.qual)

    def __get_mima_loci__(self,seq,qual,pattern):
        if pattern is not None:
            return self.__get_simple_mima_loci__(seq,pattern),[],pattern
        else:
            tga_mima = self.__get_simple_mima_loci__(seq,"TTAGGG")
            cta_mima = self.__get_simple_mima_loci__(seq,"CCCTAA")
            if len(cta_mima) < len(tga_mima):
                return cta_mima,[],"CCCTAA"
            else:
                return tga_mima,[],"TTAGGG"

    def __generate_mima_loci__(self,seq,pattern):
        simple_mima_loci = self.__get_simple_mima_loci__(seq,pattern)
        if len(simple_mima_loci) == 0:
            return [],[]

        segments = re.split("(%s)" % (pattern,), seq)
        segments = self.__join_segments__(segments, pattern)
        mima_loci,fuse_loci = self.__get_damage_loci__(segments,pattern)
        return_loci = [m for m in mima_loci if m in simple_mima_loci]
        return_loci.extend(fuse_loci)
       
        return sorted(return_loci),fuse_loci

    def __get_simple_mima_loci__(self,seq,pattern):
        
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
        mima_loci = []
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
                mima_loci.extend(xrange(offset,offset+len(segment)))
                prev_was_tel = False
            offset += len(segment)
        return mima_loci,fuse_loci
            
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

class ReadLogic(object):

    def __init__(self,simple_read_factory):
        self._simple_read_factory = simple_read_factory

    def get_read_type(self,read1,read2):
        get_simple_read = self._simple_read_factory.get_simple_read
        simple_reads = [get_simple_read(read) for read in [read1,read2]]
        return self.get_read_type_for_simple_reads(simple_reads)

    def get_read_type_for_simple_reads(self,simple_reads):

        is_complete =  [read.complete for read in simple_reads]
        length_check = [len(read.seq) > 33 for read in simple_reads]

        read_type = "F3"
        
        if all(is_complete):
            #Reads both completely mapped to reference are true telomere
            if all(length_check):
                read_type = "F1"
        elif any(is_complete):
            #One read not complete, test if it's on the telomere boundary
            read_type = self.__check_orientation__(simple_reads)

        # if read_type in ["F3"]:
        #     print read_type + "--"
        #     for read in simple_reads:
        #         print read.seq
        #         print read.qual,read.read_score
        #         print "".join(["1" if i in read.mima_loci else "0" for i,s in enumerate(read.seq)])
        #         print read.mima_loci
        #         print ppr(read.test_data)
        #         print ""
        #     print "--"
        #     print ""

        return read_type
        
    def __check_orientation__(self, simple_reads):
        #This function is only called when at least 
        #one read was completely telomeric 

        def sort_reads(simple_reads):
            if simple_reads[0].complete:
                return simple_reads
            else:
                return simple_reads[::-1]

        complete_read,incomplete_read = sort_reads(simple_reads)

        if len(complete_read.seq) > 33 and len(incomplete_read.seq) > 12:
            if complete_read.five_prime:
                return "F2"
            else:
                return "F4"
        return "F3"
       
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
                                                         float))

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
                "qual_sd":qual_sd}

    def __get_mean_and_sd__(self,x_sum,x_power_2,x_N):
        x_mean = x_sum / x_N
        x_sd = np.sqrt( (x_N * x_power_2) - x_sum**2) / x_N

        return x_mean,x_sd

    def get_vital_stats(self,sample_path):

        vital_stats_csv = self.__run_vital_engine__(sample_path)
        vital_stats = self.__csv_to_dict__(vital_stats_csv)
        vital_stats["phred_offset"] = vital_stats["min_qual"]
        vital_stats["qc_logic"] = QCLogic(vital_stats)
 
        # cta_read_count_path,random_path,patterns_path,tga_read_count_path = \
        #                 self.__run_read_count_engine__(sample_path, vital_stats)

        # vital_stats["error_patterns"] = self.__get_error_patterns__(patterns_path)

        # tga_profile = self.__path_to_profile__(tga_read_count_path,random_path)
        # cta_profile = self.__path_to_profile__(cta_read_count_path,random_path)

        # vital_stats["random_path"] = random_path
        # vital_stats["tga_read_count_path"] = tga_read_count_path
        # vital_stats["cta_read_count_path"] = cta_read_count_path

        # vital_stats["error_profiles"] = {"TTAGGG":None,"CCCTAA":None}

        return vital_stats

    def __get_error_patterns__(self,patterns_path):
        pattern_logic = PatternLogic()
        return pattern_logic.get_error_patterns(patterns_path)

    def __filter_zero_values__(self,observations):
        filtered_list = observations.flatten()
        return np.array([x for x in filtered_list if x > 0])

    def __path_to_profile__(self,read_counts_path,random_path):
        ##########
        # SIGNAL #
        ##########
        read_counts = genfromtxt(read_counts_path,delimiter=",")
        random_counts = genfromtxt(random_path,delimiter=",")
        read_counts[0,0] = 0

        normalised = read_counts - random_counts
        normalised = normalised * (normalised > 0)

        log_read_counts = log(normalised+1)

        non_zero_values = self.__filter_zero_values__(log_read_counts[:25,:25])
        mean_signal = non_zero_values.mean()
        std_signal = non_zero_values.std()

        error_profile = log_read_counts > (mean_signal + (std_signal * .5))

        mask = rot90(tril(zeros( read_counts.shape[::-1] )+1,k=-5),k=3)

        return error_profile * mask

    def read_line(self,path):
        with open(path,"r") as file_obj:
            for line in file_obj:
                line.split(",")
                print line

    def __run_vital_engine__(self,sample_path):
        def engine(read,constants,master):
            stats = {}

            if read.is_read1 and read.is_proper_pair: #and read.mapq > 35:
                insert_size = abs(read.template_length)
                stats["sum"] = {"result":insert_size}
                stats["power_2"] = {"result":insert_size**2}
                stats["N"] = {"result":1}
            
            stats["read_len"] = {"result": len(read.seq)}
            byte_vals = map(ord,read.qual)
            min_qual = min(byte_vals)
            max_qual = max(byte_vals)

            qual_mean = np.mean(byte_vals)
            stats["qual_sum"] = {"result":qual_mean}
            stats["qual_power_2"] = {"result":qual_mean**2}
            stats["qual_N"] = {"result":1}

            stats["min_qual"] = {"result":min_qual}
            stats["max_qual"] = {"result":max_qual}

            return stats

        structures = {}

        structures["sum"] = {"data":0,"store_method":"cumu"}
        structures["power_2"] = {"data":0,"store_method":"cumu"}
        structures["N"] = {"data":0,"store_method":"cumu"}
        structures["read_len"] = {"data":0,"store_method":"max"}

        structures["min_qual"] = {"data":999,"store_method":"min"}
        structures["max_qual"] = {"data":0,"store_method":"max"}


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

    def __run_read_count_engine__(self,sample_path,vital_stats):

        read_len = vital_stats["read_len"]
        phred_offset = vital_stats["phred_offset"]
        max_phred = vital_stats["max_qual"] - phred_offset
        matrix_size = max_phred+1

        structures = {"tga_read_counts":{"data":np.zeros((read_len,matrix_size)),
                                     "store_method":"cumu"},
                      "cta_read_counts":{"data":np.zeros((read_len,matrix_size)),
                                     "store_method":"cumu"},
                     "random_counts":{"data":np.zeros((read_len,matrix_size)),
                                      "store_method":"cumu"},
                     "telo_patterns":{"data":{},"store_method":"cumu"}}

        simple_read_factory = SimpleReadFactory(vital_stats,conduct_tests=False)
        pattern_logic = PatternLogic()

        def engine(read,master,constant):
            results = {}
            read_counts = zeros((read_len,matrix_size))
            random_counts = zeros((read_len,matrix_size))
            simple_read = simple_read_factory.get_simple_read(read)

            if simple_read.pattern and len(simple_read.mima_loci):

                mima_loci = simple_read.mima_loci
                mismatch_qual = simple_read_factory.__get_loci_score__\
                                        (mima_loci,simple_read.qual)

                if len(mima_loci) > 0 and mismatch_qual < 420:                    
                    read_counts = np.zeros((read_len,matrix_size))
                    read_counts[len(mima_loci),mismatch_qual] = 1
                    if simple_read.pattern == "TTAGGG":
                        results["tga_read_counts"] = {"result":read_counts}
                    elif simple_read.pattern == "CCCTAA":
                        results["cta_read_counts"] = {"result":read_counts}

            if simple_read.pattern is not None:
                patterns = pattern_logic.get_non_telo_patterns\
                                        (simple_read.seq,simple_read.pattern)
                results["telo_patterns"] = {"result":patterns}

            return results

        stat_interface = parabam.command.stat.Interface(self._temp_dir)
        out_paths = stat_interface.run(
            input_bams= [sample_path],
            total_procs = self._total_procs,
            task_size = 10000,
            user_constants = {},
            user_engine = engine,
            user_struc_blueprint = structures,
            keep_in_temp=True)

        return sorted(out_paths[sample_path])

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
            save_alignment = cmd_args.a,
            inserts_path=cmd_args.insert,
            output = cmd_args.out,
            announce=True)

    def run(self,input_paths,total_procs,task_size,verbose,output,reader_n,inserts_path=None,
        save_alignment=False,alig_params=None,announce=False,keep_in_temp=False):
        
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

            read_type_counts,trained_gmm = self.__get_read_types__(sample_path,
                                  vital_stats,total_procs,task_size,reader_n,
                                  save_alignment,keep_in_temp)

            simulation_results = self.__run_simulation__(vital_stats,
                                                         read_type_counts,
                                                         total_procs,
                                                         trained_gmm)

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
                                          reader_n,save_alignment,keep_in_temp,
                                          readlogic = None):
        self.__output__("\t- Categorising reads into telomeric read types\n",2)
        read_type_counts,trained_gmm = self.__run_read_type_engine__(sample_path,
                                        vital_stats,task_size,
                                        total_procs,
                                        reader_n,readlogic)

        self.__output__("\t\t+ F1:%d | F2a:%d | F2b+F4:%d\n" % \
                                                (read_type_counts["F1"],
                                                 read_type_counts["F2a"],
                                                  read_type_counts["F2b_F4"],),2)
        return read_type_counts,trained_gmm

    def __keep_files_decision__(self,file_paths,save_alignment,keep_in_temp):
        if save_alignment:
            if not keep_in_temp:
                self.__copy_out_of_temp__(file_paths)
        
        if not keep_in_temp:
            map(os.remove,file_paths)

    def __create_output_file__(self,output):
        if output:
            unqiue_file_ID = output
        else:
            unqiue_file_ID = "telomerecat_length_%d.csv" % (time.time(),)

        output_csv_path = os.path.join(self._temp_dir,unqiue_file_ID)
        with open(output_csv_path,"w") as total:
            header = "Sample,F1,F2a,F2b_F4,Uncertainty,Insert_mean,Insert_sd,Length\n"
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

    def __run_simulation__(self,vital_stats,read_type_counts,total_procs,trained_gmm):
        self.__output__("\t- Using read counts to estimate length\n",2)
        total_F2 = read_type_counts["F2a"]
        total_f1 = read_type_counts["F1"]
        read_length = vital_stats["read_len"]
        insert_mean = vital_stats["insert_mean"]
        insert_sd =   vital_stats["insert_sd"]

        len_mean,len_std = simulator.run_simulator_par(insert_mean,insert_sd,
                                        total_f1,total_F2,
                                         total_procs,read_length,trained_gmm,N=16)
        self.__output__("\t\t+ Length: %d\n" % (len_mean,),2)

        return {"insert_mean":insert_mean,
                "insert_sd":insert_sd,
                "length":len_mean,
                "uncertainty":len_std}
        
    def __get_gc_dist__(self,seq):
        gc_count = sum([1 for s in seq if s == "G" or s == "C"])
        gc_perc  = (gc_count / float(len(seq))) * 100
        return np.round(gc_perc,2)

    def __make_break_down__(self,read):
        #breakdown = self.__dict_to_brkdn_strings__(read.seq_error_data,"c")
        #breakdown.extend(self.__dict_to_brkdn_strings__(read.subtelo_data,"s"))
        breakdown = "seq_err:%d_subtelo:%d" % (read.seq_error_percent,read.subtelo_percent)
        return breakdown

    def __dict_to_brkdn_strings__(self,breakdown_dict,dif_char):
        breakdown = []
        for key,value in breakdown_dict.items():
            breakdown.append( "%s-%s:%d" % (dif_char,key,value)  )
        return breakdown

    def __run_read_type_engine__(self,sample_path,vital_stats,
                                        task_size,total_procs,reader_n,
                                        readlogic = None):

        if readlogic is None:
            simple_read_factory = SimpleReadFactory(vital_stats)
            readlogic = ReadLogic(simple_read_factory)
        else:
            simple_read_factory = readlogic._simple_read_factory

        def engine(reads,constants,parent):
            results = {}

            simple_reads = [simple_read_factory.get_simple_read(read) \
                            for read in reads]
            read_type = readlogic.get_read_type_for_simple_reads(simple_reads)
            
            if read_type == "F2":
                complete_end = simple_reads[0]
                if not simple_reads[0].complete:
                    complete_end = simple_reads[1]
                results["f2_comp_len"] = {"result":\
                                    np.array([len(complete_end.seq)])\
                                                                .reshape(1,-1)}
            results["read_type_master"] = {"result":{read_type:1}}
            return results

        structures = {"read_type_master":\
                            {"data":dict(),"store_method":"cumu"},
                      "f2_comp_len":\
                            {"data":np.zeros((1,1)),"store_method":"vstack"}}

        interface = parabam.command.stat.Interface(self._temp_dir)
        output_files = interface.run(input_bams=[sample_path],
                            total_procs = total_procs,
                            reader_n = reader_n,
                            task_size = 6000,
                            user_constants = {},
                            user_engine = engine,
                            user_struc_blueprint = structures,
                            keep_in_temp = True,
                            pair_process = True)

        return self.__parabam_results_to_dict__(*sorted(output_files[sample_path]))

    def __parabam_results_to_dict__(self,f2_comp_len,read_type_csv_path):
        read_counts_csv = pd.read_csv(read_type_csv_path,header=None)
        read_counts = dict(zip(read_counts_csv.values[:,0],
                                read_counts_csv.values[:,1]))

        total_F1 = read_counts["F1"]
        called_F2 = read_counts["F2"]
        total_F4 = read_counts["F4"]

        total_F2a = called_F2 - total_F4 #Find the F2a by removing the
                                          #probablistic amount of F2bs
                                          #For each F4 we assume an F2b thus

        total_F2b_F4 = (total_F4 * 2) #Reflect the removal of F2b from F2a
                                     #by inflating the F4 count


        f2_complete_read_lens = pd.read_csv(f2_comp_len,header=None)
        trained_gmm = mixture.GMM(n_components=2,n_iter=100)
        trained_gmm.fit(f2_complete_read_lens)

        return {"F1":int(total_F1),"F2b_F4":int(total_F2b_F4),
                "F2a":int(total_F2a),
                "F2a_F2b":int(called_F2)},trained_gmm

    def __subtract_f4_from_f2__(self,f2_counts,f4_counts):
        subtract = f2_counts - f4_counts

        ppr(dict(f2_counts))
        ppr(dict(f4_counts))
        ppr(dict(subtract))
        return sum(subtract.values())

    def __master_to_breakdown_counts__(self,master_csv,target_read_type):

        breakdown_counter = Counter()

        for read_type,breakdown in master_csv:
            if target_read_type == read_type:
                breakdown_counter[breakdown] += 1

        return breakdown_counter

    def __copy_out_of_temp__(self,file_paths,copy_path="."):
        map(lambda fil: copy(fil,copy_path),file_paths)

    def get_parser(self):
        parser = self.default_parser()
        parser.description = textwrap.dedent(
        '''\
        telomerecat telbam2length
        ----------------------------------------------------------------------

            The telbam2length command allows the user to genereate a telomere
            length estimate from a previously generated TELBAM file.

            Example useage:

            telomerecat telbam2length /path/to/some_telbam.bam

            This will generate a .csv file with an telomere length estimate
            for the `some_telbam.bam` file.

        ----------------------------------------------------------------------
        ''')

        parser.add_argument('input',metavar='TELBAM(S)', nargs='+',
            help="The telbam(s) that we wish to analyse")
        parser.add_argument('--out',metavar='CSV',type=str,nargs='?',default=None,
            help='Specify output path for length estimation CSV.\n'+\
                'Automatically generated if left blank [Default: None]')
        parser.add_argument('--insert',metavar='CSV',nargs='?',type=str,default=None,
            help="A file specifying the insert length mean and std for\n"+\
                 "each input sample. If not present telomerecat will\n"+\
                 "automatically estimate insert length of sample [Default: None]")
        parser.add_argument('-a',action="store_true",default=False
            ,help="Retain fastq and telref files created by analysis")
        parser.add_argument('-v',choices=[0,1,2],default=0,type=int,
            help="Verbosity. The amount of information output by the program:\n"\
            "\t0: Silent [Default]\n"\
            "\t1: Output\n"\
            "\t2: Detailed Output")

        return parser

if __name__ == "__main__":
    print "Do not run this script directly. Type `telomerecat` for help."
