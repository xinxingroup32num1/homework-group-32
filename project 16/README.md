# *Project 16: implement sm2 2P decrypt with real network communication  

## 实验目的  

实现SM2解密算法，并使用socket完成真实网络的模拟。  


## 算法过程  

根据ppt进行设计,并且设计了两个脚本client和server来模拟左右的两个人。  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/02b1ddd1-c4b7-4db3-ab85-e2643346103f)

## 代码说明：  

 `generate_d1()`：用来生成符合sm2曲线要求的私钥。对于server来说有类似的`generate_d2()`。  
   
 `generate_G_1(G)`：G为椭圆曲线上一点`x||y`，这个函数是为了获得G的逆元-G。  

 `generate_P1(d1)`： 用于后续生成公钥P所用。  

 `Encrypt_2p(k,P,m)`：完全按照ppt所演示的sm2两方加密函数。  

 `generate_P(d2,P1)`：两方加密的时候通过交换信息由server来生成公钥P的函数。  
 


## 测试方法  

&ensp;&ensp;&ensp;&ensp;先运行server.py文件，再运行client.py，然后在client里面输入你想要加密的信息，则可以看到产生的公钥和解密结果。  


## 实验结果展示  

**服务端运行结果如下**：  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/e27a0c3a-c909-4e52-804d-8b9530e5f802)

**客户端运行结果如下**：  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/8b3b475f-bfd3-44bf-bc94-5b3c5ee081b4)
