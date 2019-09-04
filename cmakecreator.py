import builddata
import os
from targettype import TargetType
from io import IOBase


class CMakeCreator:
    def __prepare_header(self, file):
        assert isinstance(file, IOBase)

        file.write('cmake_minimum_required(VERSION 3.1...3.15)\n')
        file.write('\n')
        file.write('if(${CMAKE_VERSION} VERSION_LESS 3.12)\n')
        file.write('    cmake_policy(VERSION ${CMAKE_MAJOR_VERSION}')
        file.write('.${CMAKE_MINOR_VERSION})\n')
        file.write('endif()\n\n')

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

    def __add_sources(self, file, sources):
        assert isinstance(file, IOBase)

        file.write('set(project_sources\n')
        for source in sources:
            file.write('    \"')
            file.write(source.replace('\\', '/'))
            file.write('\"\n')
        file.write(')\n\n')

    def __add_headers(self, file, public, private):
        assert isinstance(file, IOBase)

        headers = set()
        file.write('set(public_headers\n')
        for header in public:
            header_file = os.path.basename(header)
            if header_file in headers:
                continue
            else:
                headers.add(header_file)
            file.write('    \"')
            public = os.path.join('include', header_file)
            file.write(public.replace('\\', '/'))
            file.write('\"\n')
        file.write(')\n\n')

        file.write('set(private_headers\n')
        for header in private:
            if os.path.basename(header) in headers:
                continue
            else:
                headers.add(os.path.basename(header))
            file.write('    \"')
            file.write(header.replace('\\', '/'))
            file.write('\"\n')
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

    def __add_target(self, file, target_type):
        assert isinstance(file, IOBase)
        assert isinstance(target_type, TargetType)

        if target_type == TargetType.LIBRARY:
            file.write('add_library(${PROJECT_NAME}\n')
        elif target_type == TargetType.EXECUTABLE:
            file.write('add_executable(${PROJECT_NAME}\n')
        file.write('    ${project_sources}\n')
        file.write('    ${public_headers}\n')
        file.write('    ${private_headers}\n')
        file.write('    ${project_uis}\n')
        file.write('    ${project_qrcs})\n\n')

    def __add_includes(self, file, includes, isPublic=False):
        assert isinstance(file, IOBase)

        file.write('target_include_directories(${PROJECT_NAME}\n')
        if isPublic:
            file.write('    PUBLIC\n')
            file.write('    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}')
            file.write('/include>\n')
            file.write('    $<INSTALL_INTERFACE:include>')

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

    def __add_qt_support(self, file, list_of_qt_targets, qt_ver):
        assert isinstance(file, IOBase)
        assert isinstance(qt_ver, str)

        if len(list_of_qt_targets) == 0:
            return
        file.write('set(CMAKE_AUTOMOC ON)\n')
        file.write('set(CMAKE_AUTOUIC ON)\n')
        file.write('set(CMAKE_INCLUDE_CURRENT_DIR ON)\n')
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

    def create_project(self, path, build_data):
        assert isinstance(path, str)
        assert isinstance(build_data, builddata.BuildData)

        if(not os.path.exists(path)):
            print('WARNING: ', path, ' does not exists!')
            return

        file = open(os.path.join(path, 'CMakeLists.txt'), 'w')

        self.__prepare_header(file)
        self.__prepare_project(file, build_data.target)
        self.__add_qt_support(file, build_data.list_of_qt_targets, '4.8.7')
        self.__add_sources(file, build_data.list_of_sources)
        self.__add_headers(file, build_data.public_headers,
                           build_data.private_headers)
        self.__add_uis(file, build_data.list_of_qt_uis)
        self.__add_qrcs(file, build_data.list_of_qt_qrcs)
        self.__add_dir_mimic(file, build_data.project_path)
        self.__add_target(file, build_data.target_type)
        self.__add_flags(file, build_data.list_of_flags)
        self.__add_defines(file, build_data.list_of_defines)
        self.__export_commands(file)
        self.__add_ccache(file)
        self.__add_target_features(file)
        isPublic = False
        if len(build_data.public_headers) > 0:
            isPublic = True
        self.__add_includes(file, build_data.list_of_includes, isPublic)
        if build_data.list_of_lib_paths:
            self.__add_link_dirs(file, build_data.list_of_lib_paths)
        if build_data.list_of_libs:
            self.__add_libs(file, build_data.list_of_libs)
        if build_data.target_type == TargetType.LIBRARY:
            self.__add_install(file)
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
