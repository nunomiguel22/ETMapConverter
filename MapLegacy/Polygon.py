from Plane import SimplePlane
from Vertex import Vertex
import glm
import math


class Polygon:
    def __init__(self, plane):
        self.plane = plane
        self.vertices = []
        self.center = glm.vec3(0)

    def addVertex(self, point):
        vertex = Vertex()
        vertex.point = point
        self.vertices.append(vertex)

    def size(self):
        return len(self.vertices)

    def calcCenter(self):
        for vertex in self.vertices:
            self.center += vertex.point
        if self.size() > 0:
            self.center /= self.size()

    def sortVertices(self):

        for i in range(self.size() - 2):
            a = glm.normalize(self.vertices[i].point - self.center)
            p3 = self.center + self.plane.normal
            pln = SimplePlane(self.vertices[i].point, self.center, p3)
            smallestAngle = -1
            smallest = -1

            for j in range(i + 1, self.size()):
                if pln.classifyPoint(self.vertices[j].point) != "BACK":
                    b = glm.normalize(self.vertices[j].point - self.center)
                    angle = glm.dot(a, b)

                    if angle > smallestAngle:
                        smallestAngle = angle
                        smallest = j

            temp = self.vertices[smallest]
            self.vertices[smallest] = self.vertices[i + 1]
            self.vertices[i + 1] = temp

        newpln = self.CalcPlaneFromVertices()

        if glm.dot(newpln.normal, self.plane.normal) < 0:
            self.vertices.reverse()

    def CalcPlaneFromVertices(self):
        pln = SimplePlane(0, 0, 0)
        centerMass = glm.vec3(0)

        for i in range(self.size()):
            j = i + 1

            if j >= self.size():
                j = 0

            pln.points[0] += (self.vertices[i].point.y - self.vertices[j].point.y) * \
                (self.vertices[i].point.z + self.vertices[j].point.z)
            pln.points[1] += (self.vertices[i].point.z - self.vertices[j].point.z) * \
                (self.vertices[i].point.x + self.vertices[j].point.x)
            pln.points[2] += (self.vertices[i].point.x - self.vertices[j].point.x) * \
                (self.vertices[i].point.y + self.vertices[j].point.y)

            centerMass += glm.vec3(self.vertices[i].point)

        magnitude = math.sqrt(math.pow(
            pln.normal.x, 2) + math.pow(pln.normal.y, 2) + math.pow(pln.normal.z, 2))

        pln.normal /= magnitude
        centerMass *= self.size()

        pln.d = - glm.dot(centerMass, pln.normal)

        return pln
