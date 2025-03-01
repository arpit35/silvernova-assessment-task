from typing import List, Literal

from langchain_core.embeddings import Embeddings
from tqdm import tqdm

from src.api import embed_texts


class APIEmbeddingModel(Embeddings):
    def __init__(self) -> None:
        pass

    def embed_documents(self, texts: List[str], input_type: Literal['document', 'query'] = "document") -> List[List[float]]:

        texts = list(map(lambda x: x.replace("\n", " "), texts))

        embeddings = []

        for i in tqdm(range(0, len(texts), 10)):
            embeddings.extend(embed_texts(
                texts[i:i+10], input_type)["embeddings"])

        return embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text], "query")[0]
