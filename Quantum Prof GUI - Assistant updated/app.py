from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key="ENTER_HERE")

# Function to handle communication with OpenAI
def bot(user_input, messages, assistant_id):
    messages.append({"role": "user", "content": user_input})
    thread = client.beta.threads.create(
        messages=messages
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        model="gpt-4o",
    )
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data
    latest_message_text = messages[0]
    messages.append({"role": "assistant", "content": latest_message_text})
    return latest_message_text.content[0].text.value

# Initial messages (corrected to start as an empty list)
messages = []

assistant_id = "ENTER HERE"
assistant_id_two = "ENTER_HERE"

# Home route to render the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# API route to handle user input and get response from assistant
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    response = bot(user_input, messages, assistant_id)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
