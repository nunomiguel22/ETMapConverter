from MapLegacy import __version__, __author__
from Config import config


class Writer:
    def __init__(self, filepath, polyMap, filepathMap):
        self.filepath = filepath
        self.polyMap = polyMap
        self.filepathMap = filepathMap

        self.verticesStr = "\n#Vertices:\n"
        self.normalStr = "\n#Normals:\n"
        self.texCoordStr = "\n#Texture Coordinates:\n"
        self.faceStr = "\n#Faces:\n"
        self.vertexIndex = 0
        self.normalIndex = 0

    def __vec3Str(self, vec3):
        return str(round(vec3.x, 3)) + " " + str(round(vec3.y, 3)) + " " + str(round(vec3.z, 3))

    def __vec2Str(self, vec2):
        return str(round(vec2.x, 3)) + " " + str(round(vec2.y, 3))

    def writeVertex(self, vert):
        self.verticesStr += "v " + vert.pointObjStr() + "\n"

    def writeNormal(self, normal):
        self.normalStr += "vn " + self.__vec3Str(normal) + "\n"

    def writeTexCoord(self, vert):
        self.texCoordStr += "vt " + vert.texCoordObjStr() + "\n"

    def writePoly(self, poly):
        faceStr = "f"
        self.normalIndex += 1
        self.writeNormal(poly.plane.normal)
        for vertex in poly.vertices:
            self.vertexIndex += 1
            self.writeVertex(vertex)
            self.writeTexCoord(vertex)
            faceStr += " " + str(self.vertexIndex) + \
                "/" + str(self.vertexIndex) + "/" + str(self.normalIndex)
        self.faceStr += faceStr + "\n"

    def writeMtlGroup(self):
        for tex, polyList in self.polyMap.items():
            self.faceStr += "usemtl " + tex + "\n"
            for poly in polyList:
                self.writePoly(poly)

    def writeUngrouped(self):
        for polyList in self.polyMap.values():
            for poly in polyList:
                self.writePoly(poly)

    def writeObj(self):
        file = open(self.filepath + ".obj", "w")
        header = "#Wavefront obj created by MapLegacy " + \
            __version__ + " from .map file\n"
        header += "#Author: " + __author__ + "\n\n"
        file.write(header)

        if config.usemtl:
            self.writeMtlGroup()
        else:
            self.writeUngrouped()

        file.write(self.verticesStr + "\n")
        file.write(self.texCoordStr + "\n")
        file.write(self.normalStr + "\n")
        file.write(self.faceStr)
        file.close()

    def writeMTL(self):
        file = open(self.filepath + ".mtl", "w")
        file.write("#MapLegacy " + __version__ + " MTL file\n\n")
        for tex in self.polyMap:
            file.write("newmtl " + tex + "\n")
            file.write(
                "map_Kd " + self.filepathMap[tex].texFilepath + "\n\n\n")
        file.close()

    def write(self):
        self.writeObj()

        if config.writemtl:
            self.writeMTL()
