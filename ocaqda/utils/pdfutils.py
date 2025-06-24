import io

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams


def convert_pdf_to_html(pdf_path):
    output_html = io.StringIO()
    with open(pdf_path, 'rb') as pdf_file:
        extract_text_to_fp(pdf_file, output_html, laparams=LAParams(), output_type='html', codec=None)
    html_content = output_html.getvalue()
    output_html.close()
    return html_content


