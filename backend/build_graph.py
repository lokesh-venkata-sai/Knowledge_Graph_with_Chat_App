import pandas as pd
import numpy as np
import os
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from helpers.df_helpers import documents2Dataframe
from helpers.df_helpers import df2Graph, graph2Df
import networkx as nx
from pyvis.network import Network


inputdirectory = Path(f"./input")
outputdirectory = Path(f"./output")

def load_data():
    loader = DirectoryLoader(inputdirectory, show_progress=True)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
        length_function=len,
        is_separator_regex=False,
    )

    pages = splitter.split_documents(documents)
    df = documents2Dataframe(pages)
    return df

def generate_graph_data(df, regenerate=False):
    if regenerate:
        concepts_list = df2Graph(df, model='zephyr:latest')
        dfg1 = graph2Df(concepts_list)
        if not os.path.exists(outputdirectory):
            os.makedirs(outputdirectory)
        
        dfg1.to_csv(outputdirectory/"graph.csv", sep="|", index=False)
        df.to_csv(outputdirectory/"chunks.csv", sep="|", index=False)
    else:
        dfg1 = pd.read_csv(outputdirectory/"graph.csv", sep="|")
    return dfg1

def contextual_proximity(df: pd.DataFrame) -> pd.DataFrame:
    ## Melt the dataframe into a list of nodes
    dfg_long = pd.melt(
        df, id_vars=["chunk_id"], value_vars=["node_1", "node_2"], value_name="node"
    )
    dfg_long.drop(columns=["variable"], inplace=True)
    # Self join with chunk id as the key will create a link between terms occuring in the same text chunk.
    dfg_wide = pd.merge(dfg_long, dfg_long, on="chunk_id", suffixes=("_1", "_2"))
    # drop self loops
    self_loops_drop = dfg_wide[dfg_wide["node_1"] == dfg_wide["node_2"]].index
    dfg2 = dfg_wide.drop(index=self_loops_drop).reset_index(drop=True)
    ## Group and count edges.
    dfg2 = (
        dfg2.groupby(["node_1", "node_2"])
        .agg({"chunk_id": [",".join, "count"]})
        .reset_index()
    )
    dfg2.columns = ["node_1", "node_2", "chunk_id", "count"]
    dfg2.replace("", np.nan, inplace=True)
    dfg2.dropna(subset=["node_1", "node_2"], inplace=True)
    # Drop edges with 1 count
    dfg2 = dfg2[dfg2["count"] != 1]
    dfg2["edge"] = "contextual proximity"
    return dfg2

def visualize_graph(G):
    graph_output_directory = "./index.html"

    net = Network(
        notebook=False,
        # bgcolor="#1a1a1a",
        cdn_resources="remote",
        height="900px",
        width="100%",
        select_menu=True,
        # font_color="#cccccc",
        filter_menu=False,
    )

    net.from_nx(G)
    # net.repulsion(node_distance=150, spring_length=400)
    net.force_atlas_2based(central_gravity=0.015, gravity=-31)
    # net.barnes_hut(gravity=-18100, central_gravity=5.05, spring_length=380)
    net.show_buttons(filter_=["physics"])

    net.write_html(graph_output_directory, notebook=False)
    print("Visualization stored at: ", graph_output_directory)

def build_graph(df, visualize=True, regenerate=False):
    dfg = generate_graph_data(df, regenerate=regenerate)
    nodes = pd.concat([dfg['node_1'], dfg['node_2']], axis=0).unique()
    G = nx.Graph()

    ## Add nodes to the graph
    for node in nodes:
        G.add_node(
            str(node)
        )

    ## Add edges to the graph
    for index, row in dfg.iterrows():
        G.add_edge(
            str(row["node_1"]),
            str(row["node_2"]),
            title=row["edge"],
    #         weight=row['count']/4
        )

    communities_generator = nx.community.girvan_newman(G)
    top_level_communities = next(communities_generator)
    next_level_communities = next(communities_generator)
    communities = sorted(map(sorted, next_level_communities))

    if visualize:
        visualize_graph(G)
    return G