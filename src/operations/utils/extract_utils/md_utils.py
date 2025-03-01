import os
from typing import List

from unstructured.partition.md import partition_md


def extract_md_elements(doc_folder_path: str, filename: str) -> List[dict]:
    md_elements = []

    doc_file_path = os.path.join(doc_folder_path, filename)
    elements = partition_md(filename=doc_file_path)

    processed_element = ""
    for element in elements:
        if "unstructured.documents.elements.Title" in str(type(element)):
            metadata = element.metadata.to_dict()
            tag = f"h{int(metadata['category_depth']) + 1}"
            processed_element += f"<{tag}>{str(element)}</{tag}>\n"
        else:
            processed_element += str(element)

    if processed_element:
        md_elements.append(
            {
                "content": processed_element,
                "metadata": {
                    "source": filename,
                },
            }
        )

    return md_elements
