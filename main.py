import makefileparser
import cmakecreator
import projectfixer
import os
import shutil
import configmanager


# Read config file "config.ini"
config = configmanager.ConfigManager()

# Get list of projects to transform
makefile_parser = makefileparser.MakefileParser()
subprojects_list = list()
if len(config.build_list) == 0:
    # all
    subprojects_list = [
        name
        for name in os.listdir(config.build_path)
        if os.path.isfile(os.path.join(config.build_path, name, "qt4", "makefile"))
        or os.path.isfile(os.path.join(config.build_path, name, "qt5", "makefile"))
    ]
    print("Number of projects found: ", len(subprojects_list))
else:
    # just one
    subprojects_list = config.build_list

projects = dict()
print("")  


for subproject in subprojects_list:
    print("=======================================")
    print("transforming: ", subproject)
    makef_path = os.path.join(config.build_path, subproject, "qt4", "makefile")
    makef_path_qt5 = os.path.join(config.build_path, subproject, "qt5", "makefile")
    sub_path = os.path.join(config.src_path, subproject)

    qt_version = 4
    if os.path.isfile(makef_path_qt5) is True:
        makef_path = makef_path_qt5
        qt_version = 5

    print(makef_path)
    print(sub_path)
    print('Qt version: ', qt_version)

    if os.path.isdir(sub_path) is False:
        print("Projekt nie istnieje!")
        continue

    build_data = makefile_parser.parse_file(makef_path, sub_path)
    if build_data != None:
        projects[build_data.target] = build_data
     
print("Podsumowanie:")
print("Ogółem projektów: ", len(subprojects_list))

print(config.static_libs)
for key, value in projects.items():
    value.reevaluate_deps(projects.keys())
    for item in config.static_libs:
        if key == item:
            print("jest hardcoded na static: ", key)
            value.set_library_type("lib")
    cmake = cmakecreator.CMakeCreator(config.proj_type, config.proj_bit)
    cmake.create_project(value.project_path, value)

main_cmake = cmakecreator.CMakeCreator(config.proj_type, config.proj_bit)
main_cmake.create_main_project(config.src_path, subprojects_list, config.proj_name)
