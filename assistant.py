from openai import OpenAI

client = OpenAI(api_key="ENTER_KEY")



#question = "Explain Quantum Computing"
def bot(user_input, messages, assistant_id):
    messages.append({"role": "assistant", "content": user_input})

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

    latest_message = messages[0]
    messages.append({"role": "assistant", "content": latest_message})

    return latest_message.content[0].text.value
    




    # run = client.beta.threads.runs.create(
    # thread_id=thread_id,
    # assistant_id=assistant_id,
    # model="gpt-4o",
    # )
    # while run.status != "completed":
    #     run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

    # message_response = client.beta.threads.messages.list(thread_id=thread_id)
    # messages = message_response.data

    # latest_message = messages[0]
if __name__ == '__main__':
    assistant_id = "ENTER_ID"
    messages = [
        {"role": "assistant", "content": """

        """}
    ]

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Session ended.")
            break

        response = bot(user_input, messages, assistant_id )
        print("Assistant:", response)