import matplotlib.pyplot as plt

# Inisialisasi parameter dan variabel terkait

best_distances = []  # Menyimpan jarak terbaik dalam setiap iterasi

# Loop iterasi algoritma koloni semut
for iteration in range(100):
    # ... Proses iterasi algoritma koloni semut ...

    best_ant = min(ant_distances)
    best_distances.append(best_ant)

    print(f"Iteration {iteration + 1}: Best distance = {best_ant}")

# Menampilkan grafik
plt.plot(range(1, 101), best_distances, marker='o')
plt.xlabel('Iteration')
plt.ylabel('Best Distance')
plt.title('Best Distance vs. Iteration')
plt.grid(True)
plt.show()
