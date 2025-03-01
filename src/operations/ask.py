import os
import pickle

from src.api import execute_prompt


class LLMAsker:
    def __init__(self, doc_folder_path, knowledge_vector_filename):
        self.knowledge_vector_database = self.load(
            doc_folder_path, knowledge_vector_filename)

    def load(self, doc_folder_path, knowledge_vector_filename):
        knowledge_vector_file_path = os.path.join(
            doc_folder_path, f"{knowledge_vector_filename}.pkl")

        with open(knowledge_vector_file_path, "rb") as f:
            knowledge_vector_database = pickle.load(f)

        return knowledge_vector_database

    def _get_prompt(self, context: str, question: str) -> str:
        return f"""
            Using the provided context, generate a precise and relevant answer to the question.  
            - Ensure the response is concise and directly addresses the question.  
            - Reference sources explicitly like - Source(File Name → Page Name/Page Number → Sentence).
            - If the answer is not present in the context, state that no answer can be provided.  

            **Context:**  
            "{context}"  

            **Question:**  
            "{question}"  
            """

    def ask(self, question: str) -> str:
        print('Thinking...')

        retrieved_docs = self.knowledge_vector_database.similarity_search(
            query=question, k=4)

        response = execute_prompt(self._get_prompt(
            [{"metadata": doc.metadata, "page_content": doc.page_content} for doc in retrieved_docs], question))

        return response['response']
