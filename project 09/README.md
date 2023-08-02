# *Project9: SM4 software implementation  

  
## 实验内容  

SM4软件实现

## 代码说明  

&ensp;&ensp;&ensp;&ensp;128bit的明文或密文输入经初始变换分成4个字节，与轮密钥经过轮函数的运算经过 32 轮的迭代完成加解密运算。输入为`（x0,x1,x2,x3）`,输出`（y0,y1,y2,y3）`，加密密钥长度为`128bit`，表示为`（mk0,mk1,mk2,mk3）`，其中`mki (i=0,1,2,3)`为字。轮密钥表示为`rki（i=0,1,2.....,31）`为字。`FK=(FK0,FK1,FK2,FK3)`为系统参数，`CK=(CK0,CK1,.....,CK31)`为固定参数。其中T为一个合成置换，由非线性变换和线性变换复合而成。非线性变换由4个平行的S盒构成，S盒的数据均采用16进制。  


## 测试方法  

将sm4.h作为头文件，sm4.cpp放到Visual stutio中运行即可。

## 实验结果展示  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/5a142bf7-2dfb-461c-bf5e-6f4ebb65d3de)

**如上图所示，运行时间约为20微秒。**
