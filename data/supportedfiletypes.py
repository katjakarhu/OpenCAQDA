import enum
from csv import excel


class supportedfiletypes(enum.Enum):
    PLAIN_TEXT = ["TXT", "LOG", "XML", "SRT", "ENC", "RIS", "1", "VTT", "ASC", "PLIST", "XLOG", "ASS", "SUB", "CONF"]
    PDF = ["PDF"]
    HTML = ["HTML", "HTM"]
    MARKDDOWN = ["MD"]
    CSV = ["CSV"]

    @classmethod
    def is_plain_text(cls, file_type):
        pass

