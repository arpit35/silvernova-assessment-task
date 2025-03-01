import os
from typing import List

from unstructured.partition.xlsx import partition_xlsx


def extract_xlsx_elements(doc_folder_path: str, filename: str) -> List[dict]:
    xlsx_elements = []
    xlsx_text_elements = {}
    doc_file_path = os.path.join(doc_folder_path, filename)

    elements = partition_xlsx(filename=doc_file_path, include_header=True)

    for element in elements:
        metadata = element.metadata.to_dict()

        if "unstructured.documents.elements.Table" in str(type(element)):
            xlsx_elements.append({"content": metadata["text_as_html"], "metadata": {
                "source": filename, "page_name": metadata["page_name"]}})
        else:
            if metadata['page_name'] not in xlsx_text_elements:
                xlsx_text_elements[metadata['page_name']] = {"content": str(element), "metadata": {
                    "source": filename, "page_name": metadata["page_name"]}}
            else:
                xlsx_text_elements[metadata['page_name']
                                   ]["content"] += f"\n{str(element)}"

    xlsx_elements.extend(list(xlsx_text_elements.values()))
    return xlsx_elements
