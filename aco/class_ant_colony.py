import numpy as np

def vrp_capacitated_ant_colony_algorithms (num_ants, evaporation_rate, num_iterations,rho,
                                           listPorts,startPorts,distance_matrix,
                                           max_cargo_capacity,max_vehicle_capacity,max_passenger_capacity,
                                           cargo_demands,vehicle_demands,passenger_demands,alpha,beta
                                           ):
    best_route=[]
    total_route=[]

    # Inisialisasi pheromone
    pheromone_matrix = np.ones((len(listPorts), len(listPorts)))

    # Algoritma ACO
    for iteration in range(num_iterations):
        ant_routes = []
        print("____________iteration ",iteration),(" _____________________________________")
    
         # Construction phase
        for ant in range(num_ants):
            vehicle_remaining_capacities = max_vehicle_capacity
            cargo_remaining_capacities = max_cargo_capacity
            passenger_remaining_capacities = max_passenger_capacity

            print("-----------Construction Phase-----------")
            print('1. vehicle_remaining_capacities : ',vehicle_remaining_capacities)
            print('2. cargo_remaining_capacities : ',cargo_remaining_capacities)
            print('3. passenger_remaining_capacities : ',passenger_remaining_capacities)

            #memilih titik awalan
            current_port = startPorts
            #current_port = 1
            route = [current_port]
            print('5. route : ',route)
            print('6. ant : ',ant)
            
        
            while len(route) <= len(listPorts) and ((sum(cargo_demands[port] for port in route) <= cargo_remaining_capacities)
                                            and (sum(vehicle_demands[port] for port in route) <= vehicle_remaining_capacities)
                                            and (sum(passenger_demands[port] for port in route) <= passenger_remaining_capacities) ):
                next_port = None
                print ('len(route) = ',len(route))
                # Menggunakan rule probabilistik untuk memilih port berikutnya
                probabilities = []
                for port in range(len(listPorts)):
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
                if vehicle_remaining_capacities > max_vehicle_capacity:
                    vehicle_remaining_capacities = max_vehicle_capacity
                
                cargo_remaining_capacities -= cargo_demands[next_port]
                if cargo_remaining_capacities > max_cargo_capacity:
                    cargo_remaining_capacities = max_cargo_capacity

                passenger_remaining_capacities -= passenger_demands[next_port]
                if passenger_remaining_capacities > max_passenger_capacity:
                    passenger_remaining_capacities = max_passenger_capacity
                
                print('vehicle_remaining_capacities dikurangi demands[next_port] : ',vehicle_remaining_capacities)
                print('cargo_remaining_capacities dikurangi demands[next_port] : ',cargo_remaining_capacities)
                print('passenger_remaining_capacities dikurangi demands[next_port] : ',passenger_remaining_capacities)
                current_port = next_port
            
            ant_routes.append(route)
    
    # Update pheromone
    for i in range(len(listPorts)):
        for j in range(len(listPorts)):
            pheromone_matrix[i][j] *= (1 - rho)
    
    for route in ant_routes:
        total_distance = sum(distance_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        total_distance += distance_matrix[route[-1]][route[0]]  # Kembali ke awal
        
        for i in range(len(route)-1):
            pheromone_matrix[route[i]][route[i+1]] += 1 / total_distance

    total_distance = 0
    for i in range(len(route) - 1):
        from_port = route[i]
        to_port = route[i + 1]
        total_distance += distance_matrix[from_port][to_port]

    
    return route,total_distance
