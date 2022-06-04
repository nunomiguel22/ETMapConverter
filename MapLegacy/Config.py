
import configparser

__version__ = "0.1.2"
__author__ = "Nuno Miguel Fernandes Marques"

# Config dicts
configDrawDict = {
    "nodraw": "false",
    "clip": "false",
    "triggers": "false",
    "caulk": "false",
    "hints": "false",
    "skybox": "false",
    "terrain": "true",
    "skip": "false",
    "slick": "false",
    "origin": "false",
    "ladder": "false",
    "road": "true"
}

configDrawValDict = {
    "nodraw": "nodraw",
    "clip": "clip",
    "triggers": "trigger",
    "caulk": "caulk",
    "hints": "common/hint",
    "skybox": "skies",
    "terrain": "common/terrain",
    "skip": "common/skip",
    "slick": "common/slick",
    "origin": "common/origin",
    "ladder": "common/ladder",
    "road": "road"
}

configOptionsDict = {
    "usemtl": "true",
    "write_mtl_file": "true",
    "mtl_tex_folder": "textures/",
    "textures_path": "Output/textures/",
    "default_tex_width": "256",
    "default_tex_height": "256",
    "z_upwards": "true",
    "scale": "0.1"
}


class Config:
    def __init__(self):
        self.texFilter = []
        self.usemtl = True
        self.writemtl = True
        self.mtlTexFolder = "textures/"
        self.texFolder = "Output/textures"
        self.epsilon = 0.001  # floating error limit
        self.defaultTexHeight = 256
        self.defaultTexWidth = 256

        config = configparser.ConfigParser()
        config["DRAW"] = configDrawDict
        config["OPTIONS"] = configOptionsDict
        config.read("options.ini")
        with open('options.ini', 'w') as configfile:
            config.write(configfile)
        self.texFilter = self.__getDrawFilter(config)
        self.__setConfigGlobals(config)

    def __getDrawFilter(self, config):
        drawFilter = []
        for key in config["DRAW"]:
            if not config["DRAW"].getboolean(key):
                drawFilter.append(configDrawValDict[key])
        return drawFilter

    def __setConfigGlobals(self, config):
        self.usemtl = config["OPTIONS"].getboolean("usemtl")
        self.writemtl = config["OPTIONS"].getboolean("write_mtl_file")
        self.mtlTexFolder = config["OPTIONS"]["mtl_tex_folder"]
        self.texFolder = config["OPTIONS"]["textures_path"]
        self.defaultTexHeight = int(config["OPTIONS"]["default_tex_height"])
        self.defaultTexWidth = int(config["OPTIONS"]["default_tex_width"])
        self.zUpwards = config["OPTIONS"].getboolean("z_upwards")
        self.scale = float(config["OPTIONS"]["scale"])


config = Config()
