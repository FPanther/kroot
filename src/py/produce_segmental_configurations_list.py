# Produces a .txt file with the segmental configurations of the input list of syllabified Kaytetye forms.
import sys
import re
import os

def main(syl_txt_dir):
    # create flat syllable list
    syl_list = open(syl_txt_dir, 'r', encoding="utf-8").read().splitlines()
    syl_list = [line.split(".") for line in syl_list]
    syl_list = [item for sublist in syl_list for item in sublist]

    # create a vector of split syllables using the syllable nucleus as a delimiter
    vowel_regex = "[ɐəiu:]+"
    vowel_capture = "([ɐəiu:]+)"
    split_list = []
    for syl in syl_list:
        # throw error if there are two vowels in the same syllable
        if len(re.findall(vowel_regex, syl)) > 1:
            print(syl)
            raise RuntimeError
        cons_split = re.split(vowel_regex, syl)
        for cs in cons_split:
            if cs == '':
                split_list.append("0")
            else:
                split_list.append(cs)
        # add the nucleus
        split_list.append(re.compile(vowel_regex).findall(syl)[0])
    uniq_seqs = set(split_list)
    with open(os.path.dirname(syl_txt_dir) + "\\phon_configs.txt", 'w', encoding="utf-8") as f:
        f.writelines("\n".join(uniq_seqs))


if __name__ == "__main__":
    main(sys.argv[1])
