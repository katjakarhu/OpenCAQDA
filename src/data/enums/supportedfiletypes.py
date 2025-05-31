import enum


class SupportedFileTypes(enum.Enum):
    PLAIN_TEXT = ["TXT", "LOG", "XML", "SRT", "ENC", "RIS", "1", "VTT", "ASC", "PLIST", "XLOG", "ASS", "SUB", "CONF"]
    PDF = ["PDF"]

    @classmethod
    def is_plain_text(cls, file_type):
        return str(file_type).upper() in cls.PLAIN_TEXT
