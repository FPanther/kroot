import sys
import lex_io
import kEntropy

def main(lex_dir):
    syl_lexicon = lex_io.read_lexicon_file(lex_dir)
    max_count = kEntropy.get_max_syl_count(syl_lexicon)
    print(max_count)
    for num in range(0, max_count):
        print(num)

if __name__ == "__main__":
    main(sys.argv[1])
