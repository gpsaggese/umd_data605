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
