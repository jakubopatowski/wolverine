import makefileparser
import cmakecreator
import projectfixer
import os
import configparser
import shutil


# Read config file "config.ini"
config = configparser.ConfigParser()
config.sections()
config.read("config.ini")
print(config.sections())

proj_type = config["build_type"]["type"]
proj_bit = config["build_type"]["bit"]
src_path = os.path.join(config["paths"]["src_path"])
build_path = os.path.join(config["paths"]["build_path"])
static_libs = config["projects"]["static_libs"].split(",")
build_list = list()
if config.has_option("projects", "build") == True:
    projects = config["projects"]["build"]
    if len(projects):
        build_list = config["projects"]["build"].split(",")

# Get list of projects to transform
makefile_parser = makefileparser.MakefileParser()
subprojects_list = list()
if len(build_list) == 0:
    # all
    subprojects_list = [
        name
        for name in os.listdir(build_path)
        if os.path.isfile(os.path.join(build_path, name, "qt4", "makefile"))
        or os.path.isfile(os.path.join(build_path, name, "qt5", "makefile"))
    ]
    print("Number of projects found: ", len(subprojects_list))
else:
    # just one
    subprojects_list = build_list

projects = dict()
print("")  


for subproject in subprojects_list:
    print("=======================================")
    print("transforming: ", subproject)
    makef_path = os.path.join(build_path, subproject, "qt4", "makefile")
    makef_path_qt5 = os.path.join(build_path, subproject, "qt5", "makefile")
    sub_path = os.path.join(src_path, subproject)

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

print(static_libs)
for key, value in projects.items():
    value.reevaluate_deps(projects.keys())
    for item in static_libs:
        if key == item:
            print("jest hardcoded na static: ", key)
            value.set_library_type("lib")
    cmake = cmakecreator.CMakeCreator(proj_type, proj_bit)
    cmake.create_project(value.project_path, value)

main_cmake = cmakecreator.CMakeCreator(proj_type, proj_bit)
main_cmake.create_main_project(src_path, subprojects_list, "syndis")
