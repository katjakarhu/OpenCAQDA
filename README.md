# OpenCAQDA - Open Source Computer-Assisted Qualitative Data Analysis Tool

[![Python application](https://github.com/katjakarhu/OpenCAQDA/actions/workflows/python-app.yml/badge.svg)](https://github.com/katjakarhu/OpenCAQDA/actions/workflows/python-app.yml)

WORK-IN-PROGRESS: Use at your own risk! See open issues for known defects and missing
features: https://github.com/katjakarhu/OpenCAQDA/issues

If you would like to participate, feel free to tackle unassigned issues!

## Background

OpenCAQDA is an easy-to-use open source desktop application for qualitative data analysis. The goal is to provide the
user with visibility, traceability, and control over the coding process.


<img width="1000" alt="Screenshot" src="https://raw.githubusercontent.com/katjakarhu/OpenCAQDA/refs/heads/main/screenshot.png" />

## Features

Supported file formats are plain text, MD, PDF and HTML files

Create research projects, that contain a set of files and codes.

Drag and drop coding: select text and drag code over it (left mouse button).

Drag and drop code hierarchy: with right button, drag and drop codes over each other to create a hierarchy (TODO: save
relationship to database, now this resets everytime you restart the application)

Quick filter codes: find the relevant codes easily

Searching within one or multiple files

You can attach memos to codes or files in the "Memos" tab

### Supported file formats:

- Plain text (*.txt)
- PDF (*.pdf)
- HTML (*.html)
- Markdown (*.md)

## Technical details

The data is stored in an SQLite database locally (TODO: add possibility for user the change the URL to database for
shared database use)

### Running the application

You will need to have Python 3 installed.

Go to project directory.Set the application directory to Python path:

`export PYTHONPATH=$PYTHONPATH:.`

Install requirements:

`pip install -r requirements.txt`

Run app:

`python3 ocaqda/main.py`

### Architecture

- **database/**       contains classes related to database connectivity
- **data/**           contains enums, entities (models.py)
- **services/**       handles fetching and saving data, call these methods from the UI
- **ui/**             contains the views
- **utils/**          contains useful methods that can be used anywhere

## Planned features

See also "Issues" for open issues.

### Mandatory

- Code relationships: visualization and editing
- Coding functionality
    - Managing codes (delete, rename)
- Importing and exporting:
    - Codes
    - Memos
    - Projects

### High priority:

- Better user flow when:
    - Settings file does not exist
    - Database does not exist
- App configuration
    - User configuration: preliminary version exists
    - Database configuration: preliminary version exists
- More unit tests
- Multi-user projects (with shared database)
    - Editable DB settings
    - Storing DB credentials
    - Other than SQLite support (MySQL, Postgres, etc.)

### Nice to have:

- Activity log:
    - Who did what (added memos, files, codes, edited codes, memos)
    - Can be used for reporting your analysis process
- Case study features:
    - Cross case analysis view: compare the codes in cases

### Maybe some day

- Word cloud
- Sentiment analysis
- Investigate other data analysis possibilities with Python
- Image coding support (e.g. image to text, or other)
- Video file coding support
- CSV and Excel file coding (can be circumvented by converting to PDF or txt)
- DOCX coding (can be circumvented by converting to PDF or txt)
- RTF file coding (can be circumvented by converting to PDF ot txt)
- Many projects open at the same time
