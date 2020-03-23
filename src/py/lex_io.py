# Functions relating to reading in files
from pathlib import Path
import os
import csv


def read_lexicon_file(directory):
    with open(directory, encoding="utf-8") as f:
        lex_array = f.readlines()
        for i in range(len(lex_array)):
            lex_array[i] = lex_array[i].strip('\n')
    return lex_array


def read_csv(dir):
    file = open(dir, encoding="utf-8-sig")
    output = csv.DictReader(file)
    return list(output)


def write_dict_to_csv(out_dict, output_name, out_dir):
    with open(out_dir + "\\" + output_name + ".csv", 'w', encoding="utf-8") as output:
        w = csv.DictWriter(output, out_dict[0].keys())
        w.writeheader()
        w.writerows(out_dict)
