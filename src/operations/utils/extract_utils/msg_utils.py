import os
import re
from datetime import timezone
from typing import List

import extract_msg
from bs4 import BeautifulSoup


def find_separators(soup: BeautifulSoup) -> List[BeautifulSoup]:
    outlook_separator_id_pattern = re.compile(r".*divRplyFwdMsg")
    gmail_email_pattern = re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    )
    separators = []

    for element in soup.find_all(True):
        # Removing the element with caution text
        if (
            element.name == "table"
            and element.get("style")
            and "font-family: Arial !important;" in element["style"]
            and "table-layout: auto;" in element["style"]
            and "font-size: 12px !important;" in element["style"]
            and "background-color: #fffbcc;" in element["style"]
            and "padding: 8px;" in element["style"]
            and "border-left: solid 6px #ffef2b;" in element["style"]
        ):
            element.decompose()

        # Removing the elements with display: none
        elif (
            (element.name == "div" or element.name == "span")
            and element.get("style")
            and "display:none" in element["style"]
        ):
            element.decompose()

        # finding an email in Outlook with the specified separator style
        elif (
            element.name == "div"
            and element.get("style")
            and "border:none" in element["style"]
            and (
                "border-top:solid #B5C4DF 1.0pt" in element["style"]
                or "border-top:solid #E1E1E1 1.0pt" in element["style"]
            )
            and "padding:3.0pt 0cm 0cm 0cm" in element["style"]
        ):
            separators.append(element)

        # finding an email in Outlook with the specified separator style
        elif element.name == "div" and outlook_separator_id_pattern.match(
            element.get("id", "")
        ):
            separators.append(element)

        # finding an email in gmail with the specified separator style
        elif element.name == "blockquote":
            preceding_element = element.find_previous_sibling()
            if preceding_element and gmail_email_pattern.search(
                preceding_element.get_text()
            ):
                separators.append(preceding_element)

    return separators


def extract_text_from_html(email_html_content: str) -> str:
    email_text = BeautifulSoup(email_html_content, "html.parser").get_text(
        separator=" ", strip=True
    )
    if email_text:
        return email_text
    return None


def extract_msg_elements(doc_folder_path: str, filename: str) -> List[dict]:
    msg_elements = []

    msg_file_path = os.path.join(doc_folder_path, filename)

    msg = extract_msg.Message(msg_file_path)
    html_body = msg.htmlBody or msg.body

    if not html_body:
        raise ValueError("HTML body cannot be empty.")

    soup = BeautifulSoup(html_body, "html.parser")

    separators = find_separators(soup)

    current_pos = 0

    msg_metadata = {
        "source": filename,
        "to": msg.to,
        "from": msg.sender,
        "cc": msg.cc,
        "subject": msg.subject,
        "date": msg.date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z'),
    }

    # Process the HTML content from beginning of the eml file to 1st separator
    if separators:
        for separator in separators:
            msg_metadata["mail_history_header"] = extract_text_from_html(
                separator.decode_contents())

            email_html_content = soup.decode_contents()[
                current_pos: soup.decode_contents().index(str(separator))
            ]
            msg_elements.append({"content": extract_text_from_html(
                email_html_content), "metadata": msg_metadata})
            current_pos = soup.decode_contents().index(
                str(separator)
            ) + len(str(separator))

        # Process any remaining HTML content after the last separator
        remaining_content = soup.decode_contents()[current_pos:]
        msg_elements.append({"content": extract_text_from_html(
            remaining_content), "metadata": msg_metadata})
    else:
        email_html_content = soup.decode_contents()
        msg_elements.append({"content": extract_text_from_html(
            email_html_content), "metadata": msg_metadata})

    return msg_elements
