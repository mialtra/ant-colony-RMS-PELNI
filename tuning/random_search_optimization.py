import numpy as np
import class_ant_colony as caco
import matplotlib.pyplot as plt

# Data dan parameter

num_ports = 10

num_vehicles = 1
max_cargo_capacities = 1000
max_passenger_capacities = 1000
max_vehicle_capacities = 1000

# Inisialisasi matriks jarak antar port (dapat diisi dengan jarak acak)
list_ports = ['port ABC', 'port DEF','port GHI','port JKL','port MNO','port PQR','port STU','port VWX','port YZA','port AAA']
startPorts = 2
np.random.seed(0)  # Untuk reproduktibilitas
distance_matrix = np.random.randint(10, 200, size=(num_ports, num_ports))  # Contoh matriks jarak
np.fill_diagonal(distance_matrix, 0)

# Inisialisasi list muatan dari setiap port (dapat diisi dengan muatan acak)
cargo_demands = np.array([170, 150, -120, 33, -23, 100, -180, 25, 150, -147])
passenger_demands = np.array([70, 50, -22, 33, -23, 10, -18, 27, 15, -15])
vehicle_demands = np.array([700, 500, -220, 330, -230, 100, -180, 270, 150, -250])

# Evaluasi rute
def evaluate_route(route):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i], route[i + 1]]
    return total_distance


# Random Search for Parameter Tuning
best_params = None
best_distance = float('inf')
num_random_searches = 1000  # Jumlah pencarian acak yang akan dilakukan
results = []

for _ in range(num_random_searches):
    num_ants = np.random.choice([50, 100, 200])
    pheromone_decay = np.random.uniform(0.1, 0.3)
    num_iterations = np.random.choice([50, 100, 200])
    alpha =1
    beta=3
    
    route, distance = caco.vrp_capacitated_ant_colony_algorithms(
        num_ants=num_ants,
        evaporation_rate=pheromone_decay, 
        num_iterations=num_iterations,
        rho=pheromone_decay,
        listPorts=list_ports,
        startPorts=startPorts,
        distance_matrix=distance_matrix,
        max_cargo_capacity=max_cargo_capacities,
        max_vehicle_capacity=max_vehicle_capacities,
        max_passenger_capacity=max_passenger_capacities,
        cargo_demands=cargo_demands,
        vehicle_demands=vehicle_demands,
        passenger_demands=passenger_demands,
        alpha=alpha,
        beta=beta
    )
    results.append((num_ants, pheromone_decay, num_iterations, distance))
    
    
    if distance < best_distance:
        best_distance = distance
        best_params = (num_ants, pheromone_decay, num_iterations)

print("Best Parameters:", best_params)
print("Best Distance:", best_distance)
#Best Parameters: (50, 0.2405220234488369, 50)
#Best Distance: 87

# Menampilkan hasil dalam bentuk grafik
x = np.arange(num_random_searches)
distances = [result[3] for result in results]

plt.bar(x, distances, align='center')
plt.xlabel('Random Search Iteration')
plt.ylabel('Distance')
plt.title('Random Search Results for Parameter Tuning')
#plt.xticks(x, [f"Iteration {i+1}" for i in range(num_random_searches)])
plt.show()