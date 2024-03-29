import re
import os
import builddata
import tools


class MakefileParser:

    line_continue_pattern = r'\\\n'
    target_pattern = 'TARGET\\s*=\\s*(\\w*)'
    defines_pattern = 'DEFINES\\s*=\\s*(.*)'
    define_pattern = '-D(\\S*)'
    cxx_flags_pattern = 'CXXFLAGS\\s*=\\s(.*)'
    flag_pattern = '(?:^|\\s)([^\\$\\s]\\S*[^\\$\\s])'
    includes_pattern = 'INCPATH\\s*=\\s(.*)'
    include_pattern = '\\-I"*(\\S*)\\"*'
    target_type_pattern = '\\#\\s*Template:\\s*([\\w]*)'
    sources_pattern = 'SOURCES\\s*=\\s*(.*)'
    libs_pattern = 'LIBS\\s*=\\s*(.*)'
    libpath_pattern = '\\/LIBPATH:(\\S*)'
    entry_pattern = '\\S*'
    exclude = ['.ccls-cache', 'include']
    export_macro = r'#define ([A-Z0-9_]*) __declspec\s*\(\s*dllexport\s*\)'
    header_file_pat = re.compile(r'\\(\w*\.(hpp|h))')

    header_pat = re.compile(r'\w*.(h|hpp)$')
    ui_pat = re.compile(r'\w*.(ui)$')
    qrc_pat = re.compile(r'\w*.(qrc)$')

    def __init__(self):
        self.subprojects = []

    def __get_qt_files(self, project_path):
        """Return list of all ui nad qrc files in a given project_path
        (including subdirs). List will have files with relative paths
        according to project_path."""
        assert isinstance(project_path, str)

        uis = tools.get_files(project_path, self.ui_pat, None, True)
        qrcs = tools.get_files(project_path, self.qrc_pat, None, True)
        return uis, qrcs

    def __get_export_macro(self, project_path):
        assert isinstance(project_path, str)

        files = tools.get_files(project_path, self.header_pat)
        for file in files:
            with open(file, errors='replace') as h_file:
                h_data = h_file.read()
            match = re.search(self.export_macro, h_data)
            if match is not None:
                return match[1]
        return None

    def __file_starts(self, file_path, pattern):
        assert isinstance(file_path, str)
        assert isinstance(pattern, str)

        if not os.path.isfile(file_path):
            return None

        with open(file_path, errors='replace') as f:
            first_line = f.readline()

        if first_line.startswith(pattern):
            return True
        return False

    def __is_public(self, file_path, export_macro):
        assert isinstance(file_path, str)
        assert isinstance(export_macro, str)

        if not os.path.isfile(file_path):
            return None

        with open(file_path, errors='replace') as h_file:
            h_data = h_file.read()

        pattern = re.compile(export_macro)
        if re.search(pattern, h_data) is not None:
            return True

        return False

    def __get_headers(self, project_path, makefile_path, export_macro,
                      header_set):
        assert isinstance(project_path, str)
        assert isinstance(makefile_path, str)

        public_headers = []
        private_headers = []
        interface_headers = []

        files = tools.get_files(project_path, self.header_pat, self.exclude)
        for file in files:
            header_name = os.path.basename(file)
            if header_name not in header_set:
                continue
            header_abs_path = os.path.join(project_path, file)
            header_rel_path = tools.change_rel_path(makefile_path,
                                                    project_path,
                                                    header_abs_path)
            if export_macro is not None and self.__is_public(
                    header_abs_path, export_macro):
                public_headers.append(header_rel_path)
            elif self.__file_starts(
                    header_abs_path, '//install'):
                interface_headers.append(header_rel_path)
            else:
                private_headers.append(header_rel_path)

        return public_headers, private_headers, interface_headers

    def parse_file(self, makefile_path, project_path):
        assert isinstance(makefile_path, str)
        assert isinstance(project_path, str)

        # ToDo: usunąć poniższą zależność
        # przenieść jako osobną funkcjonalność
        self.subprojects.append(project_path)

        if not os.path.isfile(makefile_path):
            return None

        with open(makefile_path) as makefile:
            makefile_data = makefile.read()

        # delete line continuations
        makefile_data = re.sub(self.line_continue_pattern, '',
                               makefile_data)

        result = builddata.BuildData()
        result.set_project_path(project_path)

        # export macro
        macro = self.__get_export_macro(project_path)
        if macro is not None:
            result.set_export_macro
            print(macro)

        # targets
        targets = re.findall(self.target_pattern, makefile_data)
        result.set_target_name(targets[0])

        # target type
        target_type = re.findall(self.target_type_pattern, makefile_data)
        result.set_target_type(target_type[0])

        # defines
        defines = re.findall(self.defines_pattern, makefile_data)
        result.set_defines(re.findall(self.define_pattern, defines[0]))

        # flags
        flags = re.findall(self.cxx_flags_pattern, makefile_data)
        result.set_flags(re.findall(self.flag_pattern, flags[0]))

        # includes
        includes = re.findall(self.includes_pattern, makefile_data)
        list_of_includes = re.findall(self.include_pattern, includes[0])
        includes = set()
        for include in list_of_includes:
            includes.add(tools.change_rel_path(makefile_path, project_path,
                                               include))

        result.set_includes(includes)

        # sources
        sources = re.findall(self.sources_pattern, makefile_data)
        list_of_sources = []
        for source in sources[0].split():
            list_of_sources.append(tools.change_rel_path(makefile_path,
                                                         project_path, source))

        result.set_sources(list_of_sources)

        # headers
        header_set = set()
        matches = self.header_file_pat.finditer(makefile_data)
        for match in matches:
            header_set.add(match.group(1))

        public, private, interface = self.__get_headers(
            project_path, makefile_path, macro, header_set)
        result.set_public_headers(public)
        result.set_private_headers(private)
        result.set_interface_headers(interface)
        if len(interface) > 0:
            print(interface)

        # qt ui files
        uis, qrcs = self.__get_qt_files(project_path)
        result.set_qt_files(uis, qrcs)

        # libraries
        libraries = re.findall(self.libs_pattern, makefile_data)

        # print('libraries:', libraries)
        if not libraries:
            print("There are no libraries!")
        else:
            string = libraries[0]
            library_list = re.split('\\s*([^\\s\\"\']+)|\\"([^\\"]*)\\"|\'([^\']*)\'', string)
            library_list = list(filter(None, library_list))
            #library_list = string.split()
            libpath_list = []
            libs_list = []
            # print('library_list:', library_list)
            for entry in library_list:
                if not entry or entry.strip() == '':
                    continue
                if re.search('.res', entry) is not None:
                    continue

                libpath = re.findall(self.libpath_pattern, entry)
                if len(libpath) <= 0:
                    libs_list.append(entry)
                elif len(libpath) > 0:
                    path = libpath[0]
                    libpath_list.append(tools.change_rel_path(makefile_path,
                                                              project_path,
                                                              path))
            print('libs_list:', libs_list)
            print('libpath_list:', libpath_list)
            result.set_libs(libs_list)
            result.set_lib_paths(libpath_list)

        return result
