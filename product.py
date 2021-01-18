#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, re,datetime, glob,gzip


list = list2 =list3 =list1 = []
dict = {}
merge_sv=open(sys.argv[3],'w')
ref_genome=sys.argv[1]

##add length
with open ("chr_length") as f:
	for line in f:
		list2 = line.split()
		dict[list2[0]] = list2[1]

		
with gzip.open (sys.argv[2]) as f:
	for line in f:
		if "#" in line:
			continue
		row_list = line.split()
		if len(row_list[3]) >1:
			continue
###去重
		if_repeat = row_list[0] + "_" + row_list[1] + "_" +  row_list[0]
		if if_repeat not in list3:
			if int(row_list[1]) > 1000:
				pre_n_start = str(int(row_list[1])-1000)
				pre_n_end = str(int(row_list[1])-1)
			else:
				pre_n_start = str(1)
				pre_n_end = str(int(row_list[1])-1)
			pre_n = os.popen('samtools faidx '+ref_genome+' '+row_list[0]+ ':'+pre_n_start+'-'+pre_n_end).readlines()[1:]
			pre_seq=''
			for i in pre_n:
				i=i.strip()
				pre_seq+=i
			pre_seq=pre_seq.strip()
			middle_seq = row_list[4]
			length = int(len(row_list[4])) 
			end_n_start = str(int(row_list[1])+length)
			end_n_end = str(int(row_list[1])+length+999)
			if int(dict[row_list[0]])< int(end_n_end):
				end_n_end = dict[row_list[0]]
			end_n = os.popen('samtools faidx '+ref_genome+' '+row_list[0]+ ':'+end_n_start+'-'+end_n_end).readlines()[1:]
			end_seq=''
			for i in end_n:
				i=i.strip()
				end_seq+=i
			end_seq=end_seq.strip()
			
			final_seq = pre_seq + row_list[4] + end_seq + "\n"
			ID = ">" + row_list[0]+"_"+row_list[1]+"_"+ str(int(end_n_start)-1) + "\n"
			merge_sv.write(ID)
			merge_sv.write(final_seq)
			repeat = row_list[0] + "_" + row_list[1] + "_" +  row_list[0]
			list3.append(repeat)

