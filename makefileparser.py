import re
import os
import builddata
import logging


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

    def parse_file(self, makefile_path, project_path):
        assert isinstance(makefile_path, str)
        assert isinstance(project_path, str)

        self.subprojects.append(project_path)

        if not os.path.isfile(makefile_path):
            return None

        logging.info('makefile exists')
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

        # libraries
        libraries = re.findall(self.libs_pattern, makefile_data)

        if not libraries:
            print("There are no libraries!")
        else:
            library_list = libraries[0].split()
            libpath_list = []
            libs_list = []
            for entry in library_list:
                print(entry)
                if re.search('.res', entry) is not None:
                    continue

                libpath = re.findall(self.libpath_pattern, entry)
                if libpath is None:
                    libs_list.append(entry)
                elif len(libpath) > 0:
                    path = libpath[0]
                    libpath_list.append(self.src_rel_path(makefile_path,
                                                          project_path, path))
            result.set_libs(libs_list)
            result.set_lib_paths(libpath_list)

        return result
