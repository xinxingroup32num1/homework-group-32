# *Project 11: impl sm2 with RFC6979  


## 实验目的  

使用RFC6979实现sm2

## 代码分析  

**1. 椭圆曲线定义**：椭圆曲线使用的参数包括有限域的阶P、椭圆曲线的阶N、曲线参数A、B，以及基点G的横纵坐标(G_X, G_Y)。这里采用的椭圆曲线是 NIST P-256 曲线，也称为 secp256r1。  

**2. 密钥生成**：使用generate_key()函数生成公钥和私钥对。generate_key()函数使用随机生成的私钥，并通过椭圆曲线上的点乘法生成相应的公钥。  

**3. 椭圆曲线点加法和倍乘**：elliptic_add(p, q)函数实现了椭圆曲线上不同点的加法。elliptic_double(p)函数实现了椭圆曲线上同一点的倍乘（即*2运算）。  

**4. 预计算函数**：precomputation(ID, A, B, G_X, G_Y, pub_x, pub_y)函数用于对一系列参数进行级联并计算SM3哈希值，得到预计算的结果Z_A。预计算过程包括将各个参数转换为字节对象并级联，然后对级联后的数据进行SM3哈希运算。  

**5. 签名生成**：sign(private_key, mes, Z_A)函数实现了对消息进行签名。签名过程包括计算消息的哈希值e，使用RFC6979生成保密的唯一的随机数k，计算椭圆曲线点(x_1, y_1)=[k]G，然后计算签名r和s。最终签名为(r, s)。  

**6. 验证签名**：verify(public_key, ID, mes, sig)函数实现了对签名的验证。验证过程中，先预计算Z_A，然后再次计算e。接着，使用公钥和签名中的(r, s)计算椭圆曲线点(x1, y1)=[s]G和点(x2, y2)=[t]public_key，其中t=(r+s)%N。然后对点(x1, y1)和点(x2, y2)进行加法运算得到点(point_x, point_y)。最后，计算R=(e+point_x)%N，并与签名中的r进行比较，如果R和r相等，即为签名验证通过。

## 测试方法  

将sm2_RFC6979.py文件放到项目中运行即可。

## 实验结果展示  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/40bf025f-066c-4acd-bf83-1cf1dede791d)

如上图所示，运行时间约为11 ms。 
