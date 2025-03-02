import logging
from collections import OrderedDict
from os import environ
from typing import List

from langchain_core.vectorstores import VectorStore
from ragatouille import RAGPretrainedModel

from src.operations.utils.helper import load_pkl_file, search_and_rerank

logger = logging.getLogger(__name__)


class SearchEngine:

    def __init__(self, doc_folder_path: str, knowledge_vector_filename: str) -> None:
        logger.info("Search Engine initialized")
        self.reranker = RAGPretrainedModel.from_pretrained(
            "colbert-ir/colbertv2.0")

        self.knowledge_vector_database: VectorStore = load_pkl_file(
            doc_folder_path, knowledge_vector_filename)

        self.fetch_doc_count = int(environ.get('FETCHED_DOC_COUNT', 15))
        self.reranked_doc_count = int(environ.get('RERANKED_DOC_COUNT', 3))

    def search(self, query: str) -> List[str]:
        logger.info("Starting retrieval for query = %s...", query)
        retrieved_docs = search_and_rerank(
            self.knowledge_vector_database, self.reranker, query, self.fetch_doc_count, self.reranked_doc_count)

        source = OrderedDict()

        for doc in retrieved_docs:
            source[doc.metadata["source"]] = None

            formatted_sources = "\n# Documents Found\n" + \
                "\n".join(f"- {key}" for key in source.keys())
        return formatted_sources
