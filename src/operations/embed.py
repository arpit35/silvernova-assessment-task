import logging
import os
import pickle
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.embeddings import Embeddings
from tqdm import tqdm
from transformers import AutoTokenizer

from src.api import embed_texts

logger = logging.getLogger('embed')

MARKDOWN_SEPARATORS = [
    "\n#{1,6} ",
    "```\n",
    "\n\\*\\*\\*+\n",
    "\n---+\n",
    "\n___+\n",
    "\n\n",
    "\n",
    " ",
    "",
]


class APIEmbeddingModel(Embeddings):
    def __init__(self):
        pass

    def embed_documents(self, texts: List[str], input_type="document") -> List[List[float]]:

        texts = list(map(lambda x: x.replace("\n", " "), texts))

        embeddings = []

        for i in tqdm(range(0, len(texts), 10)):
            embeddings.extend(embed_texts(
                texts[i:i+10], input_type)["embeddings"])

        return embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text], "query")[0]


class EmbedService:

    def __init__(self, doc_folder_path, knowledge_base_filename):
        self.doc_folder_path = doc_folder_path

        self.raw_knowledge_base = self.load(
            doc_folder_path, knowledge_base_filename)

        self.knowledge_vector_database = None

    def load(self, doc_folder_path, knowledge_base_filename):
        knowledge_base_file_path = os.path.join(
            doc_folder_path, f"{knowledge_base_filename}.pkl")

        with open(knowledge_base_file_path, "rb") as f:
            raw_knowledge_base = pickle.load(f)

        return raw_knowledge_base

    def embed(self) -> List[float]:

        text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            AutoTokenizer.from_pretrained("thenlper/gte-small"),
            chunk_size=512,
            chunk_overlap=int(512 / 10),
            add_start_index=True,
            strip_whitespace=True,
            separators=MARKDOWN_SEPARATORS,
        )

        processed_knowledge_base = []
        for doc in self.raw_knowledge_base:
            processed_knowledge_base.extend(
                text_splitter.split_documents([doc]))

        embedding_model = APIEmbeddingModel()

        self.knowledge_vector_database = FAISS.from_documents(
            processed_knowledge_base, embedding_model, distance_strategy=DistanceStrategy.COSINE
        )

    def save(self, knowledge_vector_filename):
        knowledge_vector_file_path = os.path.join(
            self.doc_folder_path, f"{knowledge_vector_filename}.pkl")

        with open(knowledge_vector_file_path, "wb") as f:
            pickle.dump(self.knowledge_vector_database, f)
