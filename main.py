import random
import copy

class Truck:
    def __init__(self, name, capacity):
        """initialize the truck object"""
        self.name = name
        self.capacity = capacity
        self.path = []

class Space:
    def __init__(self):
        """Initialize the map of the city and the trucks using the input.txt file.

        Reads the input from the input.txt file, which contains the following:
        - The first n lines of this file contain the city map as n x n matrix (elements in the rows are separated by comma)
        - n+1 line onwards, are the information about the trucks that belong to the courier service in the format truck_<<number>>#<<capacity>>

        The city map is represented as a 2D array using lists, where each inner list represents a row of the map.
        The trucks are represented as a list of Truck objects.

        Attributes:
        cityMap (list): A list of lists representing the map of the city.
        trucks (list): A list of Truck objects representing the trucks.
        path_of_trucks (list): A list of lists representing the path of each truck.
        """
        self.cityMap = []
        self.trucks = []
        self.path_of_trucks = []

        with open("input.txt") as f:
            contents = f.read()
            contents = contents.splitlines()

            n = len(contents[0].split(",")) # number of delivery locations + courier service station
            no_of_trucks = len(contents) - n

            # creating the map of the city as a 2D array
            for i in range(n):
                content_row = contents[i]
                content_row = content_row.split(",")
                self.cityMap.append(content_row)

            # creating the list of trucks
            for i in range(no_of_trucks):
                capacity = int(contents[n + i].split("#")[-1])
                self.trucks.append(Truck((i), capacity))


    def get_initial_state(self, trucks):
        """
        Returns the initial state of the solution which is a set of cities assigned for each truck (path_of_trucks).
        
        Args:
        - trucks (list): A list of Truck objects representing the trucks available.
        
        Returns:
        - path_of_trucks (list): A list of lists representing the cities assigned to each truck.
        """

        namesOfCities = [x for x in range(1, len(self.cityMap))] # list of cities in the city map without the courier service station (ex: 1,2,3...n)
        random.shuffle(namesOfCities) # shuffle the list of cities to assign them randomly to the trucks, creating a random intial state
        path_of_trucks = []

        for i in range(len(trucks)): 
            no_of_deliveries = 0
            truck_i_path = [] # list of cities assigned to i th truck

            # assign cities to the i th truck until the truck's capacity is reached
            while no_of_deliveries < self.trucks[i].capacity :
                no_of_deliveries += 1
                truck_i_path.append(namesOfCities.pop()) # last element of the list is popped and added to the truck's path, resulting a random city assignment because of the shuffle
            path_of_trucks.append(truck_i_path) # add the truck's path to the list of paths of all trucks
            
        # calculate the cost of the path of each truck and update the city map with the cost of the path
        for i in range(len(self.cityMap)):
            for j in range(i, len(self.cityMap)):
                if self.cityMap[i][j] == "N": # for the cities with no direct connections, calculate the minimum cost of the path using dijkstras algorithm
                    cost = self.get_min_cost_of_path(i, j)
                    self.cityMap[i][j] = cost 
                    self.cityMap[j][i] = cost # update the cost of the path for the other direction because the city map is undirected
                else:
                    # convert string values of cost of the path to an integer
                    self.cityMap[i][j] = int(self.cityMap[i][j])
                    self.cityMap[j][i] = int(self.cityMap[j][i]) 

        return(path_of_trucks)
    

    def get_min_cost_of_path(self, start, end):
        """
        Returns the minimum cost of a path between two cities using Dijkstra's algorithm.

        Args:
        - start: starting city
        - end: destination city

        Returns:
        - An integer representing the minimum cost of the path from start to end.
        """
        map = self.cityMap
        no_of_cities = len(map)
        visited = [False] * no_of_cities
        distance = [float("inf")] * no_of_cities 
        distance[start] = 0

        for i in range(no_of_cities):
            min_dist = float("inf")
            min_index = -1
            for j in range(no_of_cities): # find the city with the minimum distance from the start city
                if visited[j] == False and distance[j] < min_dist:
                    min_dist = distance[j]
                    min_index = j
            
            visited[min_index] = True
            neighbours = self.get_neighbours(min_index)
            for neighbour in neighbours: # update the distance of the neighbours of the min_index city
                if visited[neighbour] == False and map[min_index][neighbour] != "N" and map[min_index][neighbour] != "0":
                    if distance[neighbour] > distance[min_index] + int(map[min_index][neighbour]): # if the distance of the neighbour is greater than the distance of the min_index city + the cost of the path between them, update the distance of the neighbour
                        distance[neighbour] = distance[min_index] + int(map[min_index][neighbour])
        
        return distance[end]


            
    def get_neighbours(self, city):
        """
        Returns the set of neighbours of a given city.

        Args:
            city (int): The integer representation of the city to get the neighbours of.

        Returns:
            List[int]: A list of integers representing the indices of the neighbouring cities.
        """
        map = self.cityMap
        neighbours = []
        for j in range(len(map)):
            if(map[city][j] != "N" and map[city][j] != "0"):
                neighbours.append(j)

        return neighbours
                
    def hill_climb(self, maxima=20):
        """Performs the hill climbing algorithm to find the best solution.

        Args:
            maxima (int): The maximum number of iterations to perform the hill climbing algorithm.

        Returns:
            tuple: A tuple containing the final cost of the solution and the path of each truck.
        """
        final_cost = 0
        no_of_cities = len(self.cityMap)

        self.path_of_trucks = self.get_initial_state(self.trucks) # get a random initial state of the solution using the get_initial_state() method
        
        # calculating the cost of the initial state
        for i in range(len(self.path_of_trucks)):
            truck_path = self.path_of_trucks[i]
            truck_path.insert(0, 0) # add the courier service station to the beginning of the path of each truck
            for j in range(len(truck_path)-1): # calculate the cost of the path of each truck
                final_cost += self.cityMap[truck_path[j]][truck_path[j+1]]

        # now final_cost contains the cost of the initial state

        count = 0
        # perform the hill climbing algorithm until the maximum number of iterations is reached
        while(count < maxima): #maxima can be changed to a different value or the default value (20) will be used
            count += 1
            current_cost = 0

            copyof_trucks = copy.deepcopy(self.path_of_trucks) # create a copy of the path_of_trucks to perform the hill climbing algorithm
            
            # randomly select two cities to swap them to get a new state
            city1 = random.randrange(1, no_of_cities) # 0 is the courier service station, so it is omitted
            city2 = random.randrange(1, no_of_cities)
            while city2 == city1: # if the same city is selected, select another city
                city2 = random.randrange(1, no_of_cities)

            # swap the two cities in the path of the trucks (copyof_trucks)
            for i in range(len(copyof_trucks)):
                truck_path = copyof_trucks[i]
                #if cities are in the same truck's path
                if city1 in truck_path and city2 in truck_path:
                    index1 = truck_path.index(city1)
                    index2 = truck_path.index(city2)
                    truck_path[index1], truck_path[index2] = truck_path[index2], truck_path[index1] # swap the two cities(this will change the order of the truck visits)
                    copyof_trucks[i] = truck_path
                    break

                # if cities are in different paths
                # swap the cities in the paths of the trucks
                elif city1 in truck_path:
                    index1 = truck_path.index(city1)
                    truck_path[index1] = city2
                    copyof_trucks[i] = truck_path
                    
                elif city2 in truck_path:
                    index2 = truck_path.index(city2)
                    truck_path[index2] = city1
                    copyof_trucks[i] = truck_path
            
            #calculate the cost of the new paths of the trucks           
            for i in range(len(copyof_trucks)):
                truck_path = copyof_trucks[i]
                for j in range(len(truck_path)-1):
                    current_cost += self.cityMap[truck_path[j]][truck_path[j+1]]
            
            # if the cost of the new state is less than the cost of the previous state, update the final cost and the path of the trucks
            if(current_cost < final_cost):
                final_cost = current_cost
                self.path_of_trucks = copy.deepcopy(copyof_trucks)

        return (final_cost, self.path_of_trucks)

    def random_restart(self, maxima=None):
        """Performs the hill climbing algorithm with random restarts to find the optimal solution.
        
            Args:
                - maxima (int): The maximum number of iterations to perform the hill climbing algorithm.
            
            Returns:
                - tuple: A tuple containing the final cost of the solution and the path of each truck.

            This function will create the output text file with the results.
            """
        
        lowest_cost = float("inf") # initialize the lowest cost to infinity
        lowest_cost_truck_paths = []

        if maxima == None:
            maxima = len(self.cityMap) * len(self.cityMap) # maxima is set to the square of number of cities in the city map

        count = 0
        # perform the hill climbing algorithm with random restarts until the maximum number of iterations is reached
        while count < maxima:
            count += 1                
            curr_cost = 0
            curr_truck_paths = []
            self.path_of_trucks = self.get_initial_state(self.trucks) # get a random initial state for each random restart

            curr_cost, curr_truck_paths = self.hill_climb() # perform the hill climbing algorithm for each random restart

            # update the lowest cost and the path of the trucks, if the cost of the current state is less than the lowest cost already found
            if curr_cost < lowest_cost:
                lowest_cost = curr_cost
                lowest_cost_truck_paths = curr_truck_paths
        
        # print the lowest cost and the path of the trucks
        print(f"\nlowest cost: {lowest_cost}")
        print(f"lowest cost truck paths: {lowest_cost_truck_paths}")
        
        self.output_result(lowest_cost, lowest_cost_truck_paths) # write the result into a text file

        return (lowest_cost, lowest_cost_truck_paths)
    
    def output_result(self, cost, truck_paths):
        """
            Writes the output to a text file which is named with my index number (210262P.txt).

            Args:
            - cost (int): The cost of the solution.
            - truck_paths (list): A list of lists representing the path of each truck.
        """

        with open("210262P.txt", "w") as output_file: # open the text file

            for i in range(len(truck_paths)):
                truck_path = truck_paths[i]
                output_line = f"truck_{i+1}#" # a string is used to easily remove the last comma(,)

                for j in range(1,len(truck_path)):
                    destination = chr(truck_path[j] + 96) # convert the city index to the city name (ex: 1 -> a, 2 -> b, 3 -> c...)
                    output_line += f"{destination},"

                output_file.write(output_line[:-1] + "\n") # remove the last comma(,) and add a new line character(\n) and write the line to the text file

            output_file.write(f"{cost}") # write the cost of the optimal solution found

            output_file.close()
            
# create a Space object and call the random_restart() method to find the optimal solution
myMap = Space()
myMap.random_restart()