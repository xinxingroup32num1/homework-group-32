# *Project 19: forge a signature to pretend that you are Satoshi

## 实验目的

伪造签名，假装我是中本聪。

## 算法思路

算法设计依照ppt进行。

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/5124922a-0abc-4902-ad61-e4779b5a5112)


## 代码说明：

&ensp;&ensp;&ensp;&ensp;本次实验引用了ecdsa库，这个库里面有各种椭圆曲线以及对应的方法，可以保证实验结果的权威性;同时，引用了 Crypto.Util.num，主要利用其中的求逆函数。

```python
import ecdsa
import random
from hashlib import sha256
from Crypto.Util.number import *
```

&ensp;&ensp;&ensp;&ensp;首先获得NIST256p椭圆曲线的生成元，并获得该曲线的阶。随机生成一个合法的私钥作为satoshi的私钥（因为无法获知真实的satoshi的公钥)，仅用于生成公钥P。最后生成ecdsa的公钥对象，用于检验最后的签名是否合理。

```python
G=ecdsa.NIST256p.generator#获得NIST256p的生成元
n=G.order()#NIST256p椭圆曲线的阶
privateKey = random.randint(1,n-1)#生成一个随机私钥
print("假设的saotoshi的私钥",privateKey)
P=G*privateKey#此为公钥
publicKey = ecdsa.ecdsa.Public_key(G,G * privateKey)#生成公钥对象
```

&ensp;&ensp;&ensp;&ensp;生成两个随机数u、v并且计算`R=u*G+v *P`,得到ppt中所提到的 r' 。按照公式计算出伪造的签名和对应的消息的hash。

```python
u=random.randint(1,n-1)
v=random.randint(1,n-1)

R=G.mul_add(u,P,v)#此为u*G+v*P
x1=R.x()
r1=x1%n
e1=(r1*u*inverse(v,n))%n
s1=(r1*inverse(v,n))%n
```

&ensp;&ensp;&ensp;&ensp;最后输出两个签名以及消息的hash，生成签名对象，并输出验证结果。

```python
print("伪造签名(r,s):(%d,%d)"%(r1,s1),"对应的消息签名为：",e1)
sig=ecdsa.ecdsa.Signature(r1,s1)

print("验证结果",publicKey.verifies(e1,sig))
```

## 测试方法：

将forge.py文件放到idle中运行即可，需要利用pip安装ecdsa。

## 实验结果展示：

<img width="605" alt="image" src="https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/1f4616f8-5add-45aa-ac7c-94184eb2e6aa">

如上图所示，运行时间约为1.9946ms。
