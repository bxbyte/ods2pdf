import typing

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject
from re import sub, search


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
                if options:
                    yield cell_id, field_name, *map(lambda s: s.strip(), options.rsplit(' ', 1))
                else:
                    yield cell_id, field_name
            except Exception:
                pass


def generate_from_fields(template_path: str, result_path: str, fields_data: dict[str, str]):
    """Create a PdfWritre with fields filled.

    Args:
        template_path (str): File path to pdf template.
        result_path (str): File path to the pdf result.
        fields_data (dict[str, str]): Pair of fields key-value.

    Returns:
        PdfWriter: Filled PdfWriter.
    """
    reader = PdfReader(template_path, strict=False)
    reader.trailer["/Root"]["/AcroForm"].update(
        {NameObject("/NeedAppearances"): BooleanObject(True)}
    )
    
    writer = PdfWriter()
    writer._root_object.update({
        NameObject("/AcroForm"): reader.trailer["/Root"]["/AcroForm"]
    })

    for i, page in enumerate(reader.pages):
        writer.add_page(page)
        writer.update_page_form_field_values(
            writer.get_page(i),
            fields_data
        )
    
    writer.write(result_path)