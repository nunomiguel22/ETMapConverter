from Brush import Brush
from Mesh import Mesh


class Entity:
    def __init__(self, node):
        self.node = node
        self.properties = {}
        self.brushes = []
        for child in node.children:
            if child.data == "property":
                self.properties[str(child.children[0])] = str(
                    child.children[1])
            elif child.data == "brush":
                self.brushes.append(Brush(child))
        self.meshes = []
        for brush in self.brushes:
            self.meshes.append(Mesh(brush))

    def hasBrushes(self):
        return len(self.brushes) > 0

    def hasMeshes(self):
        return len(self.meshes) > 0
