from __future__ import annotations
import typing

from uno import fileUrlToSystemPath
from const import CTX, SM


def create_instance(name: str, with_context: bool = False) -> typing.Any:
    """Create a LibreOffice instance.

    Args:
        name (str): classified name of instance
        with_context (bool, optional): Create instance with current context. Defaults to False.

    Returns:
        typing.Any: Instance from LibreOffice.
    """
    if with_context:
        instance = SM.createInstanceWithContext(name, CTX)
    else:
        instance = SM.createInstance(name)
    return instance


def msgbox(message: str, title='LibreOffice', buttons: int = 1 | 0x10000, type_msg = 'infobox') -> int:
    """Create a simple message dialog.

    See more [here](https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1awt_1_1XMessageBoxFactory.html)

    Args:
        message (str): The message.
        title (str, optional): The window title. Defaults to 'LibreOffice'.
        buttons (int, optional): The [combination of buttons](https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1awt_1_1MessageBoxButtons.html) displayed. Defaults to 1 for an OK_BUTTON.
        type_msg (str, optional): The [type of message box](https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1awt.html#ad249d76933bdf54c35f4eaf51a5b7965). Defaults to 'infobox'.

    Returns:
        int: The [message box result](https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1awt_1_1MessageBoxResults.html).
    """    
    tk = create_instance('com.sun.star.awt.Toolkit')
    parent = tk.getDesktopWindow()
    mb = tk.createMessageBox(parent, type_msg, buttons, title, str(message))
    return mb.execute()


def filebox(*files_ext: tuple[tuple[str, str]], path : str = None, mode: int = 0) -> str | None:
    """Create a file dialog and return the result.

    Args:
        path (str, optional): Default dialog folder path. Defaults to None.
        mode (int, optional): The [type of file dialog](https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1ui_1_1dialogs_1_1TemplateDescription.html). Defaults to 0.

    Returns:
        str | None: OS path to the selected file. If no file where selected return None.
    """    """"""
    filepicker = create_instance("com.sun.star.ui.dialogs.OfficeFilePicker")
    if path:
        filepicker.setDisplayDirectory(path)
    for desc, ext in files_ext:
        filepicker.appendFilter(desc, ext)
    filepicker.initialize((mode,))
    if filepicker.execute():
        return fileUrlToSystemPath(filepicker.getFiles()[0])