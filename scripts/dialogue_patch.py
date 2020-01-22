from script_config import *
from nltk.tokenize.util import is_cjk
import textwrap
import argparse
import sys
import re

LINE_LENGTH = 24
PARAGRAPH_LENGTH = LINE_LENGTH * 3

w = textwrap.TextWrapper()
w.drop_whitespace = True
#w.drop_whitespace = False
w.width = LINE_LENGTH



with open(f"{GAME_DATA_IN_DIR}/BIN/OPENDEMO.BIN", "rb") as f: filedata = f.read()

data_en = []
data_ja = []

#for i in range(11, 27, 1):
for i in range(27):
    with open(f'opendemo/en/{i}.txt', 'r') as f:
        data_en.append(f.read())
    with open(f'opendemo/ja/{i}.txt', 'r') as f:
        data_ja.append(f.read())

print(f"Filedata: {len(filedata)}")

for i in range(len(data_ja)):
    en = data_en[i].encode('shift-jis')
    ja = data_ja[i].encode('shift-jis')

    diff = len(ja) - len(en)
    if diff < 0:
        print(f"====\nError: Must shorten {i} by {diff} bytes\n{data_en[i]}\n=====")
        sys.exit(0)

    print("=======================================")
    print(en)
    print(len(en))
    print("=======================================")
    print()
    filedata = filedata.replace(ja, en)

print(f"Filedata: {len(filedata)}")

with open(f"{GAME_DATA_OUT_DIR}/BIN/OPENDEMO.BIN", "wb") as f: f.write(filedata)










