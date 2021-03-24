import builddata
import os
from targettype import TargetType
from librarytype import LibraryType
from io import IOBase


class CMakeCreator:
    def __init__(self, type, bit):
        self.build_type = type.lower()
        self.bit_type = bit
        if (bit != '32' and bit != '64'):
            print('Podana architektóra projektu różna od 32 i 64!\n')
        if (type != 'debug' and type != 'release'):
            print('Podany typ budowy różny od "debug" i "release"!\n')

    def __prepare_header(self, file):
        assert isinstance(file, IOBase)

        file.write('cmake_minimum_required(VERSION 3.14)\n\n')

    def __prepare_project(self, file, project_name):
        assert isinstance(file, IOBase)
        assert isinstance(project_name, str)

        file.write('project(')
        file.write(project_name)
        file.write(' VERSION 1.0 LANGUAGES C CXX)\n')
        file.write('message(STATUS "${PROJECT_NAME}")\n\n')

    def __add_flags(self, file, flags):
        assert isinstance(file, IOBase)

        file.write('if(MSVC)\n')
        file.write('    target_compile_options(${PROJECT_NAME}\n')
        file.write('      PRIVATE\n')
        for flag in flags:
            file.write('        ')
            file.write(flag.replace('\\', '/'))
            file.write('\n')
        file.write(')\n')
        file.write('endif()\n')
        file.write('\n')

    def __add_dir_mimic(self, file, project_path):
        assert isinstance(file, IOBase)
        assert isinstance(project_path, str)
        # source
        file.write('source_group(TREE ')
        path = os.path.join(project_path, '../..')
        path = os.path.normpath(path)
        # path = project_path
        file.write(path.replace('\\', '/'))
        file.write(' PREFIX "Sources" FILES ${project_sources})\n')
        # headers
        file.write('source_group(TREE ')
        file.write(path.replace('\\', '/'))
        file.write(' PREFIX "Headers" ')
        file.write('FILES ${public_headers} ${private_headers} ')
        file.write('${interface_headers})\n\n')

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

    def __add_sources(self, file, sources, excludes):
        assert isinstance(file, IOBase)

        file.write('set(project_sources\n')
        for source in sources:
            isIn = False
            for exclude in excludes:
                isIn = exclude in source
            if isIn:
                continue
            file.write('    \"')
            source_path = os.path.join('${PROJECT_SOURCE_DIR}', source)
            file.write(source_path.replace('\\', '/'))
            file.write('\"\n')
        file.write(')\n\n')

    def __add_new_lines(self, file, collection, check_duplicates):
        for item in collection:
            # header_file = os.path.basename(item)
            header_file = item
            if header_file in check_duplicates:
                continue
            else:
                check_duplicates.add(header_file)
            file.write('    \"')
            public = os.path.join('${PROJECT_SOURCE_DIR}', header_file)
            file.write(public.replace('\\', '/'))
            file.write('\"\n')

    def __add_headers(self, file, public, private, interface):
        assert isinstance(file, IOBase)

        headers = set()
        file.write('set(headers\n')
        self.__add_new_lines(file, public, headers)
        self.__add_new_lines(file, private, headers)
        self.__add_new_lines(file, interface, headers)
        file.write(')\n\n')

    def __add_uis(self, file, uis):
        assert isinstance(file, IOBase)

        file.write('set(project_uis\n')
        for ui in uis:
            file.write('    \"')
            file.write(ui.replace('\\', '/'))
            file.write('\"\n')
        file.write(')\n\n')

    def __add_qrcs(self, file, qrcs):
        assert isinstance(file, IOBase)

        file.write('set(project_qrcs\n')
        for qrc in qrcs:
            file.write('    \"')
            file.write(qrc.replace('\\', '/'))
            file.write('\"\n')
        file.write(')\n\n')

    def add_target(self, file, target_type, lib_type=LibraryType.UNKNOWN):
        assert isinstance(file, IOBase)
        assert isinstance(target_type, TargetType)
        if target_type == TargetType.UNKNOWN:
            print('Target typ is unknown!')
            return
        elif (
            target_type == TargetType.LIBRARY or
            target_type == TargetType.HEADER_LIBRARY
        ):
            file.write('add_library(${PROJECT_NAME}')
            if lib_type == LibraryType.SHARED:
                file.write(' SHARED')
            elif lib_type == LibraryType.STATIC:
                file.write(' STATIC')
        elif target_type == TargetType.EXECUTABLE:
            file.write('add_executable(${PROJECT_NAME}')

        file.write(' "")\n\n')

    def __add_target_sources(self, file):
        assert isinstance(file, IOBase)

        file.write('target_sources(${PROJECT_NAME}\n')
        file.write('  PRIVATE\n')
        file.write('    ${project_sources}\n')
        file.write('    ${headers}\n')
        file.write('    ${project_uis}\n')
        file.write('    ${project_qrcs}\n')
        file.write(')\n\n')

    def __get_proper_dir(self):
        result = 'win'
        result += self.bit_type
       
        result += '-msvc2017_'
        if (self.build_type == 'debug'):
            result += 'd'
        else:
            result += 'r'

        return result

    def __add_includes(self, file, includes, excludeList=None, is_qt4=False, is_qt5=False):
        assert isinstance(file, IOBase)
        assert isinstance(is_qt4, bool)
        assert isinstance(is_qt5, bool)

        file.write('target_include_directories(${PROJECT_NAME}\n')
        file.write('  PRIVATE\n')
        for include in includes:
            isIn = False
            for exclude in excludeList:
                isIn = exclude in include
                if isIn:
                    break
            if isIn:
                continue
            if include == r'../include' or include == r'..\include':
                continue

            file.write('    \"')
            file.write(include.replace('\\', '/').replace("\"", ""))
            file.write('\"\n')

        file.write('    "../../' + self.__get_proper_dir() + '/include"\n')
        file.write('    "../include"\n')
        if(is_qt4 == True):
            file.write('    "../thirdparty/qt-4.8.7-stl521/include"\n')
            file.write('    "../thirdparty/qt-4.8.7-stl521/include/Qt"\n')
            file.write('    "../thirdparty/qt-4.8.7-stl521/include/QtCore"\n')
            file.write('    "../thirdparty/qt-4.8.7-stl521/include/QtGui"\n')
            file.write(
                '    "../thirdparty/qt-4.8.7-stl521/include/Qt3Support"\n')
            file.write(
                '    "../thirdparty/qt-4.8.7-stl521/mkspecs/win' + self.bit_type + '-msvc2017"\n')

        if (is_qt5 == True):
            file.write('    "../thirdparty/qt-5.12.5/include"\n')
            file.write('    "../thirdparty/qt-5.12.5/include/QtCore"\n')
            file.write('    "../thirdparty/qt-5.12.5/include/QtGui"\n')
            file.write('    "../thirdparty/qt-5.12.5/include/QtNetwork"\n')
            file.write('    "../thirdparty/qt-5.12.5/include/QtConcurrent"\n')
            file.write('    "../thirdparty/qt-5.12.5/include/QtWebSockets"\n')
            file.write('    "../thirdparty/qt-5.12.5/mkspecs/win' + self.bit_type +'-msvc2017"\n')
        file.write(')\n\n')

    def __add_ccache(self, file):
        assert isinstance(file, IOBase)

        file.write('find_program(CCACHE_PROGRAM ccache)\n')
        file.write('if(CCACHE_FOUND)\n')
        file.write('  set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")\n')
        file.write('endif()\n\n')

    def __add_link_dirs(self, file, link_dirs, is_qt4=False, is_qt5=False):
        assert isinstance(file, IOBase)
        assert isinstance(is_qt4, bool)
        assert isinstance(is_qt5, bool)

        file.write('target_link_directories(${PROJECT_NAME}\n')
        file.write('  PRIVATE\n')
        for link_dir in link_dirs:
            file.write('    "')
            file.write(link_dir.replace('\\', '/'))
            file.write('"\n')

        if (is_qt4 == True):
            file.write('    "')
            file.write('../' + self.__get_proper_dir() + '/tools/qt4/lib')
            file.write('"\n')

        if (is_qt5 == True):
            file.write('    "')
            file.write('../' + self.__get_proper_dir() + '/tools/qt5/lib')
            file.write('"\n')

        file.write(')\n\n')

    def __add_libs(self, file, libs):
        assert isinstance(file, IOBase)
        file.write('target_link_libraries(${PROJECT_NAME}\n')
        file.write('  PRIVATE\n')
        for lib in libs:
            file.write('    "')
            lib_file = os.path.basename(lib)
            file.write(lib_file.replace('\\', '/'))
            file.write('"\n')

        file.write(')\n\n')

    def __add_target_features(self, file):
        assert isinstance(file, IOBase)

        file.write('target_compile_features(${PROJECT_NAME} ')
        file.write('PRIVATE cxx_std_11)\n')
        file.write('set_target_properties(${PROJECT_NAME} ')
        file.write('PROPERTIES CXX_EXTENSIONS OFF)\n\n')

    def __add_qt_support(self, file, list_of_qt_targets, qt_ver):
        assert isinstance(file, IOBase)
        assert isinstance(qt_ver, str)

        if len(list_of_qt_targets) == 0:
            return
        file.write('set(CMAKE_INCLUDE_CURRENT_DIR ON)\n')
        file.write('set(CMAKE_AUTOMOC ON)\n')
        file.write('set(CMAKE_AUTOUIC ON)\n')
        file.write('set(CMAKE_AUTORCC ON)\n')
        file.write('find_package(Qt4 ')
        file.write(qt_ver)
        file.write(' REQUIRED COMPONENTS')
        for target in list_of_qt_targets:
            if target == 'QtWebKit':
                continue
            file.write(' ')
            file.write(target)
        file.write(')\n\n')

    def __add_install(self, file):
        assert isinstance(file, IOBase)

        file.write('install (TARGETS\n')
        file.write('         ${PROJECT_NAME}\n')
        file.write('         EXPORT ${PROJECT_NAME}Config\n')
        file.write('         ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}\n')
        file.write('         LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}\n')
        file.write('         RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}\n')
        file.write(')\n\n')
        file.write('export (TARGETS\n')
        file.write('        ${PROJECT_NAME}\n')
        file.write('        NAMESPACE ${PROJECT_NAME}::\n')
        file.write('        FILE "${CMAKE_CURRENT_BINARY_DIR}')
        file.write('/${PROJECT_NAME}Config.cmake"\n')
        file.write(')\n\n')
        file.write('install (EXPORT\n')
        file.write('         ${PROJECT_NAME}Config\n')
        file.write('         DESTINATION "${CMAKE_INSTALL_DATADIR}')
        file.write('/${PROJECT_NAME}/cmake"\n')
        file.write('         NAMESPACE ${PROJECT_NAME}::\n')
        file.write(')\n\n')

    def __add_target_property(self, file, property_name, value):
        assert isinstance(file, IOBase)
        assert isinstance(property_name, str)
        assert isinstance(value, str)

        file.write('set_property(TARGET ${PROJECT_NAME} PROPERTY ')
        file.write(property_name)
        file.write(' ')
        file.write(value)
        file.write(')\n\n')

    def create_project(self, path, build_data):
        assert isinstance(path, str)
        assert isinstance(build_data, builddata.BuildData)

        if(not os.path.exists(path)):
            print('WARNING: ', path, ' does not exists!')
            return

        file = open(os.path.join(path, 'CMakeLists.txt'), 'w')

        self.__prepare_header(file)
        self.__prepare_project(file, build_data.target)
        self.add_target(file, build_data.target_type, build_data.library_type)
        if build_data.is_there_qt4:
            self.__add_qt_support(file, build_data.list_of_qt_targets, '4.8.7')
            self.__add_target_property(file, 'AUTOMOC', 'ON')

        cpp_excludes = [self.__get_proper_dir()]
        self.__add_sources(file, build_data.list_of_sources, cpp_excludes)

        self.__add_headers(file, build_data.public_headers,
                           build_data.private_headers,
                           build_data.interface_headers)

        self.__add_uis(file, build_data.list_of_qt_uis)
        self.__add_qrcs(file, build_data.list_of_qt_qrcs)

        # self.__add_dir_mimic(file, build_data.project_path)
        self.__add_target_sources(file)
        self.__add_flags(file, build_data.list_of_flags)
        self.__add_defines(file, build_data.list_of_defines)
        self.__export_commands(file)
        # self.__add_ccache(file)
        self.__add_target_features(file)

        header_excludes = ['win32-msvc2017_d', 'win32-msvc2017_r',
                           'win64-msvc2017_d', 'win64-msvc2017_r']
        # header_excludes = ['qt-4.8.7-stl521', 'win32-msvc2017_d',
        #                   'win32-msvc2017_r']
        self.__add_includes(file, build_data.set_of_includes,
                            header_excludes, build_data.is_there_qt4,
                            build_data.is_there_qt5)
        if build_data.list_of_lib_paths:
            self.__add_link_dirs(file, build_data.list_of_lib_paths,
                                 build_data.is_there_qt4,
                                 build_data.is_there_qt5)
        if build_data.list_of_libs:
            self.__add_libs(file, build_data.list_of_libs)
        # if build_data.target_type == TargetType.LIBRARY:
        #    self.__add_install(file)
        file.close()

    def create_main_project(self, path, subprojects, project_name):
        assert isinstance(path, str)
        assert isinstance(project_name, str)

        file = open(os.path.join(path, 'CMakeLists.txt'), 'w')
        self.__prepare_header(file)
        self.__prepare_project(file, 'Syndis')
        for project in subprojects:
            project_path = os.path.join(path, project)
            if os.path.isfile(os.path.join(project_path, 'CMakeLists.txt')):
                file.write('add_subdirectory(')
                file.write(project)
                file.write(')\n')

        file.close()
