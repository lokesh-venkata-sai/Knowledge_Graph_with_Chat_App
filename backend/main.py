from flask import Flask, request, jsonify
from flask_cors import CORS
from scrape_data import search_and_extract_text
from build_graph import build_graph
app = Flask(__name__)

CORS(app)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    message = data.get('message')
    response = generate_response_test(message)
    return jsonify({'response': response})


@app.route('/build_kg', methods=['GET'])
def build_kg():
    topic = request.args.get('topic')
    urls = search_and_extract_text(topic, num_results=1) #scraping
    result = build_graph() # Building Knowledge Graph
    if result:
        return "Built Knowledge Graph using these sources"
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
