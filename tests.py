import unittest
from main import DataBase, read_json_files

class TestDatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.database = DataBase('TASK1', 'postgres', '1', 'localhost', '5432')

    def test_creating_table(self):
        self.assertIsNone(self.database.creating_table())

    def test_filling_table(self):
        students = read_json_files('./jsonfiles/students.json')
        rooms = read_json_files('./jsonfiles/rooms.json')
        self.assertIsNone(self.database.filling_table(students, rooms))

    def test_make_queries(self):
        self.assertIsNone(self.database.make_queries('./quaeries', 'xml'))

if __name__ == '__main__':
    unittest.main()
