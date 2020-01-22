MIN_REF_LEN = 2
MAX_REF_LEN = 0xf
HEADER_SIZE = 8
WINDOW_SIZE = 0xfff
MAX_WINDOW_SIZE = 0x1000
count = 0

def correct_offset(raw_offset, tail):
    return tail - ((tail - raw_offset) & WINDOW_SIZE)

def byte_header_size(total_size):
    chunk = bytearray()
    chunk.append((total_size & 0x000000ff))
    chunk.append((total_size & 0x0000ff00) >> 8)
    chunk.append((total_size & 0x00ff0000) >> 16)
    chunk.append((total_size & 0xff000000) >> 24)
    return chunk

def find_data(data, i):
    min_idx = (( i // MAX_WINDOW_SIZE ) * MAX_WINDOW_SIZE)
    subdata = data[min_idx:i]
    for k in range(16, 1, -1):
        chunk = data[i:i+k]
        offset = subdata.rfind(chunk)
        if offset > -1:
            sublen = len(subdata)
            length = len(chunk)
            return (offset, length)
    return None

def decompress(data, remove_header=True):
    if remove_header:
        # MONBOOK.TIM has 1A 2B 01 00 30 AB 03 00 (compressed size, decompressed size)
        data = data[HEADER_SIZE:]

    result = bytearray()
    idx = 0

    while idx < len(data)-7:
        flags = data[idx]
        idx += 1

        for t in range(8):
            flag = flags & 1
            flags = flags >> 1

            if flag > 0:
                result.append(data[idx])
                idx += 1

            else:
                byte1, byte2 = data[idx:idx+2]
                idx += 2

                offset = (((byte1 << 8) | byte2) >> 4) & WINDOW_SIZE
                length = ((byte1 << 8) | byte2) & 0xf
                offset = correct_offset(offset, len(result))

                if length == 0:
                    result.append(result[offset-1])
                    result.append(result[offset])

                else:
                    for k in range(length+2):
                        result.append(result[offset-1+k])
    return result

def compress(data):
    total_size = byte_header_size(len(data))
    result = bytearray()
    idx = 0
    max_len = len(data)
    startprint = False
    while idx < max_len:
        flag = 0
        chunk = bytearray()

        for bit in range(8):
            
            match = find_data(data, idx)
            if match:
                offset, length = match
                l = (length-2)
                o = (offset + 1) & WINDOW_SIZE

                chunk.append(((o & 0xff0) >> 4))
                chunk.append(((o & 0xf) << 4) | ((l & 0xf)))
                idx += length
            else:
                if idx < max_len:
                    flag |= (1 << bit)
                    chunk.append(data[idx])
                    idx += 1
                else:
                    break

        result.append(flag)
        result += chunk
        chunk = bytearray()

    total_size_result = byte_header_size(len(result))

    return (total_size_result + total_size + result)

if __name__ == "__main__":
    compressit = False

    if not compressit:
        with open("MONBOOK.TIM", "rb") as f: d = f.read()
        data = d[HEADER_SIZE:]
        res = decompress(bytearray(data))
        print(f"Decompressed {len(res)} bytes")
        with open("MONBOOK.TIM.OUT", "wb") as f: f.write(res)
    else:
        with open("MONBOOK.TRANSLATED.TIM", "rb") as f: d = f.read()

        #total_size = byte_header_size(len(d))
        res = compress(d)
        print(f"Compressed {len(res)} bytes")
        #total_size_res = byte_header_size(len(res))
        #res = total_size_res + total_size + res

        with open("MONBOOK.MINE.TIM", "wb") as f: f.write(res)




