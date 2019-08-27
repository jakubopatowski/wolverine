import os
import unittest
import tools
import re


class TestTools(unittest.TestCase):

    def test_change_rel_path(self):
        self.assertEqual(
            tools.change_rel_path(
                '/home/jopa/Projekty/wolverine/',
                '/home/jopa/Projekty/banshee/',
                '../banshee/main.cpp'), 'main.cpp')
        self.assertEqual(
            tools.change_rel_path(
                '/home/jopa/Projekty/banshee/',
                '/home/jopa/Projekty/barracuda/',
                '../wolverine/main.cpp'),
            os.path.join('..', 'wolverine', 'main.cpp'))
        self.assertEqual(
            tools.change_rel_path(
                '/home/jopa/Projekty/banshee/makedir/',
                '/home/jopa/Projekty/barracuda/',
                '../../main.cpp'),
            os.path.join('..', 'main.cpp'))

    def test_get_files(self):
        exclude = ['.ccls-cache']
        files = tools.get_files(
            'c:/Projekty/trunk/src/radosc',
            re.compile(r'\w*.(h|hpp)$'),
            exclude)
        print(files)


if __name__ == '__main__':
    unittest.main()
