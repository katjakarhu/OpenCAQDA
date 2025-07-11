class CodeTree(object):
    def __init__(self, code, children=None):
        self.code = code
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.code

    def add_child(self, node):
        assert isinstance(node, CodeTree)
        self.children.append(node)
