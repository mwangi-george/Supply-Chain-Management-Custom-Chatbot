import requests
from dotenv import load_dotenv
import os
load_dotenv()
my_chat_key = os.getenv("CHAT_PDF_API_KEY")


def file_poster(file_to_post):
    # API rquirements
    headers = {'x-api-key': my_chat_key}

    # post file to model
    file_post = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file',
        headers=headers,
        files=file_to_post
    )

    if file_post.status_code == 200:
        source_id = file_post.json()['sourceId']
        print('Source ID:', source_id)
        return source_id
    else:
        print('Status:', file_post.status_code)
        print('Error:', file_post.text)


# Chat with AI
def chat_with_ai(prompt, source_id):
    source_id = file_poster(file_to_post=files)
    # API rquirements
    headers = {'x-api-key': my_chat_key}

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

    response = requests.post(
        url, json=data, headers=headers, stream=True)
    output = response.json()["content"]
    return output
