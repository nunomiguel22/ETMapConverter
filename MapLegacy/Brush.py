from Plane import Plane


class Brush:
    def __init__(self, node):
        self.node = node
        self.planes = []
        for child in node.children:
            self.planes.append(Plane(child))

    def size(self):
        return len(self.planes)
