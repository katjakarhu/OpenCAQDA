import unittest
from ocaqda.utils.singleton import Singleton

class DummySingleton(metaclass=Singleton):
    pass

class SingletonTest(unittest.TestCase):
    def test_singleton_instance(self):
        a = DummySingleton()
        b = DummySingleton()
        self.assertIs(a, b)

    def test_singleton_type(self):
        self.assertTrue(isinstance(DummySingleton(), DummySingleton))

if __name__ == '__main__':
    unittest.main() 