import re
import os
import sys
from PySide2.QtWidgets import QApplication, QLabel
from enum import Enum


class ProjectBuildData:
    """
    @brief      Placeholder for makefile parsed data

    @details    This class holds data about c++ project that are needed
    to build process.
    """

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


class MakefileParser:

    line_continue_pattern = r'\\\n'
    # co robi r ?
    target_pattern = 'TARGET\\s*=\\s*(\\w*)'
    defines_pattern = 'DEFINES\\s*=\\s*(.*)'
    define_pattern = '-D(\\S*)'
    cxx_flags_pattern = 'CXXFLAGS\\s*=\\s(.*)'
    cxx_flag_pattern = '(?:^|\\s)([^\\$\\s]\\S*[^\\$\\s])'
    includes_pattern = 'INCPATH\\s*=\\s(.*)'
    include_pattern = '\\"(\\S*)\\"'
    target_type_pattern = '\\#\\s*Template:\\s*([\\w]*)'
    sources_pattern = 'SOURCES\\s*=\\s*(.*)'

    def __init__(self, project_path, verbose):
        assert isinstance(project_path, str)
        assert isinstance(verbose, bool)
        self.project_path = project_path
        self.verbose = verbose

    def transform_project(self):
        self.list_of_subprojects = self.get_subprojects()
        for subproject in self.list_of_subprojects:
            makefile_path = os.path.join('c:\\', 'Projekty', 'trunk',
                                         'win32-msvc2015_d', subproject, 'qt4',
                                         'makefile')
            if(self.verbose):
                print('Generating cmake for subproject: ', subproject)

            self.parse_file(makefile_path)

    def make_main_cmake():
        print(project_path)

    def get_subprojects(self):
        return [name for name in os.listdir(self.project_path)
                if os.path.isdir(os.path.join(self.project_path, name))]

    def parse_file(self, makefile_path, project_path):
        assert isinstance(makefile_path, str)

        if os.path.isfile(makefile_path):
            with open(makefile_path) as makefile:
                makefile_data = makefile.read()

            makefile_dir = os.path.dirname(makefile_path)

            # delete line continuations
            makefile_data = re.sub(self.line_continue_pattern, '',
                                   makefile_data)

            new_makefile = open('new_makefile', 'w')
            new_makefile.write(makefile_data)
            new_makefile.close()

            result = ProjectBuildData()
            result.set_project_path(project_path)

            # targets
            targets = re.findall(self.target_pattern, makefile_data)
            result.set_target_name(targets[0])
            if(self.verbose):
                print('list_of_targets:', result.target)

            # target type
            target_type = re.findall(self.target_type_pattern, makefile_data)
            result.set_target_type(target_type[0])
            if(self.verbose):
                print('target_type:', result.target_type)

            # defines
            defines = re.findall(self.defines_pattern, makefile_data)
            result.set_defines(re.findall(self.define_pattern, defines[0]))
            if(self.verbose):
                print('list_of_defines:', result.list_of_defines)

            # cxx flags
            cxx_flags = re.findall(self.cxx_flags_pattern, makefile_data)
            result.set_flags(re.findall(self.cxx_flag_pattern, cxx_flags[0]))
            if(self.verbose):
                print('list_of_cxx_flags:', result.list_of_flags)

            # includes
            includes = re.findall(self.includes_pattern, makefile_data)
            result.set_includes(re.findall(self.include_pattern, includes[0]))
            if(self.verbose):
                print('list_of_includes:', result.list_of_includes)

            # sources
            sources = re.findall(self.sources_pattern, makefile_data)
            list_of_sources = []
            for source in sources[0].split():
                full_path = os.path.normpath(os.path.join(makefile_dir,
                                                          source))
                full_path = os.path.relpath(full_path, subproject_path)
                list_of_sources.append(full_path)

            result.set_sources(list_of_sources)
            if(self.verbose):
                print('list_of_sources', result.list_of_sources)

            return result

    def make_cmake(self, build_data):
        assert isinstance(build_data, ProjectBuildData)

        print('Creating CMakeLists.txt')
        cmake_path = os.path.join(build_data.project_path, 'CMakeLists.txt')
        cmake = open(cmake_path, 'w')
        cmake.write('cmake_minimum_required(VERSION 3.1...3.15)\n')
        cmake.write('\n')
        cmake.write('if(${CMAKE_VERSION} VERSION_LESS 3.12)\n')
        cmake.write('    cmake_policy(VERSION ${CMAKE_MAJOR_VERSION}')
        cmake.write('.${CMAKE_MINOR_VERSION})\n')
        cmake.write('endif()\n')
        cmake.write('\n')
        cmake.write('if(MSVC)\n')
        cmake.write('    message(status \"Setting MSVC flags\")\n')
        cmake.write('    set(CMAKE_CXX_FLAGS')
        for cxx_flag in build_data.list_of_flags:
            cmake.write(' ')
            cmake.write(cxx_flag)
        for define in build_data.list_of_defines:
            cmake.write(' ')
            cmake.write('-D')
            cmake.write(define)

        cmake.write(')\n')
        cmake.write('endif()\n')
        cmake.write('set(CMAKE_EXPORT_COMPILE_COMMANDS ON)\n')
        cmake.write('message(status "** CMAKE_CXX_FLAGS: ')
        cmake.write('${CMAKE_CXX_FLAGS}")\n')
        cmake.write('set(project_sources\n')
        for source in build_data.list_of_sources:
            cmake.write('    \"')
            cmake.write(source.replace('\\', '/'))
            cmake.write('\"\n')

        cmake.write(')\n')
        if build_data.target_type == build_data.TargetType.LIBRARY:
            cmake.write('add_library(${PROJECT_NAME}\n')
            cmake.write('    ${project_sources})\n')
        elif build_data.target_type == build_data.TargetType.EXECUTABLE:
            cmake.write('add_executable(${PROJECT_NAME}\n')
            cmake.write('    ${project_sources})\n')

        cmake.write('target_include_directories(${PROJECT_NAME}\n')
        cmake.write('    PRIVATE\n')
        for include in build_data.list_of_includes:
            cmake.write('    \"')
            cmake.write(include.replace('\\', '/'))
            cmake.write('\"\n')

        cmake.write(')\n')


project_path = os.path.join('c:\\', 'Projekty', 'trunk', 'src')
makefile_parser = MakefileParser(project_path, False)
subprojects_list = makefile_parser.get_subprojects()

for subproject in subprojects_list:
    print('analyzing: ', subproject)
    makefile_path = os.path.join('c:\\', 'Projekty', 'trunk',
                                 'win32-msvc2015_d', subproject, 'qt4',
                                 'makefile')
    subproject_path = os.path.join('c:\\', 'Projekty', 'trunk', 'src',
                                   subproject)

    build_data = makefile_parser.parse_file(makefile_path, subproject_path)
    makefile_parser.make_cmake(build_data)
# print(makefile_parser.list_of_subprojects())

# app = QApplication(sys.argv)
# label = QLabel("Hello World!")
# label.show()
# sys.exit(app.exec_())
