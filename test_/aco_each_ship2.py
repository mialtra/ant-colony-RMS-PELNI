import numpy as np

# Parameter ACO
num_ants = 10
num_iterations = 2
alpha = 1  # Pheromone factor
beta = 3   # Heuristic factor
rho = 0.1  # Evaporation rate

num_ports = 10
#num_vehicles = 3
#vehicle_capacities = [100, 100, 100,100,100]
num_vehicles = 1
ship_capacities = 200
vehicle_ship_capacities,vehicle_ship_capacities_before = 1000,1000
cargo_ship_capacities, cargo_ship_capacities_before = 1000,1000
passenger_ship_capacities,passenger_ship_capacities_before = 1000,1000

# Inisialisasi matriks jarak antar port (dapat diisi dengan jarak acak)
np.random.seed(0)  # Untuk reproduktibilitas
distance_matrix = np.random.randint(10, 100, size=(num_ports, num_ports))
np.fill_diagonal(distance_matrix, 0)

# Inisialisasi list muatan dari setiap port (dapat diisi dengan muatan acak)
demands = np.random.randint(5, 30, size=num_ports)
passenger_demands = np.array([-70, 50, -22, 33, -23, 10, -18, 27, 15, -15])
cargo_demands = np.array([-10, 14, -22, 30, -130, 70, -90, 20, 50, -75])
vehicle_demands = np.array([-70, 140, -80, 30, -75, 100, -70, 120, 50, -75])

# Inisialisasi pheromone
pheromone_matrix = np.ones((num_ports, num_ports))
    
print ('num_ports :',num_ports)
print ('num_vehicles :',num_vehicles)
print ('distance_matrix : \n',distance_matrix)
print ('demands :',demands)
print ('current_port :', np.random.randint(num_ports))




# Algoritma ACO
for iteration in range(num_iterations):
    ant_routes = []
    
    # Construction phase
    for ant in range(num_ants):
        #vehicle_remaining_capacities = list(vehicle_capacities)
        #vehicle_remaining_capacities = vehicle_capacities
        #vehicle_remaining_capacities = vehicle_ship_capacities
        cargo_remaining_capacities = cargo_ship_capacities
        passenger_remaining_capacities = passenger_ship_capacities
        #print('1. vehicle_remaining_capacities : ',vehicle_remaining_capacities)
        current_port = np.random.randint(num_ports)
        route = [current_port]
        #print('2. route : ',route)
        #print('3. ant : ',ant)
        #print('4. [route[-1] : ',route[-1])
        
        
        """ Flow 
        I. Kondisi stop :
            1. jumlah rute < jumlah port.
            2. Total demand port <= total muatan kapal
        
        """
        #while len(route) < num_ports and sum(demands[port] for port in route) <= vehicle_capacities[0]:
        #while len(route) <= num_ports and sum(demands[port] for port in route) <= vehicle_capacities:
        while len(route) <= num_ports and ((sum(passenger_demands[port] for port in route) <= passenger_ship_capacities) 
                                           and (sum(cargo_demands[port] for port in route) <= cargo_ship_capacities) 
                                           and (sum(vehicle_demands[port] for port in route) <= vehicle_ship_capacities)):
            next_port = None
            
            # Menggunakan rule probabilistik untuk memilih port berikutnya
            probabilities = []
            for port in range(num_ports):
                print('route : ',route)
                
                #if port not in route and demands[port] <= vehicle_remaining_capacities[route[-1]]:
                if port not in route and ((sum(passenger_demands[port] for port in route) <= passenger_ship_capacities) 
                                           and (sum(cargo_demands[port] for port in route) <= cargo_ship_capacities) 
                                           and (sum(vehicle_demands[port] for port in route) <= vehicle_ship_capacities)):
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
            passenger_ship_capacities -= passenger_demands[next_port]
            cargo_ship_capacities -= cargo_demands[next_port]
            vehicle_ship_capacities -= vehicle_demands[next_port]
            
            print('passenger_demands[next_port] : ',passenger_demands[next_port])
            print('cargo_demands[next_port] : ',cargo_demands[next_port])
            print('vehicle_demands[next_port] : ',vehicle_demands[next_port])
            #vehicle_remaining_capacities -= demands[next_port]
            print('vehicle_remaining_capacities dikurangi vehicle_demands[next_port] : ',vehicle_ship_capacities)
            print('cargo_remaining_capacities dikurangi cargo_demands[next_port]) : ',cargo_ship_capacities)
            print('passenger_remaining_capacities dikurangi demands[next_port] : ',passenger_ship_capacities)
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


# Menampilkan hasil rute untuk masing-masing kendaraan
print("rute optimal = ", route)
"""for vehicle in range(num_vehicles):
    start_city = vehicle * (num_cities // num_vehicles)
    end_city = (vehicle + 1) * (num_cities // num_vehicles)
    print(f"Rute Kendaraan {vehicle+1}: {route[start_city:end_city+1]}")
    """