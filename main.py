import makefileparser
import cmakecreator
import os


project_path = os.path.join('c:\\', 'Projekty', 'trunk', 'src')
project2_path = os.path.join('c:\\', 'Projekty', 'trunk',
                             'win32-msvc2015_d')
makefile_parser = makefileparser.MakefileParser(project_path)

subprojects_list = [name for name in os.listdir(project2_path)
                    if os.path.isfile(os.path.join(project2_path, name, 'qt4',
                                                   'makefile'))]
# subprojects_list = ['rvs_espim']

for subproject in subprojects_list:
    print('analyzing: ', subproject)
    makef_path = os.path.join(project2_path, subproject, 'qt4', 'makefile')
    sub_path = os.path.join(project_path, subproject)

    build_data = makefile_parser.parse_file(makef_path, sub_path)
    cmake = cmakecreator.CMakeCreator()
    cmake.create_project(sub_path, build_data)

main_cmake = cmakecreator.CMakeCreator()
main_cmake.create_main_project(project_path, subprojects_list)
