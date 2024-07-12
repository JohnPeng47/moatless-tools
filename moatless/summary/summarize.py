from typing import Dict, Any, List

from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import os


from llama_index.core.schema import TextNode

from moatless.index.code_node import CodeNode

from .models import OpenAIModel, AnthropicModel, ModelArguments

# os.environ.pop("DEEPSEEK_API_KEY", None)

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

SUMMARIZE_PROMPT_HIGHLEVEL = """
Generate a summary of the following chunk of code with the following {code_id}. 
Your summary should provide a high level description of what the code is used for, 
and not focusing on specifics. Give your summary in a flat list of bullet points. 
Keep it concise and avoid superfluous language.
For your last sentence generate a summary of your previous points:
{code}

"""

SUMMARIZE_PROMPT_REF_VARS = """
Generate a summary of the following chunk of code with the following {code_id}. 
Your summary should provide a high level description of what the code is used for, 
and not focusing on specifics (however, in your description, reference at least one variable that is being used in the current code). 
Give your summary in a flat list of bullet points. Keep it concise and avoid superfluous language. 
For your last sentence, give a general summary of your previous points:
{code}
"""


class SummaryNode(TextNode):
    pass


def generate_summary(nodes: List[CodeNode], anthropic=False, ref_vars=False):
    model = (
        OpenAIModel(ModelArguments(model_name="gpt4", api_key=api_key))
        if not anthropic
        else AnthropicModel(
            ModelArguments(model_name="claude-sonnet-3.5", api_key=anthropic_api_key)
        )
    )
    prompt = SUMMARIZE_PROMPT_REF_VARS if ref_vars else SUMMARIZE_PROMPT_HIGHLEVEL
    summary_nodes = []

    def summarize_node(node):
        print(f"Summarizing node: {node.node_id}")
        res = model.query_sync(prompt.format(code_id=node.node_id, code=node.text))
        return res, node

    for node in nodes:
        res, node = summarize_node(node)
        metadata = node.metadata.copy()
        metadata["node_id"] = node.node_id
        summary_nodes.append(SummaryNode(text=res, metadata=metadata))

    # for node in nodes:

    #     def summarize_node(node):
    #         print(f"Summarizing node: {node.node_id}")
    #         res = model.query_sync(prompt.format(code_id=node.node_id, code=node.text))
    #         return res, node

    #     with ThreadPoolExecutor(max_workers=5) as executor:
    #         future_to_node = {
    #             executor.submit(summarize_node, node): node for node in nodes
    #         }
    #         for future in as_completed(future_to_node):
    #             res, node = future.result()
    #             metadata = node.metadata.copy()
    #             metadata["node_id"] = node.node_id
    #             summary_nodes.append(SummaryNode(text=res, metadata=metadata))

    return summary_nodes
