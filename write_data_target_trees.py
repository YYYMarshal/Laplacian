"""
将 main.py 中两个条件都不满足的所有树，根据txt文件中的信息，生成 nx.Graph 类型的一组图，
并以 graphml 形式保存到文件夹中。
（因为在 main.py 中，只是将两个条件都不满足的树以图片形式保存了，并没有以 graphml 形式保存，
这后续的需求又是在这组树的基础上进行限制，所以需要还原这一组树。）
"""
import ast
from utility import *


def create_graph_from_string(input_string: str) -> nx.Graph:
    # 创建空图
    graph = nx.Graph()
    # 解析字符串，添加边
    edges = ast.literal_eval(input_string)
    for edge in edges:
        graph.add_edge(edge[0], edge[1])
    return graph


def generate_target_trees() -> []:
    target_trees = []
    with open("target_trees.txt", "r", encoding='utf-8') as file:
        for line in file:
            # 找到冒号的位置
            colon_index = line.index("：")
            # 截取冒号后面的字符串并去除空白字符
            edges_str = line[colon_index + 1:].strip()
            # print(edges_str, end="")
            # print(edges_str)
            g = create_graph_from_string(edges_str)
            # show_figure(g, True)
            target_trees.append(g)
    return target_trees


def write_data_target_trees():
    target_trees = generate_target_trees()
    tree_dict = {}
    for tree in target_trees:
        nodes_count = len(tree)
        if nodes_count not in tree_dict:
            tree_dict[nodes_count] = [tree]
        else:
            tree_dict[nodes_count].append(tree)
    for trees in tree_dict.values():
        write_data(trees, FolderName.graphml_target_trees)
        for i, tree in enumerate(trees):
            save_figure(tree, 0, i + 1, FolderName.figures_observation)


def main():
    check_folder(FolderName.graphml_target_trees)
    check_folder(FolderName.figures_observation)

    write_data_target_trees()


main()
