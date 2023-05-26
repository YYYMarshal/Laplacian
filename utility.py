"""
version:
python: 3.8
networkx: 3.0
matplotlib: 3.7.1
pandas: 1.2.4
scipy: 1.10.1
"""
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import shutil


class FolderName:
    """ main.py """
    figures_main = "figures_main"

    """ write_data_target_trees.py """
    # 观察测试用
    figures_observation = "figures_observation"

    """ remove_nodes.py """
    # 两个条件（Laplacian、n - 2 个节点的树存在）都不满足的树
    figures_target_trees = "figures_target_trees"
    # target_trees 中移除特殊组（一个中心节点附带n个度为1的结点）的树
    figures_remove_special_group_trees = "figures_remove_special_group_trees"
    # remove_special_group_trees 中移除一对（一个度为1，一个度为2）节点的树
    figures_remove_couple_trees = "figures_remove_couple_trees"

    """ add_couple.py """
    # 以一个或两个点为基础图，逐个新增一对节点的树
    figures_add_couple_trees = "figures_add_couple_trees"

    """ add_forks.py """
    figures_add_forks_trees = "figures_add_forks_trees"
    figures_add_forks_two_for_one = "figures_add_forks_two_for_one"
    figures_add_forks_two_for_two = "figures_add_forks_two_for_two"
    figures_add_forks_three_for_one = "figures_add_forks_three_for_one"
    figures_add_forks_three_for_two = "figures_add_forks_three_for_two"

    graphml_trees = "graphml_trees"
    graphml_satisfy_laplacian_trees = "graphml_satisfy_laplacian_trees"

    graphml_target_trees = "graphml_target_trees"
    """ add_couple.py """
    graphml_add_couple_trees = "graphml_add_couple_trees"


def is_isomorphic(graph: nx.Graph, graphs: []) -> bool:
    """
    判断 目标图 graph 是否与 列表 graphs 中的某个元素同构；如果是，返回 True，否则返回 False

    :param graph: 目标图
    :param graphs: 一组图
    :return: True, False
    """
    for item in graphs:
        if nx.is_isomorphic(item, graph):
            return True
    return False


def show_figure(graph: nx.Graph, is_with_labels=False):
    plt.figure()
    nx.draw(graph, with_labels=is_with_labels)
    plt.show()
    plt.close()


def show_adjacent_matrix(graph: nx.Graph, i: int):
    """
    以二维数组形式查看图的邻接矩阵

    :param graph: 目标图
    :param i: 编号
    """
    print(f"图 {i}：", graph.nodes(), graph.edges())
    adj = nx.adjacency_matrix(graph)
    df = pd.DataFrame(adj.todense(), index=graph.nodes(), columns=graph.nodes())
    print("邻接矩阵：\n", df)


def check_folder(folder_name: str, is_delete=False):
    """
    每次运行程序时，先检查是否存在目标文件夹，不存在就新建。
    如果存在则根据传入的 is_delete 的值确定是否删除后再创建。

    :param folder_name: 文件夹名称
    :param is_delete: 如果目标文件夹存在，是否先删除再创建。
    :return:
    """
    if os.path.exists(folder_name):
        if is_delete:
            shutil.rmtree(folder_name)
            os.mkdir(folder_name)
    else:
        os.mkdir(folder_name)


def save_figure(graph: nx.Graph, n: int, i: int, folder_name: str, is_with_labels=False, info=""):
    """
    将图的图片保存到目标文件夹中

    :param graph: 要绘制的目标图
    :param n: 输出信息，若 n = 0，则输出为 len(graph.nodes)，若 n > 0，则输出 n
    :param i: 编号
    :param folder_name: 文件夹名称
    :param is_with_labels: 图片上是否显示节点的编号
    :param info: 额外的信息
    :return:
    """
    plt.figure()
    nx.draw(graph, with_labels=is_with_labels)
    if n == 0:
        n = len(graph.nodes)
    # 图片文件的名称
    figure_name = f"n = {n}, Tree {i}"
    if info != "":
        figure_name += f", {info}"
    plt.savefig(os.path.join(folder_name, figure_name))
    # plt.show()
    plt.close()


def save_figures(graphs: [], folder_name: str, is_with_labels=True, n=0, info=""):
    """
    将一组图的图片保存到目标文件夹中

    :param graphs: 要绘制的目标图列表
    :param folder_name: 文件夹名称
    :param is_with_labels: 图片上是否显示节点的编号
    :param n: 输出信息，若 n = 0，则输出为 len(graph.nodes)，若 n > 0，则输出 n
    :param info: 额外的信息
    :return:
    """
    for i, graph in enumerate(graphs):
        plt.figure()
        nx.draw(graph, with_labels=is_with_labels)
        if n == 0:
            n = len(graph.nodes)
        # 图片文件的名称
        figure_name = f"n = {n}, graph {i + 1}"
        if info != "":
            figure_name += f", {info}"
        plt.savefig(os.path.join(folder_name, figure_name))
        plt.close()


def write_data(graphs: [], folder_name: str):
    """
    将一组图保存到目标文件夹中

    :param graphs:
    :param folder_name:
    :return:
    """
    for i, graph in enumerate(graphs):
        file_name = f"n = {len(graph.nodes)}, i = {i + 1}"
        nx.write_graphml(graph, os.path.join(folder_name, file_name))


def read_data(n: int, folder_name: str) -> []:
    """
    从目标文件夹中读取以 "n = x," 开头的所有文件的内容，并转化为 nx.Graph 类型的一组图

    :param n:
    :param folder_name:
    :return:
    """
    file_name = f"n = {n},*"
    # 获取目标文件夹中，文件名以 file_name 为前缀的所有文件。
    files = glob.glob(os.path.join(folder_name, file_name))
    graphs = []
    for file in files:
        graph = nx.read_graphml(file)
        # 加上这句是因为 nx.read_graphml() 中获取的图的节点是字符串类型的，所以要将其转换为整型。
        graph = nx.convert_node_labels_to_integers(graph, first_label=1)
        graphs.append(graph)
    return graphs
