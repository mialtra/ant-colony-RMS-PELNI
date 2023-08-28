import numpy as np

# Parameter ACO
num_ants = 10
num_iterations = 10
alpha = 1  # Pheromone factor
beta = 3   # Heuristic factor
rho = 0.1  # Evaporation rate

num_ports = 10
num_vehicles = 1
max_cargo_capacities = 1000
max_passenger_capacities = 1000
max_vehicle_capacities = 1000


# Inisialisasi matriks jarak antar port (dapat diisi dengan jarak acak)
np.random.seed(0)  # Untuk reproduktibilitas
distance_matrix = np.random.randint(10, 100, size=(num_ports, num_ports))
np.fill_diagonal(distance_matrix, 0)

# Inisialisasi list muatan dari setiap port (dapat diisi dengan muatan acak)
#demands = np.random.randint(5, 30, size=num_ports)
cargo_demands = np.array([170, 150, -120, 33, -23, 100, -180, 25, 150, -147])
passenger_demands = np.array([70, 50, -22, 33, -23, 10, -18, 27, 15, -15])
vehicle_demands = np.array([700, 500, -220, 330, -230, 100, -180, 270, 150, -250])
# Inisialisasi pheromone
pheromone_matrix = np.ones((num_ports, num_ports))
    


# Algoritma ACO
for iteration in range(num_iterations):
    ant_routes = []
    print("____________iteration ",iteration),(" _____________________________________")
    
    # Construction phase
    for ant in range(num_ants):
        vehicle_remaining_capacities = max_vehicle_capacities
        cargo_remaining_capacities = max_cargo_capacities
        passenger_remaining_capacities = max_passenger_capacities


        print("-----------Construction Phase-----------")

        print('1. vehicle_remaining_capacities : ',vehicle_remaining_capacities)
        print('2. cargo_remaining_capacities : ',cargo_remaining_capacities)
        print('3. passenger_remaining_capacities : ',passenger_remaining_capacities)

        #memilih titik awalan
        current_port = np.random.randint(num_ports)
        #current_port = 1
        route = [current_port]
        print('5. route : ',route)
        print('6. ant : ',ant)
        
        
        """ Flow 
        I. Kondisi stop :
            1. jumlah rute < jumlah port.
            2. Total demand port <= total muatan kapal
        
        """
        while len(route) <= num_ports and ((sum(cargo_demands[port] for port in route) <= cargo_remaining_capacities)
                                           and (sum(vehicle_demands[port] for port in route) <= vehicle_remaining_capacities)
                                           and (sum(passenger_demands[port] for port in route) <= passenger_remaining_capacities) ):
            next_port = None
            print ('len(route) = ',len(route))
            # Menggunakan rule probabilistik untuk memilih port berikutnya
            probabilities = []
            for port in range(num_ports):
                if port not in route and ((cargo_demands[port] <= cargo_remaining_capacities)
                                          and (passenger_demands[port] <= passenger_remaining_capacities)
                                          and(vehicle_demands[port] <= vehicle_remaining_capacities)):
                    pheromone = pheromone_matrix[current_port][port]
                    distance = distance_matrix[current_port][port]
                    probability = (pheromone ** alpha) * ((1 / distance) ** beta)
                    probabilities.append((port, probability))
            
            if not probabilities:
                break
            
            probabilities = sorted(probabilities, key=lambda x: x[1], reverse=True)
            selected_port = np.random.choice([p[0] for p in probabilities])
            next_port = selected_port
            
            route.append(next_port)
            #vehicle_remaining_capacities[route[-2]] -= demands[next_port]
            print('cargo_remaining_capacities : ',cargo_remaining_capacities)
            print('cargo demands[next_port] : ',cargo_demands[next_port])

            print('vehicle_remaining_capacities : ',vehicle_remaining_capacities)
            print('vehicle demands[next_port] : ',vehicle_demands[next_port])

            print('passenger_remaining_capacities : ',passenger_remaining_capacities)
            print('passenger demands[next_port] : ',passenger_demands[next_port])

            vehicle_remaining_capacities -= vehicle_demands[next_port]
            if vehicle_remaining_capacities > max_vehicle_capacities:
                vehicle_remaining_capacities = max_vehicle_capacities
            
            cargo_remaining_capacities -= cargo_demands[next_port]
            if cargo_remaining_capacities > max_cargo_capacities:
                cargo_remaining_capacities = max_cargo_capacities

            passenger_remaining_capacities -= passenger_demands[next_port]
            if passenger_remaining_capacities > max_passenger_capacities:
                passenger_remaining_capacities = max_passenger_capacities
            
            print('vehicle_remaining_capacities dikurangi demands[next_port] : ',vehicle_remaining_capacities)
            print('cargo_remaining_capacities dikurangi demands[next_port] : ',cargo_remaining_capacities)
            print('passenger_remaining_capacities dikurangi demands[next_port] : ',passenger_remaining_capacities)
            current_port = next_port
        
        ant_routes.append(route)
    
    # Update pheromone
    for i in range(num_ports):
        for j in range(num_ports):
            pheromone_matrix[i][j] *= (1 - rho)
    
    for route in ant_routes:
        total_distance = sum(distance_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        total_distance += distance_matrix[route[-1]][route[0]]  # Kembali ke awal
        
        for i in range(len(route)-1):
            pheromone_matrix[route[i]][route[i+1]] += 1 / total_distance


print("rute optimal = ", route)

total_distance = 0
for i in range(len(route) - 1):
    from_port = route[i]
    to_port = route[i + 1]
    total_distance += distance_matrix[from_port][to_port]

print("Total distance of best route:", total_distance)