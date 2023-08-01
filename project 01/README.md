# *Project1: implement the naïve birthday attack of reduced SM3

## 代码说明：

  **生日攻击**：利用哈希函数发生碰撞的可能性，穷举找到一对输入使其哈希相同。
  
  对长为nbit的串进行攻击，则进行**O(n^1/2)次**搜索即可以较高概率找到碰撞。
  
  我从github上找到了SM3的python实现，加入了生日攻击函数，即可得到结果。


## 测试方法：

将sm3生日攻击.cpp文件放到项目中运行即可

  
## 实验结果展示：


<img width="596" alt="1" src="https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/d67d7156-efc9-4beb-8d3c-728b893bb889">

        
        如上图所示，运行时间约为0.06s.
       
