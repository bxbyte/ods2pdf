# ODS to PDF

A simple LibreOffice extention for Calc that transcribe cells to PDF file's fields.


## Table of contents

- [ODS to PDF](#ods-to-pdf)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
  - [Configuration](#configuration)
    - [Template](#template)
    - [Table](#table)
  - [Usage](#usage)
  - [O2P Table Files](#o2p-table-files)
    - [Definition](#definition)
    - [Exemple](#exemple)


## Installation

Download the extension [here](https://github.com/bxbyte/ods2pdf/releases/tag/release).

Then navigate on LibreOffice to `Tools>Extension Manager...` menu, then click on the `Add` button and select your `ods2pdf.oxt` file downloaded before in the file dialog.

<u>You must also accept the Conditions & Terms of Usage (GNU 3 license).</u>


## Configuration

### Template

Go to the `Tools>Macro>Run Macro..` LibreOffice menu, then in the next dialog navigate to `My Macros>ods2pdf.oxt>main` and click on the `configure_template` macro. Now select your template in the file dialog (a .pdf file).

### Table

Go to the `Tools>Macro>Run Macro..` LibreOffice menu, then in the next dialog navigate to `My Macros>ods2pdf.oxt>main` and click on the `configure_table` macro. Now select your table in the file dialog (a .o2p file).


## Usage

Now to run the program, click on the `ODS to PDF` icon next to the `Export directly to PDF` icon on the top left side of the window.


## O2P Table Files

A file that made the connection between ODF cells and PDF fiels.

### Definition

Everything prefixed with '#' is commented to the end of the line.

Otherwise following this format :

`<cell identifier> <field name> <?format string> <?regexp>`

- A cell identifier is like A1 or WS28
- A field name is a string of non space character
- A format string is a string template that can be formated with the python string.format() method, go see https://docs.python.org/fr/3.5/library/string.htmlformatstrings
- A regexp string to match some named or not groups, recommended to test it on https://regex101.com/

### Exemple

```o2p
# Person fields

B1  Name
B2  Address
B3  CityCode
B3  CityPrefix  {code}  ^(?P<code>\d{2})
D1  Phone
D2  Mail
```

---

Copyright (c) BxByte 2023.