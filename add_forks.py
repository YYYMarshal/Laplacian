from utility import *
from main import generate_satisfy_laplacian_trees, is_satisfy_laplacian


def get_fork(count_one_degree: int, start_node: int) -> nx.Graph:
    fork = nx.Graph()
    fork.add_node(start_node)
    for i in range(start_node + 1, start_node + count_one_degree + 1):
        fork.add_edge(start_node, i)
    return fork


def add_fork(graph: nx.Graph, count_one_degree: int) -> []:
    graphs = []
    count_nodes = len(graph.nodes)
    start_node = count_nodes + 1
    fork = get_fork(count_one_degree, start_node)
    for node in graph.nodes:
        merge_graph = nx.Graph(nx.union(graph, fork))
        merge_graph.add_edge(node, start_node)
        if not is_isomorphic(merge_graph, graphs):
            graphs.append(merge_graph)
    return graphs


def generate_add_fork_graphs(graphs: [], count_one_degree: int) -> []:
    graphs_for_graphs = []
    for tree in graphs:
        graphs_for_graph = add_fork(tree, count_one_degree)
        for item in graphs_for_graph:
            if not is_isomorphic(item, graphs_for_graphs):
                graphs_for_graphs.append(item)
    return graphs_for_graphs


def check_condition(n: int, count_one_degree: int, figures_folder_name: str,
                    graphml_folder_name: str, folder_name_figures_laplacian: str):
    add_couple_trees = read_data(n, graphml_folder_name)
    add_fork_trees = generate_add_fork_graphs(add_couple_trees, count_one_degree)
    for i, tree in enumerate(add_fork_trees):
        info = ""
        if is_satisfy_laplacian(tree):
            info = "laplacian"
            save_figure(tree, n, i + 1, folder_name_figures_laplacian, True, info)
        save_figure(tree, n, i + 1, figures_folder_name, True, info)
    # save_figures(add_fork_trees, figures_folder_name)
    # satisfy_laplacian_trees = generate_satisfy_laplacian_trees(add_fork_trees)
    # save_figures(satisfy_laplacian_trees, folder_name_figures_laplacian)


def main():
    check_folder(FolderName.figures_add_forks_trees)

    # add_couple 操作中选择以一个点还是两个点的图作为初始图（1 或 2）
    initial_graph_index = 1
    # 加的叉子形状的节点中，度为1的节点的数量（2 或 3）
    count_one_degree = 3
    # folder_name_figures, folder_name_graphml = select_fork_type(initial_graph_index, count_one_degree)

    folder_name_figures = os.path.join(
        FolderName.figures_add_forks_trees,
        f"initial_graph_index = {initial_graph_index}, count_one_degree = {count_one_degree}")
    folder_name_graphml = os.path.join(FolderName.graphml_add_couple_trees,
                                       f"initial_graph_index = {initial_graph_index}")
    folder_name_figures_laplacian = os.path.join(folder_name_figures,
                                                 "satisfy_laplacian_trees")
    check_folder(folder_name_figures, True)
    check_folder(folder_name_figures_laplacian, True)

    end_index = 7
    for i in range(1, end_index + 1):
        count_nodes = initial_graph_index + 2 * i
        count_nodes_add_fork = count_nodes + count_one_degree + 1
        print(f"i = {i}, count_nodes = {count_nodes}, count_nodes_add_fork = {count_nodes_add_fork}")
        check_condition(count_nodes, count_one_degree, folder_name_figures,
                        folder_name_graphml, folder_name_figures_laplacian)


main()
