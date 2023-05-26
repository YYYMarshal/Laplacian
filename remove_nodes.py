from utility import *


def remove_special_group(tree: nx.Graph) -> nx.Graph:
    """
    移除一组符合特定规则的节点（叉状）。
    特定规则为：有 n(n ≥ 2) 个度为 1 的节点，这 n 个节点共同连接到一个中心结点上，而这个中心节点的所有邻居节点中，
    除了这 n 个度为 1 的节点之外，有且仅有一个度不为 1 的节点。

    :param tree:
    :return:
    """
    for node in tree.nodes:
        temp_tree = tree.copy()
        # 从某个度为 1 的节点开始
        if temp_tree.degree(node) == 1:
            neighbor_node = list(temp_tree.neighbors(node))[0]
            # 找到一个连着一组度为 1 的中心节点
            if temp_tree.degree(neighbor_node) >= 3:
                # 获取中心节点的所有邻居节点
                neighbors = list(temp_tree.neighbors(neighbor_node))
                # 将要移除的所有节点
                remove_nodes = []
                # 中心节点的邻居节点中度为 1 的节点的数量
                count = 0
                for neighbor in neighbors:
                    # 寻找中心节点的邻居节点中度为 1 的节点，这种节点就是将要移除的节点
                    if temp_tree.degree(neighbor) == 1:
                        count += 1
                        remove_nodes.append(neighbor)
                # 如果 中心节点的邻居节点中度为 1 的节点的数量 不符合 中心节点的邻居节点的数量 - 1，则退出本次循环
                if count != len(neighbors) - 1:
                    continue
                # 移除所有与中心节点相连且度为 1 的节点
                for remove_node in remove_nodes:
                    temp_tree.remove_node(remove_node)
                # 移除中心节点
                temp_tree.remove_node(neighbor_node)
                # 递归，继续寻找且移除符合条件的中心节点及其度为 1 的邻居节点
                return remove_special_group(temp_tree)
    return tree


def remove_couple(tree: nx.Graph) -> nx.Graph:
    for node in tree.nodes:
        temp_tree = tree.copy()
        if temp_tree.degree(node) == 1:
            neighbor_node = list(temp_tree.neighbors(node))[0]
            if temp_tree.degree(neighbor_node) == 2:
                temp_tree.remove_node(node)
                temp_tree.remove_node(neighbor_node)
                return remove_couple(temp_tree)
    return tree


def check_condition(n: int):
    target_trees = read_data(n, FolderName.graphml_target_trees)
    print(f"n = {n}, count = {len(target_trees)}")
    for i, tree in enumerate(target_trees):
        index = i + 1
        # show_figure(tree, True)
        save_figure(tree, 0, index, FolderName.figures_target_trees, True)
        g = remove_special_group(tree)
        # show_figure(g, True)
        save_figure(g, n, index, FolderName.figures_remove_special_group_trees, True)
        g = remove_couple(g)
        save_figure(g, n, index, FolderName.figures_remove_couple_trees, True)


def main():
    check_folder(FolderName.figures_target_trees, True)
    check_folder(FolderName.figures_remove_special_group_trees, True)
    check_folder(FolderName.figures_remove_couple_trees, True)

    for i in range(9, 17 + 1):
        check_condition(i)


main()
