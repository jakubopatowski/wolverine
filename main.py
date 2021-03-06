import makefileparser
import cmakecreator
import projectfixer
import os
import configparser
import shutil


config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
print(config.sections())

src_path = os.path.join(config['paths']['src_path'])
build_path = os.path.join(config['paths']['build_path'])
static_libs = config['projects']['static_libs'].split(',')

makefile_parser = makefileparser.MakefileParser()

subprojects_list = [name for name in os.listdir(build_path)
                    if os.path.isfile(os.path.join(build_path, name, 'qt4',
                                                   'makefile'))]
# subprojects_list = ['rvs_help']

projects = dict()
for subproject in subprojects_list:
    print('=======================================')
    print('transforming: ', subproject)
    makef_path = os.path.join(build_path, subproject, 'qt4', 'makefile')
    sub_path = os.path.join(src_path, subproject)
    if os.path.isdir(sub_path) is False:
        print("Projekt nie istnieje!")
        continue

    build_data = makefile_parser.parse_file(makef_path, sub_path)
    projects[build_data.target] = build_data
    fixer = projectfixer.ProjectFixer()
    include_dir = os.path.join(sub_path, 'include')
    shutil.rmtree(include_dir, ignore_errors=True)
    if len(build_data.public_headers) > 0:
        fixer.copy_file(include_dir, build_data.public_headers, sub_path)
    if len(build_data.interface_headers) > 0:
        fixer.copy_file(include_dir, build_data.interface_headers, sub_path)
    fixer.create_file(include_dir, '.ignore')

print(static_libs)
for key, value in projects.items():
    value.reevaluate_deps(projects.keys())
    for item in static_libs:
        if key == item:
            print('jest hardcoded na static: ', key)
            value.set_library_type('lib')
    cmake = cmakecreator.CMakeCreator()
    cmake.create_project(value.project_path, value)

main_cmake = cmakecreator.CMakeCreator()
main_cmake.create_main_project(src_path, subprojects_list, 'syndis')
