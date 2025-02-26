import logging
import os
import pickle

from langchain.docstore.document import Document as LangchainDocument
from unstructured.partition.pdf import partition_pdf

logger = logging.getLogger("markdown-extractor")


class MarkdownExtractor:

    def __init__(self):
        logger.info("MarkdownExtractor initialized")
        # Doc Folder path
        self.doc_folder_path = "documents/"
        self.RAW_KNOWLEDGE_BASE = []

    def _extract_pdf_elements(self, path, fname):
        return partition_pdf(
            filename=path + fname,
            infer_table_structure=True,
            strategy="hi_res",
            chunking_strategy="by_title",
            max_characters=4000,
            new_after_n_chars=3800,
            combine_text_under_n_chars=2000,
        )

    def _append_to_knowledge_base(self, element, element_type):
        element_metadata = element.metadata.to_dict()

        metadata = {
            "source": element_metadata["filename"],
            "page_number": element_metadata["page_number"],
            "element_type": element_type,
        }

        self.RAW_KNOWLEDGE_BASE.append(LangchainDocument(
            page_content=str(element), metadata=metadata))

    def _categorize_pdf_elements(self, raw_pdf_elements):
        for element in raw_pdf_elements:
            if "unstructured.documents.elements.Table" in str(type(element)):
                self._append_to_knowledge_base(element, "table")
            elif "unstructured.documents.elements.CompositeElement" in str(
                type(element)
            ):
                self._append_to_knowledge_base(element, "text")

    def process(self):
        # Checking if folder exists
        if not os.path.exists(self.doc_folder_path):
            logger.error("Folder '%s' does not exist.", self.doc_folder_path)
            return

        for file in os.listdir(self.doc_folder_path):
            if file.endswith(".pdf"):
                self._categorize_pdf_elements(
                    self._extract_pdf_elements(self.doc_folder_path, file))

        print("RAW_KNOWLEDGE_BASE", self.RAW_KNOWLEDGE_BASE)

    def save(self):
        doc_file_path = os.path.join("self.doc_folder_path", "documents.pkl")

        with open(doc_file_path, "wb") as f:
            pickle.dump(self.RAW_KNOWLEDGE_BASE, f)

        # # Load from file
        # with open("documents.pkl", "rb") as f:
        #     docs = pickle.load(f)
