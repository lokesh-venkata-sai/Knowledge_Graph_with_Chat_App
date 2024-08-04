# Knowledge_Graph_with_Chat_App
Automated Knowledge Graph KGBuilder with Chat Interface

## Steps followed to build Knowledge Graph
- Clean the text corpus (The body of work).
- Extract concepts and entities from the body of work.
- Extract relations between the entities.
- Convert a graph schema.
- Populate nodes (concepts) and edges (relations).
- Visualize and Query.

## Setup Backend

### Mistral 7B
I am using the Mistral 7B Openorca for extracting concepts out of text chunks. It can follow the system prompt instructions very well.

### Ollama
Ollama makes it easy to host any model locally. The Mistral 7B OpenOrca version is already available with Ollama to use out of the box. To set up this project, you must install Ollama on your local machine.

1. **Install Ollama**: Follow the instructions at [Ollama](https://ollama.ai).
2. **Run Ollama server**:
   ```sh
   ollama run zephyr

### Setup Backend

1. Create a virtual environment and activate it:
   ```sh
   - python -m venv venv
   - venv\Scripts\activate

2. 
   ```sh
   pip install -r requirements.txt
3. 
   ```sh
   python main.py

## Setup React App (Frontend User Interface)
1. After creating React Application, Install axios
   ```sh
   cd chatbot-react-app
   npm install axios
2. Create .env file in root directory and add 
   - set NODE_OPTIONS=--openssl-legacy-provider
3. Update the start script in your package.json file to include the legacy OpenSSL provider option
   - "scripts": {
         "start": "react-scripts --openssl-legacy-provider start"
         }
4. Run application
   - npm start

## Techstack:
1. Python
2. React