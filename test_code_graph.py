from moatless.index import CodeIndex, IndexSettings
from moatless import FileRepository
from moatless.workspace import Workspace
from moatless.index.simple_faiss import VectorStoreType

from moatless.summary.models import num_tokens_from_string

import os

REPO_NAME = "test-ingest-small-oai"
query = """Codeblocks for imports statements. External references"""

print("Query: ", query)


def get_code_index(file_repo, persist_dir):
    # An OPENAI_API_KEY is required to use the OpenAI Models
    model = "gpt-4o-2024-05-13"
    index_settings = IndexSettings(embed_model="text-embedding-3-small")

    code_index = CodeIndex(
        file_repo=file_repo, settings=index_settings, to_summarize=False
    )
    nodes = code_index.run_ingestion()
    code_index.persist(persist_dir)

    return code_index


persist_dir = f"tests/repos/index/{REPO_NAME}"
repo_dir = f"tests/repos/{REPO_NAME}"
file_repo = FileRepository(repo_path=repo_dir)

code_index = get_code_index(file_repo, persist_dir)

# workspace = Workspace(file_repo=file_repo, code_index=code_index)
# res = code_index.search(query, store_type=VectorStoreType.SUMMARY)

# for summary, _ in res:
#     print(summary)
#     print(summary.metadata["file_path"])
