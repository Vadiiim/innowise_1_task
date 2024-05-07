import unittest
from main import DataBase
class TestDB(unittest.TestCase):
    def setUp(self) -> None:
        self.db=DataBase('TASK1','postgres','1')
    