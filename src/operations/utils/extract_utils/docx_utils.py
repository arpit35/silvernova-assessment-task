import os
import shutil
import subprocess

import fitz


def convert_docx_to_pdf(doc_folder_path, filename):
    doc_file_path = os.path.join(doc_folder_path, filename)
    temp_doc_folder_path = os.path.join(doc_folder_path, "temp")
    temp_doc_file_path = os.path.join(
        temp_doc_folder_path, os.path.splitext(filename)[0] + '.pdf')

    # Convert DOCX to PDF (LibreOffice will use the same base name as the DOCX)
    command = [
        'libreoffice',
        '--headless',
        '--convert-to', 'pdf',
        doc_file_path,
        '--outdir', temp_doc_folder_path
    ]
    subprocess.run(command, check=True)

    pdf_document = fitz.open(temp_doc_file_path)

    # Delete the temporary folder
    shutil.rmtree(temp_doc_folder_path)

    return pdf_document
