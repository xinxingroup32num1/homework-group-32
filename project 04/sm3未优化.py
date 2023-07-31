import time

def sm3_padding(message):
    original_len = len(message)
    bit_len = original_len * 8

    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'

    message += bit_len.to_bytes(8, 'big')
    return message

def sm3_rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def sm3_ffj(x, y, z, j):
    if j <= 15:
        return x ^ y ^ z
    elif j <= 63:
        return (x & y) | (x & z) | (y & z)

def sm3_ggj(x, y, z, j):
    if j <= 15:
        return x ^ y ^ z
    elif j <= 63:
        return (x & y) | (~x & z)

def sm3_compress(block, v):
    w = [0] * 68
    w[0:16] = [int.from_bytes(block[i:i+4], 'big') for i in range(0, 64, 4)]

    for j in range(16, 68):
        w[j] = (sm3_rotl(w[j-16] ^ w[j-9] ^ sm3_rotl(w[j-3], 15), 7) ^ sm3_rotl(w[j-13], 7) ^ w[j-6]) ^ (j+1)

    a, b, c, d, e, f, g, h = v

    for j in range(64):
        ss1 = sm3_rotl((sm3_rotl(a, 12) + e + sm3_rotl(0x79CC4519, j % 32)), 7) & 0xFFFFFFFF
        ss2 = ss1 ^ sm3_rotl(a, 12)
        tt1 = (sm3_ffj(a, b, c, j) + d + ss2 + w[j]) & 0xFFFFFFFF
        tt2 = (sm3_ggj(e, f, g, j) + h + ss1 + w[j]) & 0xFFFFFFFF
        d = c
        c = sm3_rotl(b, 9)
        b = a
        a = tt1
        h = g
        g = sm3_rotl(f, 19)
        f = e
        e = sm3_ffj(e, f, g, j)
        v = [a, b, c, d, e, f, g, h]

    return [(x + y) & 0xFFFFFFFF for x, y in zip(v, [a, b, c, d, e, f, g, h])]

def sm3_hash(message):
    message = sm3_padding(message)
    blocks = [message[i:i+64] for i in range(0, len(message), 64)]

    v = [
        0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
        0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E
    ]

    for block in blocks:
        v = sm3_compress(block, v)

    return b''.join([x.to_bytes(4, 'big') for x in v])

if __name__ == '__main__':
    message = b'202100460112shandongdaxue'
    start = time.time()
    for i in range(10):
        hash_value = sm3_hash(message)
    end = time.time()
    print(hash_value.hex())
    print("运行时间为",(end-start)*100,"ms")
