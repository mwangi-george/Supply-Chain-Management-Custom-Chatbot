# dependencies
import requests
from dotenv import load_dotenv
import os
load_dotenv()
my_chat_key = os.getenv("CHAT_PDF_API_KEY")

# file to analyze with AI
files = [
    ('file', ('file', open('www/pdfs/test_pdf.pdf', 'rb'), 'application/octet-stream'))
]


# API rquirements
headers = {'x-api-key': my_chat_key}

# post file to model
file_post = requests.post(
    'https://api.chatpdf.com/v1/sources/add-file',
    headers=headers,
    files=files
)


if file_post.status_code == 200:
    source_id = file_post.json()['sourceId']
    print('Source ID:', source_id)
else:
    print('Status:', file_post.status_code)
    print('Error:', file_post.text)


# Chat with AI
def chat_with_ai(prompt):
    data = {
        "sourceId": source_id,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            },
        ],
    }

    url = "https://api.chatpdf.com/v1/chats/message"

    response = requests.post(url, json=data, headers=headers, stream=True)
    output = response.json()["content"]
    print(output, "\n")
    return output


if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "bye", "exit"]:
            break
        response = chat_with_ai(user_input)
        print("")
        print("Chatbot: ", response)
