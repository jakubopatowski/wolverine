import unittest
import io
from cmakecreator import CMakeCreator
from targettype import TargetType
from librarytype import LibraryType


class TestCmakecreator(unittest.TestCase):

    def setUp(self):
        self.cmake = CMakeCreator()

    def test_add_target(self):
        f1 = io.StringIO()
        self.cmake.add_target(f1, TargetType.EXECUTABLE)
        self.assertEqual(f1.getvalue(),
                         'add_executable(${PROJECT_NAME} "")\n\n')
        f2 = io.StringIO()
        self.cmake.add_target(f2, TargetType.HEADER_LIBRARY)
        self.assertEqual(f2.getvalue(),
                         'add_library(${PROJECT_NAME} "")\n\n')
        f3 = io.StringIO()
        self.cmake.add_target(f3, TargetType.LIBRARY)
        self.assertEqual(f3.getvalue(),
                         'add_library(${PROJECT_NAME} "")\n\n')
        f4 = io.StringIO()
        self.cmake.add_target(f4, TargetType.UNKNOWN)
        self.assertEqual(f4.getvalue(), '')
        f5 = io.StringIO()
        self.cmake.add_target(f5, TargetType.EXECUTABLE, LibraryType.SHARED)
        self.assertEqual(f5.getvalue(),
                         'add_executable(${PROJECT_NAME} "")\n\n')
        f6 = io.StringIO()
        self.cmake.add_target(f6, TargetType.EXECUTABLE, LibraryType.STATIC)
        self.assertEqual(f6.getvalue(),
                         'add_executable(${PROJECT_NAME} "")\n\n')
        f7 = io.StringIO()
        self.cmake.add_target(f7, TargetType.EXECUTABLE, LibraryType.UNKNOWN)
        self.assertEqual(f7.getvalue(),
                         'add_executable(${PROJECT_NAME} "")\n\n')
        f8 = io.StringIO()
        self.cmake.add_target(f8, TargetType.LIBRARY, LibraryType.SHARED)
        self.assertEqual(f8.getvalue(),
                         'add_library(${PROJECT_NAME} SHARED "")\n\n')
        f9 = io.StringIO()
        self.cmake.add_target(f9, TargetType.LIBRARY, LibraryType.STATIC)
        self.assertEqual(f9.getvalue(),
                         'add_library(${PROJECT_NAME} STATIC "")\n\n')



if __name__ == '__main__':
    unittest.main()
