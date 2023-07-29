import random
import string

Bits_len = 32

IV = [
    0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
    0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E
]

T = [0x79cc4519, 0x7a879d8a]

def ROL(X, i):
    i = i % 32
    return ((X << i) & 0xFFFFFFFF) | ((X & 0xFFFFFFFF) >> (32 - i))

def FF(X, Y, Z, j):
    if j >= 0 and j <= 15:
        return X ^ Y ^ Z
    else:
        return ((X & Y) | (X & Z) | (Y & Z))

def GG(X, Y, Z, j):
    if j >= 0 and j <= 15:
        return X ^ Y ^ Z
    else:
        return ((X & Y) | (~X & Z))

def P0(X):
    return X ^ ROL(X, 9) ^ ROL(X, 17)

def P1(X):
    return X ^ ROL(X, 15) ^ ROL(X, 23)

def T_(j):
    if j >= 0 and j <= 15:
        return T[0]
    else:
        return T[1]

def decimalToHex(decimal_num):
    hex_chars = string.hexdigits[:-6]  # 只包含0-9和a-f的十六进制字符
    if decimal_num == 0:
        return "0x0"

    hex_string = ""
    while decimal_num > 0:
        remainder = decimal_num % 16
        hex_string = hex_chars[remainder] + hex_string
        decimal_num //= 16

    return "0x" + hex_string

def TC(message):
    m = bin(int(message, 16))[2:]
    if len(m) != len(message) * 4:
        m = '0' * (len(message) * 4 - len(m)) + m
    l = len(m)
    l_bin = '0' * (64 - len(bin(l)[2:])) + bin(l)[2:]
    m = m + '1'
    m = m + '0' * (448 - len(m) % 512) + l_bin
    m = hex(int(m, 2))[2:]
    return m

def Group(m):
    n = len(m) // 128
    M = []
    for i in range(n):
        M.append(m[0 + 128 * i:128 + 128 * i])
    return M

def Expand(M, n):
    W = []
    W_ = []
    for j in range(16):
        W.append(int(M[n][0 + 8 * j:8 + 8 * j], 16))
    for j in range(16, 68):
        W.append(P1(W[j - 16] ^ W[j - 9] ^ ROL(W[j - 3], 15)) ^ ROL(W[j - 13], 7) ^ W[j - 6])
    for j in range(64):
        W_.append(W[j] ^ W[j + 4])
    return W, W_

def CF(V, M, i):
    A, B, C, D, E, F, G, H = V[i]
    W, W_ = Expand(M, i)
    for j in range(64):
        SS1 = ROL((ROL(A, 12) + E + ROL(T_(j), j % 32)) % (2 ** 32), 7)
        SS2 = SS1 ^ ROL(A, 12)
        TT1 = (FF(A, B, C, j) + D + SS2 + W_[j]) % (2 ** 32)
        TT2 = (GG(E, F, G, j) + H + SS1 + W[j]) % (2 ** 32)
        D = C
        C = ROL(B, 9)
        B = A
        A = TT1
        H = G
        G = ROL(F, 19)
        F = E
        E = P0(TT2)

    a, b, c, d, e, f, g, h = V[i]
    V_ = [a ^ A, b ^ B, c ^ C, d ^ D, e ^ E, f ^ F, g ^ G, h ^ H]
    return V_

def SM3(M, IVV):
    n = len(M)
    V = []
    V.append(IVV)
    for i in range(n):
        V.append(CF(V, M, i))
    return V[n]

def RandomList(n):
    numbers = []
    while len(numbers) < n:
        i = random.randint(0, pow(2, 64))
        if i not in numbers:
            numbers.append(i)
    return numbers

def LengthAttack(M, IVV, num):
    for i in range(num):
        M = '0' + M
    m2 = TC(M)
    print("m2:", m2)
    M2 = Group(m2)
    Vn1 = SM3(M2, IVV)
    return Vn1


if __name__ == "__main__":
    list_r_value = []
    list_r = ['1234', '5678']
    m = TC(list_r[0])
    list_m = m + list_r[1]
    M = Group(m)

    Vn = SM3(M, IV)
    aa = ""
    for x in Vn:
        aa += hex(x)[2:]
    list_r_value.append(aa)

    print(Vn)
    print(IV)
    print(list_m)

    m1 = TC(list_m)
    print('m1:', m1)
    M1 = Group(m1)
    Vn1 = SM3(M1, IV)
    aa1 = ""
    for x in Vn1:
        aa1 += hex(x)[2:]
    list_r_value.append(aa1)

    Vn2 = LengthAttack(list_r[1], Vn, 128)
    aa2 = ""
    for x in Vn2:
        aa2 += hex(x)[2:]
    list_r_value.append(aa2)

    print(list_r_value)
