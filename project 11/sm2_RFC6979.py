from gmssl import sm3, func
from hashlib import sha256
import secrets
from Crypto.Util import number

A = 115792089210356248756420345214020892766250353991924191454421193933289684991996
B = 18505919022281880113072981827955639221458448578012075254857346196103069175443
G_X = 22963146547237050559479531362550074578802567295341616970375194840604139615431
G_Y = 85132369209828568825618990617112496413088388631904505083283536607588877201568
G = (G_X, G_Y)  # G为基点
# 有限域的阶
P = 115792089210356248756420345214020892766250353991924191454421193933289684991999
# 椭圆曲线的阶
N = 115792089210356248756420345214020892766061623724957744567843809356293439045923


# 椭圆曲线上的不同点加法运算
def elliptic_add(p, q):
    if p == [0, 0] and q == [0, 0]:
        return [0, 0]
    elif p == [0, 0]:
        return q
    elif q == [0, 0]:
        return p
    else:
        # 保证p[0]<=q[0]
        if p[0] > q[0]:
            temp = p
            p = q
            q = temp
        r = []
        # 当P！=Q时，两点纵坐标相减的值与横坐标相减的值相除就是直线的斜率
        slope = (q[1] - p[1]) * number.inverse(q[0] - p[0], P) % P
        r.append((slope ** 2 - p[0] - q[0]) % P)
        r.append((slope * (p[0] - r[0]) - p[1]) % P)
        return (r[0], r[1])


# 椭圆曲线上的同一点加法运算（*2运算）
def elliptic_double(p):
    # 当P=Q，计算过P(Q)点切线的斜率为椭圆曲线公式两边求导相除：λ = (3*p[0]² + A)/2*p[1]
    r = []
    slope = (3 * (p[0] ** 2) + A) * number.inverse(2 * p[1], P) % P
    r.append((slope ** 2 - 2 * p[0]) % P)
    r.append((slope * (p[0] - r[0]) - p[1]) % P)
    return (r[0], r[1])


# 椭圆曲线上的乘法运算
def elliptic_multiply(s, p):
    n = p
    r = [0, 0]  # 无穷远点
    s_bin = bin(s)[2:]  # 转化为二进制
    s_len = len(s_bin)  # 二进制长度
    for i in reversed(range(s_len)):  # 从s_len-1到0逐位计算
        if s_bin[i] == '1':
            r = elliptic_add(r, n)
        n = elliptic_double(n)  # n乘2,继续循环
    return r


# 生成公私钥
def generate_key():
    # 私钥：大整数
    # 公钥：椭圆曲线上的点,有基点和私钥生成
    prikey = int(secrets.token_hex(32), 16)  # 返回十六进制随机文本字符串,有n个字节的随机字节，每个字节转换为两个十六进制数字
    pubkey = elliptic_multiply(prikey, G)
    return prikey, pubkey


# 计算比特位
def bit_num(x):
    if isinstance(x, str):
        return len(x.encode()) << 3  # 一个字节8个比特


# 预计算部分，传入参数包括：ID,椭圆曲线参数A,B,G点的横纵坐标G_X,G_Y,公钥的横纵坐标public_key[0],public_key[1]
def precomputation(ID, A, B, G_X, G_Y, pub_x, pub_y):
    # 将必要信息转化为字符串，以便转化为字节对象进行操作
    A = str(A)
    B = str(B)
    G_X = str(G_X)
    G_Y = str(G_Y)
    pub_x = str(pub_x)
    pub_y = str(pub_y)
    ENTLA = str(bit_num(ID))  # 签名者A具有长度为entlen比特的可辨别标识ID，ENTLA是由整数entlen转换而成的两个字节
    # print(ENTLA)
    cascading = ENTLA + ID + A + B + G_X + G_Y + pub_x + pub_y  # 级联
    cascading_bytes = bytes(cascading, encoding='utf-8')
    digest = sm3.sm3_hash(func.bytes_to_list(cascading_bytes))  # 转换为列表后利用库函数进行sm3的hash
    # print(type(digest))
    return digest  # 计算出Z_A=H256(ENTLA||ID||a||b||G_X||G_Y||pub_x||pub_y)


# 签名生成（r,s）
def sign(private_key, mes, Z_A):
    mes2 = Z_A + mes  # m*=Z_A||m
    mes2_bytes = bytes(mes2, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(mes2_bytes))  # e=Hash(m*)
    e = int(e, 16)
    ##    k=secrets.randbelow(P)#0-P的随机数
    K_bytes = bytes(ID + str(A) + str(B) + mes, encoding='utf-8')
    k = sm3.sm3_hash(func.bytes_to_list(K_bytes))
    k = int(k, 16)  # RFC6979产生保密且唯一确定的数k
    # 计算椭圆曲线点(x_1,y_1)=[k]G
    point1 = elliptic_multiply(k, G)  # 该点为k*G
    print("生成的椭圆曲线上的点：", point1)
    # 计算 r=(e+x_1)mod n
    r = (e + point1[0]) % N
    # 计算s=((1+private_key)^(-1)⋅(k−r⋅private_key))mod n
    s = (number.inverse(1 + private_key, N) * (k - r * private_key)) % N
    return (r, s)


# 验证签名（r,s）
def verify(public_key, ID, mes, sig):
    r = sig[0]
    s = sig[1]
    Z_A = precomputation(ID, A, B, G_X, G_Y, public_key[0], public_key[1])
    mes2 = Z_A + mes  # m*=Z_A||m
    mes2_bytes = bytes(mes2, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(mes2_bytes))  # e=Hash(m*)
    e = int(e, 16)
    t = (r + s) % N
    point1 = elliptic_multiply(s, G)
    point2 = elliptic_multiply(t, public_key)
    point = elliptic_add(point1, point2)
    x1 = point[0]
    R = (e + x1) % N
    print('R', R)
    print('r', r)
    return R == r


private_key, public_key = generate_key()
print("公钥：", public_key)
print("私钥：", private_key)
mes = "yanxincai"
ID = '2021'
Z_A = precomputation(ID, A, B, G_X, G_Y, public_key[0], public_key[1])
# print(Z_A)
sig = sign(private_key, mes, Z_A)
print("签名：", sig)
if verify(public_key, ID, mes, sig) == 1:
    print("验证通过")