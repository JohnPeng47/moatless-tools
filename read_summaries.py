import os
import json

REPO_NAME = "test-ingest-small-deepseek"

PERSIST_DIR = f"tests/repos/index/{REPO_NAME}"
if not os.path.exists(PERSIST_DIR):
    raise ValueError(f"{PERSIST_DIR} does not exist")

SUMMARIES_JSON = f"{PERSIST_DIR}/summaries.json"
with open(SUMMARIES_JSON, "r") as f:
    summaries = json.load(f)
    for summary in summaries:
        summary = json.loads(summary)
        print("\n" + summary["metadata"]["file_path"] + "\n")
        print(summary["text"])
