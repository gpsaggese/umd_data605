import hopenai

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


def add_comments_one_shot_learning1(user):
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
    print(hopenai.response_to_txt(response))


def add_docstring_one_shot_learning1(user):
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
    print(hopenai.response_to_txt(response))


import ast
import textwrap


def split_code_by_function(code):
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


import re


def remove_docstring(code):
    # Remove multi-line comments (docstrings)
    code = re.sub(r'"""[\s\S]*?"""', '', code)
    code = re.sub(r"'''[\s\S]*?'''", '', code)
    # Remove empty lines.
    code = '\n'.join(line for line in code.splitlines() if line.strip())
    return code


def remove_comments(code):
    # Remove single-line comments.
    code = re.sub(r'^\s*#.*', '', code)
    # Remove empty lines.
    code = '\n'.join(line for line in code.splitlines() if line.strip())
    return code


import helpers.hio as hio

def get_functions():
    txt = hio.from_file("helpers/hdbg.py")
    functions = split_code_by_function(txt)
    return functions


def get_in_out_functions():
    in_out = []
    functions = get_functions()
    for func in functions:
        in_out.append((remove_comments(func), func))
    return in_out


def print_in_out(in_out):
    text = ""
    text += "\nInput:\n"
    text += f"'''\n{in_out[0]}\n'''"
    text += "\nOutput:\n"
    text += f"'''\n{in_out[1]}\n'''"
    return text


def get_in_out_example(idx, func):
    text = ""
    func_no_comments = remove_comments(func)
    text += f"\n\nExample {idx}\n"
    text += "\nInput:\n"
    text += f"'''\n{func_no_comments}\n'''"
    text += "\nOutput:\n"
    text += f"'''\n{func}\n'''"
    return text


def build_few_shot_learning():
    functions = get_functions()

    # #print(functions[2])
    # func_no_comments = snippets.remove_comments(functions[2])
    # print(func_no_comments)

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

#print("\n".join(examples))[:100]

# # Example usage
# code = '''
# def function1():
#     print("This is function 1")
#
# def function2(arg):
#     return arg * 2
#
# def function3():
#     """This is a docstring"""
#     a = 1
#     b = 2
#     return a + b
# '''
#
# snippets = split_code_by_function(code)
#
# for i, snippet in enumerate(snippets, 1):
#     print(f"Function {i}:")
#     print(snippet)
#     print("-" * 40)