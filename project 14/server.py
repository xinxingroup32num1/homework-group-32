import socket
import time
from gmssl import sm2, func
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
MaxBytes=1024*1024
private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.settimeout(60)
host = '127.0.0.1'
#host = socket.gethostname()
port = 11223
server.bind((host, port))        # 绑定端口
server.listen(1)                      # 监听
try:
    client,addr = server.accept()          # 等待客户端连接
    print(addr," 客户端连接")
    client.send(public_key.encode())#向客户端发送公钥
    while True:
        data = client.recv(MaxBytes)#服务器接受数据
        enc_key = client.recv(MaxBytes)#接受加密的密钥
        if not data:
            print('数据为空，链接中断')
            break
        localTime = time.asctime( time.localtime(time.time()))
        print(localTime,' 接收到数据字节数:',len(data))
        ###数据解密

        dec_key =sm2_crypt.decrypt(enc_key)#解出密钥
        print("得到密钥："+dec_key.decode())
        iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # bytes类型
        crypt_sm4 = CryptSM4()
        crypt_sm4.set_key(dec_key, SM4_DECRYPT)
        dec_data = crypt_sm4.crypt_ecb(data)  #解出数据
        print("解密数据成功")
        print(dec_data.decode())
        client.send(("服务器收到"+dec_data.decode()).encode())

except BaseException as e:
    print("出现异常：")
    print(repr(e))
finally:
    server.close()                    # 关闭连接
    print("关闭链接")
