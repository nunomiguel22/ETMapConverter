from Entity import Entity


class Map:
    def __init__(self, node):
        self.node = node
        self.entities = []
        for child in node.children:
            self.entities.append(Entity(child))
