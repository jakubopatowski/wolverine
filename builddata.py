from enum import Enum


class BuildData:
    """
    @brief      Placeholder for makefile parsed data

    @details    This class holds data about c++ project that are needed
    to build process.
    """

    def __init__(self):
        "docstring"
        self.makefile_path = None
        self.project_path = None
        self.target = None
        self.target_type = None
        self.list_of_defines = None
        self.list_of_flags = None
        self.list_of_includes = None
        self.list_of_sources = None
        self.list_of_libs = None
        self.list_of_lib_paths = None

    # path to makefile
    def set_makefile_path(self, path):
        self.makefile_path = path

    # path to project
    def set_project_path(self, path):
        self.project_path = path

    # target name
    def set_target_name(self, target):
        self.target = target

    # target type
    class TargetType(Enum):
        EXECUTABLE = 1
        LIBRARY = 2
        HEADER_LIBRARY = 3

    def set_target_type(self, target_type):
        if target_type == 'app':
            self.target_type = self.TargetType.EXECUTABLE
        elif target_type == 'lib':
            self.target_type = self.TargetType.LIBRARY

    # defines
    def set_defines(self, defines):
        self.list_of_defines = defines

    # flags
    def set_flags(self, flags):
        self.list_of_flags = flags

    # includes
    def set_includes(self, includes):
        self.list_of_includes = includes

    # sources
    def set_sources(self, sources):
        self.list_of_sources = sources

    def set_libs(self, libs):
        self.list_of_libs = libs

    def set_lib_paths(self, lib_paths):
        self.list_of_lib_paths = lib_paths
