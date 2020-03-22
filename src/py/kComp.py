import sys

import lex_io
import kEntropy
import kSurprisal
import kTest.test_kEntropy as kt
import os


def test_module(syl_lex_dir, cons_config_dir):
    # prepare documents
    syl_lex = lex_io.read_lexicon_file(syl_lex_dir)
    cons_configs = lex_io.read_lexicon_file(cons_config_dir)

    # prepare surprisal document
    freq_dict = kEntropy.get_frequency_of_each_config_in_word_position(syl_lex, cons_configs)
    phonol_surprisals = kEntropy.get_phonotactic_surprisals(freq_dict)

    kt.test_get_frequency_of_each_config_in_word_position(syl_lex, cons_configs)

    kt.test_get_surprisals_of_lexicon(["ŋkəḻ.ṯə.lə"], phonol_surprisals)


def main(syl_lex_dir, seg_config_dir):
    syl_lex = lex_io.read_lexicon_file(syl_lex_dir)
    seg_configs = lex_io.read_lexicon_file(seg_config_dir)

    # make new phonotactic fqs
    freq_dict = kEntropy.get_frequency_of_each_config_in_word_position(syl_lex, seg_configs)
    # save document
    lex_io.write_dict_to_csv(freq_dict, "phonotactic_fqs", os.path.dirname(syl_lex_dir))
    # calculate entropy for syllable positions
    phon_ent = kEntropy.get_phontactic_entropies(freq_dict)
    lex_io.write_dict_to_csv(phon_ent, "phonological_entropy", os.path.dirname(syl_lex_dir))

    # get positional surprisals
    phonol_surprisals = kEntropy.get_phonotactic_surprisals(freq_dict)
    # save phonological surprisals
    lex_io.write_dict_to_csv(phonol_surprisals, "positional_surprisals", os.path.dirname(syl_lex_dir))

    # get surprisals of lexicon
    lex_sur = kSurprisal.get_surprisals_of_lexicon(syl_lex, phonol_surprisals)
    # save lexicon surprisals
    lex_io.write_dict_to_csv(lex_sur, "lexical_surprisals", os.path.dirname(syl_lex_dir))


if __name__ == "__main__":
    # test_module(sys.argv[1], sys.argv[2], sys.argv[3])
    main(sys.argv[1], sys.argv[2])
