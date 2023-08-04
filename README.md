# 创新创业实践课程作业  

## 个人信息  

**组号**：Group 32  

**姓名**：蔡彦心  

**学号**：202100460112  

**项目贡献说明：个人独立完成**

## 实现项目清单（共16个）  

***Project1:** implement the naïve birthday attack of reduced SM3  
***Project2:** implement the Rho method of reduced SM3  
***Project3:** implement length extension attack for SM3, SHA256, etc.  
***Project4:** do your best to optimize SM3 implementation (software)  
***Project5:** Impl Merkle Tree following RFC6962  
***Project8:** AES impl with ARM instruction  
***Project9:** AES / SM4 software implementation   
***Project10:** report on the application of this deduce technique in Ethereum with ECDSA  
***Project11:** impl sm2 with RFC6979  
***Project12:** verify the above pitfalls with proof-of-concept code  
***Project14:** Implement a PGP scheme with SM2  
***Project15:** implement sm2 2P sign with real network communication  
***Project16:** implement sm2 2P decrypt with real network communication  
***Project17:** 比较Firefox和谷歌的记住密码插件的实现区别  
***Project19:** forge a signature to pretend that you are Satoshi  
***Project22:** research report on MPT  


## 未完成项目  

***Project6:** impl this protocol with actual network communication  
***Project7:** Try to Implement this scheme  
***Project13:** Implement the above ECMH scheme  
***Project18:** send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself  
***Project21:** Schnorr Bacth  

## 实验环境说明  

**硬件环境**  

处理器：12th Gen Intel(R) Core(TM) i7 12700H @ 2.40GHz  
内存：16.0 GB (15.8 GB 可用 )  

**软件环境**  

Win 11操作系统  
Microsoft Visual Studio 2022  
Pycharm  

## 项目实现说明  

### Project 1：SM3生日攻击 ###  
**实现方式：**
利用哈希函数发生碰撞的可能性，穷举找到一对输入使其哈希相同。  
**实现效果：**
运行时间约为0.06s。     

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/d8edcb23-9d83-4495-a5e4-cad1aee3c52d)

### Project 2：Rho 攻击 ###
**实现方式：**
求出循环周期，使两个变量同步迭代，逐次比较，找到二者第一次相等的位置，即碰撞发生的位置。  
**实现效果：**
针对32位简化 SM3 算法的 Rho Method 攻击，经测试在O3优化下单次攻击耗时约 136 ms。
  
![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/40ba86d9-56a2-4575-89d1-0795cd4eb827)

### Project 3：SM3长度扩展攻击 ###
**实现方式：**
详见project 03文件夹中README.md文件。  
**实现效果：**
运行时间约为0.999ms。
  
![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/dd1c3f5a-93c6-4fe0-92c5-da7b427fd788)

### Project 4：优化SM3软件实现 ### 
**实现方式：**
循环展开、内存对齐、使用标准整数算法。  
**实现效果：**
对比可发现，优化后速度得到一定的提升。  
**优化前：**  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/298c2799-a4ab-4a42-8640-2b283c8b2cb9)

**优化后：**  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/b41751ba-5fc6-4bf6-b40d-45119a55493d)

### Project 5：按照RFC6962实现Merkle Tree ###
**实现方式：**
详见project 05文件夹中README.md文件。  
**实现效果：**  
生成一个有10w个叶子节点的Merkel Tree所需要的时间如下：

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/351f2dae-2a07-49c3-b292-eb8024ba3a78)

证明所需时间如下：  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/13cace1d-c300-4c40-9313-6b8cab6ef843)

### Project 8：运用ARM指令实现AES ###
**实现方式：**
详见project 08文件夹中README.md文件。  
**实现效果：**
由于电脑架构为x86，所以我只完成了代码的实现，并通过了代码bug的检查。  

### Project 9：SM4软件实现 ###
**实现方式：**
用c++编写代码。  
**实现效果：**
运行时间约为20微秒。  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/38be0234-6951-4fbd-875c-918d77ea4039)

### Project 10：通过sm2签名推导公钥的技术在以太坊ECDSA中的应用研究报告 ###
**实现方式：**
从隐私保护、轻量级验证、身份验证、可信证书验证四方面展开论述。  


### Project 11：使用RFC6979实现sm2 ###
**实现方式：**
详见project 11文件夹中README.md文件。  
**实现效果：**
运行时间约为11 ms。 
 
![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/0c4cb0be-7c96-48cd-97db-403a33f585cb)

### Project 12：实现在SM2签名下由已知的泄露的k退出私钥d ###
**实现方式：**
详见project 12文件夹中README.md文件。  
**实现效果：**
运行时间约为4.9989 ms。  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/85d5b942-1dfb-4d56-aac0-c5717d15fa17)

### Project 14：使用sm2实现PGP方案 ###
**实现方式：**
详见project 14文件夹中README.md文件。  
**实现效果：**  
服务端运行结果如下：  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/74f5057d-4f8d-4564-a9d0-3deb5a434fb4)

客户端运行结果如下：  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/a9b4dfe8-e283-4a2c-9ba4-db5a613c032e)

### Project 15：实现SM2签名算法，并使用socket完成真实网络的模拟 ###
**实现方式：**
依照PPT算法思路。  
**实现效果：**  
服务端运行结果如下：  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/ded17f3a-42f4-470a-9049-62df8e60c0e6)

客户端运行结果如下：  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/ed6c650f-1a0a-49d4-816c-e103d8a7a496)

### Project 16：实现SM2解密算法，并使用socket完成真实网络的模拟 ###
**实现方式：**
根据ppt进行设计,并且设计了两个脚本client和server来模拟左右的两个人。  
**实现效果：**  
服务端运行结果如下：  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/36829449-6c7d-4da6-b834-5f9053d98dc1)

客户端运行结果如下：  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/8084a681-c427-4ebe-8289-d89e4da99713)

### Project 17：比较Firefox和谷歌的记住密码插件的实现区别 ###
**实现方式：**
分别从存储方式、跨设备同步、安全性、自动填充表单、第三方密码管理器集成、用户界面和设置选项六方面展开论述。  

### Project 19：假装是中本聪伪造签名 ###
**实现方式：**
根据ppt进行设计。  
**实现效果：**
运行时间约为1.9946ms。  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/081bc50d-a125-4787-8d72-f1329de0745e)

### Project 22：MPT研究报告 ###
**实现方式：**
本研究报告对MPT进行了深入的研究和探讨。首先，我们介绍了MPT的背景和概念，包括其发展历史和用途。然后，我们详细讨论了MPT的结构和操作原理，并与传统的Merkle树进行了对比。接着，我们探讨了MPT在区块链技术中的应用，以及其在提高数据验证效率和降低存储空间成本方面的优势。最后，我们总结了MPT的优缺点，并展望了未来对MPT改进的研究方向。  

**注：**  
* 详细项目信息请移步对应文件夹，实现方法描述详见各文件夹中README.md文件。  
* 由于项目完成进度和上传仓库进度并不同步，导致仓库显示的上传时间较晚，更新时间较新，请老师谅解。   

