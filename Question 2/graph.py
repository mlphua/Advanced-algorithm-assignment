"""Generic unweighted directed graph (Question 2).

The graph knows nothing about courses: a vertex can be any hashable object.
Both outgoing and incoming adjacency are stored, so listing the incoming
neighbours of a vertex is O(in-degree) rather than a scan of the whole graph.
"""


class Graph:
    def __init__(self):
        self._outgoing = {}   # vertex -> set of vertices it points to
        self._incoming = {}   # vertex -> set of vertices pointing to it

    def addVertex(self, vertex):
        """Add a new vertex. Returns False if it already exists."""
        if vertex in self._outgoing:
            return False
        self._outgoing[vertex] = set()
        self._incoming[vertex] = set()
        return True

    def addEdge(self, source, target):
        """Add a directed edge source -> target. Returns False if not added."""
        if source not in self._outgoing or target not in self._outgoing:
            raise KeyError("Both vertices must exist in the graph")
        if source == target or target in self._outgoing[source]:
            return False
        self._outgoing[source].add(target)
        self._incoming[target].add(source)
        return True

    def removeEdge(self, source, target):
        """Remove the edge source -> target. Returns True if it existed."""
        if source not in self._outgoing or target not in self._outgoing[source]:
            return False
        self._outgoing[source].remove(target)
        self._incoming[target].remove(source)
        return True

    def listIncomingAdjacentVertex(self, vertex):
        """All vertices that have an edge coming INTO vertex."""
        if vertex not in self._incoming:
            raise KeyError("Vertex not in graph")
        return list(self._incoming[vertex])

    def listOutgoingAdjacentVertex(self, vertex):
        """All vertices that vertex has an edge going OUT to."""
        if vertex not in self._outgoing:
            raise KeyError("Vertex not in graph")
        return list(self._outgoing[vertex])

    def hasEdge(self, source, target):
        return source in self._outgoing and target in self._outgoing[source]

    def hasPath(self, start, goal):
        """True if goal can be reached from start by following edges (DFS)."""
        seen, stack = set(), [start]
        while stack:
            v = stack.pop()
            if v == goal:
                return True
            if v in seen:
                continue
            seen.add(v)
            stack.extend(self._outgoing[v])
        return False

    def vertices(self):
        return list(self._outgoing)

    def __contains__(self, vertex):
        return vertex in self._outgoing

    def __len__(self):
        return len(self._outgoing)
