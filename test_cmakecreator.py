import unittest
import io
from cmakecreator import CMakeCreator
from targettype import TargetType


class TestCmakecreator(unittest.TestCase):

    def setUp(self):
        self.cmake = CMakeCreator()

    def test_add_target(self):
        f = io.StringIO()
        target_type = TargetType.EXECUTABLE
        self.cmake.add_target(f, target_type)
        self.assertEqual(f.getvalue(),
                         'add_executable(${PROJECT_NAME} "")\n\n')
        target_type = TargetType.HEADER_LIBRARY


if __name__ == '__main__':
    unittest.main()
