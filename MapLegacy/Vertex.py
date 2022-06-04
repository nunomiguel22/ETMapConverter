import glm


class Vertex:
    def __init__(self):
        self.point = glm.vec3(0)
        self.texCoord = glm.vec2(0)

    def pointObjStr(self):
        return str(round(self.point.x, 3)) + " " + str(round(self.point.y, 3)) + " " + str(round(self.point.z, 3))

    def texCoordObjStr(self):
        return str(round(self.texCoord.x, 3)) + " " + str(round(self.texCoord.y, 3))
