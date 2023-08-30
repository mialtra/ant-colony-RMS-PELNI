import numpy as np

class AntColonyOptimizer:
    def __init__(self, num_ants, num_iterations, evaporation_rate=0.5, alpha=1.0, beta=1.0):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta

    def solve_ship_route(self, distance_matrix):
        num_ports = distance_matrix.shape[0]
        pheromone_matrix = np.ones((num_ports, num_ports))  # Initialize pheromone matrix

        best_route = None
        best_distance = float('inf')

        for iteration in range(self.num_iterations):
            ant_routes = []

            for ant in range(self.num_ants):
                route = self._construct_route(pheromone_matrix, distance_matrix)
                ant_routes.append(route)

                distance = self._calculate_route_distance(route, distance_matrix)

                if distance < best_distance:
                    best_distance = distance
                    best_route = route

            self._update_pheromone_matrix(pheromone_matrix, ant_routes)

        return best_route, best_distance

    def _construct_route(self, pheromone_matrix, distance_matrix):
        num_ports = pheromone_matrix.shape[0]
        current_port = np.random.randint(num_ports)
        unvisited_ports = set(range(num_ports))
        unvisited_ports.remove(current_port)
        route = [current_port]

        while unvisited_ports:
            next_port = self._select_next_port(current_port, unvisited_ports, pheromone_matrix, distance_matrix)
            route.append(next_port)
            unvisited_ports.remove(next_port)
            current_port = next_port

        route.append(route[0])  # Return to the starting port

        return route

    def _select_next_port(self, current_port, unvisited_ports, pheromone_matrix, distance_matrix):
        pheromone_values = pheromone_matrix[current_port, list(unvisited_ports)]
        attractiveness = 1.0 / (distance_matrix[current_port, list(unvisited_ports)] + 1e-8)
        probabilities = (pheromone_values ** self.alpha) * (attractiveness ** self.beta)
        probabilities /= np.sum(probabilities)

        return np.random.choice(list(unvisited_ports), p=probabilities)

    def _calculate_route_distance(self, route, distance_matrix):
        distance = 0
        num_ports = len(route)

        for i in range(num_ports - 1):
            distance += distance_matrix[route[i], route[i + 1]]

        return distance

    def _update_pheromone_matrix(self, pheromone_matrix, ant_routes):
        pheromone_matrix *= self.evaporation_rate

        for route in ant_routes:
            route_distance = self._calculate_route_distance(route, distance_matrix)
            for i in range(len(route) - 1):
                pheromone_matrix[route[i], route[i + 1]] += 1.0 / route_distance
            pheromone_matrix[route[-1], route[0]] += 1.0 / route_distance

# Example usage
if __name__ == "__main__":
    np.random.seed(42)  # For reproducibility

    # Example distance matrix for 10 ports
    distance_matrix = np.array([[0, 10, 15, 20, 25, 30, 35, 40, 45, 50],
                                [10, 0, 12, 18, 20, 25, 33, 35, 40, 45],
                                [15, 12, 0, 15, 17, 22, 28, 30, 35, 40],
                                [20, 18, 15, 0, 10, 12, 18, 20, 25, 30],
                                [25, 20, 17, 10, 0, 8, 15, 18, 22, 25],
                                [30, 25, 22, 12, 8, 0, 10, 12, 15, 20],
                                [35, 33, 28, 18, 15, 10, 0, 6, 10, 12],
                                [40, 35, 30, 20, 18, 12, 6, 0, 8, 10],
                                [45, 40, 35, 25, 22, 15, 10, 8, 0, 8],
                                [50, 45, 40, 30, 25, 20, 12, 10, 8, 0]])

    num_ants = 200
    num_iterations = 500
    aco = AntColonyOptimizer(num_ants=num_ants, num_iterations=num_iterations)
    best_route, best_distance = aco.solve_ship_route(distance_matrix)

    print("Best Route:", best_route)
    print("Best Distance:", best_distance)
