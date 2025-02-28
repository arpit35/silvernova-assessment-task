import io
import os

import fitz
from unstructured.partition.pdf import partition_pdf


def split_pdf_into_pages(doc_folder_path, filename, pdf_document=None):

    if not pdf_document:
        doc_file_path = os.path.join(doc_folder_path, filename)
        pdf_document = fitz.open(doc_file_path)

    pages = []

    for i in range(pdf_document.page_count):
        pdf_writer = fitz.open()  # Create a new blank PDF
        pdf_writer.insert_pdf(pdf_document, from_page=i, to_page=i)

        # Save the single-page PDF to a bytes buffer
        page_bytes = io.BytesIO()
        pdf_writer.save(page_bytes)
        pdf_writer.close()

        page_bytes.seek(0)  # Reset the pointer to the beginning
        pages.append(
            {"content": page_bytes, "filename": filename, "page_number": i + 1})

    return pages


def extract_pdf_elements(pages):
    pdf_elements = []

    for page in pages:
        elements = partition_pdf(
            file=page["content"],
            infer_table_structure=True,
            strategy="hi_res",
            chunking_strategy="by_title",
            max_characters=4000,
            new_after_n_chars=3800,
            combine_text_under_n_chars=2000,
        )

        for element in elements:
            element_type = None
            if "unstructured.documents.elements.Table" in str(type(element)):
                element_type = "table"
            elif "unstructured.documents.elements.CompositeElement" in str(
                type(element)
            ):
                element_type = "text"

            if element_type:
                pdf_elements.append(
                    {
                        "content": str(element),
                        "metadata": {
                            "source": page["filename"],
                            "page_number": page["page_number"],
                            "element_type": element_type,
                        },
                    }
                )

    return pdf_elements
