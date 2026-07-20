import os

from docx2pdf import convert


def convert_word_to_pdf(input_path, output_folder):
    """
    Converts a DOCX file to PDF.

    Args:
        input_path (str): Full path to the uploaded DOCX file.
        output_folder (str): Folder where the PDF should be saved.

    Returns:
        str: Full path to the generated PDF.
    """

    filename = os.path.basename(input_path)

    pdf_filename = os.path.splitext(filename)[0] + ".pdf"

    output_path = os.path.join(
        output_folder,
        pdf_filename,
    )

    convert(input_path, output_path)

    return output_path