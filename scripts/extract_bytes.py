from script_config import *
from nltk.tokenize.util import is_cjk
import argparse
import sys
import re

replacer = False
MAX_LINE_LENGTH = 24
MAX_PARAGRAPH_LENGTH = MAX_LINE_LENGTH * 3

#pattern = re.compile(r'([\p{IsHira}]+)', re.UNICODE)
def is_text(data):
    if b'\x00' in data: return False
    if (b'\x83' not in data) and (b'\x82' not in data) and (b'\x81' not in data): return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to extract and examine dialogue.')
    parser.add_argument('filename', help='Name of game file (e.g. "slps" or "battle")')

    args = parser.parse_args(sys.argv[1:])

    with open(f"{GAME_DATA_IN_DIR}/BIN/{args.filename.upper()}.BIN", "rb") as f: rawdata = f.read()
    lines = []
    count = 0
    for d in re.split(b'\x00',rawdata):
        if len(d) > 1 and is_text(d):
            try:
                line = d.decode('shift-jis')
                for dd in d.split(b'\x0C'):
                    print(dd.decode('shift-jis'))
                    lines.append(dd.decode('shift-jis'))
            except:
                pass
