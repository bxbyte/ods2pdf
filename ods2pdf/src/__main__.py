# import typing

# from pypdf import PdfReader, PdfWriter
# from re import sub


# COMMENT_DECORATOR = "#"


# def get_table(filepath: str) -> typing.Generator[tuple[str, str], None, None]:
#     """Read and extract pairs of ods to pdf fields keys from .o2f file

#     Args:
#         filepath (str): File path to a .o2f file.

#     Yields:
#         Iterator[typing.Generator[tuple[str, str], None, None]]: Pairs of ods to pdf fields keys, like ["A1", "Name"].
#     """
#     with open(filepath, 'r') as file:
#         for line in file.readlines():
#             line = sub(r"\s+\t", ' ', line) # Replace exceding space with single one
#             line = sub(r"#.*$|\n|\r", '', line) # Remove comments & line espace char
            
#             if line.strip():
#                 yield line.split(' ', 1)


# def generate(filepath: str, data: dict[str, str]) -> PdfWriter:
#     """Create a PdfWritre filled with data.

#     Args:
#         filepath (str): File path to pdf template.
#         data (dict[str, str]): Pair of fields key-value.

#     Returns:
#         PdfWriter: Filled PdfWriter.
#     """
#     reader = PdfReader("/home/bixbyte/Projects/ods2pdf/test/gevasco vierge.pdf")
#     writer = PdfWriter()
    
#     for i, page in enumerate(reader.pages):
#         writer.add_page(page)
#         writer.update_page_form_field_values(
#             writer.pages[i], data
#         )

#     return writer


# del typing

# print(dict(get_table("./fields.o2p")))

import uno
import unohelper
from com.sun.star.task import XJobExecutor

class TestButton( unohelper.Base, XJobExecutor ):
    def __init__( self, ctx ):
        self.ctx = ctx
 
    def trigger( self, args ):
        desktop = self.ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", self.ctx )
 
        doc = desktop.getCurrentComponent()
        print("Pressed Button!")
        
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    TestButton,
    "com.platformedia.libreoffice.extensions.mdda_fn.TestButton",
    ("com.sun.star.task.Job",),
)


if __name__ == "__main__":
    import os
 
    # Start OpenOffice.org, listen for connections and open testing document
    #os.system( "/etc/openoffice.org-1.9/program/soffice '-accept=socket,host=localhost,port=2002;urp;' -writer ./WaveletTest.odt &" )
    os.system( "/usr/bin/oocalc '-accept=socket,host=localhost,port=2002;urp;' ./Test-mdda-fns.ods &" )
 
    # Get local context info
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
 
    ctx = None
 
    # Wait until the OO.o starts and connection is established
    while ctx == None:
        try:
            ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        except:
            pass
 
    print("About to do TestButton")
 
    # Trigger our job
    testjob = TestButton( ctx )
    testjob.trigger( () )

    print("Done TestButton")