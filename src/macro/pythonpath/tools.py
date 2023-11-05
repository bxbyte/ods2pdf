import typing

from pypdf import PdfWriter
from re import sub, search
from io import BytesIO


def load_table(file_path: str) -> typing.Generator[tuple[str, str], None, None]:
    """Read and extract pairs of ods to pdf fields keys from .o2p file

    Args:
        file_path (str): File path to a .o2p file.

    Yields:
        Iterator[typing.Generator[tuple[str, str], None, None]]: Pairs of ods to pdf fields keys, like ["A1", "Name"].
    """
    with open(file_path, 'r') as file:
        for line in file.readlines():
            line = sub(r"#.*$|\n|\r", '', line) # Remove comments & line escape char
            try:
                cell_id, field_name, options = search(r"^(\S*)\s+(\S*)\s*(.*)?$", line).groups()
                cell_id = cell_id.strip()
                field_name = field_name.strip()
                if options:
                    yield cell_id, field_name, *map(lambda s: s.strip(), options.rsplit(' ', 1))
                else:
                    yield cell_id, field_name
            except Exception:
                pass


def generate_from_fields(pdf_bytes: BytesIO, result_path: str, fields_data: dict[str, str]):
    """Write a PDF with fields filled by fields_data.

    Args:
        pdf_bytes (BytesIO): File path to pdf template.
        result_path (str): File path to the pdf result.
        fields_data (dict[str, str]): Pair of fields key-value.

    Returns:
        PdfWriter: Filled PdfWriter.
    """
    writer = PdfWriter(clone_from=pdf_bytes)

    for page in writer.pages:
        writer.update_page_form_field_values(
            page,
            fields_data
        )
    
    writer.write(result_path)