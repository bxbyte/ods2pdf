# ODS to PDF

A simple LibreOffice extention for Calc that transcribe cells to PDF file's fields.


---

## Table of contents

- [ODS to PDF](#ods-to-pdf)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
  - [Configuration](#configuration)
    - [Template](#template)
    - [Table](#table)
  - [O2P Files](#o2p-files)

---

## Installation

Download the extension [here]().
Then 

---

## Configuration

### Template

Go to the `Tools>Macro>Run Macro..` menu, then in the next dialog navigate to `My Macros>ods2pdf.oxt>main` and click on the `configure_template` macro. Now select your template in the file dialog (a .pdf file).

### Table

Go to the `Tools>Macro>Run Macro..` menu, then in the next dialog navigate to `My Macros>ods2pdf.oxt>main` and click on the `configure_table` macro. Now select your table in the file dialog (a .o2p file).

---

## O2P Files

An ODF cells to PDF fiels table file.

Everything prefixed with '#' is commented to the end of the line.

Otherwise following this format :

`<cell identifier> <field name> <?format string> <?regexp>`

- A cell identifier is like A1 or WS28
- A field name is a string of non space character
- A format string is a string template that can be formated with the python string.format() method, go see https://docs.python.org/fr/3.5/library/string.htmlformatstrings
- A regexp string to match some named or not groups, recommended to test it on https://regex101.com/



---

Copyright (c) BxByte 2023.