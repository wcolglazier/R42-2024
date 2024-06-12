import openai
import fitz  # PyMuPDF
import os

# Set OpenAI API key directly (for testing purposes only)
api_key = 'key'
if not api_key:
    raise ValueError("API key is not set. Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client
openai.api_key = api_key

def read_pdf(file_path, num_pages=5):
    """Read content from the first few pages of a PDF file and return as a string."""
    try:
        doc = fitz.open(file_path)
        content = ""
        for page_num in range(min(num_pages, len(doc))):
            page = doc.load_page(page_num)
            content += page.get_text()
        return content
    except Exception as e:
        print(f"Error reading PDF file {file_path}: {e}")
        return ""

def bot(user_input, messages):
    messages.append({"role": "user", "content": user_input})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        message = response['choices'][0]['message']['content']
        messages.append({"role": "assistant", "content": message})
        return message, messages
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return "There was an error processing your request.", messages

if __name__ == '__main__':
    # Provide paths to PDF files
    pdf_path_1 = "/Users/williamcolglazier/Desktop/0010117v1.pdf"
    pdf_path_2 = "/Users/williamcolglazier/Desktop/9701001v1.pdf"

    # Read the first few pages of each PDF
    pdf_content_1 = read_pdf(pdf_path_1, num_pages=5)
    pdf_content_2 = read_pdf(pdf_path_2, num_pages=5)

    if not pdf_content_1 or not pdf_content_2:
        print("Error: Could not read one or both PDF files. Please check the file paths and try again.")
    else:
        system_content = pdf_content_1 + "\n\n" + pdf_content_2

        messages = [
            {"role": "system", "content": system_content}
        ]

        while True:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                print("Session ended.")
                break

            response, messages = bot(user_input, messages)
            print("Assistant:", response)
