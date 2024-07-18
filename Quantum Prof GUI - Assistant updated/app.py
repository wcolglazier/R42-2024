from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import markdown
import time

app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key="")

thread = client.beta.threads.create()

# Function to handle communication with OpenAI
def bot(user_input, assistant_id):
    thread_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        model="gpt-4o",
    )

    tries = 0

    while tries < 100:
        tries += 1
        print("trying to retrieve run, attempt", tries)
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(run_status)
        if run_status.status == "completed":
            break
        time.sleep(1)

    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data
    latest_message_text = messages[0]
    # messages.append({"role": "user", "content": latest_message_text})
    return markdown.markdown(latest_message_text.content[0].text.value)

# Initial messages (corrected to start as an empty list)
# messages = []

assistant_id_tuned = "" #Quintus
assistant_id_untuned = "" #Professor Quint

# Home route to render the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# API route to handle user input and get response from assistant
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    response = bot(user_input, assistant_id_tuned)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
