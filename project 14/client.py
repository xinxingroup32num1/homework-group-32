import socket
import time
from gmssl import sm2, func
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import hashlib


def create_key(data):  # 生成对称加密密钥，长度16的字符串
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    n = m.hexdigest()
    return n[0:16]


MaxBytes = 1024 * 1024
host = '127.0.0.1'
port = 11223
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(30)
client.connect((host, port))

public_key = client.recv(MaxBytes).decode()  # 连接后接收服务器的公钥
private_key = ''
sm2_crypt = sm2.CryptSM2(
    public_key=public_key, private_key=private_key)

while True:
    inputData = input();  # 等待输入数据
    if (inputData == "quit"):
        print("退出")
        break
    if (inputData == ''):
        print("请输入信息")
        continue

    ###发送数据
    key = create_key(inputData).encode()  # 生成对称密钥
    iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(key, SM4_ENCRYPT)
    encrypt_data = crypt_sm4.crypt_ecb(inputData.encode())  # 加密信息
    enc_key = sm2_crypt.encrypt(key)  # 对密钥进行加密
    sendBytes = client.send(encrypt_data)  # 客户端发送数据
    sendBytes2 = client.send(enc_key)
    print("客户端发送了：" + inputData)
    if sendBytes <= 0:
        break;
    recvData = client.recv(MaxBytes)
    if not recvData:
        print('服务器不响应，退出')
        break
    localTime = time.asctime(time.localtime(time.time()))
    print(localTime, '服务器成功接受消息')
    # print(localTime, ' 接收到数据字节数:',len(recvData))

    # print(recvData.decode())
client.close()
print("关闭链接")
