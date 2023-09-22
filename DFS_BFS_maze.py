"""
Maze with DFS and BFS search algorithms for Assigment 1 of DV2619
"""

class Maze:
    """
    Create a maze, which is a matrix of nodes with four directions each
    """
    class Node:
        """
        Maze nodes
        """
        def __init__(self, id):
            self.id = id
            self.up = None
            self.left = None
            self.right = None
            self.down = None

    def __init__(self, height, width):
        self._start = None
        self._end = None
        self.height = height
        self.width = width
        self.map = []
        for row in range(height):
            self.map.append([])
            for column in range(width):
                self.map[row].append(self.Node(row * width + column))

    def set_start(self, node_id):
        """
        Set starting node of maze to node 'node_id'
        """
        if self._start is None:
            start_row = node_id // self.width
            start_column = node_id % self.width
            self._start = self.map[start_row][start_column]
            return 0
        print("Error: Start position already set")
        return -1

    def set_end(self, node_id):
        """
        Set finish node of maze to 'node_id'
        """
        if self._end is None:
            end_row = node_id // self.width
            end_column = node_id % self.width
            self._end = self.map[end_row][end_column]
            return 0
        print("Error: End position already set")
        return -1

    def make_map(self):
        """
        Make a string representing map of maze
        Walls are marked with #
        Paths are empty space
        """
        tot_map_width = self.width * 2 + 1
        map_string_list = [["#"] * tot_map_width]
        for row in self.map:
            map_string_list.append(["#"])
            for node in row:
                map_string_list[-1].append(" ")
                if node.up:
                    (map_string_list[-2][len(map_string_list[-1]) - 1]) = " "
                if node.right:
                    map_string_list[-1].append(" ")
                else:
                    map_string_list[-1].append("#")
            map_string_list.append(["#"] * tot_map_width)
        if self._start:
            start_pos = []
            start_pos.append(self._start.id // self.width)
            start_pos.append(self._start.id % self.width)
            map_string_list[start_pos[0] * 2 + 1][start_pos[1] * 2 + 1] = "S"
        if self._end:
            end_pos = []
            end_pos.append(self._end.id // self.width)
            end_pos.append(self._end.id % self.width)
            map_string_list[end_pos[0] * 2 + 1][end_pos[1] * 2 + 1] = "E"
        map_string = ""
        for row in map_string_list:
            for i in row:
                map_string += i
            map_string += "\n"
        return map_string

    def connect_node(self, node_id, direction):
        """
        Connect node with id 'node_id' in direction 'direction'
        'direction' must be in ("up", "u", "left", "l", "right", "r", "down", "d")
        """
        if node_id < 0 or node_id >= (self.height * self.width):
            print("Error: Invalid node number")
            return -1
        if direction.lower() not in ("up", "u", "left", "l", "right", "r", "down", "d"):
            print("Error: Invalid direction")
            return -1
        node_row = node_id // self.width
        node_column = node_id % self.width
        if node_column == (self.width - 1):
            if direction.lower() in ("right", "r"):
                print("Error: No node to the right")
                return -1
        elif node_column == (0):
            if direction.lower() in ("left", "l"):
                print("Error: No node to the left")
                return -1
        elif node_row == (self.height - 1):
            if direction.lower() in ("down", "d"):
                print("Error: No node below")
                return -1
        elif node_row == (0):
            if direction.lower() in ("up", "u"):
                print("Error: No node above")
                return -1
        if direction.lower() in ("right", "r"):
            if self.map[node_row][node_column + 1].left or self.map[node_row][node_column].right:
                print("Error: Already connected")
                return -1
            self.map[node_row][node_column].right = 1
            self.map[node_row][node_column + 1].left = self.map[node_row][node_column]
        elif direction.lower() in ("left", "l"):
            if self.map[node_row][node_column - 1].right or self.map[node_row][node_column].left:
                print("Error: Already connected")
                return -1
            self.map[node_row][node_column].left = 1
            self.map[node_row][node_column - 1].right = self.map[node_row][node_column]
        elif direction.lower() in ("down", "d"):
            if self.map[node_row + 1][node_column].up or self.map[node_row][node_column].down:
                print("Error: Already connected")
                return -1
            self.map[node_row][node_column].down = 1
            self.map[node_row + 1][node_column].up = self.map[node_row][node_column]
        elif direction.lower() in ("up", "u"):
            if self.map[node_row - 1][node_column].down or self.map[node_row][node_column].up:
                print("Error: Already connected")
                return -1
            self.map[node_row][node_column].up = 1
            self.map[node_row - 1][node_column].down = self.map[node_row][node_column]
        return 0

    def BFS(self):
        """
        Solve maze with BFS algorithm
        """
        visited = []
        queue = []
        solved = 0
        queue.append(self._start)
        while len(queue) > 0:
            visited.append(queue.pop(0))
            if visited[-1] == self._end:
                solved = 1
                break
            node_row = visited[-1].id // self.width
            node_column = visited[-1].id % self.width
            if visited[-1].left:
                if self.map[node_row][node_column - 1] not in visited:
                    queue.append(self.map[node_row][node_column - 1])
            if visited[-1].down:
                if self.map[node_row + 1][node_column] not in visited:
                    queue.append(self.map[node_row + 1][node_column])
            if visited[-1].right:
                if self.map[node_row][node_column + 1] not in visited:
                    queue.append(self.map[node_row][node_column + 1])
            if visited[-1].up:
                if self.map[node_row - 1][node_column] not in visited:
                    queue.append(self.map[node_row - 1][node_column])
        if not solved:
            print("End not found")
        visited_id = []
        for node in visited:
            visited_id.append(node.id)
        return visited_id

    def DFS(self, direction = 0, start_node = 0):
        """
        Solve maze with DFS algorithm
        """
        if start_node == 0:
            start_node = self._start
        node_row = start_node.id // self.width
        node_column = start_node.id % self.width
        new_nodes, finished = 0, 0
        visited = []
        visited.append(start_node)
        if start_node == self._end:
            return visited, 1
        if start_node.left and direction != "r" and not finished:
            new_nodes, finished = self.DFS("l", self.map[node_row][node_column - 1])
            visited += new_nodes
        if start_node.down and direction != "u" and not finished:
            new_nodes, finished =self.DFS("d", self.map[node_row + 1][node_column])
            visited += new_nodes
        if start_node.right and direction != "l" and not finished:
            new_nodes, finished =self.DFS("r", self.map[node_row][node_column + 1])
            visited += new_nodes
        if start_node.up and direction != "d" and not finished:
            new_nodes, finished =self.DFS("u", self.map[node_row - 1][node_column])
            visited += new_nodes
        return visited, finished

    def make_solution_map(self):
        """
        Make string representing map of maze with solution marked
        Each node on the path taken is marked with a .
        """
        node = self._end
        solution = []
        while node != self._start:
            if type(node.up) == self.Node:
                solution.append(node.up.id)
                node = node.up
                continue
            elif type(node.left) == self.Node:
                solution.append(node.left.id)
                node = node.left
                continue
            elif type(node.right) == self.Node:
                solution.append(node.right.id)
                node = node.right
                continue
            elif type(node.down) == self.Node:
                solution.append(node.down.id)
                node = node.down
                continue
        solution.reverse()
        tot_map_width = self.width * 2 + 1
        map_string_list = [["#"] * tot_map_width]
        for row in self.map:
            map_string_list.append(["#"])
            for node in row:
                if node.id in solution:
                    map_string_list[-1].append(".")
                else:
                    map_string_list[-1].append(" ")
                if node.up:
                    (map_string_list[-2][len(map_string_list[-1]) - 1]) = " "
                if node.right:
                    map_string_list[-1].append(" ")
                else:
                    map_string_list[-1].append("#")
            map_string_list.append(["#"] * tot_map_width)
        if self._start:
            start_pos = []
            start_pos.append(self._start.id // self.width)
            start_pos.append(self._start.id % self.width)
            map_string_list[start_pos[0] * 2 + 1][start_pos[1] * 2 + 1] = "S"
        if self._end:
            end_pos = []
            end_pos.append(self._end.id // self.width)
            end_pos.append(self._end.id % self.width)
            map_string_list[end_pos[0] * 2 + 1][end_pos[1] * 2 + 1] = "E"
        map_string = ""
        for row in map_string_list:
            for i in row:
                map_string += i
            map_string += "\n"
        return map_string

def assignment_maze():
    """
    Makes the maze for DV2619 Assignment 1
    """
    maze = Maze(7, 20)
    maze.set_start(0)
    maze.set_end(138)
    maze.connect_node(0, "r")
    maze.connect_node(1, "r")
    maze.connect_node(2, "r")
    maze.connect_node(3, "r")
    maze.connect_node(3, "d") #split
    maze.connect_node(23, "l")
    maze.connect_node(22, "l")
    maze.connect_node(21, "l")
    maze.connect_node(20, "d")
    maze.connect_node(40, "r")
    maze.connect_node(41, "r")
    maze.connect_node(42, "d")
    maze.connect_node(62, "r")
    maze.connect_node(63, "d")
    maze.connect_node(83, "l")
    maze.connect_node(82, "l")
    maze.connect_node(81, "u")
    maze.connect_node(61, "l")
    maze.connect_node(60, "d")
    maze.connect_node(80, "d")
    maze.connect_node(100, "d") #dead end
    maze.connect_node(4, "r")
    maze.connect_node(5, "r")
    maze.connect_node(6, "d")
    maze.connect_node(26, "r")
    maze.connect_node(27, "d")
    maze.connect_node(47, "r")
    maze.connect_node(48, "u")
    maze.connect_node(28, "r")
    maze.connect_node(29, "u")
    maze.connect_node(9, "r")
    maze.connect_node(9, "l") #split
    maze.connect_node(8, "l") #dead end
    maze.connect_node(10, "r")
    maze.connect_node(11, "d")
    maze.connect_node(31, "r")
    maze.connect_node(32, "r")
    maze.connect_node(33, "d")
    maze.connect_node(53, "l")
    maze.connect_node(53, "d") #split
    maze.connect_node(52, "l")
    maze.connect_node(51, "l")
    maze.connect_node(50, "u") #dead end
    maze.connect_node(50, "l")
    maze.connect_node(49, "d")
    maze.connect_node(69, "d")
    maze.connect_node(89, "d")
    maze.connect_node(109, "l")
    maze.connect_node(108, "u")
    maze.connect_node(88, "u")
    maze.connect_node(68, "l")
    maze.connect_node(67, "l")
    maze.connect_node(66, "l")
    maze.connect_node(65, "l")
    maze.connect_node(64, "u")
    maze.connect_node(44, "l") #dead end
    maze.connect_node(44, "r")
    maze.connect_node(45, "r") #dead end
    maze.connect_node(45, "u")
    maze.connect_node(25, "l") #dead end
    maze.connect_node(73, "r")
    maze.connect_node(74, "r")
    maze.connect_node(75, "r")
    maze.connect_node(76, "r")
    maze.connect_node(77, "r")
    maze.connect_node(77, "d") #split
    maze.connect_node(78, "r")
    maze.connect_node(79, "u")
    maze.connect_node(59, "u")
    maze.connect_node(39, "l")
    maze.connect_node(38, "u")
    maze.connect_node(18, "r") #dead end
    maze.connect_node(18, "l")
    maze.connect_node(17, "d")
    maze.connect_node(37, "d")
    maze.connect_node(57, "r") #dead end
    maze.connect_node(57, "l")
    maze.connect_node(56, "l")
    maze.connect_node(55, "l")
    maze.connect_node(54, "u")
    maze.connect_node(34, "r")
    maze.connect_node(35, "r")
    maze.connect_node(36, "u")
    maze.connect_node(16, "l")
    maze.connect_node(15, "l")
    maze.connect_node(14, "l")
    maze.connect_node(13, "l") #dead end
    maze.connect_node(97, "l")
    maze.connect_node(97, "d") #split
    maze.connect_node(96, "l")
    maze.connect_node(95, "d")
    maze.connect_node(115, "r") #dead end
    maze.connect_node(117, "d")
    maze.connect_node(117, "r") #split
    maze.connect_node(137, "l")
    maze.connect_node(136, "l")
    maze.connect_node(135, "l")
    maze.connect_node(134, "u")
    maze.connect_node(114, "u")
    maze.connect_node(94, "l")
    maze.connect_node(93, "d")
    maze.connect_node(113, "l")
    maze.connect_node(112, "u")
    maze.connect_node(92, "l")
    maze.connect_node(92, "u") #split
    maze.connect_node(91, "d")
    maze.connect_node(111, "d")
    maze.connect_node(131, "r")
    maze.connect_node(132, "r") #dead end
    maze.connect_node(72, "l")
    maze.connect_node(71, "l")
    maze.connect_node(70, "d")
    maze.connect_node(90, "d")
    maze.connect_node(110, "d")
    maze.connect_node(130, "l")
    maze.connect_node(129, "l")
    maze.connect_node(128, "l")
    maze.connect_node(127, "l")
    maze.connect_node(127, "u") #split
    maze.connect_node(126, "l") #dead end
    maze.connect_node(107, "u")
    maze.connect_node(87, "l")
    maze.connect_node(86, "d")
    maze.connect_node(106, "l")
    maze.connect_node(105, "u")
    maze.connect_node(85, "l")
    maze.connect_node(84, "d")
    maze.connect_node(104, "d")
    maze.connect_node(124, "l")
    maze.connect_node(123, "u")
    maze.connect_node(103, "l")
    maze.connect_node(102, "l")
    maze.connect_node(101, "d")
    maze.connect_node(121, "r") #dead end
    maze.connect_node(118, "u")
    maze.connect_node(98, "r")
    maze.connect_node(99, "d")
    maze.connect_node(119, "d")
    maze.connect_node(139, "l") #end
    return maze

def main():
    maze = assignment_maze()
    print(maze.make_map())

    print("Solve maze:\n   1. BFS\n   2. DFS")
    user_input = input(">> ")
    if user_input not in "12":
        print("Invalid input")
        return -1
    elif user_input == "1":
        print(maze.make_solution_map())
        solution_list = maze.BFS()
        print(solution_list)
        print("Steps taken: " + str(len(solution_list) - 1))
    elif user_input == "2":
        print(maze.make_solution_map())
        solution_list, solved = maze.DFS()
        solution_list_id = []
        for node in solution_list:
            solution_list_id.append(node.id)
        print(solution_list_id)
        print("Steps taken: " + str(len(solution_list_id) - 1))
        if not solved:
            print("Could not find end")
    return 0

if __name__ == "__main__":
    main()