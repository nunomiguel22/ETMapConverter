from Polygon import Polygon
from Plane import Plane

import glm


class Mesh:
    def __init__(self, brush):
        self.brush = brush
        self.polygons = []
        for plane in brush.planes:
            self.polygons.append(Polygon(plane))
        self.__calcVertices()
        self.__sortPolyVertices()

    def __calcVertices(self):
        for i in range(self.size() - 2):
            for j in range(i, self.size() - 1):
                for k in range(j, self.size()):
                    if i == j or i == k or j == k:
                        continue

                    pln1 = self.polygons[i].plane
                    pln2 = self.polygons[j].plane
                    pln3 = self.polygons[k].plane

                    hasInter, vertex = Plane.calcIntersection(pln1, pln2, pln3)

                    if hasInter:
                        if not self.isVertexIllegal(vertex):
                            self.polygons[i].addVertex(vertex)
                            self.polygons[j].addVertex(vertex)
                            self.polygons[k].addVertex(vertex)

    def __sortPolyVertices(self):
        for polygon in self.polygons:
            polygon.calcCenter()
            polygon.sortVertices()

    def size(self):
        return len(self.polygons)

    def isVertexIllegal(self, vertex):
        illegal = False

        for polygon in self.polygons:
            pln = polygon.plane
            pointcls = pln.classifyPoint(vertex)
            if pointcls == "FRONT":
                return True
        return illegal
