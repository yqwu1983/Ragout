from collections import namedtuple, defaultdict
import sibelia_parser as sp

Colors = ["red", "green", "blue", "yellow", "black"]
Edge = namedtuple("Edge", ["vertex", "color", "distance"])

class Node:
    def __init__(self):
        self.edges = []


def build_graph(permutations, blocks_coords):
    #find duplications
    duplications = set()
    for perm in permutations:
        current = set()
        for block in perm.blocks:
            if abs(block) in current:
                duplications.add(abs(block))
            current.add(abs(block))
    print "Duplications found: ", duplications

    graph = defaultdict(Node)
    color = 0
    for perm in permutations:
        prev = 0
        while abs(perm.blocks[prev]) in duplications:
            prev += 1
        cur = prev + 1
        while True:
            while cur < len(perm.blocks) and abs(perm.blocks[cur]) in duplications:
                cur += 1
            if cur >= len(perm.blocks):
                break

            left_block = perm.blocks[prev]
            right_block = perm.blocks[cur]
            dist = sp.get_blocks_distance(abs(left_block), abs(right_block), color, blocks_coords)
            graph[-left_block].edges.append(Edge(right_block, color, dist))
            graph[right_block].edges.append(Edge(-left_block, color, dist))
            prev = cur
            cur += 1
        color += 1
    return graph

def output_graph(graph, dot_file, trivial_con=False):
    dot_file.write("graph {\n")
    used_vertexes = set()
    for node_id, node in graph.iteritems():
        for edge in node.edges:
            if edge.vertex not in used_vertexes:
                dot_file.write("""{0} -- {1} [color = "{2}"];\n"""
                                .format(node_id, edge.vertex, Colors[edge.color]))
        used_vertexes.add(node_id)

    if trivial_con:
        for i in xrange(max(graph.keys()) + 1):
            dot_file.write("""{0} -- {1} [color = "black"];\n""".format(i, -i))
    dot_file.write("}")


def get_connected_components(graph):
    con_comp = []

    visited = set()
    def dfs(vertex, component):
        visited.add(vertex)
        component.append(vertex)
        for edge in graph[vertex].edges:
            if edge.vertex not in visited:
                dfs(edge.vertex, component)

    for vertex in graph:
        if vertex not in visited:
            con_comp.append([])
            dfs(vertex, con_comp[-1])

    return con_comp