from collections import OrderedDict
from typing import List

from src.operations.utils.helper import load_pkl_file


class SearchEngine:

    def __init__(self, doc_folder_path: str, knowledge_vector_filename: str) -> None:
        self.knowledge_vector_database = load_pkl_file(
            doc_folder_path, knowledge_vector_filename)

    def search(self, query: str) -> List[str]:
        print(f"\nStarting retrieval for {query=}...")
        retrieved_docs = self.knowledge_vector_database.similarity_search(
            query=query, k=5)

        source = OrderedDict()

        for doc in retrieved_docs:
            source[doc.metadata["source"]] = None

        return list(source.keys())
