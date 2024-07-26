import hopenai
import logging
from typing import Any, Dict, List, Tuple, Optional

import helpers.hdbg as hdbg

_LOG = logging.getLogger(__name__)

def get_code_snippet1() -> str:
    """
    Code snippet without docstring.
    """
    code_snippet = """
def _extract(obj: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    hdbg.dassert_isinstance(obj, dict)
    obj_tmp = {}
    for key in keys:
        hdbg.dassert_in(key, obj)
        obj_tmp[key] = getattr(obj, key)
    return obj_tmp
    """
    return code_snippet


def get_code_snippet3() -> str:
    """
    Example of code with comments.
    """
    code_snippet = """
def get_coding_style_assistant(
        assistant_name: str,
        instructions: str,
        vector_store_name: str,
        file_paths: List[str],
        *,
        model: str = "gpt-4o") -> Assistant:
    client = OpenAI()
    assistant = client.beta.assistants.create(
        name=assistant_name,
        instructions=instructions,
        model=model,
        tools=[{"type": "file_search"}],
    )
    _LOG.debug("Creating vector store ...")
    # Create a vector store and upload the files to the vector store.
    vector_store = client.beta.vector_stores.create(name=vector_store_name)
    file_streams = [open(path, "rb") for path in file_paths]
    _LOG.debug("Uploading vector store ...")
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    _LOG.debug("File_batch: %s", file_batch)
    # Update the assistant.
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    return assistant
"""
    return code_snippet


# #############################################################################
# Manipulate code.
# #############################################################################


import ast
import textwrap
import re
import helpers.hio as hio


def remove_code_delimiters(text: str) -> str:
    """
    Remove ```python and ``` delimiters from a given text.

    :param text: The input text containing code delimiters.
    :return: The text with the code delimiters removed.
    """
    # Replace the ```python and ``` delimiters with empty strings
    text = text.replace("```python", "").replace("```", "")
    return text.strip()


def remove_docstring(code: str) -> str:
    # Remove multi-line comments (docstrings)
    code = re.sub(r'"""[\s\S]*?"""', "", code)
    code = re.sub(r"'''[\s\S]*?'''", "", code)
    # Remove empty lines.
    code = "\n".join(line for line in code.splitlines() if line.strip())
    return code


def remove_comments(code: str) -> str:
    # Remove single-line comments.
    code_tmp = []
    for line in code.split("\n"):
        if not re.search(r"^\s*\#.*", line):
            code_tmp.append(line)
    code = "\n".join(code_tmp)
    return code


def split_code_by_function(code: str) -> List[str]:
    # Parse the code into an AST
    tree = ast.parse(code)
    # Initialize a list to store function snippets
    function_snippets = []
    # Iterate through the AST nodes
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            # Get the source code for the function
            function_code = ast.get_source_segment(code, node)
            # Dedent the function code
            function_code = textwrap.dedent(function_code)
            # Add the function code to our list
            function_snippets.append(function_code)
    return function_snippets


def get_functions(tag: str) -> List[str]:
    # Read code.
    if tag == "hdbg":
        txt = hio.from_file("helpers/hdbg.py")
    elif tag == "code_snippets1":
        txt = hio.from_file("code_snippets1.txt")
    elif tag == "code_snippets2":
        txt = hio.from_file("code_snippets2.txt")
    else:
        raise ValueError(f"Invalid tag='{tag}'")
    #
    functions = split_code_by_function(txt)
    return functions


# #############################################################################


from dataclasses import dataclass


@dataclass
class InOut:
    in_: str
    out: str
    act: str

    def __str__(self) -> str:
        text = ""
        text += "\nInput:\n"
        text += f"'\n{self.in_}\n'"
        text += "\nOutput:\n"
        text += f"'\n{self.out}\n'"
        return text


# TODO(gp): -> in_out_to_gpt_text
def get_in_out_example(idx: int, func: str) -> str:
    text = ""
    func_no_comments = remove_comments(func)
    return text


def get_in_out_functions(function_tag: str, transform_tag: str) -> List[InOut]:
    # Get code.
    functions = get_functions(function_tag)
    # Pick transform function.
    if transform_tag == "remove_comments":
        transform = remove_comments
    elif transform_tag == "remove_docstring":
        transform = remove_docstring
    else:
        raise ValueError(f"Invalid transform_tag='{transform_tag}'")
    # Convert in input / output examples.
    in_outs = []
    for func in functions:
        in_ = transform(func)
        out = func
        in_outs.append(InOut(in_, out, ""))
    return in_outs


def _functions_to_file(funcs: List[str], file_name: str) -> None:
    hdbg.dassert_isinstance(funcs, list)
    txt = "\n\n".join(funcs)
    hio.to_file(file_name, txt)


def in_outs_to_files(in_outs: List[InOut]) -> None:
    hdbg.dassert_isinstance(in_outs, list)
    ins = []
    outs = []
    acts = []
    for in_out in in_outs:
        ins.append(in_out.in_)
        outs.append(in_out.out)
        acts.append(in_out.act)
    _LOG.info("Saving results ...")
    _functions_to_file(ins, "in.txt")
    _functions_to_file(outs, "out.txt")
    _functions_to_file(acts, "act.txt")


def in_outs_to_str(in_outs: List[InOut]) -> str:
    hdbg.dassert_isinstance(in_outs, list)
    ins = []
    outs = []
    acts = []
    for in_out in in_outs:
        ins.append(in_out.in_)
        outs.append(in_out.out)
        acts.append(in_out.act)
    ret = ""
    ret += "\n\n### in.txt ###\n"
    ret += "\n\n".join(ins)
    ret += "\n\n### out.txt ###\n"
    ret += "\n\n".join(outs)
    ret += "\n\n### act.txt ###\n"
    ret += "\n\n".join(acts)
    return ret

# #############################################################################
# Prompts.
# #############################################################################


def add_comments_one_shot_learning1(user: str) -> str:
    system = """
You are a proficient Python coder.
Given the Python code passed below, 
every 10 lines of code add comment explaining the code.
Comments should go before the logical chunk of code they describe.
Comments should be in imperative form, a full English phrase, and end with a period.
    """
    # You are a proficient Python coder and write English very well.
    # Given the Python code passed below, improve or add comments to the code.
    # Comments must be for every logical chunk of 4 or 5 lines of Python code.
    # Do not comment every single line of code and especially logging statements.
    # Each comment should be in imperative form, a full English phrase, and end with a period.
    response = hopenai.get_completion(user, system=system)
    ret = hopenai.response_to_txt(response)
    ret = remove_code_delimiters(ret)
    return ret


def add_docstring_one_shot_learning1(user: str) -> str:
    system = """
You are a proficient Python coder.
Add a docstring to the function passed.
The first comment should be in imperative mode and fit in a single line of less than 80 characters.
To describe the parameters use the REST style, which requires each parameter to be prepended with :param
    """
    # If the first comment is not clear enough and needs more details then you can add another comment shorter than one 3 lines.
    # Do not change the code, but print it exactly as it is
    # Do not specify the types of the parameters.
    response = hopenai.get_completion(user, system=system)
    ret = hopenai.response_to_txt(response)
    ret = remove_code_delimiters(ret)
    return ret


def add_type_hints(user: str) -> str:
    system = """
You are a proficient Python coder.
Add type hints to the function passed.
    """
    response = hopenai.get_completion(user, system=system)
    ret = hopenai.response_to_txt(response)
    ret = remove_code_delimiters(ret)
    return ret


def build_few_shot_learning() -> str:
    functions = get_functions1()
    text = """
You are a proficient Python coder.

I will provide you with 5 examples of adding comments to a Python function. For
each example, I will show you the function without comments and then the same
function with comments added.

Then, I want you to perform the same task on a new input.
"""
    examples_idx = [1, 2, 3, 4]
    for idx in examples_idx:
        func = functions[idx]
        text += get_in_out_example(idx, func)
    text += """
Now, perform the task on this new input.
    """
    return text


def apply_prompt(prompt_tag: str, txt: str) -> str:
    if prompt_tag == "comment":
        txt = add_comments_one_shot_learning1(txt)
    elif prompt_tag == "docstring":
        txt = add_docstring_one_shot_learning1(txt)
    elif prompt_tag == "typehints":
        txt = add_type_hints(txt)
    else:
        raise ValueError("Invalid prompt_tag=%s" % prompt_tag)
    return txt


# #############################################################################
# Eval.
# #############################################################################

import tqdm

def eval_prompt(function_tag: str, transform_tag: str, prompt_tag: str, *,
                save_to_file: bool = True,
                ) -> List[
    InOut]:
    in_outs = get_in_out_functions(function_tag, transform_tag)
    _LOG.info("Processing %s examples", len(in_outs))
    in_outs_tmp = []
    for in_out in tqdm.tqdm(in_outs):
        txt = apply_prompt(prompt_tag, in_out.in_)
        hdbg.dassert_ne(txt, "")
        in_out.act = txt
        in_outs_tmp.append(in_out)
    if save_to_file:
        in_outs_to_files(in_outs_tmp)
    return in_outs_tmp


