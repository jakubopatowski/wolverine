import makefileparser
import cmakecreator
import os
import logging


logging.basicConfig(filename='make2cmake.log',
                    filemode='w',
                    level=logging.DEBUG,
                    format='%(asctime)s ..|.. %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')

project_path = os.path.join('c:\\', 'Projekty', 'trunk', 'src')
project2_path = os.path.join('c:\\', 'Projekty', 'trunk',
                             'win32-msvc2015_d')
logging.info('project_path: %s', project_path)
logging.info('project_path2: %s', project2_path)
makefile_parser = makefileparser.MakefileParser(project_path)

# subprojects_list = [name for name in os.listdir(project2_path)
#                     if os.path.isfile(os.path.join(project2_path, name, 'qt4',
#                                                    'makefile'))]
subprojects_list = ['radosc']

for subproject in subprojects_list:
    print('transforming: ', subproject)
    logging.debug('')
    logging.debug('Analyzing: %s', subproject)
    makef_path = os.path.join(project2_path, subproject, 'qt4', 'makefile')
    sub_path = os.path.join(project_path, subproject)
    logging.debug('makefile path: %s', makef_path)
    logging.debug('source path: %s', sub_path)

    build_data = makefile_parser.parse_file(makef_path, sub_path)
    logging.debug('build data: %s', str(build_data.__dict__))
    cmake = cmakecreator.CMakeCreator()
    cmake.create_project(sub_path, build_data)

main_cmake = cmakecreator.CMakeCreator()
main_cmake.create_main_project(project_path, subprojects_list)
