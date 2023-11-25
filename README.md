# ODS to PDF

A simple LibreOffice embeded macro for Calc that transcribe cells to PDF file's fields.

## Table of Contents
- [ODS to PDF](#ods-to-pdf)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Export](#export)
    - [Set Template](#set-template)
  - [O2P YAML Files](#o2p-yaml-files)
    - [Definition](#definition)
    - [Exemple](#exemple)

---

## Installation

Download the repo with `git clone git@github.com:bxbyte/ods2pdf.git`

Then add your pdf template as template.pdf in `src/Config/`, your LibreOffice Calc sheet in the main folder as `template_src.ods`.

Now execute the makefile with `make` and your LibreOffice Calc sheet shoud be `template.ods`.

## Usage

### Export

Go to the `Tools>Macro>Run Macro..` LibreOffice menu, then in the next dialog navigate to `template.ods>main` and click on the `export` macro. Now select the output file in the file dialog (a .pdf file) and wait for the export.

### Set Template

Go to the `Tools>Macro>Run Macro..` LibreOffice menu, then in the next dialog navigate to `template.ods>main` and click on the `set_template` macro. Now select your template in the file dialog (a .pdf file).

---

## O2P YAML Files

A file that made the connection between ODF cells and PDF fiels.

### Definition

```yml
page_name:
    fied_name: cell name
    # Or
    field_name:
        cell: cell name
        format: format string
        regex: regex string
```

- A cell identifier is like A1 or WS28
- A field name is a string of non empty character
- A format string is a string template that can be formated with the python string.format() method, 
  go see https://docs.python.org/fr/3.5/library/string.htmlformatstrings. The formated was extented and now support :
    - 'u' Specifier for convertion to uppercase.
    - 'l' Specifier for convertion to lowercase.
    - 't' Specifier for convertion to title.
- A regexp string to match some named or not groups, recommended to test it on https://regex101.com/

### Exemple

```yml
# Person fields
"person 1":
    Address: B1
    CityCode: B3
    CityPrefix:
        cell: B3
        format: "{code}"
        regex: ^(?P<code>\d{2})
    Phone: D1
    Mail: D2
```

---

Copyright (c) BxByte 2023.