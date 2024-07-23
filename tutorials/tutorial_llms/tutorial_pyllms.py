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

# +
# #!pip install openai
# -


# %load_ext autoreload
# %autoreload 2

import hopenai

# ## Chat

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

# ## Chat using helpers

hopenai.get_completion("hello")


# ## Assistant

def response_to_txt(response):
    import openai
    
    if isinstance(response, openai.types.chat.chat_completion.ChatCompletion):
        return response.choices[0].message.content
    elif isinstance(messages, openai.pagination.SyncCursorPage):
        return response.data[0].content[0].text.value


# ### Assistant Quickstart

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

print(response_to_txt(messages))

# ### Assistants Deep dive

# +
import csv

# Sample data for the revenue forecast
data = [
    ["Month", "Forecasted Revenue"],
    ["January", 10000],
    ["February", 12000],
    ["March", 15000],
    ["April", 13000],
    ["May", 14000],
    ["June", 16000],
    ["July", 17000],
    ["August", 18000],
    ["September", 15000],
    ["October", 16000],
    ["November", 20000],
    ["December", 22000]
]

# File name
filename = "revenue-forecast.csv"

# Writing to csv file
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Writing the data
    writer.writerows(data)

print(f"File '{filename}' created successfully.")
# -

file = client.files.create(
  file=open("revenue-forecast.csv", "rb"),
  purpose='assistants'
)

assistant = client.beta.assistants.create(
  name="Data visualizer",
  description="You are great at creating beautiful data visualizations. You analyze data present in .csv files, understand trends, and come up with data visualizations relevant to those trends. You also share a brief text summary of the trends observed.",
  model="gpt-4o",
  tools=[{"type": "code_interpreter"}],
  tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
  }
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Create 3 data visualizations based on the trends in this file.",
      "attachments": [
        {
          "file_id": file.id,
          "tools": [{"type": "code_interpreter"}]
        }
      ]
    }
  ]
)

# +
run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
)

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages)
else:
  print(run.status)
# -

#print(messages.data[0].content[1].text.value)
print(messages.data[1].content[0])

messages.to_dict()

# +
#messages = client.beta.threads.messages.list(thread_id)
import io
from IPython.display import display, Image, Markdown

for message in reversed(messages.data):
    for message_content in message.content:
        #print(message_content)
        if hasattr(message_content, "text"):
            print(message_content.text.value)
        if hasattr(message_content, "image_file"):
            file_id = message_content.image_file.file_id
            resp = client.files.with_raw_response.retrieve_content(file_id)
            if resp.status_code == 200:
                image_data = io.BytesIO(resp.content).getvalue()
                #print(image_data.getvalue())
                #assert 0
                #img = Image(image_data)
                display(Image(data=image_data))
                #display(img)

# +
import pprint

pprint.pprint(messages)
# -

file = client.files.create(
  file=open("myimage.png", "rb"),
  purpose="vision"
)
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is the difference between these images?"
        },
        {
          "type": "image_url",
          "image_url": {"url": "https://example.com/image.png"}
        },
        {
          "type": "image_file",
          "image_file": {"file_id": file.id}
        },
      ],
    }
  ]
)

# ### Tools

assistant = client.beta.assistants.create(
  name="Financial Analyst Assistant",
  instructions="You are an expert financial analyst. Use you knowledge base to answer questions about audited financial statements.",
  model="gpt-4o",
  tools=[{"type": "file_search"}],
)

# ### 

# +
# #!curl https://www.sec.gov/Archives/edgar/data/1652044/000165204423000016/goog-20221231.htm

import requests

# URL of the PDF you want to download
pdf_url = 'https://www.sec.gov/Archives/edgar/data/1652044/000165204423000016/goog-20221231.htm'

# Send a GET request to the URL
response = requests.get(pdf_url, headers={"User-Agent": "Mozilla/5.0 (Company info@company.com)"})

# Check if the request was successful
if response.status_code == 200:
    # Write the content of the response to a PDF file
    with open('document.pdf', 'wb') as file:
        file.write(response.content)
    print("Download completed!")
else:
    print(f"Failed to download PDF. Status code: {response.status_code}")
# -

# !ls -l document.pdf

# +
# Create a vector store called "Financial Statements".
vector_store = client.beta.vector_stores.create(name="Financial Statements")
 
# Ready the files for upload to OpenAI
file_paths = ["document.pdf"]
file_streams = [open(path, "rb") for path in file_paths]
 
# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)
 
# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)
# -

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

# +
# Create a thread and attach the file to the message
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "How many shares of Google were outstanding at the end of of October 2023?",
      # Attach the new file to the message.
      #"attachments": [
      #  { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
      #],
    }
  ]
)
 
# The thread now has a vector store with that file in its tool resources.
print(thread.tool_resources.file_search)

# +
# Use the create and poll SDK helper to create a run and poll the status of
# the run until it's in a terminal state.

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

message_content = messages[0].content[0].text
annotations = message_content.annotations
citations = []
for index, annotation in enumerate(annotations):
    message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
    if file_citation := getattr(annotation, "file_citation", None):
        cited_file = client.files.retrieve(file_citation.file_id)
        citations.append(f"[{index}] {cited_file.filename}")

print(message_content.value)
print("\n".join(citations))
# -

# # Query 
#
# > cp /Users/saggese/src/cmamp1/docs/coding/all.coding_style.how_to_guide.md .

# +
assistant = client.beta.assistants.create(
  name="Coding style expert",
  instructions="You are an expert Python coder. Use you knowledge base to answer questions about how to write code.",
  model="gpt-4o",
  tools=[{"type": "file_search"}],
)

# Create a vector store called "Financial Statements".
vector_store = client.beta.vector_stores.create(name="Coding style")
 
# Ready the files for upload to OpenAI
file_paths = ["all.coding_style.how_to_guide.md"]
file_streams = [open(path, "rb") for path in file_paths]
 
# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)
 
# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)
# -

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

# +
# Create a thread and attach the file to the message
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "What is DRY?",
      # Attach the new file to the message.
      #"attachments": [
      #  { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
      #],
    }
  ]
)
 
# The thread now has a vector store with that file in its tool resources.
print(thread.tool_resources.file_search)

# +
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
print(messages)

# message_content = messages[0].content[0].text
# annotations = message_content.annotations
# citations = []
# for index, annotation in enumerate(annotations):
#     message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
#     if file_citation := getattr(annotation, "file_citation", None):
#         cited_file = client.files.retrieve(file_citation.file_id)
#         citations.append(f"[{index}] {cited_file.filename}")

# print(message_content.value)
# print("\n".join(citations))
# -
# ## Query using library.

# ## 



# Force reloading a module.
import hopenai
from importlib import reload
reload(hopenai)

assistant = hopenai.get_coding_style_assistant()

hopenai.pprint(assistant)


question = "What is DRY?"
messages = hopenai.get_query_assistant(assistant, question)

print(messages)

type(messages[0])

hopenai.pprint(messages[0])

print(hopenai.response_to_txt(messages[0]))
