import hashlib
import random
import string
import copy
import time

# 定义叶节点
class Node:
    def __init__(self):
        # 每个节点的元素包括父节点和左右子节点，及value和对应的hash值
        self.value = None
        self.hash = None
        self.leftNode = None
        self.rightNode = None
        self.parent = None

    # 计算hash值
    def calculator(self, tmp: str):
        return hashlib.sha256(tmp.encode('utf-8')).hexdigest()


listofnodes = []


def order(root: Node):  # 遍历树的到所有的节点
    if root:
        listofnodes.append(root.hash)
        order(root.leftNode)
        order(root.rightNode)


# 定义Merkle_Tree:
class Merkle_Tree:
    def __init__(self, leaf: list[Node]):  # 创建merkle tree时传入一个包含叶节点的列表类型
        # 定义叶节点
        self.leaf = leaf
        self.root = Node()

    def print_root(self):
        print("root: ", self.root)
        print("root value", self.root.value)
        print("root hash", self.root.hash)

    def create_tree(self):
        leaf_nodes = copy.deepcopy(self.leaf)
        while len(leaf_nodes) > 1:
            parent_nodes = []
            for i in range(0, len(leaf_nodes), 2):
                lfnodes = leaf_nodes[i]
                lfnodes.hash = lfnodes.calculator(lfnodes.value)
                if i + 1 < len(leaf_nodes):
                    rtnodes = leaf_nodes[i + 1]
                    rtnodes.hash = rtnodes.calculator(rtnodes.value)
                else:
                    parent_nodes.append(leaf_nodes[i])
                    break
                # 父节点的value值等于左右子节点的hash值
                p = Node()
                lfnodes.parent = p
                rtnodes.parent = p
                p.leftNode = lfnodes
                p.rightNode = rtnodes
                p.value = lfnodes.hash + rtnodes.hash
                p.hash = p.calculator(p.value)
                parent_nodes.append(p)
            leaf_nodes = parent_nodes
        self.root = copy.deepcopy(leaf_nodes[0])

    # check inclusion or exclusion

    def check(self, check_hash: str):
        if check_hash in listofnodes:
            return " is inclusion "
        else:
            return " is exclusion "


if __name__ == "__main__":
    length_of_string = 64
    check_hash = ''.join(
        random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string))

    # 生成100k个叶节点
    ls_nodes = []
    for i in range(100000):
        n = Node()
        n.value = ''.join(random.sample(string.ascii_letters, 8))
        ls_nodes.append(n)

    # 测试构建 Merkle Tree 的时间
    start_time = time.time()
    mymerkletree = Merkle_Tree(ls_nodes)
    mymerkletree.create_tree()
    end_time = time.time()

    print("Merkle Tree 构建时间：", end_time - start_time, "秒")

    mymerkletree.print_root()
    order(mymerkletree.root)

    # 测试检查哈希值的时间
    start_time = time.time()
    print("随机hash为 ", check_hash)
    print("随机hash ", mymerkletree.check(check_hash))
    print("root hash ", mymerkletree.check(mymerkletree.root.hash))
    end_time = time.time()

    print("哈希验证时间：", end_time - start_time, "秒")