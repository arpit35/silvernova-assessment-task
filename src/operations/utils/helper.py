import logging
import os
import pickle
from typing import Any, Iterable, List

from langchain.docstore.document import Document as LangchainDocument
from langchain_core.vectorstores import VectorStore
from ragatouille import RAGPretrainedModel
from tqdm import tqdm

logger = logging.getLogger(__name__)


def load_pkl_file(folder: str, filename: str) -> Any:
    file_path = os.path.join(folder, f"{filename}.pkl")

    with open(file_path, "rb") as f:
        return pickle.load(f)


def dump_pkl_file(folder: str, filename: str, data: Any) -> None:
    file_path = os.path.join(folder, f"{filename}.pkl")

    with open(file_path, "wb") as f:
        pickle.dump(data, f)


def search_and_rerank(knowledge_vector_database: VectorStore, reranker: RAGPretrainedModel, query: str, num_retrieved_docs: int,
                      num_docs_final: int) -> List[LangchainDocument]:

    retrieved_docs = knowledge_vector_database.similarity_search(
        query=query, k=num_retrieved_docs)

    retrieved_docs_content = [doc.page_content for doc in retrieved_docs]

    logger.info("Reranking retrieved documents...")
    relevant_docs = reranker.rerank(
        query, retrieved_docs_content, k=num_docs_final)

    relevant_docs_ids = [doc['result_index'] for doc in relevant_docs]

    return [retrieved_docs[i] for i in relevant_docs_ids]


def progress_bar(iterable: Iterable[str], **kwargs) -> tqdm:
    return tqdm(iterable, dynamic_ncols=True, bar_format="{l_bar}{bar}| [{elapsed}<{remaining}, {rate_fmt}{postfix}]", **kwargs)
