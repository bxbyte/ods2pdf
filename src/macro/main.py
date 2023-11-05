import sys
import os.path as path

from shutil import copyfile
from re import search
from base64 import b64encode, b64decode
from io import BytesIO

# Try to import hidden module
try:
    module_dir = path.join(path.dirname(__file__), "pythonpath")
    sys.path.insert(0, sys.path.pop(sys.path.index(module_dir)))
except Exception:
    ...

from dialog import msgbox, filebox
from tools import generate_from_fields, load_table
from config import load_config, ENCODING, CONFIG_PATH
from formatter import FORMATTER


class ODS2PDFError(Exception):
    ...


### Here's the LibreOffice callable functions


def export_fields(*args):
    """Export configured cells into the configured template's PDF file fields.
    """
    global XSCRIPTCONTEXT
    
    with load_config() as config:
        if not config["template_b64"]:
            raise ODS2PDFError("no pdf template configured !")
        
        if not config["table"]:
            raise ODS2PDFError("no o2p table configured !")
        
        res_path = filebox(("PDF File (.pdf)", "*.pdf"), mode=10)
        if not res_path:
            return
        
        fields_data = {}
        sheet = XSCRIPTCONTEXT.getDocument().getCurrentController().getActiveSheet()
        for cell_id, field, *options in config["table"]:
            if options:
                format_str = options[0]
                regexp = options[1] if len(options) == 2 else r".*"
                search_res = search(regexp, sheet.getCellRangeByName(cell_id).getString())
                try:
                    fields_data[field] = FORMATTER.format(format_str, *search_res.groups(), **search_res.groupdict())
                except (KeyError, IndexError, AttributeError):
                    fields_data[field] = ""
            else:
                fields_data[field] = sheet.getCellRangeByName(cell_id).getString()
        
        generate_from_fields(
            BytesIO(b64decode(config["template_b64"].encode(ENCODING))),
            res_path, 
            fields_data
        )
        
        msgbox("Done.", "ODS2PDF")


def configure_template(*args):
    """ Encode a PDF template in the configuration file.
    """
    with load_config() as config:
        template_b64 = filebox(
            ("PDF Files (.pdf)", "*.pdf"),
            mode=11
        )
        if not template_b64:
            return
        
        with open(template_b64, "rb") as file:
            config["template_b64"] = b64encode(file.read()).decode(ENCODING)

        msgbox("Template configured.", "ODS2PDF")


def configure_table(*args):
    """ Register a tables into the configuration file.
    """
    with load_config() as config:
        table_path = filebox(
            ("ODS2PDF Files (.o2p)", "*.o2p")
        )
        if not table_path:
            return
        
        config["table"] = tuple(load_table(table_path))

        msgbox("Table configured.", "ODS2PDF")


def import_configuration(*args):
    """Inport a o2p.json file.
    """
    config_path = filebox(("JSON Configuration file (.json)", "*.json"), mode=10)
    if not config_path:
        return
    
    copyfile(config_path, CONFIG_PATH)
    msgbox("Configuration imported.")
    

### Exported python functions
g_exportedScripts = (
    export_fields,
    import_configuration,
    configure_template,
    configure_table
)