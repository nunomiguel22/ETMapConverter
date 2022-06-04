import os.path
from os import path

from Config import config
from PIL import Image
import math
import glm


class Texture:
    epsilon = 0.01

    def __init__(self, texpath):
        self.texFilepath = texpath
        self.height = config.defaultTexHeight
        self.width = config.defaultTexWidth


class PolyManager:
    def __init__(self, map):
        self.map = map
        self.degPolyCount = 0
        self.limits = [glm.vec2(-9999, 9999),
                       glm.vec2(-9999, 9999), glm.vec2(-9999, 9999)]
        self.__buildPolyMap()
        self.__calcCenter()
        self.__transform()

    def __buildPolyMap(self):
        self.polyMap = {}
        self.filepathMap = {}
        for entity in self.map.entities:
            for mesh in entity.meshes:
                for polygon in mesh.polygons:
                    self.__addPoly(polygon)

    def __addPoly(self, poly):
        # Ignore degenerate polys
        if poly.size() < 3:
            self.degPolyCount += 1
            return

        # Filter out texture entities
        texName = poly.plane.texName
        for tex in config.texFilter:
            if texName.find(tex) != -1:
                return

        # Add Poly to polymap
        if texName in self.polyMap:
            self.polyMap[texName].append(poly)
        else:
            self.polyMap[texName] = []
            self.polyMap[texName].append(poly)
            self.__setupTexture(texName)

        self.__calculateTextureCoordinates(poly, self.filepathMap[texName])

    def __setupTexture(self, texName):
        # Add correct filepath to mtl information
        if path.exists(config.texFolder + texName + ".tga"):
            texPath = config.mtlTexFolder + \
                texName + ".tga"
            tex = Texture(texPath)
            im = Image.open(config.texFolder + texName + ".tga")
            tex.width, tex.height = im.size

        else:
            texPath = config.mtlTexFolder + \
                texName + ".jpg"
            tex = Texture(texPath)
            if path.exists(config.texFolder + texName + ".jpg"):
                im = Image.open(config.texFolder + texName + ".jpg")
                tex.width, tex.height = im.size
        self.filepathMap[texName] = tex

    def __calculateTextureCoordinates(self, polygon, texture):
        mins = glm.vec2(99999, 99999)
        vecs = polygon.plane.textureVecs

        for vertex in polygon.vertices:
            self.__updateLimits(vertex)
            dot = glm.dot(glm.vec3(vecs[0]), vertex.point)
            vertex.texCoord[0] = vecs[0][3] + dot
            dot = glm.dot(glm.vec3(vecs[1]), vertex.point)
            vertex.texCoord[1] = vecs[1][3] + dot

            vertex.texCoord[0] /= texture.width
            vertex.texCoord[1] /= texture.height

        for i in range(2):
            if vertex.texCoord[i] - math.floor(vertex.texCoord[i]) <= Texture.epsilon:
                vertex.texCoord[i] = math.floor(vertex.texCoord[i])

            if math.ceil(vertex.texCoord[i]) - vertex.texCoord[i] <= Texture.epsilon:
                vertex.texCoord[i] = math.ceil(vertex.texCoord[i])
            if vertex.texCoord[i] < mins[i]:
                mins[i] = vertex.texCoord[i]

        for i in range(2):
            mins[i] = math.floor(mins[i])

        for vertex in polygon.vertices:
            vertex.texCoord -= mins

    def __updateLimits(self, vertex):
        for i in range(3):
            if vertex.point[i] > self.limits[i][0]:
                self.limits[i][0] = vertex.point[i]

            if vertex.point[i] < self.limits[i][1]:
                self.limits[i][1] = vertex.point[i]

    def __calcCenter(self):
        self.center = glm.vec3(0)
        for i in range(3):
            self.center[i] = (self.limits[i][0] + self.limits[i][1]) / 2

    def __transform(self):
        mat = glm.identity(glm.mat4)
        mat2 = glm.identity(glm.mat4)

        if config.scale != 0 and config.scale != 1:
            mat = glm.scale(mat, glm.vec3(config.scale))

        if config.zUpwards:
            mat = glm.rotate(mat, math.radians(90), glm.vec3(1, 0, 0))
            mat2 = glm.rotate(mat2, math.radians(90), glm.vec3(1, 0, 0))

        for polyList in self.polyMap.values():
            for polygon in polyList:
                if config.zUpwards:
                    polygon.plane.normal = glm.vec4(
                        polygon.plane.normal, 1) * mat2
                for vertex in polygon.vertices:
                    vertex.point = glm.vec4(vertex.point, 1) * mat
