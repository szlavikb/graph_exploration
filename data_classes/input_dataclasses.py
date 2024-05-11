from dataclasses import dataclass

@dataclass
class Node:
    node: str

@dataclass
class graphEdge:
    node_u: Node
    node_v: Node
    weight_uv_edge: int

@dataclass
class graphDetails:
    nodes: list[Node]
    edges: list[graphEdge]

