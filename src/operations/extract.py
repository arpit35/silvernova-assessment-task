import logging
import os
from typing import List

from langchain.docstore.document import Document as LangchainDocument

from src.operations.utils.extract_utils.docx_utils import convert_docx_to_pdf
from src.operations.utils.extract_utils.md_utils import extract_md_elements
from src.operations.utils.extract_utils.msg_utils import extract_msg_elements
from src.operations.utils.extract_utils.pdf_utils import (
    extract_pdf_elements,
    split_pdf_into_pages,
)
from src.operations.utils.extract_utils.xlsx_utils import extract_xlsx_elements
from src.operations.utils.helper import dump_pkl_file, progress_bar

logger = logging.getLogger(__name__)


class MarkdownExtractor:

    def __init__(self, doc_folder_path: str) -> None:
        logger.info("Markdown Extractor initialized")
        # Doc Folder path
        self.doc_folder_path = doc_folder_path
        self.raw_knowledge_base = []

    def _append_to_knowledge_base(self, elements: List[dict]) -> None:
        for element in elements:
            self.raw_knowledge_base.append(
                LangchainDocument(
                    page_content=element["content"], metadata=element["metadata"])
            )

    def process(self) -> None:
        # Checking if folder exists
        if not os.path.exists(self.doc_folder_path):
            logger.error("Folder '%s' does not exist.", self.doc_folder_path)
            return

        logger.info("Processing files in folder '%s'", self.doc_folder_path)
        for filename in progress_bar(os.listdir(self.doc_folder_path), desc="Processing files"):
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

    def save(self, knowledge_base_filename: str) -> str:
        dump_pkl_file(self.doc_folder_path,
                      knowledge_base_filename, self.raw_knowledge_base)

        return "\n## Knowledge Base Successfully created and saved to disk\n"
