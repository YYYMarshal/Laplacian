from utility import *
from main import generate_satisfy_laplacian_trees


def add_couple(graph: nx.Graph) -> []:
    """
    对于某个图，生成其加一组节点后的所有非同构的图

    :param graph:
    :return:
    """
    graphs = []
    for node in graph.nodes:
        temp_graph = graph.copy()
        node_one = len(graph.nodes) + 1
        node_two = node_one + 1
        temp_graph.add_edge(node, node_one)
        temp_graph.add_edge(node_one, node_two)
        if not is_isomorphic(temp_graph, graphs):
            graphs.append(temp_graph)
    return graphs


def generate_add_couple_graphs(graphs: []) -> []:
    """
    对于n个节点的所有非同构图，生成其加一组节点后的所有非同构的图

    :param graphs:
    :return:
    """
    graphs_for_graphs = []
    for graph in graphs:
        graphs_for_graph = add_couple(graph)
        for item in graphs_for_graph:
            if not is_isomorphic(item, graphs_for_graphs):
                graphs_for_graphs.append(item)
    return graphs_for_graphs


def check_condition(trees: [], folder_name_figures: str,
                    folder_name_graphml: str, folder_name_figures_laplacian: str):
    save_figures(trees, folder_name_figures)
    write_data(trees, folder_name_graphml)
    satisfy_laplacian_trees = generate_satisfy_laplacian_trees(trees)
    save_figures(satisfy_laplacian_trees, folder_name_figures_laplacian)


def get_initial_graph(initial_graph_index: int):
    graph = nx.Graph()
    if initial_graph_index == 1:
        graph.add_node(1)
    elif initial_graph_index == 2:
        graph.add_node(1)
        graph.add_node(2)
        graph.add_edge(1, 2)
    else:
        print("SELECT ERROR!")
    return graph


def main():
    check_folder(FolderName.figures_add_couple_trees)
    check_folder(FolderName.graphml_add_couple_trees)

    # 选择以一个节点还是两个节点的图作为初始图（1 或 2）
    initial_graph_index = 2
    initial_graph = get_initial_graph(initial_graph_index)

    folder_name_figures = os.path.join(FolderName.figures_add_couple_trees,
                                       f"initial_graph_index = {initial_graph_index}")
    folder_name_graphml = os.path.join(FolderName.graphml_add_couple_trees,
                                       f"initial_graph_index = {initial_graph_index}")
    folder_name_figures_laplacian = os.path.join(folder_name_figures,
                                                 "satisfy_laplacian_trees")
    check_folder(folder_name_figures)
    check_folder(folder_name_graphml)
    check_folder(folder_name_figures_laplacian)

    pre_graphs = [initial_graph]

    # 添加的组的数量
    n = 7
    for i in range(1, n + 1):
        graphs = generate_add_couple_graphs(pre_graphs)
        print(f"i = {i}, count_nodes = {len(graphs[0].nodes)}")
        check_condition(graphs, folder_name_figures, folder_name_graphml,
                        folder_name_figures_laplacian)
        pre_graphs = graphs


main()
