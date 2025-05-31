# OpenCAQDA

OpenCAQDA is an easy to use desktop application for qualitative data analysis.  
The goal is to provide high visibility and control over the coding process for the user.

You can:

- Code plain text and PDF files
- Define hierarchies and relationships between codes
    - Themes, sub-themes, categories
    - Relationships can have labels
-

## Features

Create research projects, that contain a set of files and codes.

Drag and drop coding.

You can define parent-child hierarchies with codes that you can use for
example in defining themes, sub-themes and categories.

Quick filter codes.

### Supported file formats:

- Plain text (*.txt)
- PDF (*.pdf)

## Technical details

The data is stored in an SQLite database locally.

## Planned features

### Mandatory

- Coding functionality
- Configuration
- User functionality
- Note functionality
    - For files
    - For codes
-

### High priority:

- Multi-user projects (with shared database)
    - Editable DB settings
    - Storing DB credentials
    - Other than SQLite support (MySQL, Postgres, etc)
- Text search within multiple files
- Code relationship visualization and editing

### Nice to have:

- Importing and exporting:
    - Codes
    - Notes
    - Projects
- Activity log:
    - Who did what
    - Can be used as a basis for reporting your analysis process

### Maybe some day

- Codes to word cloud
- Notes to word cloud
- Video file coding support
- HTML file coding (can be circumvented by converting to PDF)
- DOCX coding (can be circumvented by converting to PDF))
- CSV and Excel file coding
- Image coding support (e.g. image to text, or other)
- RTF file coding
