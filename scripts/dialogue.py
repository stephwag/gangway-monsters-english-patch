from script_config import *
import textwrap
import argparse
import sys
import re

# NOTES
# - each line in a paragraph much have an even number of chars
# - use spaces instead of newline for <name> since that has variable length

LINE_LENGTH = 24
PARAGRAPH_LENGTH = LINE_LENGTH * 3

w = textwrap.TextWrapper()
w.drop_whitespace = True
#w.drop_whitespace = False
w.break_on_hyphens = True
w.width = LINE_LENGTH


def fill_bytes(l):
    return w.fill(l.decode('shift-jis')).encode('shift-jis')

def fill_bytes_ja(l):
    dat = [s.encode('shift-jis') for s in w.wrap(l.decode('shift-jis'))]
    return b'\x81\x40\x0A'.join(dat)

def wrap_bytes(p):
    lines = [s.encode('shift-jis') for s in w.wrap(p.decode('shift-jis'))]
    return lines

def count_lines(p):
    return len(wrap_bytes(p))

def fix_dialogue(data, diff, idx):
    p = data.split(b'\x0C')
    last_p = len(p)-1

    for i in range(len(p)):
        prev_size = len(p[i])
        lines = p[i].split(b'\n')
        for k in range(len(lines)):
            if len(lines[k]) % 2 > 0 and len(lines[k]) < LINE_LENGTH:
                if diff > 0:
                    lines[k] += b'\x20'
                    diff -= 1
                else:
                    raise ValueError(f"Error, this is odd {lines[k]} at file {idx}")

        if len(lines) == 2 and len(lines[0]) == LINE_LENGTH:
            p[i] = b''.join(lines)
            diff += 1

        else:
            p[i] = b'\n'.join(lines)

    if diff > 1:
        for i in range(len(p)):
            if count_lines(p[i]) == 1:
                while len(p[i]) < PARAGRAPH_LENGTH and diff > 1:
                    p[i] += b'\x20\x20'
                    diff -= 2
                    if diff == 0: break

    if diff > 0:
        while len(p[last_p]) < PARAGRAPH_LENGTH and diff > 0:
            p[i] += b'\x20'
            diff -= 1
            if diff == 0: break

    print(f"final diff: {diff}")
    return b'\x0C'.join(p)

with open(f"{GAME_DATA_IN_DIR}/BIN/OPENDEMO.BIN", "rb") as f: filedata = f.read()

data_en = []
data_ja = []

for i in range(27):
    with open(f'opendemo/en_raw/{i}.txt', 'r') as f:
        data_en.append(f.read())
    with open(f'opendemo/ja/{i}.txt', 'r') as f:
        data_ja.append(f.read())

print(f"Filedata: {len(filedata)}")

for i in range(len(data_ja)):
    en = data_en[i].encode('shift-jis')
    ja = data_ja[i].encode('shift-jis')


    p = en.split(b'\x0C')
    for k in range(len(p)):
        p[k] = fill_bytes(p[k])

    en = b'\x0C'.join(p)

    diff = len(ja) - len(en)
    if diff < 0:

        print(f"====\nError: Must shorten {i} by {diff} bytes\n{data_en[i]}\n=====")
        sys.exit(0)

    en = fix_dialogue(en, diff, i)
    print(len(en))
    with open(f'opendemo/en/{i}.txt', 'w') as f: f.write(en.decode('shift-jis'))

    print("=======================================")
    print(en)
    print(len(en))
    print("=======================================")
    print()
    filedata = filedata.replace(ja, en)

print(f"Filedata: {len(filedata)}")
#with open(f"{GAME_DATA_OUT_DIR}/BIN/OPENDEMO.BIN", "wb") as f: f.write(filedata)










