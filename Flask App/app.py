# Import necessary libraries and modules
from flask import Flask, render_template, request, jsonify
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Download NLTK resources (if not already downloaded)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Load the maintenance data from a JSON file
with open('Lumos.json', 'r') as file:
    maintenance_data = json.load(file)

# Create a Flask web application
app = Flask(__name__)

# Define a function to handle user maintenance queries
def answer_maintenance_query(query):
    # Tokenize the user's query
    tokens = word_tokenize(query)
    
    # Perform part-of-speech tagging (POS tagging) to identify named entities
    tagged_tokens = pos_tag(tokens)
    
    # Extract equipment name and test type from the tagged tokens
    equipment_name = None
    test_type = None
    
    for token, pos in tagged_tokens:
        if pos == 'NN' and not equipment_name:
            equipment_name = token
        elif pos == 'NN' and equipment_name:
            test_type = token
            break
    
    # Search for the equipment and test type in the maintenance data
    if equipment_name and test_type:
        equipment_name = equipment_name.lower()
        test_type = test_type.lower()
        
        for equipment in maintenance_data["equipment"]:
            if equipment["name"].lower() == equipment_name:
                for test in equipment["test_procedures"]:
                    if test["test_name"].lower() == test_type:
                        return {
                            "response": f"Procedure for {test['test_name']} on {equipment['name']}:\n{test['procedure']}",
                            "acceptable_limits": test['acceptable_limits']
                        }
    
    # If the query doesn't match any known patterns
    return {"response": "I'm sorry, I couldn't understand your query."}

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for getting responses to user queries
@app.route('/get_response', methods=['POST'])
def get_response():
    user_query = request.form['user_query']
    chatbot_response = answer_maintenance_query(user_query)
    return jsonify(chatbot_response)

# Run the Flask app if this script is the main program
if __name__ == '__main__':
    app.run()
