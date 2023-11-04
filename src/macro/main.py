import re
import typing

import sys
import os.path as path

from re import search
from json import dump, load
from contextlib import contextmanager

# Try to import hidden module
try:
    module_dir = path.join(path.dirname(__file__), "pythonpath")
    sys.path.insert(0, sys.path.pop(sys.path.index(module_dir)))
except Exception:
    ...

import dialog
import tools


CONFIG_PATH = f"{dialog.CONFIG_DIR_PATH}/o2p.json"


class CurrentConfig(typing.TypedDict):
    template_path: str
    table: tuple[tuple[str, str, str, str], ...]


class ODS2PDFError(Exception):
    ...


@contextmanager
def load_config() -> typing.Iterator[CurrentConfig]:
    data = dict(
        template_path="",
        table={}
    )
    if path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as file:
            try:
                data.update(load(file))
            except ValueError:
                ...
    try:
        try:
            yield data
        except Exception as error:
            dialog.msgbox(f"Error: {error}", f"ODS2PDF : {error.__class__.__name__}", 5 | 0x20000, "errorbox")
    finally:
        with open(CONFIG_PATH, 'w') as file:
            file.seek(0)
            dump(data, file, indent=4)
            file.truncate()


### Here's the LibreOffice callable functions


def export_fields_dialog(*args):
    """Export configured cells into the cnfigured template's PDF file fields.
    """
    global XSCRIPTCONTEXT
    
    with load_config() as config:
        if not config["template_path"]:
            raise ODS2PDFError("no pdf template configured !")
        
        if not config["table"]:
            raise ODS2PDFError("no pdf o2p table configured !")
        
        res_path = dialog.filebox(("PDF File (.pdf)", "*.pdf"), mode=10)
        if not res_path:
            return
        
        fields_data = {}
        sheet = XSCRIPTCONTEXT.getDocument().CurrentController.ActiveSheet
        for cell_id, field, *options in config["table"]:
            if options:
                format_str = options[0]
                regexp = options[1] if len(options) == 2 else r".*"
                search_res = search(regexp, sheet[cell_id].getString())
                if not search_res:
                    raise ODS2PDFError(f"No match found for {cell_id} with regexp: {regexp}")
                fields_data[field] = format_str.format(*search_res.groups(), **search_res.groupdict())
                    
            else:
                fields_data[field] = sheet[cell_id].getString()
        
        dialog.msgbox(f"{fields_data}.", "ODS2PDF")
        
        tools.generate_from_fields(config["template_path"], res_path, fields_data)
        dialog.msgbox("Done.", "ODS2PDF")


def configure_template(*args):
    """ Setup template configuration for ODS2PDF.
    """
    with load_config() as config:
        template_path = dialog.filebox(
            ("PDF Files (.pdf)", "*.pdf"),
            mode=11
        )
        if template_path:
            config["template_path"] = template_path
        else:
            raise ODS2PDFError("no template selected !")

        dialog.msgbox("Template configured.", "ODS2PDF")


def configure_table(*args):
    """ Setup table configuration for ODS2PDF.
    """
    with load_config() as config:
        table_path = dialog.filebox(
            ("ODS2PDF Files (.o2p)", "*.o2p")
        )
        if table_path:
            config["table"] = tuple(tools.load_table(table_path))
        else:
            raise ODS2PDFError("no o2p table selected !")

        dialog.msgbox("Table configured.", "ODS2PDF")


### Exported python functions
g_exportedScripts = (
    export_fields_dialog,
    configure_template,
    configure_table
)