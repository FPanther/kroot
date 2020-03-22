# functions relating to surprisal 'profiles' of average surprisal values of each word in the Kaytetye lexicon.
import kEntropy
import math


def get_surprisal_of_syllable(syl, num, word_len, sur_dict_list):
    surprisal_in_positions = [0] * 3
    syl_poss = kEntropy.split_syllable_into_phonotactic_positions(syl)
    for k_row in sur_dict_list:
        # special behaviour if final syllable
        if num == word_len - 1:
            if k_row["syllable"] == str(num) + "_onset":
                surprisal_in_positions[0] = float(k_row[syl_poss[0]])
            elif k_row["syllable"] == "final_nucleus":
                surprisal_in_positions[1] = float(k_row[syl_poss[1]])
            elif k_row["syllable"] == "final_coda":
                # final coda will always be 0, and is factored out of calculation
                surprisal_in_positions[2] = float(k_row[syl_poss[2]])
        else:
            if k_row["syllable"] == str(num) + "_onset":
                surprisal_in_positions[0] = float(k_row[syl_poss[0]])
            elif k_row["syllable"] == str(num) + "_nucleus":
                surprisal_in_positions[1] = float(k_row[syl_poss[1]])
            elif k_row["syllable"] == str(num) + "_coda":
                surprisal_in_positions[2] = float(k_row[syl_poss[2]])

    return sum(surprisal_in_positions)


def get_surprisals_of_lexicon(syl_lex, sur_dict_list):
    out_dict_list = []
    for lexeme in syl_lex:
        lex_sylab = lexeme.split(".")
        surprisal_value = 0
        out_dict = {}
        for i, syl in enumerate(lex_sylab):
            surprisal_value = surprisal_value + get_surprisal_of_syllable(syl, i, len(lex_sylab), sur_dict_list)
        out_dict["phoneme"] = lexeme
        out_dict["mean_surprisal"] = surprisal_value / ((len(lex_sylab)*3)-1) #three phonotactic positions for each
        # syllable excluding final coda
        out_dict_list.append(out_dict)
    return out_dict_list
