import unittest
import makefileparser


class TestMakefileParser(unittest.TestCase):

    def setUp(self):
        self.makefile_path = 'makefile'
        self.project_path = '.'
        self.false_makefile_path = './saoduifojasdf/makefile'
        self.parser = makefileparser.MakefileParser()

    def test_parse_file_none(self):
        self.assertEqual(self.parser.parse_file(self.false_makefile_path,
                                                self.project_path), None)

    def test_parse_file_ok(self):
        self.assertIsNot(self.parser.parse_file(self.makefile_path,
                                                self.project_path),
                         None)


if __name__ == '__main__':
    unittest.main()
