def show_graph(graph_map):
    import pydot
    from IPython.display import Image, display

    from ..pointer.graph.state_enum import PointerState

    # Create the directed graph object
    graph = pydot.Dot(graph_type="digraph")  # Notice the change here

    for key, value in graph_map.items():
        style = (
            "filled"
            if not value.predecessor or value.state == PointerState.RUNNING
            else ""
        )
        fillcolor = "green" if value.state == PointerState.FINISHED else ""
        fillcolor = "red" if value.count == 0 else fillcolor
        node = pydot.Node(
            key,
            style=style,
            fillcolor=fillcolor,
            label=key[:4],
            xlabel=value.count,
        )
        graph.add_node(node)
        for parent in value.parents:
            if len(graph.get_node(parent)) > 0:
                parent_node = graph.get_node(parent)
                graph.add_edge(
                    pydot.Edge(parent_node, node, label=value.path),
                )
            else:
                style = (
                    "filled"
                    if not graph_map[parent].predecessor
                    or graph_map[parent].state == PointerState.RUNNING
                    or graph_map[parent].state == PointerState.FINISHED
                    else ""
                )
                fillcolor = (
                    "green"
                    if graph_map[parent].state == PointerState.FINISHED
                    else ""
                )
                fillcolor = (
                    "red" if graph_map[parent].count == 0 else fillcolor
                )
                parent_node = pydot.Node(
                    parent,
                    style=style,
                    fillcolor=fillcolor,
                    label=parent[:4],
                    xlabel=graph_map[parent].count,
                )
                graph.add_node(parent_node)
                graph.add_edge(
                    pydot.Edge(parent_node, node, label=value.path),
                )

    # Convert to PNG and display within Jupyter Notebook
    plt_image = Image(graph.create_png())
    display(plt_image)
    return graph
