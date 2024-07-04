from moatless.index import CodeIndex, IndexSettings
from moatless import FileRepository
from moatless.workspace import Workspace
from moatless.index.simple_faiss import VectorStoreType

import os

REPO_NAME = "test-ingest-small"


def get_code_index(file_repo, persist_dir):
    # An OPENAI_API_KEY is required to use the OpenAI Models
    model = "gpt-4o-2024-05-13"
    index_settings = IndexSettings(embed_model="text-embedding-3-small")

    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        print("Load from disk")
        code_index = CodeIndex.from_persist_dir(persist_dir, file_repo=file_repo)
    else:
        code_index = CodeIndex(
            file_repo=file_repo, settings=index_settings, to_summarize=True
        )
        nodes = code_index.run_ingestion()
        code_index.persist(persist_dir)

    return code_index


persist_dir = f"tests/repos/index/{REPO_NAME}"
repo_dir = f"tests/repos/{REPO_NAME}"
file_repo = FileRepository(repo_path=repo_dir)

code_index = get_code_index(file_repo, persist_dir)

workspace = Workspace(file_repo=file_repo, code_index=code_index)
res = code_index.search(
    "What does the _build_path_tree function do?", store_type=VectorStoreType.SUMMARY
)

for summary, _ in res:
    print(summary)

# for node in nodes:
#     print(node)
#     print(node.metadata)
# print(node.node_id)
# print(node.metadata["file_path"])

# code_index.persist(persist_dir)

# file_context = workspace.create_file_context(files_with_spans=res.hits)
# for hit in res.hits:
#     for span in hit.spans:
#         file_context.add_span_to_context(hit.file_path, span.span_id, tokens=1)

# print(
#     "Search results: ",
#     file_context.create_prompt(
#         show_span_ids=False,
#         show_line_numbers=False,
#         exclude_comments=True,
#         show_outcommented_code=False,
#     ),
# )
