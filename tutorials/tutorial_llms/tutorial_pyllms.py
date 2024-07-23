# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # pyllms

import llms

# +
model = llms.init('gpt-4')
result = model.complete("what is 5+5")

print(result.text)
# -
print(result.meta)

result = model.complete(
    "what is the capital of country where mozzart was born",
    temperature=0.1,
    #temperature=1.1,
    max_tokens=200
)

print(result.text)
print(result.meta)

# +
#dir(result)
# -

var_names = [
     '_meta',
     'cost',
     'function_call',
     'meta',
     'model_inputs',
     'provider',
     'text',
     #'to_json',
     'tokens',
     'tokens_completion',
     'tokens_prompt']
for var_name in var_names:
    print("# %s\n  %s" % (var_name, getattr(result, var_name)))

# # OpenAI

# !pip install openai


# +
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)
# -

print(completion)

print(dir(completion))

print(completion.choices[0].message.content)

completion.choices[0].message.content

response = client.chat.completions.create(
  #model="gpt-3.5-turbo",
  model="gpt-4o-mini",
  messages=[
    {
      "role": "system",
      "content": "You will be provided with statements, and your task is to convert them to standard English."
    },
    {
      "role": "user",
      "content": "She no went to the market."
    }
  ],
  temperature=0.0,
  max_tokens=64,
  top_p=1
)
print(response.choices[0].message.content)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is a LLM?"}
  ]
)
print(response.choices[0].message.content)

print(response.usage)

# +
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

print(response.choices[0].message.content)
# -

print(type(response))

# ## Assistant

# +
assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4o",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

# +
# Without streaming.

run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages)
else:
  print(run.status)


# -

def response_to_txt(response):
    import openai
    
    if isinstance(response, openai.types.chat.chat_completion.ChatCompletion):
        return response.choices[0].message.content
    elif isinstance(messages, openai.pagination.SyncCursorPage):
        return response.data[0].content[0].text.value


print(response_to_txt(messages))
