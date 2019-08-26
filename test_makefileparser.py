import unittest
import makefileparser


class TestMakefileParser(unittest.TestCase):

    def setUp(self):
        self.makefile_path = 'makefile'
        self.project_path = '.'
        self.false_makefile_path = './saoduifojasdf/makefile'
        self.parser = makefileparser.MakefileParser()

    def test___src_rel_path(self):
        self.assertEqual(self.parser.change_rel_path(
            '/home/jopa/Projekty/wolverine/', '/home/jopa/Projekty/banshee/',
            '../banshee/main.cpp'), 'main.cpp')
        self.assertEqual(self.parser.change_rel_path(
            '/home/jopa/Projekty/banshee/', '/home/jopa/Projekty/barracuda/',
            '../wolverine/main.cpp'), '../wolverine/main.cpp')
        self.assertEqual(self.parser.change_rel_path(
            '/home/jopa/Projekty/banshee/makedir/',
            '/home/jopa/Projekty/barracuda/', '../../main.cpp'), '../main.cpp')

    def test_parse_file_none(self):
        self.assertEqual(self.parser.parse_file(self.false_makefile_path,
                                                self.project_path), None)

    def test_parse_file_ok(self):
        self.assertIsNot(self.parser.parse_file(self.makefile_path,
                                                self.project_path),
                         None)


if __name__ == '__main__':
    unittest.main()
