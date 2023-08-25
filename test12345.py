import numpy as np

# Parameter ACO
num_ants = 10
num_iterations = 2
alpha = 1  # Pheromone factor
beta = 3   # Heuristic factor
rho = 0.1  # Evaporation rate


ports_code = np.array(['Port1','Port2','Port3','Port4','Port5','Port6','Port7','Port8','Port9','Port10'])
num_ports = len(ports_code)
#num_vehicles = 3
#vehicle_capacities = [100, 100, 100,100,100]
num_vehicles = 1
vehicle_max_capacities = 500


# Inisialisasi matriks jarak antar port (dapat diisi dengan jarak acak)
np.random.seed(0)  # Untuk reproduktibilitas
distance_matrix = np.random.randint(10, 100, size=(num_ports, num_ports))
np.fill_diagonal(distance_matrix, 0)

# Inisialisasi list muatan dari setiap port (dapat diisi dengan muatan acak)
#demands = np.random.randint(5, 30, size=num_ports)
demands = np.array([70, 50, -22, 33, -23, 10, -18, 27, 15, -30])
# Inisialisasi pheromone
pheromone_matrix = np.ones((num_ports, num_ports))
    


# Algoritma ACO
for iteration in range(num_iterations):
    ant_routes = []
    print ("iterasi ke = ",iteration)
    
    # Construction phase
    for ant in range(num_ants):
        print("Construction phase............")
        vehicle_remaining_capacities = vehicle_max_capacities
        print('1. vehicle_remaining_capacities sebelum loading port awal : ',vehicle_remaining_capacities)
        # current_port = np.random.randint(num_ports)
        # memilih titik awal
        current_port = 9
        print('2. curent_port = ',current_port,'demand port = ',demands[current_port])
        route = [current_port]
        vehicle_remaining_capacities -= demands[current_port]
        if vehicle_remaining_capacities > vehicle_max_capacities:
            vehicle_remaining_capacities = vehicle_max_capacities
            
        print('3. vehicle_remaining_capacities sesudah loading port awal : ',vehicle_remaining_capacities)
        
        
        """ Flow 
        I. Kondisi stop :
            1. jumlah rute < jumlah port.
            2. Total demand port <= total muatan kapal
        
        """
        while len(route) <= num_ports and sum(demands[port] for port in route) <= vehicle_remaining_capacities:
            next_port = None
            print ('len(route) = ',len(route))
           # print ('sum(demands[port] = ',sum(demands[port]))
            # Menggunakan rule probabilistik untuk memilih port berikutnya
            probabilities = []
            for port in range(num_ports):
                print('iteration port :',port)
                print ('iteration num_ports',num_ports)
                print('route : ',route)
                print('vehicle_remaining_capacities abc : ',vehicle_remaining_capacities)
                
                #if port not in route and demands[port] <= vehicle_remaining_capacities[route[-1]]:
                if port not in route and demands[port] <= vehicle_remaining_capacities:
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
            print('demands[next_port] : ',demands[next_port])
            vehicle_remaining_capacities -= demands[next_port]
            print('vehicle_remaining_capacities dikurangi demands[next_port] : ',vehicle_remaining_capacities)
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