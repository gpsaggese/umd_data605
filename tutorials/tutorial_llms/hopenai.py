import sys
sys.path.append('/data')

from openai import OpenAI
from typing import Optional

import helpers.hdbg as hdbg
import os

import logging

_LOG = logging.getLogger(__name__)

#
#import helpers.hlogging as hlogging
#hdbg.set_logger_verbosity(logging.DEBUG)
hdbg.set_logger_verbosity(logging.INFO)

_LOG.debug = _LOG.info


def get_completion(user: str, *, system: str = "",
                   model: Optional[str] = None, **create_kwargs) -> str:
    model = "gpt-4o-mini" if model is None else model
    client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        **create_kwargs
    )
    return completion.choices[0].message.content

# messages = [
#   {"role": "system",
#    "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#   {"role": "user",
#    "content": "Compose a poem that explains the concept of recursion in programming."}
# ]


def get_coding_style_assistant():
    client = OpenAI()
    instructions = "You are an expert Python coder. Use you knowledge base to answer questions about how to write code."
    model = "gpt-4o"
    assistant = client.beta.assistants.create(
        name="Coding style expert",
        instructions=instructions,
        model=model,
        tools=[{"type": "file_search"}],
    )
    # Create a vector store.
    vector_store = client.beta.vector_stores.create(name="Coding style")
    # Ready the files for upload to OpenAI.
    file_paths = ["all.coding_style.how_to_guide.md"]
    file_streams = [open(path, "rb") for path in file_paths]
    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    # You can print the status and the file counts of the batch to see the
    # result of this operation.
    #hdbg.dassert_eq(file_batch.status, "succeeded")
    _LOG.debug("File_batch: %s", file_batch)
    #
    assistant = client.beta.assistants.update(
      assistant_id=assistant.id,
      tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    return assistant


def get_query_assistant(assistant, question):
    client = OpenAI()
    # Create a thread and attach the file to the message.
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": question,
                # Attach the new file to the message.
                # "attachments": [
                #  { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
                # ],
            }
        ]
    )
    # The thread now has a vector store with that file in its tool resources.
    _LOG.debug("thread=%s", thread.tool_resources.file_search)
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )
    messages = list(
        client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    return messages


def response_to_txt(response):
    import openai

    if isinstance(response, openai.types.chat.chat_completion.ChatCompletion):
        return response.choices[0].message.content
    elif isinstance(response, openai.pagination.SyncCursorPage):
        return response.data[0].content[0].text.value
    elif isinstance(response, openai.types.beta.threads.message.Message):
        return response.content[0].text.value
    else:
        raise ValueError(f"Unknown response type: {type(response)}")


# TODO(gp): Clean up this.
from pprint import pformat
from typing import Any

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer


def pprint(obj: Any) -> None:
    """
    Pretty-print in color.
    """
    if hasattr(obj, "to_dict"):
        obj = obj.to_dict()
    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()), end="")