# NAME: test.py
# CREATED: 24-MAR-20
# CREATOR: Forrest Panther (Fpan020)
# EMAIL: forrestapanther@gmail.com
# test functions public functions in info_theory_functions.py
import info_theory_functions as itf
from math import log

# test 1: get_frequency_of_each_config_in_word_position
print("Test 1: phonotactic frequency...")
lexicon = ["ɐ.ɰə", "ɐ.ṯə.ɾə", "ɐ.ṯim.pə", "ə.ḻə", "ku.nə", "pɐɾ.cə"]
config_list = ["0", "ɐ", "ɰ", "ə", "ṯ", "i", "ɾ", "m", "p", "ḻ", "k", "u", "n", "p", "c"]
test_phonotac_freq = itf.get_frequency_of_each_config_in_word_position(lexicon, config_list)
# assert correct output
assert test_phonotac_freq[0]["0"] == 4, "Wrong number of null initial syllable onsets!"
assert test_phonotac_freq[1]["ɐ"] == 4, "Wrong number of 'ɐ' initial syllable nucleus!"
assert test_phonotac_freq[2]["0"] == 5, "Wrong number of null initial syllable codas!"
assert test_phonotac_freq[3]["ɰ"] == 1, "Wrong number of second syllable onset ɰ!"
assert test_phonotac_freq[4]["ə"] == 1, "Wrong number of second syllable nulceus schwas!"
assert test_phonotac_freq[5]["m"] == 1, "Wrong number of second syllable coda 'm'!"
assert test_phonotac_freq[6]["p"] == 1, "Wrong number of third syllable onset 'p'!"
assert test_phonotac_freq[7]["ə"] == 0, "Wrong number of third syllable nucleus 'ə'!"
assert test_phonotac_freq[8]["n"] == 0, "Wrong number of third syllable coda 'n'!"
assert test_phonotac_freq[9]["ə"] == 6, "Wrong number for final syllable nucleus schwa!"
print("Test 1 was successful!")

# test 2: get_phonotactic_surprisals
print("Test 2: phonotactic surprisals...")
test_phonotac_surp = itf.get_phonotactic_surprisals(test_phonotac_freq)
assert test_phonotac_surp[0]["0"] == log((4/6), 2) * -1, "Wrong surprisal for initial syllable onset '0'!"
assert test_phonotac_surp[1]["ɐ"] == log((4/6), 2) * -1, "Wrong surprisal for initial syllable nucleus 'ɐ'!"
assert test_phonotac_surp[3]["ɰ"] == log((1/6), 2) * -1, "Wrong surprisal for second syllable onset ɰ!"
assert test_phonotac_surp[4]["i"] == log((1/2), 2) * -1, "Wrong surprisal for second syllable nucleus 'i'!"
assert test_phonotac_surp[5]["m"] == log((1/2), 2) * -1, "Wrong surprisal for second syllable coda 'm'!"
assert test_phonotac_surp[9]["ə"] == log((6/6), 2) * -1, "Wrong surprisal for final syllable nucleus schwa!"
print("Test 2 was successful!")

# test 3: get_surprisals_of_lexicon
print("Test 3: lexical surprisals...")
test_lex_surp = itf.get_surprisals_of_lexicon(lexicon, test_phonotac_surp)

assert test_lex_surp[0]['mean_surprisal'] == ((log(4/6, 2) * -1) + (log(4/6, 2) * -1) + (log(5/6, 2) * -1) + (log(1/6, 2) * -1) + (log(6/6, 2) * -1)) / 5, "Mean surprisals of word do not match!" 
assert test_lex_surp[1]['mean_surprisal'] == ((log(4/6, 2) * -1) + (log(4/6, 2) * -1) + (log(5/6, 2) * -1) + (log(2/6, 2) * -1) + (log(1/2, 2) * -1) + (log(1/2, 2) * -1) + (log(1/2, 2) * -1) + (log(6/6, 2) * -1)) / 8, "Mean surprisals of word do not match!"
assert test_lex_surp[2]['mean_surprisal'] == ((log(4/6, 2) * -1) + (log(4/6, 2) * -1) + (log(5/6, 2) * -1) + (log(2/6, 2) * -1) + (log(1/2, 2) * -1) + (log(1/2, 2) * -1) + (log(1/2, 2) * -1) + (log(6/6, 2) * -1)) / 8, "Mean surprisals of word do not match!"
assert test_lex_surp[3]['mean_surprisal'] == ((log(4/6, 2) * -1) + (log(1/6, 2) * -1) + (log(5/6, 2) * -1) + (log(1/6, 2) * -1) + (log(6/6, 2) * -1)) / 5, "Mean surprisals of word do not match!"
assert test_lex_surp[4]['mean_surprisal'] == ((log(1/6, 2) * -1) + (log(1/6, 2) * -1) + (log(5/6, 2) * -1) + (log(1/6, 2) * -1) + (log(6/6, 2) * -1)) / 5, "Mean surprisals of word do not match!"
assert test_lex_surp[5]['mean_surprisal'] == ((log(1/6, 2) * -1) + (log(4/6, 2) * -1) + (log(1/6, 2) * -1) + (log(1/6, 2) * -1) + (log(6/6, 2) * -1)) / 5, "Mean surprisals of word do not match!" 
print("Test 3 was successful!!")

#test 4: get_phonotactic_entropy
print("Test 4: phonotactic entropy...")
test_entropies = itf.get_phontactic_entropies(test_phonotac_freq)
assert test_entropies[0]['entropy'] == ((log(4/6, 2) * -1) * 4/6) + ((log(1/6, 2) * -1) * 1/6) + ((log(1/6, 2) * -1) * 1/6)
assert test_entropies[1]['entropy'] == ((log(4/6, 2) * -1) * 4/6) + ((log(1/6, 2) * -1) * 1/6) + ((log(1/6, 2) * -1) * 1/6)
assert test_entropies[2]['entropy'] == ((log(5/6, 2) * -1) * 5/6) + ((log(1/6, 2) * -1) * 1/6)
assert test_entropies[3]['entropy'] == ((log(1/6, 2) * -1) * 1/6) + ((log(2/6, 2) * -1) * 2/6) + ((log(1/6, 2) * -1) * 1/6) + ((log(1/6, 2) * -1) * 1/6) + ((log(1/6, 2) * -1) * 1/6)
assert test_entropies[4]['entropy'] == ((log(1/2, 2) * -1) * 1/2) + ((log(1/2, 2) * -1) * 1/2)
assert test_entropies[5]['entropy'] == ((log(1/2, 2) * -1) * 1/2) + ((log(1/2, 2) * -1) * 1/2)
assert test_entropies[6]['entropy'] == ((log(1/2, 2) * -1) * 1/2) + ((log(1/2, 2) * -1) * 1/2)
assert test_entropies[9]['entropy'] == ((log(6/6, 2) * -1) * 1/2)
print("Test 4 was successful!")

