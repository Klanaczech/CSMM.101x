import sys
import re
import copy


class State:
    def __init__(self, state, parent=None):
        self.matrix = state
        self.moves = []
        self.color = 'w'
        self.parent = parent
        self.generate_moves()

    def print_state(self):
        for i in range(3):
            print
            for j in range(3):
                print self.matrix[3*i + j],

    def generate_moves(self):
        i_c = 5
        j_c = 5

        for i in range(3):
            for j in range(3):
                if self.matrix[3*i + j] is 0:
                    i_c = i
                    j_c = j
                    break

        if i_c is not 0:
            temp_matrix = copy.deepcopy(self.matrix)
            temp = temp_matrix[3*i_c + j_c]
            temp_matrix[3*i_c + j_c] = temp_matrix[3*(i_c - 1) + j_c]
            temp_matrix[3*(i_c - 1) + j_c] = temp
            self.moves.append(temp_matrix)

        if j_c is not 0:
            temp_matrix = copy.deepcopy(self.matrix)
            temp = temp_matrix[3*i_c + j_c]
            temp_matrix[3*i_c + j_c] = temp_matrix[3*i_c + (j_c - 1)]
            temp_matrix[3*i_c + (j_c - 1)] = temp
            self.moves.append(temp_matrix)

        if j_c is not 2:
            temp_matrix = copy.deepcopy(self.matrix)
            temp = temp_matrix[3*i_c + j_c]
            temp_matrix[3*i_c + j_c] = temp_matrix[3*i_c + (j_c + 1)]
            temp_matrix[3*i_c + (j_c + 1)] = temp
            self.moves.append(temp_matrix)

        if i_c is not 2:
            temp_matrix = copy.deepcopy(self.matrix)
            temp = temp_matrix[3*i_c + j_c]
            temp_matrix[3*i_c + j_c] = temp_matrix[3*(i_c + 1) + j_c]
            temp_matrix[3*(i_c + 1) + j_c] = temp
            self.moves.append(temp_matrix)


class Graph:
    def __init__(self, first_state):
        self.init_state = State(first_state)
        self.vertices = {str(first_state): self.init_state}
        self.nodes_expanded = 0

    def bfs(self):
        q = list()
        q.append(self.init_state.matrix)

        for v in self.init_state.moves:
            q.append(v)
            self.vertices[str(v)] = State(v, self.init_state.matrix)

        while len(q) > 0:
            u = q.pop(0)

            if str(u) == '[0, 1, 2, 3, 4, 5, 6, 7, 8]':
                print 'Gotcha!'
                print ('Nodes expanded: ' + str(self.nodes_expanded))
                print self.vertices.keys()
                self.finish(u)
                break

            node_u = self.vertices[str(u)]
            if node_u.color == 'w':
                for v in node_u.moves:
                    if str(v) not in self.vertices.keys():
                        self.vertices[str(v)] = State(v, u)
                    node_v = self.vertices[str(v)]
                    if node_v.color is 'w':
                        q.append(v)
                        self.nodes_expanded = self.nodes_expanded + 1

            node_u.color = 'r'

    def dfs(self):
        q = list()
        q.append(self.init_state.matrix)

        for v in reversed(self.init_state.moves):
            q.append(v)
            self.vertices[str(v)] = State(v, self.init_state.matrix)

        while len(q) > 0:
            u = q.pop()
            State(u).print_state()
            print

            if str(u) == '[0, 1, 2, 3, 4, 5, 6, 7, 8]':
                print 'Gotcha!'
                print ('Nodes expanded: ' + str(self.nodes_expanded))
                print self.vertices.keys()
                self.finish(u)
                break

            node_u = self.vertices[str(u)]
            if node_u.color == 'w':
                for v in reversed(node_u.moves):
                    if str(v) not in self.vertices.keys():
                        self.vertices[str(v)] = State(v, u)
                    node_v = self.vertices[str(v)]
                    if node_v.color is 'w':
                        q.append(v)
                        self.nodes_expanded = self.nodes_expanded + 1

            node_u.color = 'r'

    def finish(self, node):
        ptr = self.vertices[str(node)]
        string_list = [node]
        cost = 0

        while ptr.parent is not None:
            string_list.append(ptr.parent)
            ptr = self.vertices[str(ptr.parent)]

        for i in reversed(string_list):
            for a in range(3):
                print
                for b in range(3):
                    print i[3*a + b],
            print
            cost = cost + 1
        print('Cost:' + str(cost))

initial_state = map(int, re.findall('\d+', sys.argv[2]))
g = Graph(initial_state)

if str(sys.argv[1]) == 'dfs':
    g.dfs()
elif str(sys.argv[1]) == 'bfs':
    g.bfs()
else:
    print 'Invalid parameter'
