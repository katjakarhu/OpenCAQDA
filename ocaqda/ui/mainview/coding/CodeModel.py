from PySide6.QtCore import QAbstractItemModel


class CodeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(CodeModel, self).__init__(parent)

