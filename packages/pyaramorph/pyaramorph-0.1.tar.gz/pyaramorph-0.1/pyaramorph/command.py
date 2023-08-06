# command.py
# Command line interface to pyaramorph

import readline
import pyaramorph

def main():
    """ Read user input, analyze, output results. """
    analyzer = pyaramorph.Analyzer()
    print("Unicode Arabic Morphological Analyzer (press ctrl-d to exit)")
    while True:
        try:
            s = input("$ ")
            analyzer.process(s)
        except EOFError:
            print("Goodbye!")
            break
        except UnicodeDecodeError:
            print("Decode error. Skipping.")

if __name__ == '__main__':
    main()

