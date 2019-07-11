import makefileparser
import cmakecreator
import os


project_path = os.path.join('c:\\', 'Projekty', 'trunk', 'src')
makefile_parser = makefileparser.MakefileParser(project_path, False)
subprojects_list = makefile_parser.get_subprojects()
# subprojects_list = ['rvs_espim']

for subproject in subprojects_list:
    print('analyzing: ', subproject)
    makefile_path = os.path.join('c:\\', 'Projekty', 'trunk',
                                 'win32-msvc2015_d', subproject, 'qt4',
                                 'makefile')
    subproject_path = os.path.join('c:\\', 'Projekty', 'trunk', 'src',
                                   subproject)

    build_data = makefile_parser.parse_file(makefile_path, subproject_path)
    cmake = cmakecreator.CMakeCreator()
    cmake.create_project(subproject_path, build_data)

main_cmake = cmakecreator.CMakeCreator()
main_cmake.create_main_project(project_path, subprojects_list)
