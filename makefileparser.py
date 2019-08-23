import re
import os
import builddata


class MakefileParser:

    line_continue_pattern = r'\\\n'
    # co robi r ?
    target_pattern = 'TARGET\\s*=\\s*(\\w*)'
    defines_pattern = 'DEFINES\\s*=\\s*(.*)'
    define_pattern = '-D(\\S*)'
    cxx_flags_pattern = 'CXXFLAGS\\s*=\\s(.*)'
    flag_pattern = '(?:^|\\s)([^\\$\\s]\\S*[^\\$\\s])'
    includes_pattern = 'INCPATH\\s*=\\s(.*)'
    include_pattern = '\\"(\\S*)\\"'
    target_type_pattern = '\\#\\s*Template:\\s*([\\w]*)'
    sources_pattern = 'SOURCES\\s*=\\s*(.*)'
    libs_pattern = 'LIBS\\s*=\\s*(.*)'
    libpath_pattern = '\\/LIBPATH:(\\S*)'
    entry_pattern = '\\S*'
    dll_export = ['RADOSC_EXP', 'RTOOLKIT_EXPORT', 'ZKOD_EXP',
                  'RVVNETCLIENT_EXP', 'RV_VNET_EXPORT', 'SID_EXP',
                  'AVRCLASSES_EXPORT', 'RVL_BACKUP_EXPORT', 'RCHART_EXPORT',
                  'RCLASSES_EXPORT', 'RVL_COMTRADE_EXPORT', 'DECLDIR',
                  '//install', 'RVL_CURL_EXPORT']

    def __init__(self):
        self.subprojects = []

    def src_rel_path(self, makefile_path, project_path, path):
        assert isinstance(makefile_path, str)
        assert isinstance(project_path, str)
        assert isinstance(path, str)

        makefile_dir = os.path.dirname(makefile_path)
        full_path = os.path.normpath(os.path.join(makefile_dir,
                                                  path))
        full_path = os.path.relpath(full_path, project_path)
        return full_path

    def __get_qt_files(self, project_path):
        assert isinstance(project_path, str)

        ui_files = []
        qrc_files = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(".ui"):
                    ui_file = os.path.join(root, file)
                    print(ui_file)
                    ui_files.append(os.path.relpath(ui_file, project_path))
                elif file.endswith(".qrc"):
                    qrc_file = os.path.join(root, file)
                    print(qrc_file)
                    qrc_files.append(os.path.relpath(qrc_file, project_path))
        return ui_files, qrc_files

    def __is_public(self, file_path):
        assert isinstance(file_path, str)

        if not os.path.isfile(file_path):
            return None

        with open(file_path, errors='replace') as h_file:
            h_data = h_file.read()

        for item in self.dll_export:
            if re.search(item, h_data) is not None:
                return True

        return False

    def __get_headers(self, project_path, makefile_path):
        assert isinstance(project_path, str)
        assert isinstance(makefile_path, str)
        exclude = ['.ccls-cache']

        public_headers = []
        private_headers = []
        for root, dirs, files in os.walk(project_path, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude]
            for file in files:
                if file.endswith('.h') or file.endswith('.hpp'):
                    header_abs_path = os.path.join(root, file)
                    header_rel_path = self.src_rel_path(makefile_path,
                                                        project_path,
                                                        header_abs_path)
                    if self.__is_public(header_abs_path):
                        public_headers.append(header_rel_path)
                    else:
                        private_headers.append(header_rel_path)
        return public_headers, private_headers

    def parse_file(self, makefile_path, project_path):
        assert isinstance(makefile_path, str)
        assert isinstance(project_path, str)

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
        includes = []
        for include in list_of_includes:
            includes.append(self.src_rel_path(makefile_path, project_path,
                                              include))

        result.set_includes(includes)

        # sources
        sources = re.findall(self.sources_pattern, makefile_data)
        list_of_sources = []
        for source in sources[0].split():
            list_of_sources.append(self.src_rel_path(makefile_path,
                                                     project_path, source))

        result.set_sources(list_of_sources)

        # headers
        public, private = self.__get_headers(project_path, makefile_path)
        result.set_public_headers(public)
        result.set_private_headers(private)

        # qt ui files
        uis, qrcs = self.__get_qt_files(project_path)
        result.set_qt_files(uis, qrcs)

        # libraries
        libraries = re.findall(self.libs_pattern, makefile_data)

        print('libraries:', libraries)
        if not libraries:
            print("There are no libraries!")
        else:
            library_list = libraries[0].split()
            libpath_list = []
            libs_list = []
            print('library_list:', library_list)
            for entry in library_list:
                if re.search('.res', entry) is not None:
                    continue

                libpath = re.findall(self.libpath_pattern, entry)
                if len(libpath) <= 0:
                    libs_list.append(entry)
                elif len(libpath) > 0:
                    path = libpath[0]
                    libpath_list.append(self.src_rel_path(makefile_path,
                                                          project_path, path))
            print('libs_list:', libs_list)
            print('libpath_list:', libpath_list)
            result.set_libs(libs_list)
            result.set_lib_paths(libpath_list)

        return result
