from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import markdown
import time
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key="")

assistant_id_tuned = "" #Quintus
#assistant_id_untuned = "" #Professor Quint

thread = client.beta.threads.create()

#assistant = client.beta.assistants.update(
#  assistant_id=assistant_id_tuned,
#  tools=[{"type": "code_interpreter"}],
#   tool_resources={"file_search": {"vector_store_ids": ["vs_n5Se4w1INuTEDT6pGHTsFzVF"]}},
#)

assistant = client.beta.assistants.retrieve(assistant_id_tuned)
#print(assistant)

# Function to handle communication with OpenAI
def bot(user_input):
    thread_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        model="gpt-4o",
    )

    tries = 0

    while tries < 100:
        tries += 1
        print("trying to retrieve run, attempt", tries) 
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        #print(run_status)
        if run_status.status == "completed":
            break
        time.sleep(1)

    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data
    latest_message_text = messages[0] 
    # messages.append({"role": "user", "content": latest_message_text})


    latest_message_text = messages[0]
    text = latest_message_text.content[0].text.value

    # Use regular expression to find all code blocks enclosed in backticks
    code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)

    # If there are code blocks, format them and replace the original text
    if code_blocks:
        for code in code_blocks:
            # Try to guess the language
            lexer = get_lexer_by_name('python')  # default to Python
            for lang in ['python', 'java', 'javascript', 'c++']:
                if lang in code.lower():
                    lexer = get_lexer_by_name(lang)
                    break

            # Format the code
            formatter = HtmlFormatter()
            formatted_code = highlight(code, lexer, formatter)

            # Replace the original code block with the formatted code
            text = text.replace(f'```{code}```', formatted_code)
    return markdown.markdown(text)

# Initial messages (corrected to start as an empty list)
# messages = []



# Home route to render the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/untuned')
# def untuned():
#     return render_template('untuned.html')

# API route to handle user input and get response from assistant
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    response = bot(user_input)
    return jsonify({'response': response})


# @app.route('/chat_untuned', methods=['POST'])
# def chat_untuned():
#     user_input = request.form['message']
#     response = bot(user_input, assistant_id_untuned)
#     return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
