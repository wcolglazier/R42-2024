from flask import Flask, request, render_template, redirect, url_for
from chatbot import bot  # Import the bot function from chatbot.py

app = Flask(__name__)

# Initialize the messages list globally
messages = [
    {"role": "system", "content": """Your system message here"""}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    global messages
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input:
            response, messages = bot(user_input, messages)
            return redirect(url_for('index'))

    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)