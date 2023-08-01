# *Project2: implement the Rho method of reduced SM3
## 算法说明：

&ensp;&ensp;&ensp;&ensp;考虑数列 $\lbrace H_n\rbrace$，其中 $H_0=seed,\ H_{n+1}=hash(H_n)$，易知该数列最终一定会进入一个循环，且数列进入循环前的最后一个值与该循环周期的最后一个值能够发生碰撞。设此循环的周期为 $\rho$，求出该 $\rho$ 的值，然后，令变量 $i$ 和 $j$ 分别从 $H_0$ 和 $H_\rho$ 出发同步迭代，并逐次比较 $i$ 和 $j$ 的值，当判断出二者第一次相等时，即找到了碰撞发生的位置。其中，求 $\rho$ 值可通过如下算法实现：

&ensp;&ensp;&ensp;&ensp;令变量 $i$ 在数列中迭代：第一轮迭代 $1$ 次得到 $H_1$，将其与 $H_0$ 比较；第二轮迭代 $2$ 次得到 $H_2$ 和 $H_3$，依次与 $H_1$ 比较；第三轮迭代 $4$ 次得到 $H_4$, $H_5$, $H_6$ 和 $H_7$，依次与 $H_3$ 比较……如是重复，每轮迭代 $2^{n-1}$ 次，并依次与上一轮最后一次迭代得到的值比较，直到比较出相同为止，此时 $i$ 在当前轮中迭代的次数即为 $\rho$. 经测试，该算法比原始 Rho Method 通过两变量一快一慢遍历数列求 $\rho$ 值的效率更高，用该算法最终找到一组碰撞的平均总耗时约能达到原方法的 $0.6$ 倍。
        
&ensp;&ensp;&ensp;&ensp;*注：修改 rho_method.cpp 中 `hash_size` 的值可改变 hash 函数的输出字节数，例如，将 `hash_size` 设置为 `8` 即可测试针对 *64* 位简化 SM3 算法（即只保留原始 SM3 算法输出的前 64 位）的 Rho Method 攻击。*       
       

## 代码说明：

&ensp;&ensp;&ensp;&ensp;伪代码如下：
       

```
func get_rho(seed):
    i = seed
    for n = 1, 2, 4, 8, ...:
        t = i
        for rho = 1 .. n:
            i = hash(i)
            if i == t:
                return rho

func rho_method(seed):
    rho = get_rho(seed)
    x = y = seed
    for i = 1 .. rho:
        y = hash(y)
    while 1:
        if hash(x) == hash(y):
            return x, y
        x = hash(x)
        y = hash(y)       
```

Rho Method 攻击的时间复杂度为 $O(2^{\frac{n}{2}})$，空间复杂度为 $O(1)$。
   
## 测试方法：

将sm3.h作为头文件，sm3.cpp文件放到项目中运行即可

## 实验结果展示:

针对 *32* 位简化 SM3 算法的 Rho Method 攻击，经测试在 O3 优化下单次攻击耗时约 136 ms:

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/2b915258-e6b3-4825-aed9-cdbc70a9fabc)


