import os
import openai
openai.organization = "org-u6md6sQAo6TxNMmQoGeq4WpY"
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)
print(openai.Model.list())