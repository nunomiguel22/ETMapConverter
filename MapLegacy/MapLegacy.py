from Parser import Parser
from Map import Map
from Writer import Writer
from PolyManager import PolyManager
import configparser
from Config import config


class MapLegacy:
    def __init__(self, mapFilepath):
        self.mapFilepath = mapFilepath

    def build(self, mapName):
        print("Warning: on large files this make take a few minutes")
        print("Parsing " + self.mapFilepath + "...")
        parser = Parser(self.mapFilepath)
        rootNode = parser.parse()

        print("Calculating and sorting vertex data")
        map = Map(rootNode)

        print("Filtering and updating vertex data")
        polyManager = PolyManager(map)

        print("Writing data to Output folder")
        writer = Writer("Output/" + mapName,
                        polyManager.polyMap, polyManager.filepathMap)
        writer.write()
        print("Done")
