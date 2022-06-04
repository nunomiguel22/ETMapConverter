import glm
import math

from Config import config

baseaxis = [glm.vec3(0, 0, 1), glm.vec3(1, 0, 0), glm.vec3(0, -1, 0),
            glm.vec3(0, 0, -1), glm.vec3(1, 0, 0), glm.vec3(0, -1, 0),
            glm.vec3(1, 0, 0), glm.vec3(0, 1, 0), glm.vec3(0, 0, -1),
            glm.vec3(-1, 0, 0), glm.vec3(0, 1, 0), glm.vec3(0, 0, -1),
            glm.vec3(0, 1, 0), glm.vec3(1, 0, 0), glm.vec3(0, 0, -1),
            glm.vec3(0, -1, 0), glm.vec3(1, 0, 0), glm.vec3(0, 0, -1)]


class Plane:
    def __init__(self, node):
        self.node = node
        self.points = []
        for i in range(3):
            self.points.append(self.nodeToVector3(node.children[i]))
        self.__calcValues()

        self.texName = str(node.children[3])
        shift = [float(node.children[4]), float(node.children[5])]
        rotation = float(node.children[6])
        scale = [float(node.children[7]), float(node.children[8])]
        self.__QuakeTextureVecs(shift, rotation, scale)

    def nodeToVector3(self, node):
        return glm.vec3(float(node.children[0]), float(node.children[1]), float(node.children[2]))

    def __calcValues(self):
        p1 = self.points[1] - self.points[0]
        p2 = self.points[2] - self.points[0]
        self.normal = glm.cross(p2, p1)
        self.normal = glm.normalize(self.normal)
        for val in self.normal:
            if abs(val) < config.epsilon:
                val = 0

        self.d = round(-glm.dot(self.normal, self.points[0]), 5)

    def __TextureAxisFromPlane(self):
        best = 0
        bestaxis = 0
        for i in range(6):
            dot = glm.dot(self.normal, baseaxis[i * 3])
            if dot > best:
                best = dot
                bestaxis = i

        return [glm.vec3(baseaxis[bestaxis*3+1]), glm.vec3(baseaxis[bestaxis*3+2])]

    def __QuakeTextureVecs(self, shift, rotation, scale):
        self.textureVecs = [glm.vec4(0), glm.vec4(0)]
        vecs = self.__TextureAxisFromPlane()

        if scale[0] == 0:
            scale[0] == 1
        if scale[1] == 0:
            scale[1] == 1
        scale[1] *= -1

        if rotation == 0:
            sinv = 0
            cosv = 1
        elif rotation == 90:
            sinv = 1
            cosv = 0
        elif rotation == 180:
            sinv = 0
            cosv = -1
        elif rotation == 270:
            sinv = -1
            cosv = 0
        else:
            ang = math.radians(rotation)
            sinv = math.sin(ang)
            cosv = math.cos(ang)

        if vecs[0][0] != 0:
            sv = 0
        elif vecs[0][1] != 0:
            sv = 1
        else:
            sv = 2

        if vecs[1][0] != 0:
            tv = 0
        elif vecs[1][1] != 0:
            tv = 1
        else:
            tv = 2

        for i in range(2):
            ns = cosv * vecs[i][sv] - sinv * vecs[i][tv]
            nt = sinv * vecs[i][sv] + cosv * vecs[i][tv]
            vecs[i][sv] = ns
            vecs[i][tv] = nt

        for i in range(2):
            for j in range(3):
                self.textureVecs[i][j] = vecs[i][j] / scale[i]

        self.textureVecs[0][3] = shift[0]
        self.textureVecs[1][3] = -shift[1]

    @staticmethod
    def calcIntersection(pln1, pln2, pln3):
        denom = glm.dot(pln1.normal, glm.cross(pln2.normal, pln3.normal))
        if abs(denom) < config.epsilon:
            return False, None

        num1 = pln1.d * glm.cross(pln2.normal, pln3.normal)
        num2 = pln2.d * glm.cross(pln3.normal, pln1.normal)
        num3 = pln3.d * glm.cross(pln1.normal, pln2.normal)
        vertex = (-num1 - num2 - num3) / denom
        return True, vertex

    def distanceToPlane(self, v):
        return glm.dot(self.normal, v) + self.d

    def classifyPoint(self, p):
        dist = self.distanceToPlane(p)
        if dist > config.epsilon:
            return "FRONT"

        if dist < -config.epsilon:
            return "BACK"

        return "ONPLANE"


class SimplePlane:
    def __init__(self, p1, p2, p3):
        self.points = []
        self.points.append(p1)
        self.points.append(p2)
        self.points.append(p3)
        self.__calcValues()

    def __calcValues(self):
        p1 = glm.vec3(self.points[2] - self.points[1])
        p2 = glm.vec3(self.points[0] - self.points[1])
        self.normal = glm.cross(p1, p2)
        self.normal = glm.normalize(self.normal)
        self.d = glm.dot(-self.normal, glm.vec3(self.points[0]))

    def distanceToPlane(self, v):
        return glm.dot(self.normal, v) + self.d

    def classifyPoint(self, p):
        dist = self.distanceToPlane(p)
        if dist > config.epsilon:
            return "FRONT"

        if dist < -config.epsilon:
            return "BACK"

        return "ONPLANE"
