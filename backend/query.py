from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from build_graph import build_graph
from helpers.prompts import graphPrompt1

# Load a pre-trained model for question answering
nlp = pipeline("question-answering")

# Function to answer questions
def answer_question(question, context):
    result = nlp(question=question, context=context)
    return result['answer']

def cosine_similarity_strings(str1, str2):
    # Initialize the vectorizer
    vectorizer = TfidfVectorizer()

    # Convert the strings to vectors using TF-IDF
    tfidf_matrix = vectorizer.fit_transform([str1, str2])

    # Calculate the cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    return similarity_matrix[0][0]

# Function to handle user queries and use the extracted information to traverse the KG
def handle_query_with_kg(G, query, query_info):
    
    # Parse the response to extract entities and user intent
    entities = query_info.get("entities", [])
    entities = [entity.lower() for entity in entities]
    
    user_intent = query_info.get("user_intent", "").lower()
    
    # print(entities, user_intent)
    
    # Filter the edges based on user intent
    subgraph_nodes = set()
    subgraph_edges = []
    
    matching_nodes = []
    for ent in entities:
        temp = []
        for node in G.nodes:
            if ent in node:
                temp.append(node)
        matching_nodes += temp
        
    # print(matching_nodes)
    
    for node in matching_nodes:
        subgraph_nodes.add(node)
        for neighbor in G.neighbors(node):
            edge_data = G.get_edge_data(node, neighbor)
            if edge_data and cosine_similarity_strings(user_intent.lower(), edge_data['title'].lower())>0:
                subgraph_nodes.add(neighbor)
                subgraph_edges.append((node, neighbor, edge_data))
    
#     print(subgraph_edges)
    # Build context from the filtered edges
    context = []
    for u, v, d in subgraph_edges:
        context.append(f"{u} {d['title'].replace('_', ' ').lower()} {v}.")
    context = " ".join(context)
    
    # Generate an answer based on the user query and the built context
    answer = None
    if context:
        answer = answer_question(query, context)
    return answer

def get_answer(query):
    query_info = graphPrompt1(query, {}, model='zephyr:latest')
    print(query_info)
    G = build_graph(None, False)
    answer = handle_query_with_kg(G, query, query_info)
    return answer