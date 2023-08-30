import numpy as np

# Jumlah kota/ports
num_cities = 40

# Jumlah kendaraan
num_vehicles = 5

# Maksimum jumlah iterasi
max_iterations = 100

# Matriks jarak antara kota/ports (misalnya, digunakan angka acak dalam contoh ini)
distance_matrix = np.random.randint(10, 100, size=(num_cities, num_cities))
np.fill_diagonal(distance_matrix, 0)  # Jarak kota ke dirinya sendiri adalah 0

# Inisialisasi pheromone pada setiap jalur
pheromone_matrix = np.ones((num_cities, num_cities))

# Algoritma Koloni Semut
for iteration in range(max_iterations):
    # Simulasi pergerakan semut
    for vehicle in range(num_vehicles):
        # Inisialisasi semut di kota awal (misalnya, kota 0)
        current_city = vehicle * (num_cities // num_vehicles)
        unvisited_cities = set(range(num_cities))
        unvisited_cities.remove(current_city)

        # Inisialisasi rute kendaraan
        route = [current_city]

        # Pergi ke kota berikutnya hingga semua kota dikunjungi
        while unvisited_cities:
            next_city = min(
                unvisited_cities,
                key=lambda city: pheromone_matrix[current_city][city]
                / distance_matrix[current_city][city],
            )
            route.append(next_city)
            unvisited_cities.remove(next_city)
            current_city = next_city

        # Kembali ke kota awal untuk menutup rute kendaraan
        route.append(vehicle * (num_cities // num_vehicles))

        # Hitung total panjang rute kendaraan
        total_distance = sum(distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))

        # Update pheromone pada rute yang baru saja dilalui oleh kendaraan
        for i in range(len(route) - 1):
            pheromone_matrix[route[i]][route[i + 1]] += 1.0 / total_distance

    # Penguapan pheromone pada setiap jalur setelah semua kendaraan telah bergerak
    pheromone_matrix *= 0.2

# Menampilkan hasil rute untuk masing-masing kendaraan
for vehicle in range(num_vehicles):
    start_city = vehicle * (num_cities // num_vehicles)
    end_city = (vehicle + 1) * (num_cities // num_vehicles)
    print(f"Rute Kendaraan {vehicle+1}: {route[start_city:end_city+1]}")
