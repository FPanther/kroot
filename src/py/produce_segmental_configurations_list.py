"""
NAME: produce_segmental_configurations_list.py
CREATED: 22-MAR-20
LAST EDIT: 22-MAR-20
CREATOR: Forrest Panther
EMAIL: forrestapanther@gmail.com
PROJECT: kroot
SUMMARY: Receives a list of syllabified Kaytetye lexemes, and outputs all possible consonant and vowel configurations
         for each phonotactic position (syllable, nucleus, coda). This output (phon_configs.txt) is required for
        produce_info_theory_docs.py
"""
import sys
import re
import os
from pathlib import Path

syl_txt_dir = sys.argv[1]
# create flat syllable list
syl_list = open(syl_txt_dir, 'r', encoding="utf-8").read().splitlines()
syl_list = [line.split(".") for line in syl_list]
syl_list = [item for sublist in syl_list for item in sublist]

# create a vector of split syllables using the syllable nucleus as a delimiter
vowel_regex = "[ɐəiu:]+"
vowel_capture = "([ɐəiu:]+)"
split_list = []
for syl in syl_list:
    # throw error if there are two vowel matches in the same syllable
    if len(re.findall(vowel_regex, syl)) > 1:
        print(syl)
        raise RuntimeError
    cons_split = re.split(vowel_regex, syl)
    for cs in cons_split:
        if cs == '':
            split_list.append("0") # treat no consonant as 0
        else:
            split_list.append(cs)
    # add the nucleus
    split_list.append(re.compile(vowel_regex).findall(syl)[0])
uniq_seqs = set(split_list)
with open(os.path.dirname(syl_txt_dir) + "\\phon_configs.txt", 'w', encoding="utf-8") as f:
    f.writelines("\n".join(uniq_seqs))
