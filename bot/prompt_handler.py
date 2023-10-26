import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.organization = os.environ["ORGANIZATION_ID"]
openai.api_key = os.environ["OPENAI_API_KEY"]

print(openai.organization)
print(openai.api_key)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user", "content": "Hello, I'm a human"
        }
    ]
)


print(response["choices"][0]["message"]["content"])

