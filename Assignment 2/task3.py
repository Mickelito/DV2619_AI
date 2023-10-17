"""
Maze and genetic algorithm for Task 3 in Assingment 2 of DV2619
"""
import numpy as np
import random
from datetime import datetime

random.seed(int(datetime.now().timestamp()))

#High value for walls to dissuade algorithm from going through them
WALL = 1000
OPEN = 1

class Maze:
    """
    Create a maze, which is a matrix of nodes with four directions each
    """
    class Node:
        """
        Maze nodes
        """
        def __init__(self, node_id):
            self.node_id = node_id
            self.up = WALL
            self.left = WALL
            self.right = WALL
            self.down = WALL

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

    def get_start(self):
        """
        Get _start node object
        """
        return self._start

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

    def get_end(self):
        """
        Get _end node object
        """
        return self._end

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
        if direction.lower() in ("right", "r"):
            if node_column == self.width - 1:
                print("Error: No node to the right")
                return -1
            self.map[node_row][node_column].right = OPEN
            self.map[node_row][node_column + 1].left = OPEN
        elif direction.lower() in ("left", "l"):
            if node_column == 0:
                print("Error: No node below")
                return -1
            self.map[node_row][node_column].left = OPEN
            self.map[node_row][node_column - 1].right = OPEN
        elif direction.lower() in ("down", "d"):
            if node_row == self.height - 1:
                print("Error: No node below")
                return -1
            self.map[node_row][node_column].down = OPEN
            self.map[node_row + 1][node_column].up = OPEN
        elif direction.lower() in ("up", "u"):
            if node_row == 0:
                print("Error: No node above")
                return -1
            self.map[node_row][node_column].up = OPEN
            self.map[node_row - 1][node_column].down = OPEN
        return 0

    def disconnect_node(self, node_id, direction):
        """
        Disonnect node with id 'node_id' in direction 'direction'
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
        if direction.lower() in ("right", "r"):
            if node_column == (self.width - 1):
                print("Error: No node to the right")
                return -1
            self.map[node_row][node_column].right = WALL
            self.map[node_row][node_column + 1].left = WALL
        elif direction.lower() in ("left", "l"):
            if node_column == (0):
                print("Error: No node below")
                return -1
            self.map[node_row][node_column].left = WALL
            self.map[node_row][node_column - 1].right = WALL
        elif direction.lower() in ("down", "d"):
            if node_row == (self.height - 1):
                print("Error: No node below")
                return -1
            self.map[node_row][node_column].down = WALL
            self.map[node_row + 1][node_column].up = WALL
        elif direction.lower() in ("up", "u"):
            if node_row == (0):
                print("Error: No node above")
                return -1
            self.map[node_row][node_column].up = WALL
            self.map[node_row - 1][node_column].down = WALL
        return 0

    def make_map(self):
        """
        Make a string representing map of maze
        Walls are marked with #
        Paths are .
        Start is marked with S
        End is marked with E
        """
        tot_map_width = self.width * 2 + 1
        map_string_list = [["#"] * tot_map_width]
        for row in self.map:
            map_string_list.append(["#"])
            for node in row:
                map_string_list[-1].append(".")
                if node.up == OPEN:
                    (map_string_list[-2][len(map_string_list[-1]) - 1]) = " "
                if node.right == OPEN:
                    map_string_list[-1].append(" ")
                else:
                    map_string_list[-1].append("#")
            map_string_list.append(["#"] * tot_map_width)
        if self._start:
            start_pos = []
            start_pos.append(self._start.node_id // self.width)
            start_pos.append(self._start.node_id % self.width)
            map_string_list[start_pos[0] * 2 + 1][start_pos[1] * 2 + 1] = "S"
        if self._end:
            end_pos = []
            end_pos.append(self._end.node_id // self.width)
            end_pos.append(self._end.node_id % self.width)
            map_string_list[end_pos[0] * 2 + 1][end_pos[1] * 2 + 1] = "E"
        map_string = ""
        for row in map_string_list:
            for i in row:
                map_string += i
            map_string += "\n"
        return map_string

    def draw_solution(self, solution: list):
        pass

def init_pop(pop_size: int, maze: Maze):
    """
    Generate initial population
    """
    population = []

    for chromosome in range(pop_size):
        node = maze.get_start()
        new_chromosome = []
        for gene in range(48):
            dir_list = ["u", "l", "r", "d"]
            cur_row = node.node_id // maze.width
            cur_col = node.node_id % maze.width
            if cur_row == 0:
                dir_list.remove("u")
            if cur_row == maze.height - 1:
                dir_list.remove("d")
            if cur_col == 0:
                dir_list.remove("l")
            if cur_col == maze.width - 1:
                dir_list.remove("r")
            next_step = random.choice(dir_list)
            if next_step == "u":
                node = maze.map[cur_row - 1][cur_col]
            elif next_step == "l":
                node = maze.map[cur_row][cur_col - 1]
            elif next_step == "r":
                node = maze.map[cur_row][cur_col + 1]
            elif next_step == "d":
                node = maze.map[cur_row + 1][cur_col]
            new_chromosome.append(next_step)

        population.append(new_chromosome)
    return population

def eval_fitness(ind: list, maze: Maze):
    """
    Evaluate fitness of individual
    """
    fitness = 0
    node = maze.get_start()
    for i, gene in enumerate(ind):
        cur_row = node.node_id // maze.width
        cur_col = node.node_id % maze.width
        # give fitness a high penalty for trying to leave the area
        if cur_row == 0 and gene == "u":
            #print("OOB: UP")
            fitness += 10000
            continue
        if cur_row == maze.height - 1 and gene == "d":
            #print("OOB: DOWN")
            fitness += 10000
            continue
        if cur_col == 0 and gene == "l":
            #print("OOB: LEFT")
            fitness += 10000
            continue
        if cur_col == maze.width - 1 and gene == "r":
            #print("OOB: RIGHT")
            fitness += 10000
            continue

        # add cost of wall/open to fitness score
        # give small penalty if trying to move backwards
        if gene == "u":
            fitness += node.up
            if ind[i - 1] == "d":
                fitness += 10
            node = maze.map[cur_row - 1][cur_col]
        elif gene == "l":
            fitness += node.left
            if ind[i - 1] == "r":
                fitness += 10
            node = maze.map[cur_row][cur_col - 1]
        elif gene == "r":
            fitness += node.right
            if ind[i - 1] == "l":
                fitness += 10
            node = maze.map[cur_row][cur_col + 1]
        elif gene == "d":
            fitness += node.down
            if ind[i - 1] == "u":
                fitness += 10
            node = maze.map[cur_row + 1][cur_col]

        if i ==  len(ind) - 1 and node.node_id == maze.get_end().node_id:
            fitness += abs(cur_col - maze.get_end().node_id % maze.width)
            fitness += abs(cur_col - maze.get_end().node_id // maze.width)
            fitness = fitness / 10
        if i == 31 and fitness == 32:
            return fitness

    return fitness

def population_fitness(population: int, maze: Maze):
    fitness = []
    for individual in population:
        fitness.append(eval_fitness(individual, maze))

    return fitness

def selection(population: list, fitness: list):
    """
    Selects individuals to mate
    """
    pop_size = len(population)
    tot_fitness = sum(fitness)
    selection_probs = []
    for score in fitness:
        selection_probs.append(tot_fitness / score)
    selection_probs[selection_probs.index(min(selection_probs))] += selection_probs[selection_probs.index(max(selection_probs))]
    selection_probs[selection_probs.index(max(selection_probs))] = 0
    pairs = []
    for i in range(int(pop_size / 2)):
        pairs.append(random.choices(population, weights = selection_probs, k = 2))
    return pairs

def crossover(parent1: list, parent2: list, maze: Maze):
    """
    Executes crossover function on parents to create two offspring
    """
    ind_size = len(parent1)
    split = random.randint(1, ind_size - 1)
    #split = ind_size // 2
    offspring1 = parent1[:split] + parent2[split:]
    offspring2 = parent2[:split] + parent1[split:]

    return offspring1, offspring2

def mutate(offspring: list, maze: Maze):
    """
    Executes mutation on new offspring
    Picks a random gene and switches it to another direction
    """
    ind_size = len(offspring)
    mut_gene = random.randint(0, ind_size - 1)
    gene = offspring[mut_gene]
    genes = ["u", "l", "r", "d"]
    genes.remove(gene)
    offspring[mut_gene] = random.choice(genes)
    return offspring

def mating(pop: list, fit: list, mutation_rate: float, maze: Maze):
    """
    Selects individuals for mating
    Runs crossover and mutation
    """
    pairs = selection(pop, fit)
    offspring = []
    for pair in pairs:
        offspring.append(crossover(pair[0], pair[1], maze)[0])
        offspring.append(crossover(pair[0], pair[1], maze)[1])
    mutate_prob = [mutation_rate, 1 - mutation_rate]
    for i, offspring_i in enumerate(offspring):
        if random.choices([1, 0], mutate_prob):
            offspring[i] = mutate(offspring_i, maze)

    return offspring

def maze_genetic_algorithm(maze: Maze, pop_size: int, mutation_rate: float, generations: int):
    """
    Genetic algorithm for finding solution to maze
    Chromosomes are lists of directions
    """
    population = init_pop(pop_size, maze)
    fitness = population_fitness(population, maze)
    best_solution = 0
    for gen in range(generations):
        population = mating(population, fitness, mutation_rate, maze)
        fitness = population_fitness(population, maze)
        best_solution = [min(fitness), population[fitness.index(min(fitness))]]
        if gen % 500 == 0:
            print(best_solution)

    return best_solution


def assignment_maze():
    """
    Makes the maze for DV2619 Assignment 2 Task 3
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
    asd = maze_genetic_algorithm(maze, 100, 0.01, 10000)
    print(asd)
    print(eval_fitness(asd[1], maze))
    return 0

if __name__ == "__main__":
    main()
