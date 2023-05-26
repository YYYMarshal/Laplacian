from time import time
import math
from utility import *


def generate_trees(pre_trees: [nx.classes.graph.Graph]) -> [nx.Graph]:
    """
    基于前面的一组具有 n 个节点且无同构的图，生成一组具有 n + 1 个节点且无同构的图

    :param pre_trees:
    :return:
    """
    trees = []
    for pre_tree in pre_trees:
        new_node = len(pre_tree.nodes) + 1
        for i in range(1, new_node):
            tree = pre_tree.copy()
            tree.add_edge(i, new_node)
            # 检查 当前图 是否连通且无环，若符合，则为树
            if nx.is_connected(tree) and (len(nx.cycle_basis(tree)) == 0):
                if not is_isomorphic(tree, trees):
                    trees.append(tree)
    return trees


def is_satisfy_laplacian(tree: nx.Graph) -> bool:
    n = len(tree.nodes)
    # 获取拉普拉斯矩阵的特征值
    eigenvalues = nx.laplacian_spectrum(tree)

    # 判断是否满足条件
    count = 0
    for eig in eigenvalues:
        if eig < (2 - 2 / n):
            count += 1
    if count == math.ceil(n / 2):
        return True
    return False


def generate_satisfy_laplacian_trees(trees: [nx.Graph]) -> []:
    """
    根据传入的一组树，找到其中满足 Laplacian 条件的所有树。

    :param trees:
    :return:
    """
    satisfy_laplacian_trees = []
    for i, tree in enumerate(trees):
        if is_satisfy_laplacian(tree):
            satisfy_laplacian_trees.append(tree)
    return satisfy_laplacian_trees


def generate_satisfy_before_trees(satisfy_laplacian_trees: [], n: int) -> []:
    if n <= 2:
        result_trees = read_data(n, FolderName.graphml_satisfy_laplacian_trees)
        return result_trees, result_trees
    pre_satisfy_laplacian_trees = read_data(n - 2, FolderName.graphml_satisfy_laplacian_trees)
    print(f"len(pre_satisfy_laplacian_trees) = {len(pre_satisfy_laplacian_trees)}")
    satisfy_before_trees = []
    not_satisfy_before_trees = []
    for tree in satisfy_laplacian_trees:
        tree = nx.classes.graph.Graph(tree)
        is_satisfy_before = False
        for node in tree.nodes:
            temp_tree = tree.copy()
            if temp_tree.degree(node) == 1:
                list_neighbors = list(temp_tree.neighbors(node))
                neighbor_node = list_neighbors[0]
                if temp_tree.degree(neighbor_node) == 2:
                    temp_tree.remove_edge(node, neighbor_node)
                    temp_tree.remove_node(node)
                    temp_tree.remove_node(neighbor_node)
                    for before_tree in pre_satisfy_laplacian_trees:
                        if nx.is_isomorphic(temp_tree, before_tree):
                            satisfy_before_trees.append(tree)
                            # 一棵树中，只要有一组 悬挂路 移除之后使得该树满足 “before” 条件，则跳出循环
                            is_satisfy_before = True
            if is_satisfy_before:
                break
        if not is_satisfy_before:
            not_satisfy_before_trees.append(tree)
    return satisfy_before_trees, not_satisfy_before_trees


def check_conditions(trees: [], n: int):
    satisfy_laplacian_trees = generate_satisfy_laplacian_trees(trees)
    write_data(satisfy_laplacian_trees, FolderName.graphml_satisfy_laplacian_trees)
    satisfy_before_trees, not_satisfy_before_trees = generate_satisfy_before_trees(satisfy_laplacian_trees, n)

    print(f"所有具有 {n} 个节点的非同构的树中：\n"
          f"    满足 Laplacian 条件的有 {len(satisfy_laplacian_trees)} 棵，\n"
          f"    满足两个条件（Laplacian、n - 2 个节点的树存在）的有 {len(satisfy_before_trees)} 棵，\n"
          f"    两个条件都不满足（将要保存为本地图片）的有 {len(not_satisfy_before_trees)} 棵。")
    for i, tree in enumerate(not_satisfy_before_trees):
        tree = nx.classes.graph.Graph(tree)
        index = i + 1
        show_adjacent_matrix(tree, index)
        save_figure(tree, 0, index, FolderName.figures_main, True)


def traversal(n: int):
    """
    遍历检查 n 个结点的所有树中，哪些满足条件，将满足条件的树的图片存储到本地。

    :param n: 结点的数量
    """
    timer = time()
    pre_trees = read_data(n - 1, FolderName.graphml_trees)
    trees = []
    # len(pre_trees) > 0，就表示本地文件中存储了 n - 1 个节点时所有的非同构树
    if len(pre_trees) > 0:
        trees = generate_trees(pre_trees)
        write_data(trees, FolderName.graphml_trees)
    if n == 1:
        tree = nx.Graph()
        tree.add_node(1)
        trees.append(tree)
        write_data(trees, FolderName.graphml_trees)
    print(f"Time - generate_trees({n}): {time() - timer}")

    timer = time()
    check_conditions(trees, n)
    print(f"Time - check_conditions: {time() - timer}")
    print("--------------------------------------------------------")


def main():
    check_folder(FolderName.figures_main)
    check_folder(FolderName.graphml_trees)
    check_folder(FolderName.graphml_satisfy_laplacian_trees)

    # 分别将具有 1 ~ n 个节点的所有树都检查一遍是否满足目标条件
    n = 100
    start_index = 1
    for i in range(start_index, n + 1):
        traversal(i)
    # traversal(12)


if __name__ == '__main__':
    main()
