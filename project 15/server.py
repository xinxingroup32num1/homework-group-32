import socket
import time
from gmssl import sm3, func
from Crypto.Util import number
import random
MaxBytes=1024*1024
A = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
B = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
#有限域的阶
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
x_G = 0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7
y_G = 0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0
#椭圆曲线的阶
N = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
G = (x_G, y_G)#G为基点
def gcd1(a, b):
    if b == 0:
        return 1,0,a
    else:
        x, y, gcd = gcd1(b, a % b)
        x, y = y, (x - (a // b) * y)
        return x,y,gcd
#椭圆曲线上的同一点加法运算（*2运算）
def elliptic_double(x1,y1):
    t1 = (3 * (x1 * x1)%p + A)%p
    t2 = gcd1((2 * y1) % p,p)[0]
    t = (t1 * t2) % p
    x3 = ((t * t) % p - x1 - x1) % p
    y3 = ((t * (x1 - x3)%p) % p - y1) % p
    return x3,y3
#椭圆曲线上的不同点加法运算
def elliptic_add(x1,y1):
    t1 = (y_G - y1) % p
    t2 =gcd1((x_G - x1) % p,p)[0]
    t = (t1 * t2) % p
    x3 = ((t * t) % p - x1 - x_G) % p
    y3 = ((t * (x1 - x3)%p) % p - y1) % p
    return x3,y3
#椭圆曲线上的乘法运算
def multiply(x1,y1,k):
    if k == 2:
        return elliptic_double(x1,y1)
    if k == 3:
        x1,y1 = elliptic_double(x1,y1)
        return elliptic_add(x1,y1)
    if k % 2 == 0:
        x1,y1 = multiply(x1, y1, k // 2)
        x1,y1 = elliptic_double(x1,y1)
        return x1,y1
    if k % 2 == 1:
        x1,y1 = multiply(x1, y1, (k - 1) // 2)
        x1,y1 = elliptic_double(x1,y1)
        x1,y1 = elliptic_add(x1,y1)
        return x1,y1
#计算比特位
def bit_num(x):
    if isinstance(x,str):
        return len(x.encode())<<3#一个字节8个比特
def precomputation(ID,A,B,G_X,G_Y):
    #将必要信息转化为字符串，以便转化为字节对象进行操作
    A=str(A)
    B=str(B)
    G_X=str(G_X)
    G_Y=str(G_Y)
    ENTLA=str(bit_num(ID))#签名者A具有长度为entlen比特的可辨别标识ID，ENTLA是由整数entlen转换而成的两个字节
    #print(ENTLA)
    cascading=ENTLA+ID+A+B+G_X+G_Y#级联
    cascading_bytes=bytes(cascading,encoding='utf-8')
    digest=sm3.sm3_hash(func.bytes_to_list(cascading_bytes))#转换为列表后利用库函数进行sm3的hash
    #print(type(digest))
    return digest#计算出Z_A=H256(ENTLA||ID||a||b||G_X||G_Y)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.settimeout(60)
host = '127.0.0.1'
port = 11223
server.bind((host, port))        # 绑定端口
server.listen(1)                      # 监听
try:
    client,addr = server.accept()          # 等待客户端连接
    print(addr," 客户端连接")
    d1=0xFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF203DF6B21C6052B53BBF40939D54123
    #生成随机数
    x1=G[0]
    y1=G[1]
    p1=multiply(x1,y1,number.inverse(d1,p))
    #print(number.inverse(d1,p))
    client.send(str(p1[0]).encode())#向客户端发送p1
    time.sleep(1)
    client.send(str(p1[1]).encode())#向客户端发p1
    ID='2020'
    Z=precomputation(ID,A,B,x_G,y_G)
    mes='xinxi'
    mes2=Z+mes#m*=Z||m
    mes2_bytes=bytes(mes2,encoding='utf-8')
    e=sm3.sm3_hash(func.bytes_to_list(mes2_bytes))#e=Hash(m*)
    k1=random.randint(1,N)#0xFFFFFFEFFFFFFFFFFFFF203DF6B21C6052B53BBF40939D54123#随机数
    q1=multiply(x1,y1,k1)
    client.send(e.encode())#向客户端发送k1
    time.sleep(1)
    client.send(str(q1[0]).encode())#向客户端发送q1
    print(q1[0])
    time.sleep(1)
    client.send(str(q1[1]).encode())#向客户端发q1
    print(q1[1])
    r=client.recv(MaxBytes).decode()
    print('r',r)
    r=int(r)
    s2=client.recv(MaxBytes).decode()
    print('s2',s2)
    s2=int(s2)
    s3=client.recv(MaxBytes).decode()
    print('s3',s3)
    s3=int(s3)
    s=((d1*k1)*s2+d1*s2-r)%N
    if s!=0 or s!=N-r:
        sig=(r,s)
        print("签名:",sig)

except BaseException as e:
    print("出现异常：")
    print(repr(e))
finally:
    server.close()                    # 关闭连接
    print("关闭链接")