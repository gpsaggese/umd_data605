from openai import OpenAI
from typing import Optional

import os

def get_completion(user: str, *, system: str = "", model: Optional[str]=None) -> (
        str):
  #api_key = os.environ["OPENAI_API_KEY"]
  model = "gpt-4o-mini" if model is None else model
  client = OpenAI()
  completion = client.chat.completions.create(
    model=model,
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": user},
    ]
  )
  return completion.choices[0].message.content



# messages = [
#   {"role": "system",
#    "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#   {"role": "user",
#    "content": "Compose a poem that explains the concept of recursion in programming."}
# ]
