from typing import List, Literal

from langchain_core.embeddings import Embeddings

from src.api import embed_texts
from src.operations.utils.helper import progress_bar


class APIEmbeddingModel(Embeddings):
    def __init__(self) -> None:
        pass

    def embed_documents(self, texts: List[str], input_type: Literal['document', 'query'] = "document") -> List[List[float]]:

        texts = list(map(lambda x: x.replace("\n", " "), texts))

        embeddings = []

        if input_type == "document":
            progress_bar_desc = "Embedding documents"
        else:
            progress_bar_desc = "Embedding queries"

        for i in progress_bar(range(0, len(texts), 10), desc=progress_bar_desc):
            embeddings.extend(embed_texts(
                texts[i:i+10], input_type)["embeddings"])

        return embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text], "query")[0]
