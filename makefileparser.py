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

    def __init__(self, project_path, verbose):
        assert isinstance(project_path, str)
        assert isinstance(verbose, bool)
        self.project_path = project_path
        self.verbose = verbose
        self.subprojects = []

    def make_main_cmake(self):
        print(self.project_path)
        file = open(os.path.join(self.project_path, 'CMakeLists.txt'), 'w')
        file.write()

    def get_subprojects(self):
        path = os.path.join('c:\\', 'Projekty', 'trunk',
                            'win32-msvc2015_d')
        return [name for name in os.listdir(path)
                if os.path.isfile(os.path.join(path, name, 'qt4',
                                               'makefile'))]

    def parse_file(self, makefile_path, project_path):
        assert isinstance(makefile_path, str)

        self.subprojects.append(project_path)
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

            result = builddata.BuildData()
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

            # flags
            flags = re.findall(self.cxx_flags_pattern, makefile_data)
            result.set_flags(re.findall(self.flag_pattern, flags[0]))
            if(self.verbose):
                print('list_of_flags:', result.list_of_flags)

            # includes
            includes = re.findall(self.includes_pattern, makefile_data)
            list_of_includes = re.findall(self.include_pattern, includes[0])
            includes = []
            for include in list_of_includes:
                full_path = os.path.normpath(os.path.join(makefile_dir,
                                                          include))
                full_path = os.path.relpath(full_path, project_path)
                includes.append(full_path)

            result.set_includes(includes)
            if(self.verbose):
                print('list_of_includes:', result.list_of_includes)

            # sources
            sources = re.findall(self.sources_pattern, makefile_data)
            list_of_sources = []
            for source in sources[0].split():
                full_path = os.path.normpath(os.path.join(makefile_dir,
                                                          source))
                full_path = os.path.relpath(full_path, project_path)
                list_of_sources.append(full_path)

            result.set_sources(list_of_sources)
            if(self.verbose):
                print('list_of_sources', result.list_of_sources)

            # libraries
            libraries = re.findall(self.libs_pattern, makefile_data)
            if not libraries:
                if self.verbose:
                    print("There are no libraries!")
            else:
                print('libraries: ', libraries)
                library_list = libraries[0].split()
                print('library_list: ', library_list)
                libpath_list = []
                libs_list = []
                for entry in library_list:
                    if re.search('.res', entry) is not None:
                        continue

                    libpath = re.search(self.libpath_pattern, entry)

                    if libpath is None:
                        libs_list.append(entry)
                    else:
                        path = libpath.group(1)
                        full_path = os.path.normpath(
                            os.path.join(makefile_dir, path))
                        full_path = os.path.relpath(full_path, project_path)
                        libpath_list.append(full_path)

                        result.set_libs(libs_list)
                        result.set_lib_paths(libpath_list)

                        print('list of libs: ', libs_list)
                        print('list of lib paths: ', libpath_list)

            return result
