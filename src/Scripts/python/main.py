"""Export configured cells into the configured template's PDF file fields.
"""

import typing
import sys
from zipfile import ZipFile
from os import remove, close
from shutil import move
from os.path import join
from re import search
from tempfile import mkstemp
from uno import fileUrlToSystemPath

# Import pythonpath (ugly but required)
global XSCRIPTCONTEXT
DOC = XSCRIPTCONTEXT.getDocument()  # noqa: F821
PYTHON_PATH = join(fileUrlToSystemPath(DOC.URL), "Scripts/python/pythonpath")
if not PYTHON_PATH in sys.path:
    sys.path.insert(0, PYTHON_PATH)

from pypdf import PdfWriter
from dialog import msgbox, filebox
from yaml import load, SafeLoader
from const import FORMATTER

ARCHIVE_PATH = fileUrlToSystemPath(DOC.getURL())
CONFIG_PATH = "Config/config.yml"
TEMPLATE_PATH = "Config/template.pdf"


class CellConfig(typing.TypedDict):
    cell: str
    format: str
    regex: str


class ODS2PDFError(Exception):
    ...
    

def export(*args):
    with ZipFile(ARCHIVE_PATH) as z:
        with z.open(CONFIG_PATH) as config_file:
            config = load(config_file, SafeLoader)
            res_path = filebox(("PDF File (.pdf)", "*.pdf"), mode=10)

            if not res_path:
                return
            
            fields_data = {}
            for page in config:
                sheet = DOC.Sheets[page]
                for field, v in config[page].items():
                    if isinstance(v, str):
                        content = sheet.getCellRangeByName(v).getString() 
                        if content:
                            fields_data[field] = content
                    else:
                        cell = v["cell"]
                        format = v.get("format", "{0}")
                        regex = v.get("regex", r".*")
                        search_res = search(regex, sheet.getCellRangeByName(cell).getString())
                        try:
                            content = FORMATTER.format(format, *search_res.groups(), **search_res.groupdict())
                            if content:
                                fields_data[field] = content
                        except (KeyError, IndexError, AttributeError):
                            pass
                        
            with z.open(TEMPLATE_PATH) as pdf_file:
                with PdfWriter(clone_from=pdf_file) as pdf:
                    for page in pdf.pages:
                        pdf.update_page_form_field_values(
                            page,
                            fields_data
                        )
                    
                    pdf.write(res_path)
        
            msgbox("Done.", "ODS2PDF")


def set_template(*args):    
    template_path = filebox(("PDF File (.pdf)", "*.pdf"), mode=11)
    with open(template_path, 'rb') as template_file:
        template_data = template_file.read()
        
    tmpfd, tmp_path = mkstemp()
    close(tmpfd)

    with ZipFile(ARCHIVE_PATH, 'r') as zin:
        with ZipFile(tmp_path, 'w') as zout:
            zout.comment = zin.comment
            for item in zin.infolist():
                if item.filename != TEMPLATE_PATH:
                    zout.writestr(item, zin.read(item.filename))
            with zout.open(TEMPLATE_PATH, 'w') as zfile:
                zfile.write(template_data)
            
    remove(ARCHIVE_PATH)
    move(tmp_path, ARCHIVE_PATH)
    
    DOC.dispose()


# Remove pythonpath from current python interpreter to avoid collision
sys.path.remove(PYTHON_PATH)

# Export functions
g_exportedScripts = (
    export,
    set_template,
)