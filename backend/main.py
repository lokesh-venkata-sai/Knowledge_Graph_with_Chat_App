from flask import Flask, request, jsonify
from flask_cors import CORS
from scrape_data import search_and_extract_text
from build_graph import build_graph, load_data
from query import get_answer
app = Flask(__name__)

CORS(app)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    message = data.get('message')
    response = get_answer(message)
    print(response)
    return jsonify({'response': response})


@app.route('/build_kg', methods=['GET'])
def build_kg():
    topic = request.args.get('topic')
    urls = search_and_extract_text(topic, num_results=1) #scraping
    df = load_data()
    result = build_graph(df) # Building Knowledge Graph
    if result:
        return "Built Knowledge Graph"
    else:
        return "Couldn't Build knowledge Graph"

@app.route('/test', methods=['GET'])
def test():
    return "Hello world! App is working"

def generate_response_test(message):
    # Simple response logic for demonstration
    if message.lower() in ['hi', 'hello']:
        return "Hi there! How can I help you?"
    else:
        return "I am not sure how to respond to that."

if __name__ == '__main__':
    app.run(debug=True)
