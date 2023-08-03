# *Project 14: Implement a PGP scheme with SM2  


## 实验内容  

使用sm2实现PGP方案

## 算法设计  

&ensp;&ensp;&ensp;&ensp;由于sm2在前面实验中已经实现过，具体的实现没有放在代码中。  

&ensp;&ensp;&ensp;&ensp;引用gmssl库中关于sm2，sm4相关算法，并提前设定好了一些参数。提前规定好sm2非对称加密的公私钥对，并将公钥传递给对方，对方利用公钥加密对称密钥，利用对称密钥加密消息连同加密后的对称密钥一起发送过来，收到后利用私钥解密得到对称密钥，利用对称密钥可以解密出明文消息。其中加密对称密钥时用sm2进行加密，加密数据时利用sm4进行加密。  


## 代码实现  

&ensp;&ensp;&ensp;&ensp;首先建立套接字，使网络中不同主机上的应用进程之间进行双向通信，提供了应用层进程利用网络协议交换数据的机制。利用套接字，服务器一方可以发送公钥并得到加密后的密钥以及密文，客户端可以接收公钥并发送加密后的密钥以及密文。  

&ensp;&ensp;&ensp;&ensp;**加密阶段**：首先要随机选取一个密钥K，用于对称密码的加密。利用SM2的公钥加密K，发送给接收者，然后用密钥K加密明文。  
     
&ensp;&ensp;&ensp;&ensp;**解密阶段**：接收者利用私钥解密出密钥K，从而解密出明文。  


## 测试方法  

先运行server.py文件，再运行client.py即可。

## 实验结果展示  

**服务端运行结果如下**：  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/53ba5e91-160b-4fb6-acdb-a5603d635a7b)

**客户端运行结果如下**：  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/788c5c2a-2efc-4f0c-8c81-5675bff5e107)
