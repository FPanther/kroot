# Takes as input the path to the relevant document with a 'words' column with kaytetye orthography,
# and the orthographic rules document, and outputs a version of the first document with phon and syl columns.
import pandas as ps
import re
import sys
import os


def main(in_path, rules_path):
    in_doc = ps.read_csv(in_path, keep_default_na=False)  # read in target doc
    rules = ps.read_csv(rules_path, keep_default_na=False)  # read in rule doc
    # get phonological rules
    phon_rules = rules.loc[rules['type'] == 'phon']
    syl_rules = rules.loc[rules['type'] == 'syl']
    # for each item 'word' column in the in_doc, convert to phon
    phons = []
    phon_syls = []
    for index, row in in_doc.iterrows():
        in_phon = row['words']
        for rule_index, rule_row in phon_rules.iterrows():
            in_phon = re.sub(rule_row['original'], rule_row['result'], in_phon)
        phons.append(in_phon)
        # create syllabified form with in_syl
        for syl_index, syl_row in syl_rules.iterrows():
            pattern = re.compile(syl_row['original'])
            in_phon = pattern.sub(syl_row['result'], in_phon)
        phon_syls.append(in_phon)
    # output .csv
    out_doc = in_doc
    out_doc['phon'] = phons
    out_doc['phon_syl'] = phon_syls
    out_doc.to_csv(os.path.dirname(in_path) + "\\output.csv", encoding="utf-8")

    # output txt documents
    with open(os.path.dirname(in_path) + "\\phon.txt", 'w', encoding="utf-8") as f:
        f.write('\n'.join(phons))
    with open(os.path.dirname(in_path) + "\\phon_syls.txt", 'w', encoding="utf-8") as f:
        f.write('\n'.join(phon_syls))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
