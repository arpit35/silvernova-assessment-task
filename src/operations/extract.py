import logging
import os
import pickle

from langchain.docstore.document import Document as LangchainDocument

from src.operations.utils.extract_utils.docx_utils import convert_docx_to_pdf
from src.operations.utils.extract_utils.md_utils import extract_md_elements
from src.operations.utils.extract_utils.msg_utils import extract_msg_elements
from src.operations.utils.extract_utils.pdf_utils import (
    extract_pdf_elements,
    split_pdf_into_pages,
)
from src.operations.utils.extract_utils.xlsx_utils import extract_xlsx_elements

logger = logging.getLogger("markdown-extractor")


class MarkdownExtractor:

    def __init__(self, doc_folder_path):
        logger.info("MarkdownExtractor initialized")
        # Doc Folder path
        self.doc_folder_path = doc_folder_path
        self.RAW_KNOWLEDGE_BASE = []

    def _append_to_knowledge_base(self, elements):
        for element in elements:
            self.RAW_KNOWLEDGE_BASE.append(
                LangchainDocument(
                    page_content=element["content"], metadata=element["metadata"])
            )

    def process(self):
        # Checking if folder exists
        if not os.path.exists(self.doc_folder_path):
            logger.error("Folder '%s' does not exist.", self.doc_folder_path)
            return

        for filename in os.listdir(self.doc_folder_path):
            if filename.endswith(".pdf"):
                pages = split_pdf_into_pages(self.doc_folder_path, filename)
                self._append_to_knowledge_base(
                    extract_pdf_elements(pages))
            elif filename.endswith(".md"):
                self._append_to_knowledge_base(
                    extract_md_elements(self.doc_folder_path, filename))
            elif filename.endswith(".docx"):
                pdf_document = convert_docx_to_pdf(
                    self.doc_folder_path, filename)
                pages = split_pdf_into_pages(
                    self.doc_folder_path, filename, pdf_document)
                self._append_to_knowledge_base(
                    extract_pdf_elements(pages))
            elif filename.endswith(".msg"):
                self._append_to_knowledge_base(
                    extract_msg_elements(self.doc_folder_path, filename))
            elif filename.endswith(".xlsx"):
                self._append_to_knowledge_base(
                    extract_xlsx_elements(self.doc_folder_path, filename))

    def save(self, knowledge_base_filename):
        doc_file_path = os.path.join(
            self.doc_folder_path, f"{knowledge_base_filename}.pkl")

        with open(doc_file_path, "wb") as f:
            pickle.dump(self.RAW_KNOWLEDGE_BASE, f)

        # # Load from file
        # with open("documents.pkl", "rb") as f:
        #     docs = pickle.load(f)
