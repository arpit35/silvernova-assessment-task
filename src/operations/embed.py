import logging
from typing import List

from langchain.docstore.document import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from transformers import AutoTokenizer

from src.models.api_embedding_model import APIEmbeddingModel
from src.operations.utils.helper import dump_pkl_file, load_pkl_file

logger = logging.getLogger(__name__)

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


class EmbedService:

    def __init__(self, doc_folder_path: str, knowledge_base_filename: str) -> None:
        logger.info("Embed Service initialized")
        self.doc_folder_path = doc_folder_path

        self.raw_knowledge_base: List[LangchainDocument] = load_pkl_file(
            doc_folder_path, knowledge_base_filename)

        self.knowledge_vector_database = None

    def embed(self) -> None:

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

    def save(self, knowledge_vector_filename: str) -> str:
        dump_pkl_file(self.doc_folder_path, knowledge_vector_filename,
                      self.knowledge_vector_database)

        return "\n## Knowledge Vector Database Successfully created and saved to disk\n"
