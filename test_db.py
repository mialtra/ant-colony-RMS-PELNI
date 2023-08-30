import psycopg2
import psycopg2.extras as extras
from db import db_config as dbconf
import numpy as np

# Membuka koneksi
#connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
connection = psycopg2.connect(**dbconf.db_params)
# Membuat objek cursor
cursor = connection.cursor()

# Contoh query SELECT
query = "SELECT origin_code, destination_code, nautical_distance FROM master_nautical_distance_2"
cursor.execute(query)
results = cursor.fetchall()

# Menampilkan hasil query
data_list = []
for row in results:
    orig_value, dest_value , distance= row
    data_list.append((orig_value, dest_value,distance))

# Menampilkan daftar hasil query
#print(data_list)

# Menutup cursor dan koneksi
cursor.close()
connection.close()
'''
data_list = [('pc1', 'pc1', 0.0), 
             ('pc2', 'pc1', 796.0), 
             ('pc3', 'pc1', 1380.0), 
             ('pc4', 'pc1', 2599.0), 
             ('pc5', 'pc1', 1576.0), 
             ('pc6', 'pc1', 1137.0), 
             ('pc7', 'pc1', 1027.0), 
             ('pc8', 'pc1', 1494.0), 
             ('pc9', 'pc1', 2419.0), 
             ('pc10', 'pc1', 625.0)]
'''
#query_results

# Find unique port codes
port_codes = set()
for item in data_list:
    port_codes.add(item[0])
    port_codes.add(item[1])

port_codes = sorted(port_codes)
num_ports = len(port_codes)

# Initialize distance matrix
distance_matrix = [[0.0] * num_ports for _ in range(num_ports)]

# Fill in distance matrix using data
for item in data_list:
    origin_index = port_codes.index(item[0])
    destination_index = port_codes.index(item[1])
    distance = item[2]
    distance_matrix[origin_index][destination_index] = distance

# Display distance matrix
for row in distance_matrix:
    print(row)
