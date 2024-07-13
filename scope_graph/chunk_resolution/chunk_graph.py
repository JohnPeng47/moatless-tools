from networkx import DiGraph
from pathlib import Path
from llama_index.core.schema import BaseNode
from typing import List

from scope_graph.build_scopes import ScopeGraph, ScopeID
from scope_graph.repo_resolution.repo_graph import RepoGraph
from scope_graph.utils import TextRange
from scope_graph.fs import RepoFs

from .types import ChunkMetadata


class ChunkGraph:
    def __init__(self, repo_path: Path, chunks: List[BaseNode]):
        self.fs = RepoFs(repo_path)
        self._graph = DiGraph()
        self._repo_graph = RepoGraph(repo_path)

        self.scopes_map = self._repo_graph.scopes_map
        self.imports_map = self._repo_graph.construct_imports(self.scopes_map, self.fs)
        self.chunks = chunks
        self.chunk_scope_map = {}

        for chunk in chunks:
            metadata = ChunkMetadata(**chunk.metadata)
            print(f"________________ NODE ________________")
            chunk_scopes = self.get_scopes(
                Path(metadata.file_path),
                metadata.start_line,
                metadata.end_line,
            )
            import_refs = self.get_import_refs(Path(metadata.file_path), chunk_scopes)
            print(f"Chunk: {chunk.get_content()}")

    def insert_chunks(self, chunks: List[BaseNode]):
        pass

    def get_scope_range(self, file: Path, range: TextRange) -> List[ScopeID]:
        return self.scopes_map[file].scopes_by_range(range, overlap=True)

    def get_scopes(self, file_path: Path, start_line: int, end_line: int):
        range = TextRange(
            start_byte=0,
            end_byte=0,
            start_point=(start_line, 0),
            end_point=(end_line, 0),
        )
        scope_graph = self.scopes_map[file_path]
        scopes = scope_graph.scopes_by_range(range, overlap=True)

        return scopes

    def get_import_refs(self, file_path: Path, scopes: List[ScopeID]):
        # get refs from the local scope that is a file-level import
        imported_refs = []
        file_imports = self._repo_graph.imports[file_path]
        scope_graph = self.scopes_map[file_path]

        for scope in scopes:
            refs = scope_graph.references_by_origin(scope)
            for ref in refs:
                ref_node = scope_graph.get_node(ref)
                for imp in file_imports:
                    if ref_node.name == imp.namespace.child:
                        print(
                            "Import: ",
                            imp.namespace,
                            ref_node.name,
                            " for scope: ",
                            scope,
                        )
                        imported_refs.append(ref_node)

        return imported_refs

    def get_modified_chunks(self):
        return self.chunks
