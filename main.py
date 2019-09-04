import makefileparser
import cmakecreator
import projectfixer
import os
import configparser
import projectdata


config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
print(config.sections())

src_path = os.path.join(config['paths']['src_path'])
build_path = os.path.join(config['paths']['build_path'])
makefile_parser = makefileparser.MakefileParser()

subprojects_list = [name for name in os.listdir(build_path)
                    if os.path.isfile(os.path.join(build_path, name, 'qt4',
                                                   'makefile'))]
# subprojects_list = ['bazatelem']

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
    projects[build_data.target] = projectdata.ProjectData(
        build_data.target, sub_path, build_data.target_type)
    fixer = projectfixer.ProjectFixer()
    if len(build_data.public_headers) > 0:
        fixer.copy_file(os.path.join(sub_path, 'include'),
                        build_data.public_headers,
                        sub_path)

    cmake = cmakecreator.CMakeCreator()
    cmake.create_project(sub_path, build_data)

main_cmake = cmakecreator.CMakeCreator()
main_cmake.create_main_project(src_path, subprojects_list, 'syndis')
