import os
import pickle
from collections import OrderedDict


class SearchEngine:

    def __init__(self, doc_folder_path, knowledge_vector_filename) -> None:
        self.knowledge_vector_database = self.load(
            doc_folder_path, knowledge_vector_filename)

    def load(self, doc_folder_path, knowledge_vector_filename):
        knowledge_vector_file_path = os.path.join(
            doc_folder_path, f"{knowledge_vector_filename}.pkl")

        with open(knowledge_vector_file_path, "rb") as f:
            knowledge_vector_database = pickle.load(f)

        return knowledge_vector_database

    def search(self, query):
        print(f"\nStarting retrieval for {query=}...")
        retrieved_docs = self.knowledge_vector_database.similarity_search(
            query=query, k=5)

        source = OrderedDict()

        for doc in retrieved_docs:
            source[doc.metadata["source"]] = None

        return list(source.keys())
