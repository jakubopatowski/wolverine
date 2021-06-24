from targettype import TargetType
from librarytype import LibraryType
import os

class BuildData:
    """
    @brief      Placeholder for makefile parsed data

    @details    This class holds data about c++ project that are needed
    in build process of that project.
    """

    def __init__(self):
        "docstring"
        self.makefile_path = None
        self.project_path = None
        self.target = None
        self.target_type = TargetType.UNKNOWN
        self.library_type = LibraryType.UNKNOWN
        self.export_macro = None
        self.target_deps = []
        self.list_of_defines = []
        self.list_of_flags = []
        self.set_of_includes = []
        self.list_of_sources = []
        self.public_headers = []
        self.private_headers = []
        self.interface_headers = []
        self.list_of_libs = []
        self.list_of_lib_paths = set()
        self.is_there_boost = False
        self.list_of_boost_libs = []
        self.is_there_qt4 = False
        self.is_there_qt5 = False
        self.list_of_qt_targets = []
        self.list_of_qt_uis = []
        self.list_of_qt_qrcs = []
        self.__valid_qt4_libs = {'QtCore', 'QtGui', 'Qt3Support',
                                 'QtAssistant', 'QtAssistantClient',
                                 'QAxContainer', 'QAxServer', 'QtDBus',
                                 'QtDesigner', 'QtDesignerComponents',
                                 'QtHelp', 'QtMotif', 'QtMultimedia',
                                 'QtNetwork', 'QtNsPlugin', 'QtOpenGL',
                                 'QtScript', 'QtScriptTools', 'QtSql',
                                 'QtSvg', 'QtTest', 'QtUiTools', 'QtWebKit',
                                 'QtXml', 'QtXmlPatterns', 'phonon'}
        self.__valid_qt5_libs = {'Qt5Core', 'Qt5WebSockets',
                                 'Qt5Network', 'Qt5Widgets',
                                 'Qt5WinExtras', 'Qt5UiTools',
                                 'Qt5Test', 'Qt5QuickWidgets',
                                 'Qt5NetworkAuth', 'Qt5Concurrent'}

    def get_qt_target(self, lib):
        assert isinstance(lib, str)

        if 'QtWebKit' in lib:
            return lib

        if '.lib' in lib:
            result = lib.replace('d.lib', '')
            result = result.replace('.lib', '')
            if result in self.__valid_qt4_libs:
                self.is_there_qt4 = True
                self.list_of_qt_targets.append(result)
                #return 'Qt4::' + result
            elif result in self.__valid_qt5_libs:
                self.is_there_qt5 = True
                self.list_of_qt_targets.append(result.replace('Qt5',''))
                #return 'Qt5::' + result

        return lib

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
    def set_target_type(self, target_type):
        if target_type == 'app':
            self.target_type = TargetType.EXECUTABLE
        elif target_type == 'lib':
            self.target_type = TargetType.LIBRARY

    def set_library_type(self, lib_type):
        if lib_type == 'lib' or lib_type == 'a':
            self.library_type = LibraryType.STATIC
        elif lib_type == 'dll' or lib_type == 'so':
            self.library_type = LibraryType.SHARED

    # defines
    def set_defines(self, defines):
        self.list_of_defines = defines

    # flags
    def set_flags(self, flags):
        self.list_of_flags = flags

    # includes
    def set_includes(self, includes):
        self.set_of_includes = includes

    # qt ui
    def set_qt_files(self, uis, qrcs):
        self.list_of_qt_uis = uis
        self.list_of_qt_qrcs = qrcs

    # sources
    def set_sources(self, sources):
        self.list_of_sources = sources

    def set_private_headers(self, headers):
        self.private_headers = headers

    def set_public_headers(self, headers):
        self.public_headers = headers

    def set_interface_headers(self, headers):
        self.interface_headers = headers

    def set_libs(self, libs):
        for item in libs:
            lib = self.get_qt_target(os.path.basename(item))
            lib_path = os.path.dirname(item)
            if lib_path is not '':
                self.set_lib_paths(lib_path)
            self.list_of_libs.append(lib)

    def reevaluate_deps(self, projects):
        tmp_list = self.list_of_libs
        for lib in tmp_list:
            result = lib.replace('.lib', '')
            if result in projects:
                id = self.list_of_libs.index(lib)
                self.list_of_libs[id] = result

    # set libraries paths
    def set_lib_paths(self, lib_paths):
        if isinstance(lib_paths, str):
            self.list_of_lib_paths.add(lib_paths)
        elif len(lib_paths) > 1:
            for item in lib_paths:
                self.list_of_lib_paths.add(item)

    def set_export_macro(self, export_macro):
        self.export_macro = export_macro
