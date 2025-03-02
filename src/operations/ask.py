import logging
from os import environ

from langchain_core.vectorstores import VectorStore
from ragatouille import RAGPretrainedModel

from src.api import execute_prompt
from src.operations.utils.helper import load_pkl_file, search_and_rerank

logger = logging.getLogger(__name__)


class LLMAsker:
    def __init__(self, doc_folder_path: str, knowledge_vector_filename: str) -> None:
        logger.info("LLM Asker initialized")
        self.reranker = RAGPretrainedModel.from_pretrained(
            "colbert-ir/colbertv2.0")

        self.knowledge_vector_database: VectorStore = load_pkl_file(
            doc_folder_path, knowledge_vector_filename)

        self.fetch_doc_count = int(environ.get('FETCHED_DOC_COUNT', 15))
        self.reranked_doc_count = int(environ.get('RERANKED_DOC_COUNT', 3))

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
        logger.info("Starting retrieval for question = %s...", question)

        retrieved_docs = search_and_rerank(
            self.knowledge_vector_database, self.reranker, question, self.fetch_doc_count, self.reranked_doc_count)

        response = execute_prompt(self._get_prompt(
            [{"metadata": doc.metadata, "page_content": doc.page_content} for doc in retrieved_docs], question))

        print(response['response'])

        return response['response'].replace('<br>', '\n')
