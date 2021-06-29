import configparser
import os


class ConfigManager:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.sections()
        config.read("config.ini")
        self.proj_name = config["project"]["name"]
        self.proj_type = config["build_type"]["type"]
        self.proj_bit = config["build_type"]["bit"]
        self.qt5_path = config["thirdparty"]["qt5_path"]
        self.qt4_path = config["thirdparty"]["qt4_path"]
        self.qt5_ver = config["thirdparty"]["qt5_ver"]
        self.qt4_ver = config["thirdparty"]["qt4_ver"]
        self.src_path = os.path.join(config["paths"]["src_path"])
        self.build_path = os.path.join(config["paths"]["build_path"])
        self.static_libs = config["projects"]["static_libs"].split(",")
        self.build_list = list()
        if config.has_option("projects", "build") == True:
            projects = config["projects"]["build"]
            if len(projects):
                self.build_list = config["projects"]["build"].split(",")