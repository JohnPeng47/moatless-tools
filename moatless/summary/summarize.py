from pydantic import BaseModel
from typing import Dict, Any, List

from dotenv import load_dotenv
import os


from llama_index.core.schema import TextNode

from moatless.index.code_node import CodeNode

from .models import OpenAIModel, ModelArguments


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


SUMMARIZE_PROMPT = """
Generate a summary of the following chunk of code with the following {code_id}. 
Your summary should provide a high level description of what the code is used for, 
and not focusing on specifics. Give your summary in a flat list of bullet points. 
Keep it concise and avoid superfluous language
{code}

"""


class SummaryNode(TextNode):
    pass


def generate_summary(nodes: List[CodeNode]):
    model = OpenAIModel(ModelArguments(model_name="gpt4", api_key=api_key))
    summary_nodes = []

    for node in nodes:
        print(f"Summarizing: {node.text}")

        res = model.query_sync(
            SUMMARIZE_PROMPT.format(code_id=node.node_id, code=node.text)
        )

        metadata = node.metadata.copy()
        # store a refernce back to original CodeNode
        metadata["node_id"] = node.node_id

        summary_nodes.append(SummaryNode(text=res, metadata=node.metadata))

    return summary_nodes
