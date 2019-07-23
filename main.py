import makefileparser
import cmakecreator
import os


src_path = os.path.join('c:\\', 'Projekty', 'trunk', 'src')
build_path = os.path.join('c:\\', 'Projekty', 'trunk',
                          'win32-msvc2015_d')
makefile_parser = makefileparser.MakefileParser()

subprojects_list = [name for name in os.listdir(build_path)
                    if os.path.isfile(os.path.join(build_path, name, 'qt4',
                                                   'makefile'))]
# subprojects_list = ['radosc']

for subproject in subprojects_list:
    print('=======================================')
    print('transforming: ', subproject)
    makef_path = os.path.join(build_path, subproject, 'qt4', 'makefile')
    sub_path = os.path.join(src_path, subproject)

    build_data = makefile_parser.parse_file(makef_path, sub_path)
    cmake = cmakecreator.CMakeCreator()
    cmake.create_project(sub_path, build_data)

main_cmake = cmakecreator.CMakeCreator()
main_cmake.create_main_project(src_path, subprojects_list)
