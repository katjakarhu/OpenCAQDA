# OpenCAQDA - Open Source Computer-Assisted Qualitative Data Analysis Tool

WORK-IN-PROGRESS: Use at your own risk! 

If you would like to participate, feel free to tackle unassigned issues! 

OpenCAQDA is an easy to use open source desktop application for qualitative data analysis. The goal is to provide the user with high visibility and control over the coding process, and therefore no AI feature are planned. 

You can:

- Code plain text and PDF files


## Features

Create research projects, that contain a set of files and codes.

Drag and drop coding: select text and drag code over it (left mouse button=.
Drag and drop code hierarchy: with right button, drag and drop codes over each other to create a hierarchy (TODO: save relationship to database, now this resets everytime you restart the application)

Quick filter codes: find the relevant codes easily


### Supported file formats:

- Plain text (*.txt)
- PDF (*.pdf)

## Technical details

The data is stored in an SQLite database locally (TODO: add possibility for user the change the URL to database for shared database use)


### Running the application

You will need to have Python 3 installed.

Install requirements:

`pip install -r requirements.txt`

Run app

`python main.py`


## Planned features

### Mandatory

- Define hierarchies and relationships between codes
    - Save drag and drop code relationships to database
    - Relationships can have labels
    - You can define parent-child hierarchies with codes that you can use for
example in defining themes, sub-themes and categories.
- Better user flow when:
    - Settings file does not exist
    - Database does not exist
- Coding functionality
    - Drag and drop coding: done for text files
    - Uncoding: TODO
    - Managing codes: TODO
- Configuration
    - User configuration: preliminary version exists
    - Database configuration: preliminary version exists 
- Note/memo functionality
    - For codes
    - For files
    - For text selection?
    - For whole project?
- More unit tests

### High priority:

- Text search within multiple files
- Multi-user projects (with shared database)
    - Editable DB settings
    - Storing DB credentials
    - Other than SQLite support (MySQL, Postgres, etc.)
- Code relationship visualization and editing

### Nice to have:

- Importing and exporting:
    - Codes
    - Notes/memos
    - Projects
- Activity log:
    - Who did what
    - Can be used as a basis for reporting your analysis process
- Case study features:
    - Cross case analysis view: compare the codes in cases

### Maybe some day

- Codes to word cloud
- Notes to word cloud
- Sentiment analysis
- Investigate other data analysis possibilities with Python that could be added here
- Image coding support (e.g. image to text, or other)
- Video file coding support
- CSV and Excel file coding (can be circumvented by converting to PDF)
- HTML file coding (can be circumvented by converting to PDF)
- DOCX coding (can be circumvented by converting to PDF)
- RTF file coding (can be circumvented by converting to PDF)
