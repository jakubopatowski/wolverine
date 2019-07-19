import builddata
import os
from io import IOBase
import logging


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

    def __add_flags(self, file, flags):
        assert isinstance(file, IOBase)

        file.write('if(MSVC)\n')
        file.write('    message(status \"Setting MSVC flags\")\n')
        file.write('    target_compile_options(${PROJECT_NAME}\n')
        file.write('      PRIVATE\n')
        for flag in flags:
            file.write('        ')
            file.write(flag)
            file.write('\n')
        file.write(')\n')
        file.write('endif()\n')
        file.write('\n')

    def __add_dir_mimic(self, file, project_path):
        assert isinstance(file, IOBase)
        assert isinstance(project_path, str)

        file.write('source_group(TREE ')
        path = os.path.join(project_path, '../..')
        path = os.path.normpath(path)
        file.write(path.replace('\\', '/'))
        file.write(' PREFIX "Source" FILES ${project_sources})\n\n')

    def __add_defines(self, file, defines):
        assert isinstance(file, IOBase)

        file.write('target_compile_definitions(${PROJECT_NAME}\n')
        file.write('  PRIVATE\n')
        for define in defines:
            file.write('    ')
            file.write(define)
            file.write('\n')
        file.write(')\n')
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
        assert isinstance(target_type, builddata.BuildData.TargetType)

        if target_type == builddata.BuildData.TargetType.LIBRARY:
            file.write('add_library(${PROJECT_NAME}\n')
            file.write('    ${project_sources})\n')
        elif target_type == builddata.BuildData.TargetType.EXECUTABLE:
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

        file.write(')\n\n')

    def __add_ccache(self, file):
        assert isinstance(file, IOBase)

        file.write('find_program(CCACHE_PROGRAM ccache)\n')
        file.write('if(CCACHE_FOUND)\n')
        file.write('  set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")\n')
        file.write('endif()\n\n')

    def __add_link_dirs(self, file, link_dirs):
        assert isinstance(file, IOBase)

        file.write('target_link_directories(${PROJECT_NAME}\n')
        file.write('  PRIVATE\n')
        for link_dir in link_dirs:
            file.write('    "')
            file.write(link_dir.replace('\\', '/'))
            file.write('"\n')

        file.write(')\n\n')

    def __add_libs(self, file, libs):
        assert isinstance(file, IOBase)
        logging.info('libs: %s', libs.exc_info)
        file.write('target_link_libraries(${PROJECT_NAME}\n')
        for lib in libs:
            file.write('    ')
            file.write(lib)
            file.write('\n')

        file.write(')\n\n')

    def __add_target_features(self, file):
        assert isinstance(file, IOBase)

        file.write('target_compile_features(${PROJECT_NAME} ')
        file.write('PRIVATE cxx_std_11)\n')
        file.write('set_target_properties(${PROJECT_NAME} ')
        file.write('PROPERTIES CXX_EXTENSIONS OFF)\n\n')

    def create_project(self, path, build_data):
        assert isinstance(path, str)
        assert isinstance(build_data, builddata.BuildData)

        if(not os.path.exists(path)):
            print('WARNING: ', path, ' does not exists!')
            return

        file = open(os.path.join(path, 'CMakeLists.txt'), 'w')

        self.__prepare_header(file)
        self.__prepare_project(file, build_data.target)
        self.__add_sources(file, build_data.list_of_sources)
        self.__add_dir_mimic(file, build_data.project_path)
        self.__add_target(file, build_data.target_type)
        self.__add_flags(file, build_data.list_of_flags)
        self.__add_defines(file, build_data.list_of_defines)
        self.__export_commands(file)
        self.__add_ccache(file)
        self.__add_target_features(file)
        self.__add_includes(file, build_data.list_of_includes)
        if build_data.list_of_lib_paths:
            self.__add_link_dirs(file, build_data.list_of_lib_paths)
        if build_data.list_of_libs:
            self.__add_libs(file, build_data.list_of_libs)

        file.close()

    def create_main_project(self, path, subprojects):
        assert isinstance(path, str)

        file = open(os.path.join(path, 'CMakeLists.txt'), 'w')
        self.__prepare_header(file)

        for project in subprojects:
            project_path = os.path.join(path, project)
            if os.path.isfile(os.path.join(project_path, 'CMakeLists.txt')):
                file.write('add_subdirectory(')
                file.write(project)
                file.write(')\n')

        file.close()
