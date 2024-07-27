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

# # Import

# +
# #!pip install openai
# -


# %load_ext autoreload
# %autoreload 2

# +
import pprint
import logging

import hopenai
import helpers.hdbg as hdbg

hdbg.init_logger()

hdbg.set_logger_verbosity(logging.INFO)
# -

import os; os.environ["OPENAI_API_KEY"] = ""

# # Prompt engineering

# +
system = """
"""
user = """
"""
response = hopenai.get_completion(user, system=system)

print(hopenai.response_to_txt(response))

# +
# Adopt a persona.
system = """
When I ask for help to write something, you will reply with a document that contains at least one joke or
playful comment in every paragraph."
"""
user = """
Write a thank you note to my steel bolt vendor for getting the delivery in on time and in short notice.
This made it possible for us to deliver an important order.
"""
response = hopenai.get_completion(user, system=system)

print(hopenai.response_to_txt(response))

# +
# Use delimiters to indicate parts of input.
system = ""
user = """
Summarize the text delimited by triple quotes with a haiku.

'''
The quick brown fox jumps over the lazy dog
'''

"""
response = hopenai.get_completion(user, system=system)

print(hopenai.response_to_txt(response))

# +
system = """
You will be provided with a thesis abstract and a suggested title for it.
The thesis title should give the reader a good idea of the topic of the thesis but should also be eye-catching.
If the title does not meet these criteria, suggest 5 alternatives.
"""
user = """
Abstract: The Internet has become a primary resource for the general public who
seek health information about a variety of topics, including breast cancer.
This particular research is part of a larger study which evaluated the use of
basic design tenets and theoretical behavioral change components in the top 157
breast cancer websites. Fourteen components were taken from three behavioral
change theories. The focus of this particular project was to assess the use of
these 14 theoretical components on breast cancer websites as they persuade
users towards prevention or detection behaviors. It will also discuss how some
of these components were additionally used to persuade users to contribute
money to the organizations that sponsor the websites. It should first be noted
that overall, theoretical components were absent from the websites in general.
Nine out of the 14 components were found to be used primarily for detection, as
opposed to prevention. This is an important finding because it is just as
valuable, if not more so, for a person to prevent a disease as it is to detect
it early. Four of the 14 were considered when assessing persuasion in terms of
fundraising. Of these four that were assessed, three were used more than 50% of
the time when soliciting money. These results lend ideas for future research on
such topics as well as ideas to better the current state of the top breast
cancer websites.

Title: 
Sensitivity Analysis of DSC Measurements of Denaturation of a Protein Mixture
"""
# Title: The Prevalence of Theoretical Behavior Change Components in the Top Breast
# Cancer Websites to Encourage Detection or Prevention Behaviors and to Solicit Donations
response = hopenai.get_completion(user, system=system)

print(hopenai.response_to_txt(response))

# +
# Specify the steps required to complete a task.
system = """
"""
user = """
"""
response = hopenai.get_completion(user, system=system)

print(hopenai.response_to_txt(response))

# +
# Specify the steps required to complete a task.
system = """
Use the following step-by-step instructions to respond to user inputs.

Step 1 - The user will provide you with text in triple quotes.
Summarize this text in one sentence with a prefix that says "Summary: ".

Step 2 - Translate the summary from Step 1 into Italian, with a prefix that says "Translation: ".
"""
user = """
'''
A large language model (LLM) is a type of artificial intelligence (AI) program
that can recognize and generate text, among other tasks. LLMs are trained on
huge sets of data — hence the name "large." LLMs are built on machine learning:
specifically, a type of neural network called a transformer model.
'''
"""
response = hopenai.get_completion(user, system=system)

print(hopenai.response_to_txt(response))

# +
# Provide examples.
system = """
Answer in a consistent style.
"""
user = """
This is awesome!
A: Negative

This is bad!
A: Positive

Wow that movie was rad!
A: Positive

What a horrible show!
"""
response = hopenai.get_completion(user, system=system)

print(hopenai.response_to_txt(response))

# +
#
system = """
"""
user = """
"""
response = hopenai.get_completion(user, system=system)

print(hopenai.response_to_txt(response))
