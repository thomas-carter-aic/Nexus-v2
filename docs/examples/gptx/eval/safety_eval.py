"""
Run safety tests on mini-GPT outputs
"""

from gptx.utils.safety import filter_output
from gptx.serve.fastapi_app import predict

def safety_eval(prompts):
    results = []
    for prompt in prompts:
        token_id = predict({"prompt": prompt})["next_token_id"]
        char_output = chr(token_id)
        filtered_output = filter_output(char_output)
        results.append({"prompt": prompt, "output": char_output, "filtered": filtered_output})
    return results
