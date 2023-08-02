# *Project 8: AES impl with ARM instruction  


## 实验内容  

运用ARM指令实现AES


## 代码说明  

* `uint8_t state_t[4][4]`：这定义了一个4x4的8位无符号整数数组‘state_t’，表示AES加密中使用的状态矩阵。  

* `SubBytes(state_t* state)`：这个函数使用S盒（Substitution box）查找表对输入的状态矩阵进行字节替换变换。  

* `ShiftRows(state_t* state)`：这个函数对输入的状态矩阵进行行位移变换，循环地将矩阵的行进行移动。
* `MixColumns(state_t* state)`：这个函数对输入的状态矩阵进行列混淆变换，对矩阵的每一列应用线性变换。
* `uint8_t mul(uint8_t a, uint8_t b)`：这个函数实现了MixColumns变换中使用的有限域乘法运算。
* `AddRoundKey(state_t* state,uint8_t* roundKey)`：这个函数将轮密钥添加到状态矩阵中。
* `KeyExpansion(uint8_t* key, uint8_t* expandedKey)`：这个函数将初始密钥扩展成在AES加密过程中使用的扩展密钥表。在这个简化的例子中，没有实现这个函数。
* `AES_Encrypt(uint8_t* input, uint8_t* output)`：这是主要的AES加密函数。它接收‘input’数组作为输入，使用AES加密后将结果存储在‘output’数组中。
* `main()`：‘main’函数演示了如何使用AES加密，它使用固定密钥对明文"love you"进行加密，并打印输出得到的密文。

## 测试方法  

将AES.cpp放到项目中运行即可。

## 实验结果展示  

由于电脑架构为x86，所以我只完成了代码的实现，并通过了代码bug的检查，并没有得出实际上的运行结果。
