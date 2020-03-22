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


def save_lex_value_pairs(lexicon, values, value_name, output_name):
    save_string = "lexeme\t" + value_name + "\n"
    for i in range(len(lexicon)):
        save_string = save_string + str(lexicon[i]) + "\t" + str(values[i]) + "\n"
    print("printing to: " + str(Path(os.getcwd()).parent) + "\\" + output_name)
    f = open(str(Path(os.getcwd()).parent) + "\\" + output_name + ".txt", 'w', encoding="utf-8")
    f.writelines(save_string)
    f.close()


def read_csv(dir):
    file = open(dir, encoding="utf-8-sig")
    output = csv.DictReader(file)
    return list(output)


def read_values_to_file(values, name):
    save_string = ""
    for i in range(len(values)):
        for j in range(len(values[i])):
            save_string = save_string + str(values[i][j]) + "_"
        save_string = save_string + "\n"
    print("printing to: " + str(Path(os.getcwd()).parent) + "\\" + name)
    f = open(str(Path(os.getcwd()).parent) + "\\" + name + ".txt", 'w', encoding="utf-8")
    f.writelines(save_string)
    f.close()


def read_values_from_file(dir):
    file = open(dir, encoding="utf-8-sig")
    output = [s.rstrip() for s in file.readlines()]
    return list(output)


def write_dict_to_csv(out_dict, output_name, out_dir):
    with open(out_dir + "\\" + output_name + ".txt", 'w', encoding="utf-8") as output:
        w = csv.DictWriter(output, out_dict[0].keys())
        w.writeheader()
        w.writerows(out_dict)
