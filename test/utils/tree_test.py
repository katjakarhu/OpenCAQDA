import unittest
from ocaqda.utils.tree import CodeTree

class TreeTest(unittest.TestCase):
    def test_tree_init(self):
        t = CodeTree(identifier=1, name='root')
        self.assertEqual(t.identifier, 1)
        self.assertEqual(t.name, 'root')
        self.assertEqual(t.children, [])

    def test_add_child(self):
        parent = CodeTree(identifier=1, name='parent')
        child = CodeTree(identifier=2, name='child')
        parent.add_child(child)
        self.assertIn(child, parent.children)
        self.assertEqual(len(parent.children), 1)

    def test_repr(self):
        t = CodeTree(name='test')
        self.assertEqual(repr(t), 'test')

    def test_add_child_type(self):
        parent = CodeTree()
        with self.assertRaises(AssertionError):
            parent.add_child('not_a_tree')

if __name__ == '__main__':
    unittest.main() 