import socket
import time
import random
from gmssl import sm2, func
from Crypto.Util import number
import hashlib
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
def elliptic_add(x1,y1,x_G,y_G):
    t1 = (y_G - y1) % p
    t2 =gcd1((x_G - x1) % p,p)[0]
    t = (t1 * t2) % p
    x3 = ((t * t) % p - x1 - x_G) % p
    y3 = ((t * (x1 - x3)%p) % p - y1) % p
    return x3,y3
#椭圆曲线上的乘法运算
def multiply(x1,y1,k,x_G,y_G):
    if k == 2:
        return elliptic_double(x1,y1)
    if k == 3:
        x1,y1 = elliptic_double(x1,y1)
        return elliptic_add(x1,y1,x_G,y_G)
    if k % 2 == 0:
        x1,y1 = multiply(x1, y1, k // 2,x_G,y_G)
        x1,y1 = elliptic_double(x1,y1)
        return x1,y1
    if k % 2 == 1:
        x1,y1 = multiply(x1, y1, (k - 1) // 2,x_G,y_G)
        x1,y1 = elliptic_double(x1,y1)
        x1,y1 = elliptic_add(x1,y1,x_G,y_G)
        return x1,y1
def signature(e,q1,d2):
    k2=random.randint(1,N)
    k3=random.randint(1,N)#0xFFFFFFFFFFF7203DF6B21C6052B53BBF40939D5412
    x1=G[0]
    y1=G[1]
    q2=multiply(x1,y1,k2,G[0],G[1])
    a1=q2[0]
    a2=q2[1]
    (x,y)=multiply(a1,a2,k3,q2[0],q2[1])
    (x1,y1)=elliptic_add(x,y,q2[0],q2[1])
    r=(x1+e)%N
    s2=(d2*k3)%N
    s3=(d2*(r+k2))%N
    return r,s2,s3
MaxBytes=1024*1024
host ='127.0.0.1'
port = 11223
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.settimeout(30)
client.connect((host,port))
p11=client.recv(MaxBytes).decode()#连接后接收服务器
print('p1[0]',p11)
p12=client.recv(MaxBytes).decode()#连接后接收服务器
print('p1[1]',p12)
p1=(int(p11),int(p12))
d2=random.randint(1,N)#0xFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123#生成随机数
x=p1[0]
y=p1[1]
P=multiply(x,y,number.inverse(d2,p),p1[0],p1[1])
e=client.recv(MaxBytes).decode()
print('e ',e)
e=int(e,16)
q11=client.recv(MaxBytes).decode()
print(q11)
q12=client.recv(MaxBytes).decode()
print(q12)
q1=(int(q11),int(q12))
##q1=(79215731080529735605946132084997522830521744382126705917961022594911097141449,
##    68542500965596772669686040959863220590570602026118856307127468140918117761845)
r,s2,s3=signature(e,q1,d2)
print('r',r)
client.send(str(r).encode())#客户端发送数据
time.sleep(1)
client.send(str(s2).encode())#客户端发送数据
print('s2',s2)
print('s3',s3)
client.send(str(s3).encode())#客户端发送数据
localTime = time.asctime( time.localtime(time.time()))
print(localTime,'服务器成功接受消息')