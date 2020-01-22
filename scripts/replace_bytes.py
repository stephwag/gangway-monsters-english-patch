# -*- coding: utf-8 -*-

from script_config import *
from lzss import compress, decompress
import argparse
import sys
import os

# strings where the English version should end with term, then padded with spaces
term_strings = [
    "レックス",
    "オークス",
    "リーダー",
    "メリック",
    "マイヤー",
    "プラーグ",
    "ピラミン",
    "ジョニー",
    "ポックル",

    "パイディア",
    "クエッキー",
    "ペリーニン",
    "スクリーム",
    "フランキー",
    "マシンガン",

    "バッドバット",

    "エンジェルマニア",
    "マシンガンジョー",
    "スピードマスター",

    "ブラー",
    "スカル",
    "エッヂ",

    "カムカムクロー",
]

MONBOOK_PARAGRAPH_LENGTH = 308
MONBOOK_LINE_LENGTH = 36

filename = "slps"

space = b'\x20'
blank = b'\xFF'
space = b'\x20'
term = b'\x00'
endline = b'\x0C'
jadash = b'\x81\x5B' # This: ー

sort_files = False

ja_keyboard = b'\x83\x52\x00\x00\x83\x50\x00\x00\x83\x4E\x00\x00\x83\x4C\x00\x00\x83\x4A\x00\x00\x81\x40\x00\x00\x83\x49\x00\x00\x83\x47\x00\x00\x83\x45\x00\x00\x83\x43\x00\x00\x83\x41\x00\x00\x83\x67\x00\x00\x83\x65\x00\x00\x83\x63\x00\x00\x83\x60\x00\x00\x83\x5E\x00\x00\x83\x5C\x00\x00\x83\x5A\x00\x00\x83\x58\x00\x00\x83\x56\x00\x00\x83\x54\x00\x00\x83\x7A\x00\x00\x83\x77\x00\x00\x83\x74\x00\x00\x83\x71\x00\x00\x83\x6E\x00\x00\x83\x6D\x00\x00\x83\x6C\x00\x00\x83\x6B\x00\x00\x83\x6A\x00\x00\x83\x69\x00\x00\x83\x88\x00\x00\x83\x86\x00\x00\x83\x84\x00\x00\x83\x82\x00\x00\x83\x81\x00\x00\x83\x80\x00\x00\x83\x7E\x00\x00\x83\x7D\x00\x00\x83\x94\x00\x00\x83\x93\x00\x00\x83\x92\x00\x00\x83\x8F\x00\x00\x83\x8D\x00\x00\x83\x8C\x00\x00\x83\x8B\x00\x00\x83\x8A\x00\x00\x83\x89\x00\x00\x83\x5D\x00\x00\x83\x5B\x00\x00\x83\x59\x00\x00\x83\x57\x00\x00\x83\x55\x00\x00\x83\x53\x00\x00\x83\x51\x00\x00\x83\x4F\x00\x00\x83\x4D\x00\x00\x83\x4B\x00\x00\x83\x7B\x00\x00\x83\x78\x00\x00\x83\x75\x00\x00\x83\x72\x00\x00\x83\x6F\x00\x00\x83\x68\x00\x00\x83\x66\x00\x00\x83\x64\x00\x00\x83\x61\x00\x00\x83\x5F\x00\x00\x83\x48\x00\x00\x83\x46\x00\x00\x83\x44\x00\x00\x83\x42\x00\x00\x83\x40\x00\x00\x83\x7C\x00\x00\x83\x79\x00\x00\x83\x76\x00\x00\x83\x73\x00\x00\x83\x70\x00\x00\x81\x5B\x00\x00\x83\x62\x00\x00\x83\x87\x00\x00\x83\x85\x00\x00\x83\x83'
en_keyboard = b'\x65\x00\x00\x00\x64\x00\x00\x00\x63\x00\x00\x00\x62\x00\x00\x00\x61\x00\x00\x00\x20\x00\x00\x00\x45\x00\x00\x00\x44\x00\x00\x00\x43\x00\x00\x00\x42\x00\x00\x00\x41\x00\x00\x00\x6A\x00\x00\x00\x69\x00\x00\x00\x68\x00\x00\x00\x67\x00\x00\x00\x66\x00\x00\x00\x4A\x00\x00\x00\x49\x00\x00\x00\x48\x00\x00\x00\x47\x00\x00\x00\x46\x00\x00\x00\x6F\x00\x00\x00\x6E\x00\x00\x00\x6D\x00\x00\x00\x6C\x00\x00\x00\x6B\x00\x00\x00\x4F\x00\x00\x00\x4E\x00\x00\x00\x4D\x00\x00\x00\x4C\x00\x00\x00\x4B\x00\x00\x00\x72\x00\x00\x00\x71\x00\x00\x00\x70\x00\x00\x00\x54\x00\x00\x00\x53\x00\x00\x00\x52\x00\x00\x00\x51\x00\x00\x00\x50\x00\x00\x00\x76\x00\x00\x00\x75\x00\x00\x00\x74\x00\x00\x00\x73\x00\x00\x00\x59\x00\x00\x00\x58\x00\x00\x00\x57\x00\x00\x00\x56\x00\x00\x00\x55\x00\x00\x00\x20\x00\x00\x00\x7A\x00\x00\x00\x79\x00\x00\x00\x78\x00\x00\x00\x77\x00\x00\x00\x21\x00\x00\x00\x3F\x00\x00\x00\x23\x00\x00\x00\x3E\x00\x00\x00\x3C\x00\x00\x00\x26\x00\x00\x00\x25\x00\x00\x00\x2A\x00\x00\x00\x24\x00\x00\x00\x5C\x00\x00\x00\x40\x00\x00\x00\x2B\x00\x00\x00\x2D\x00\x00\x00\x27\x00\x00\x00\x22\x00\x00\x00\x39\x00\x00\x00\x38\x00\x00\x00\x37\x00\x00\x00\x36\x00\x00\x00\x35\x00\x00\x00\x34\x00\x00\x00\x33\x00\x00\x00\x32\x00\x00\x00\x31\x00\x00\x00\x30\x00\x00\x00\x5F\x00\x00\x00\x2E\x00\x00\x00\x2C\x00\x00\x00\x29\x00\x00\x00\x28\x00'

allowedbuffer = 0
too_many_bytes = False

def replace_asm(filename, data):
    if filename == "slps":
        # Reduce cursor x position change from 4 shifts to 3 shifts during input mode
        data = data.replace(
                b'\x30\x00\x02\x09\x00\x42\x2A\x0E\x00\x40\x14\x00\x11\x11\x00\x05',
                b'\x30\x00\x02\x09\x00\x42\x2A\x0E\x00\x40\x14\xc0\x10\x11\x00\x05'
                )

        # Delete only one byte at a time during input mode
        data = data.replace(
                b'\x21\x10\x62\x00\xFE\xFF\x40\xA0',
                b'\x21\x10\x62\x00\xFF\xFF\x40\xA0'
                )

        # Start deletion at the first byte instead of second
        data = data.replace(
                b'\x00\x00\x00\x00\x10\x00\x42\x28',
                b'\x00\x00\x00\x00\x08\x00\x42\x28'
            )
        data = data.replace(
                b'\x21\x18\x40\x00\x02\x00\x62\x28',
                b'\x21\x18\x40\x00\x01\x00\x62\x28',
            )

    if filename == "battle":
        # 01 00 83 90 -> 00 00 83 90
        # 00 00 82 90 -> 83 00 02 34 (change command to ori with 0x83)
        # set first register with 0x83 and load the first byte of text, instead of loading two bytes
        # this will cause the text to draw again on the VS screen
        # Note that it isn't real Japanese, it is just associating characters based on ascii characters with 0x83 prepended to it
        data = data.replace(
            b'\x08\x00\xE0\x03\x60\x00\xBD\x27\x0D\x80\x02\x3C\xDC\x81\x42\x8C\x00\x00\x00\x00\x03\x00\x82\x14\x00\x00\x00\x00\x0D\x80\x02\x3C\xD8\x81\x42\x8C\x08\x00\xE0\x03\x00\x00\x00\x00\x00\x00\x82\x90\x01\x00\x83\x90\x00\x12\x02\x00\x21\x18\x62\x00\xFF\xFF\x64\x30\x5B\x81\x02\x34\x02\x00\x82\x14\x50\x00\x05\x24\x4F\x00\x05\x24\x3F\x83\x02\x34\x2B\x10\x44\x00\x0A\x00\x40\x10\x7E\x83\x02\x34\x2B\x10\x44\x00\x03\x00\x40\x14\x94\x83\x02\x34\x31\xC7\x02\x08',
            b'\x08\x00\xE0\x03\x60\x00\xBD\x27\x0D\x80\x02\x3C\xDC\x81\x42\x8C\x00\x00\x00\x00\x03\x00\x82\x14\x00\x00\x00\x00\x0D\x80\x02\x3C\xD8\x81\x42\x8C\x08\x00\xE0\x03\x00\x00\x00\x00\x83\x00\x02\x34\x00\x00\x83\x90\x00\x12\x02\x00\x21\x18\x62\x00\xFF\xFF\x64\x30\x5B\x81\x02\x34\x02\x00\x82\x14\x50\x00\x05\x24\x4F\x00\x05\x24\x3F\x83\x02\x34\x2B\x10\x44\x00\x0A\x00\x40\x10\x7E\x83\x02\x34\x2B\x10\x44\x00\x03\x00\x40\x14\x94\x83\x02\x34\x31\xC7\x02\x08'
            )
        # swap the bit shift with the command that adds 8, so it won't skip every 2nd letter when drawing battle text
        data = data.replace(
            b'\x21\x28\xA3\x00\x00\x8C\x14\x00\x03\x8C\x11\x00\x40\x80\x11\x00\x08\x00\x04\x26\x1B\xC7\x02\x0C\x21\x20\xA4\x00\x21\x80\x11\x02\x40\x80\x10\x00\x80\x02\x10\x26\x00\x84\x10\x00\x03\x24\x10\x00',
            b'\x21\x28\xA3\x00\x00\x8C\x14\x00\x03\x8C\x11\x00\x08\x00\x24\x26\x40\x80\x11\x00\x1B\xC7\x02\x0C\x21\x20\xA4\x00\x21\x80\x11\x02\x40\x80\x10\x00\x80\x02\x10\x26\x00\x84\x10\x00\x03\x24\x10\x00'
            )

        # TODOs:
        # - battle text may be aligned weirdly if the name has an odd number of bytes (or if it's longer than 8 characters)
        # - needs to draw 16 characters instead of 8
        # - if texture is updated to english, it might have to be smaller (at least for the default names, name input only allows 8).

    return data

def load_monbook_ja(filename):
    with open(filename, "rb") as f: data = decompress(f.read())
    idx = data.find(b'\x10\x00\x00\x00')
    data = data[:idx]
    results = []
    
    while len(data) > 0:
        results.append(data[:MONBOOK_PARAGRAPH_LENGTH])
        data = data[MONBOOK_PARAGRAPH_LENGTH:]

    return results

def load_monbook_translations(filename):
    with open(filename, "r") as f:
        paragraphs = f.read().strip().encode('shift-jis').split(b'\n\n\n\n')

    results = []

    for p in paragraphs:
        lines = p.split(b'\n')
        if len(lines) < 8:
            raise ValueError("Paragraph has less than 8 lines (starts with {})"
                .format(final_p[:20]))

        for i in range(len(lines)):
            line = lines[i]
            if len(line) > MONBOOK_LINE_LENGTH:
                raise ValueError(f"Line {line} is too long by {len(line)-MONBOOK_LINE_LENGTH} bytes")
            diff = 36 - len(line)
            line += (b'\x20' * diff)
            lines[i] = line

        final_p = b'\r\n'.join(lines)
        diff = (MONBOOK_PARAGRAPH_LENGTH - len(final_p)) // 2
        final_p += (b'\r\n' * diff)

        if len(final_p) > MONBOOK_PARAGRAPH_LENGTH:
            raise ValueError("Final paragraph is too long by {} bytes (starts with {})"
                .format(len(final_p)-MONBOOK_PARAGRAPH_LENGTH, final_p[:20]))

        results.append(final_p)

    return results

def fix_line(line):
    line = line.replace("\\n", "\n")
    temp = ''
    d_length = 0

    for chunk in line.split(' '):
        if (d_length + len(chunk)) > 24:
            temp += '\n' + chunk
            d_length = len(chunk)
        else:
            temp += " " + chunk
            d_length += len(chunk) + 1

    return temp.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to translate Gangway Monsters.')
    parser.add_argument('filename', help='Name of game file to modify (e.g. "slps" or "battle")')
    parser.add_argument('--sort', action='store_true',
                   help='Sort the translation pairing for the relevant game file. Use when translations have been modified. Default is false.')
    parser.add_argument('--export', action='store_false',
                   help='Build and export new game binary. Default is true.')

    args = parser.parse_args(sys.argv[1:])


    if args.filename == "monbook":
        monbook_ja = load_monbook_ja(f"{GAME_DATA_IN_DIR}/BATTLE/MONBOOK.TIM")

        try:
            monbook_en = load_monbook_translations(f"{TRANSLATIONS_PATH}/en.{args.filename}.txt")
        except ValueError as e:
            too_many_bytes = True
            too_many_bytes_reason = str(e)

        if too_many_bytes:
            print(too_many_bytes_reason)
        else:
            with open(f"{GAME_DATA_IN_DIR}/BATTLE/MONBOOK.TIM", "rb") as f:
                data = decompress(f.read())

            for i in range(len(monbook_en)):
                data = data.replace(monbook_ja[i], monbook_en[i])

            compressed_data = compress(data)
            with open(f"{GAME_DATA_OUT_DIR}/BATTLE/MONBOOK.TIM", "wb") as f: f.write(compressed_data)

    else:
        if args.filename == "slps":
            with open(f"{GAME_DATA_IN_DIR}/SLPS_014.68", "rb") as f: rawdata = f.read()
        elif args.filename == "fdevent":
            with open(f"{GAME_DATA_IN_DIR}/FIELD/FDEVENT.ACB", "rb") as f: rawdata = f.read()
        elif args.filename == "opendemo":
            # Run this after running dialogue scripts. This will translate mostly menu items.
            with open(f"{GAME_DATA_IN_DIALOGUE_DIR}/{args.filename}.BIN", "rb") as f: rawdata = f.read()
        else:
            with open(f"{GAME_DATA_IN_DIR}/BIN/{args.filename.upper()}.BIN", "rb") as f: rawdata = f.read()

        with open(f"{TRANSLATIONS_PATH}/ja.{args.filename}.txt", "r") as f: dataja = f.read()
        with open(f"{TRANSLATIONS_PATH}/en.{args.filename}.txt", "r") as f: dataen = f.read()

        linesja = dataja.split("\n")
        linesen = dataen.split("\n")

        if sort_files:
            temp_lines = []
            all_lines = []
            finalja = []
            finalen = []
            for i in range(len(linesja)):
                temp_lines.append(linesja[i] + "\t" + linesen[i])
            all_lines = sorted(temp_lines, key=len, reverse=True)
            for line in all_lines:
                parts = line.split("\t")
                finalja.append(parts[0])
                finalen.append(parts[1])
            with open(f"{TRANSLATIONS_PATH}/ja.{args.filename}.txt", "w") as f: f.write("\n".join(finalja))
            with open(f"{TRANSLATIONS_PATH}/en.{args.filename}.txt", "w") as f: f.write("\n".join(finalen))
            sys.exit(0)

        dataresult = rawdata

        for i in range(len(linesja)):
            #linesen[i] = linesen[i].replace("\\n", "\n")
            b1 = linesja[i].encode('shift-jis')
            b2 = linesen[i].encode('shift-jis')

            if len(b2) <= len(b1):
                l = len(b1) - len(b2)

                if (b1.decode('shift-jis') in term_strings) and args.filename in ["slps"]:
                    padding = (term * l)
                else:
                    padding = (space * l)

                b2 += padding
                dataresult = dataresult.replace(b1, b2)
            else:
                too_many_bytes = True
                print(b1.decode('shift-jis'))
                print(b2.decode('shift-jis'))
                print()

        if too_many_bytes:
            print("ERROR: Fix above issues first.")
        else:
            dataresult = replace_asm(args.filename, dataresult)
            if args.filename == "slps":
                dataresult = dataresult.replace(ja_keyboard, en_keyboard)
                binname = f"{GAME_DATA_OUT_DIR}/SLPS_014.68"
                with open(binname, "wb") as f: f.write(dataresult)
            elif args.filename == "fdevent":
                binname = f"{GAME_DATA_OUT_DIR}/FIELD/FDEVENT.ACB"
                with open(binname, "wb") as f: f.write(dataresult)
            else:
                fname = args.filename.upper()
                binname = f"{GAME_DATA_OUT_DIR}/BIN/{fname}.BIN"
                with open(binname, "wb") as f: f.write(dataresult)

            print(f"Written data to {binname}")

    if args.export and not too_many_bytes:
        os.system(f"/bin/bash -c \"cd {GAME_IMAGE_DIR} && psxbuild g.cat && rm {GAME_IMAGE_EMU_BIN} && cp g.bin {GAME_IMAGE_EMU_BIN}\"")
        print(f"Built and imported game binary")








