# *Project5: Impl Merkle Tree following RFC6962
  

## 实验内容  

按照RFC6962导入Merkle Tree

## 实验要求  

* 构造一个有10w个叶子节点的Merkle树
* 构建特定元素的包含证明
* 建立指定元素的排除证明

## Merkle Tree基本概念
&ensp;&ensp;&ensp;&ensp;通常也被称作Hash Tree，顾名思义，就是存储hash值的一棵树。  

&ensp;&ensp;&ensp;&ensp;Merkle树的叶子是数据块(例如，文件或者文件的集合)的hash值。非叶节点是其对应子节点串联字符串的hash。  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/4b794256-7088-4232-95cd-933410840553)

&ensp;&ensp;&ensp;&ensp;通俗来说，我们可以把Merkle Tree可以看做Hash List的泛化（Hash List可以看作一种特殊的Merkle Tree，即树高为2的多叉Merkle Tree）。

&ensp;&ensp;&ensp;&ensp;在最底层，和哈希列表一样，我们把数据分成小的数据块，有相应地哈希和它对应。但是往上走，并不是直接去运算根哈希，而是把相邻的两个哈希合并成一个字符串，然后运算这个字符串的哈希（类似于构建Huffman编码树的结构），这样每两个哈希就结婚生子，得到了一个”子哈希“。如果最底层的哈希总数是单数，那到最后必然出现一个单身哈希，这种情况就直接对它进行哈希运算，所以也能得到它的子哈希。于是往上推，依然是一样的方式，可以得到数目更少的新一级哈希，最终必然形成一棵倒挂的树，到了树根的这个位置，这一代就剩下一个根哈希了，我们把它叫做 Merkle Root。

&ensp;&ensp;&ensp;&ensp;在p2p网络下载网络之前，先从可信的源获得文件的Merkle Tree树根。一旦获得了树根，就可以从其他从不可信的源获取Merkle tree。通过可信的树根来检查其他不可信的Merkle Tree节点。如果当前检测的Merkle Tree结构是损坏的或者虚假的，舍弃当前不可信的获取源，选择其他源获得另一个Merkle Tree，直到获得一个与可信树根匹配的Merkle Tree。
  
&ensp;&ensp;&ensp;&ensp;Merkle Tree和Hash List的主要区别是，可以直接下载并立即验证Merkle Tree的一个分支。因为可以将文件切分成小的数据块，这样如果有一块数据损坏，仅仅重新下载这个数据块就行了。如果文件非常大，那么Merkle tree和Hash list都很到，但是Merkle tree可以一次下载一个分支，然后立即验证这个分支，如果分支验证通过，就可以下载数据了。而Hash list只有下载整个hash list才能验证。  

## Merkle Tree的特点

&ensp;&ensp;&ensp;&ensp;Merkle Tree本质上是一种树，以二叉树为主，也可以多叉树，无论是几叉树，它都具有树结构的所有特点。  

&ensp;&ensp;&ensp;&ensp;Merkle Tree的叶子节点的value是数据集合的单元数据或者单元数据的HASH值；非叶子节点的value是根据它下面所有的叶子节点值，然后按照Hash算法计算而得出的。  

&ensp;&ensp;&ensp;&ensp; tree的树根并不包含树的深度相关信息，这让我们更容易的伪造Merkle tree结构，可能的攻击常为second-preimage attack（第二原象攻击），即攻击者创建一个具有相同Merkle树根的虚假文档。  

&ensp;&ensp;&ensp;&ensp;一个简单的解决方法在Certificate Transparency中定义：当计算叶节点的hash时，在hash数据前加0x00。当计算内部节点是，在前面加0x01。另外一些实现限制hash tree的根，通过在hash值前面加深度前缀。因此，前缀每一步会减少，只有当到达叶子时前缀依然为正，提取的hash链才被定义为有效。使得树结构得到比较完整的保存！  

## Merkle Tree的操作  

### 1、创建Merckle Tree  

&ensp;&ensp;&ensp;&ensp;类似于Huffman树的构建过程这里不做具体叙述（上面已有），创建Merkle Tree是O(n)复杂度(这里指O(n)次hash运算)，n是数据块的大小。得到Merkle Tree的树高是log(n)+1  

### 2、检索数据块  

&ensp;&ensp;&ensp;&ensp;为了更好理解，我们假设有甲乙两台机器，甲需要与乙相同目录下有4个文件，文件分别是ABCD。这个时候我们就可以通过Merkle Tree来进行快速比较。假设我们在文件创建的时候每个机器都构建了一个Merkle Tree。具体如下图:  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/f0060ef5-1bf7-4c40-80bf-33f914e8456f)

&ensp;&ensp;&ensp;&ensp;从上图可得知，叶子节点H_A的value = hash(A),是A文件的HASH;而其父亲节点HASH_AB的value = hash(A,B)，也就是其子节点H_A,H_B共同计算出的HASH。就是这样表示一个层级运算关系。root节点的value其实是所有叶子节点的value的唯一特征。  

&ensp;&ensp;&ensp;&ensp;假如甲上的文件D与乙上的D不一样。我们怎么通过两个机器的merkle treee信息找到不相同的文件? 这个比较检索过程如下:

    Step1. 首先比较v0是否相同,如果不同，检索其孩子HASH_AB和HASH_CD.  

    Step2. HASH_AB相同，HASH_CD不同。检索HASH_CD的孩子H_C,H_D  

    Step3. H_D不同，H_C相同，H_D为叶子节点，获取其目录信息。  

    Step4. 返回其目录信息，检索比较完毕。  

&ensp;&ensp;&ensp;&ensp;以上过程的理论时间复杂度是Log(N)  

### 3、更新，插入和删除  

&ensp;&ensp;&ensp;&ensp;对于Merkle Tree数据节点的更新操作比较容易，更新完数据块，然后接着更新其到树根路径上的Hash值就可以了，这样不会改变Merkle Tree的结构；而对于Merkel Tree的插入和删除操作很有可能会改变Merkle Tree的结构，这可能就会使得Merkel Tree不平衡。  

&ensp;&ensp;&ensp;&ensp;参考【6】的插入算法，满足下面条件：re-hashing操作的次数控制在log(n)以内同时数据块的校验在log(n)+1以内除非原始树的n是偶数，插入数据后的树没有孤儿，并且如果有孤儿，那么孤儿是最后一个数据块而且其顺序保持一致，这样可以保证插入后的Merkle Tree保持平衡。  

&ensp;&ensp;&ensp;&ensp;如果要确保树是平衡的或者是树高是log(n)的，可以用任何的标准的平衡二叉树的模式，如AVL树，红黑树，伸展树，2-3树等。这些平衡二叉树的更新模式可以在O(lgn)时间内完成插入操作，并且能保证树高是O(logn)的。那么很容易可以看出更新所有的Merkle Hash可以在O((logn)^2)时间内完成（对于每个节点如要更新从它到树根O(logn)个节点，而为了满足树高的要求需要更新O(logn)个节点）。如果仔细分析的话，更新所有的hash实际上可以在O(logn)时间内完成，因为要改变的所有节点都是相关联的，即他们要不是都在从某个叶节点到树根的一条路径上，或者这种情况相近。  

&ensp;&ensp;&ensp;&ensp;查阅资料可以总结出实际上Merkle Tree的结构(是否平衡，树高限制多少)在大多数应用中并不重要，而且保持数据块的顺序也在大多数应用中也不需要。因此，可以根据具体应用的情况，设计自己的插入和删除操作。一个通用的Merkle Tree插入删除操作是没有意义的。  

## 实验思路  

&ensp;&ensp;&ensp;&ensp;对于project中要求1：构造具有10w叶节点的Merkle Tree，我们可以用任意的爬虫程序（crawler_ex.py）在网站上爬取100k的数据；调用上面实现完成的Tree_Generate()函数即可。  

&ensp;&ensp;&ensp;&ensp;对于project中要求2，3：可以对指定元素构建包含关系的证明，可以对指定元素构建不包含关系的证明。  

&ensp;&ensp;&ensp;&ensp;首先我们如果要证明一个节点位于树中，只需给出该节点的相邻兄弟节点及其父节点即可。验证思路是验证给定节点是否按照给定形式组成一棵树，根节点是否与待验证树的根节点相同。  

&ensp;&ensp;&ensp;&ensp;对于给定的证明形式，由于也是Merkle树（每层最多有两个节点），所以采用与上面实现思路中（用二维列表存储Merkel Tree）中相同的存储结构；对于待证明的节点，我们只需要确切找出它的hash值是否与树中某节点hash值相同以及该节点在树中的位置，可以求解其在list中对应的下标n；我们需要讨论待求是偶节点还是奇节点。根据其下标，如果是奇数：首先检查是否是最后一个节点。如果是，则不操作，进入下一个循环（即本层没有该节点的兄弟节点，即在Merkle Tree的逻辑表示中，该节点并不位于本层，而是在更高的层）找到该节点之后，将其右节点（下标+1的节点）与该节点一起写入列表。如果是偶数：将其左节点（下标为-1的节点）与该节点一起写入列表。之后我们就可反复地调用上面的程序，最后将根节点放入树中。  

&ensp;&ensp;&ensp;&ensp;对程序进行节点存在性证明时，首先检查待证明节点的哈希值，以及树的根节点是否在给定的证据中；然后检查作为证据给出的树的每一层的子节点之和的哈希值是否是它的父节点（即检查是否满足Merkle Tree的结构）。最后，单独测试根节点的子节点是否能够生成根节点：如果能够通过所有测试，则表明检测节点确实在给定根节点的树中。  


## 测试方法  

将MerkleTree.py和crawler_ex.py文件放到项目中运行即可。

## 实验结果展示
**生成一个有10w个叶子节点的Merkel Tree所需要的时间如下：**  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/0706805e-43ff-483c-bd59-ecd665b84d18)

**证明所需时间如下：**  

![image](https://github.com/xinxingroup32num1/homework-group-32/assets/138662552/bdff0d4d-bd9e-4f90-b08b-ef78fc3d9780)

## 参考文献  

【1】 [https://en.wikipedia.org/wiki/Merkle_tree](https://en.wikipedia.org/wiki/Merkle_tree)

【2】 [http://www.jianshu.com/p/458e5890662f](http://www.jianshu.com/p/458e5890662f)  

【3】 [https://baijiahao.baidu.com/s?id=1716922056987693631&wfr=spider&for=pc](https://baijiahao.baidu.com/s?id=1716922056987693631&wfr=spider&for=pc)  

【4】 [http://blog.csdn.net/yuanrxdu/article/details/22474697?utm_source=tuicool&utm_medium=referral](http://blog.csdn.net/yuanrxdu/article/details/22474697?utm_source=tuicool&utm_medium=referral)  

【5】 [https://blog.csdn.net/wxudong1991/article/details/109311928](https://blog.csdn.net/wxudong1991/article/details/109311928)  

【6】 [https://blog.csdn.net/wxudong1991/article/details/109311928](http://crypto.stackexchange.com/questions/22669/merkle-hash-tree-updates)  
