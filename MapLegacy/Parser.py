from lark import Lark, tree

grammar = r"""

start: map
map: entity+
entity: "{" property+ ("{" (brush | patch) )* "}"
property: ESCAPED_STRING _SPACE ESCAPED_STRING

patch: "patchDef2" "{" STRING vector5d "(" bezierline+ ")" "}" "}"
brush:  plane plane plane+ "}"
plane: vector3d _SPACE vector3d _SPACE vector3d _SPACE STRING _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER

bezierline: "(" _SPACE vector5d _SPACE vector5d _SPACE (vector5d _SPACE)+ ")"
vector5d: "(" _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE ")"
vector3d: "(" _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE SIGNED_NUMBER _SPACE ")"

COMMENT: "//" /[^\n]/*
STRING:  (("a".."z") | ("A".."Z") | "/" | "-" | "_" | "0".."9")+
SIGNED_NUMBER: ("+" | "-")? NUMBER
_SPACE: " "+

%import common.NUMBER
%import common.ESCAPED_STRING
%import common.NEWLINE
%ignore NEWLINE
%ignore COMMENT
"""


class Parser:
    def __init__(self, filePath):
        self.filePath = filePath
        self.file = open(filePath, "r")

    def parse(self):
        parser = Lark(grammar, parser="lalr")
        root = parser.parse(open(self.filePath).read())
        self.file.close()
        return root.children[0]
