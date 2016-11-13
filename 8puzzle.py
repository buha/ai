import time

class EightPuzzle:
    def __init__(self):

        self._state = [[0, 2, 3],
                       [7, 4, 6],
                       [5, 1, 8]]
        '''
        self._state = [[1, 8, 3],
                       [7, 2, 0],
                       [4, 6, 5]]'''
        self._goal_state = [[1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 0]]
        self._parent = None
        self._depth = 0

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self._state == other._state

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self._state[row][:])) + '\n\r'
        return res

    def find(self, value):
        for row in range(3):
            for col in range(3):
                if self._state[row][col] == value:
                    return row, col


    def actions(self):
        actions = []
        row, col = self.find(0)
        if col > 0:
            actions.append('W')
        if col < 2:
            actions.append('E')
        if row > 0:
            actions.append('N')
        if row < 2:
            actions.append('S')
        return actions

    def _clone(self):
        p = EightPuzzle()
        for i in range(3):
            p._state[i] = self._state[i][:]
        return p

    def act(self, action):
        x, y = self.find(0)
        xdev = 0
        ydev = 0
        if action is 'N':
            xdev = -1
        elif action is 'S':
            xdev = 1
        elif action is 'E':
            ydev = 1
        elif action is 'W':
            ydev = -1

        c = self._clone()
        c._state[x][y], c._state[x + xdev][y + ydev] = c._state[x + xdev][y + ydev], c._state[x][y]
        return c

    def solution(self, path):
        if self._parent == None:
            return path
        else:
            path.append(self)
        return self._parent.solution(path)

    def solve(self):
        def goal_test(node):
            return node._state == node._goal_state

        if goal_test(self):
            return self.solution([])

        frontier = [self]
        explored = []

        while len(frontier) > 0:
            node = frontier.pop(0)
            explored.append(node)

            # find possible actions
            actions = node.actions()

            # execute them
            successors = map(node.act, actions)
            for child in successors:
                if child not in explored and child not in frontier:
                    child._parent = node
                    child._depth = node._depth + 1
                    explored.append(child)
                    if goal_test(child):
                        return child.solution([])
                    else:
                        frontier.append(child)
        return None




def main():
    problem = EightPuzzle()
    print(problem)

    start = time.process_time()
    solution = problem.solve()
    stop = time.process_time()

    solution.reverse()
    for step in solution:
        print(step)

    print("Solution found in {0:0.5f}s".format(stop - start))
    print("{0} steps".format(len(solution)))

if __name__ == "__main__":
    main()
