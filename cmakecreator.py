import builddata
import os
from io import IOBase


class CMakeCreator:
    def __prepare_header(self, file):
        assert isinstance(file, IOBase)

        file.write('cmake_minimum_required(VERSION 3.1...3.15)\n')
        file.write('\n')
        file.write('if(${CMAKE_VERSION} VERSION_LESS 3.12)\n')
        file.write('    cmake_policy(VERSION ${CMAKE_MAJOR_VERSION}')
        file.write('.${CMAKE_MINOR_VERSION})\n')
        file.write('endif()\n')
        file.write('\n')

    def __prepare_project(self, file, project_name):
        assert isinstance(file, IOBase)
        assert isinstance(project_name, str)

        file.write('project(')
        file.write(project_name)
        file.write(' VERSION 1.0 LANGUAGES CXX)\n')

    def __add_cxx_flags(self, file, cxx_flags):
        assert isinstance(file, IOBase)

        file.write('if(MSVC)\n')
        file.write('    message(status \"Setting MSVC flags\")\n')
        file.write('    set(CMAKE_CXX_FLAGS\n')
        for cxx_flag in cxx_flags:
            file.write('        ')
            file.write(cxx_flag)
            file.write('\n')
        file.write(')\n')
        file.write('endif()')
        file.write('\n')

    def __add_defines(self, file, defines):
        assert isinstance(file, IOBase)

        file.write('add_definitions(\n')
        for define in defines:
            file.write('    -D')
            file.write(define)
            file.write('\n')
        file.write('\n')

    def __export_commands(self, file):
        assert isinstance(file, IOBase)

        file.write('set(CMAKE_EXPORT_COMPILE_COMMANDS ON)\n\n')
        file.write('\n')

    def __add_sources(self, file, sources):
        assert isinstance(file, IOBase)

        file.write('set(project_sources\n')
        for source in sources:
            file.write('    \"')
            file.write(source.replace('\\', '/'))
            file.write('\"\n')
        file.write(')\n')
        file.write('\n')

    def __add_target(self, file, target_type):
        assert isinstance(file, IOBase)
        assert isinstance(target_type, builddata.ProjectBuildData.TargetType)

        if target_type == builddata.ProjectBuildData.TargetType.LIBRARY:
            file.write('add_library(${PROJECT_NAME}\n')
            file.write('    ${project_sources})\n')
        elif target_type == builddata.ProjectBuildData.TargetType.EXECUTABLE:
            file.write('add_executable(${PROJECT_NAME}\n')
            file.write('    ${project_sources})\n')
        file.write('\n')

    def __add_includes(self, file, includes):
        assert isinstance(file, IOBase)

        file.write('target_include_directories(${PROJECT_NAME}\n')
        file.write('    PRIVATE\n')
        for include in includes:
            file.write('    \"')
            file.write(include.replace('\\', '/'))
            file.write('\"\n')

        file.make.write(')\n')

    def create_project(self, path, build_data):
        assert isinstance(path, str)
        assert isinstance(build_data, builddata.BuildData)

        file = open(os.path.join(path, 'CMakeLists.txt'), 'w')
        self.__prepare_header(file)
        self.__prepare_project(file, build_data.target)
        self.__add_cxx_flags(file, build_data.list_of_flags)
        self.__add_defines(file, build_data.list_of_defines)
        self.__export_commands(file)
        self.__add_target(file, build_data.target_type)

        file.close()
