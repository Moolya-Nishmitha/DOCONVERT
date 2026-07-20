import os

from pdf2docx import Converter


def convert_pdf_to_word(input_path, output_folder):
    """
    Converts a PDF file to DOCX.

    Args:
        input_path (str): Full path to the uploaded PDF.
        output_folder (str): Folder where the DOCX should be saved.

    Returns:
        str: Full path to the generated DOCX.
    """

    filename = os.path.basename(input_path)

    docx_filename = os.path.splitext(filename)[0] + ".docx"

    output_path = os.path.join(
        output_folder,
        docx_filename,
    )

    converter = Converter(input_path)

    converter.convert(output_path)

    converter.close()

    return output_path