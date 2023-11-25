from os import chdir
from os.path import isfile
from glob import glob
from sys import argv
from io import BytesIO
from xml.etree import ElementTree as ET
from zipfile import ZipFile


NAMESPACE = "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
ET.register_namespace("", NAMESPACE)


with ZipFile(argv[2], 'r') as zin:
    with ZipFile(argv[3], 'w') as zout:
        for item in zin.infolist():
            if item.filename == "META-INF/manifest.xml": # Get actual manifest
                xml = ET.parse(BytesIO(zin.read(item.filename)))
            else:
                zout.writestr(item, zin.read(item.filename))
                                
        def push_file_entry(full_path: str, media_type = ""):
            file_entry = ET.SubElement(xml.getroot(), "file-entry")
            file_entry.attrib["full-path"] = full_path
            file_entry.attrib["media-type"] = media_type

        # Inject files
        chdir(argv[1])
        for path in glob("**", recursive=True):
            if isfile(path):
                push_file_entry(path)
                with open(path, 'rb') as file:
                    with zout.open(path, 'w') as zfile:
                        zfile.write(file.read())
        
        # Add scripts entrie
        push_file_entry("Scripts", "application/binary")
        push_file_entry("Scripts/python", "application/binary")
        push_file_entry("Scripts/python/pythonpath", "application/binary")
        
        # Inject new manifest
        with zout.open("META-INF/manifest.xml", 'w') as manifest_file:
            xml.write(manifest_file)