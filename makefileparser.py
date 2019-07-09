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
                full_path = os.path.relpath(full_path, project_path)
                list_of_sources.append(full_path)

            result.set_sources(list_of_sources)
            if(self.verbose):
                print('list_of_sources', result.list_of_sources)

            return result
