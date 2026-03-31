from C_RAG_agent import app

def test_graph_compilation():
    assert app is not None
    print("Graph compiled successfully!")

def test_nodes_exist():
    nodes = app.get_graph().nodes.keys()
    assert "retrieve_node" in nodes
    assert "grade_node" in nodes
    assert "web_search_node" in nodes
    assert "generate_node" in nodes
    print("All nodes verified!")

if __name__ == "__main__":
    test_graph_compilation()
    test_nodes_exist()