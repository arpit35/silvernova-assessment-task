from src.api import execute_prompt
from src.operations.utils.helper import load_pkl_file


class LLMAsker:
    def __init__(self, doc_folder_path: str, knowledge_vector_filename: str) -> None:
        self.knowledge_vector_database = load_pkl_file(
            doc_folder_path, knowledge_vector_filename)

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

        return response['response'].replace('<br>', '\n')
