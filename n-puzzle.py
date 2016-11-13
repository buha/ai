from search import *
import time
import math

class EightPuzzle(Problem):
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

        # check if the initial state is valid

        for n in range(len(initial) ** 2 - 1):
            if self.findvalue(initial, n) == None:
                raise ValueError('The input puzzle has a missing ' + str(n))

        if not goal:
            # compute the goal automatically if not explicitly given
            temp = tuple(i + 1 for i in range(len(initial) ** 2 - 1)) + (0,)
            self.goal = tuple(temp[i:i+len(initial)] for i in range(0, len(temp), len(initial)))

        # pre-compute the goal positions in order to avoid computing them while searching
        self.goalPositions = {}
        for number in range(len(self.goal) ** 2 - 1):
            self.goalPositions[number] = self.findvalue(self.goal, number)

    def findvalue(self, doublelist, value):
        for row in range(len(doublelist)):
            for col in range(len(doublelist)):
                if doublelist[row][col] == value:
                    return row, col
        return None

    def actions(self, state):
        actions = []
        x, y = self.findvalue(state, 0)
        if y > 0:
            actions.append('W')
        if y < len(self.initial) - 1:
            actions.append('E')
        if x > 0:
            actions.append('N')
        if x < len(self.initial) - 1:
            actions.append('S')
        return actions
    
    def result(self, state, action):
        x, y = self.findvalue(state, 0)
        #print('Performing result({0},{1} '.format(state, action))
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

        #print('x={2}, y={3}, Computed an xdev={0} and ydev={1}'.format(xdev, ydev, x, y))
        s = [list(x) for x in state]
        s[x][y], s[x+xdev][y+ydev] = s[x+xdev][y+ydev], s[x][y]

        return tuple(tuple(x) for x in s)

    def heuristic(self, node, item_total_calc, total_calc):
        '''Returns an *estimation* of the distance from a state to the goal.
           We are using the manhattan distance.
        '''
        distance = 0

        for number in range(len(self.initial) ** 2 - 1):
            row_n, col_n = self.findvalue(node.state, number)
            row_n_goal, col_n_goal = self.findvalue(self.goal, number)

            distance += item_total_calc(row_n, row_n_goal, col_n, col_n_goal)

        return total_calc(distance)

    def h_manhattan(self, puzzle):
        return self.heuristic(puzzle,
                    lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                    lambda t: t)

    def h_manhattan_lsq(self, puzzle):
        return self.heuristic(puzzle,
                              lambda r, tr, c, tc: (abs(tr - r) + abs(tc - c)) ** 2,
                              lambda t: math.sqrt(t))

    def h_linear(self, puzzle):
        return self.heuristic(puzzle,
                              lambda r, tr, c, tc: math.sqrt(math.sqrt((tr - r) ** 2 + (tc - c) ** 2)),
                              lambda t: t)

    def h_linear_lsq(self, puzzle):
        return self.heuristic(puzzle,
                              lambda r, tr, c, tc: (tr - r) ** 2 + (tc - c) ** 2,
                              lambda t: math.sqrt(t))

def main():
    # formulate the problem
    #initialState = ((2, 0, 4), (1, 6, 3), (7, 5, 8)) # 9-step
    initialState = ((3, 7, 6), (1, 2, 8), (5, 0, 4)) # 17-step
    #initialState = ((2, 8, 7), (5, 1, 6), (4, 0, 3)) # 25-step

    #initialState = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (0, 13, 14, 15))
    #initialState = ((5, 1, 11, 4), (2, 0, 3, 15), (12, 6, 8, 10), (9, 14, 13, 7))
    problem = EightPuzzle(initialState)

    start = time.process_time()
    solution = astar_search(problem, problem.h_manhattan).solution()
    end = time.process_time()
    print('Manhattan found {2}-step solution: {0} in {1:0.5f} seconds?'.format(solution, end - start, len(solution)))

    start = time.process_time()
    solution = astar_search(problem, problem.h_manhattan_lsq).solution()
    end = time.process_time()
    print('Manhattan LSQ found {2}-step solution: {0} in {1:0.5f} seconds?'.format(solution, end - start, len(solution)))

    start = time.process_time()
    solution = astar_search(problem, problem.h_linear).solution()
    end = time.process_time()
    print(
        'Linear found {2}-step solution: {0} in {1:0.5f} seconds?'.format(solution, end - start, len(solution)))

    start = time.process_time()
    solution = astar_search(problem, problem.h_linear_lsq).solution()
    end = time.process_time()
    print(
        'Linear LSQ found {2}-step solution: {0} in {1:0.5f} seconds?'.format(solution, end - start, len(solution)))

if __name__ == "__main__":
    main()


