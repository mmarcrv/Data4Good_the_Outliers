import json
import csv
from collections import Counter


# Create a file containing the most popular routes based on the frequency of each subroute

# Change the input and output file paths to match the desired files
# The input has to be the one generated in code 2_route_for_id.py
input_file = "/home/mmarcrv/Data4good/j_data/id_to_route_j.json"
output_file = "/home/mmarcrv/Data4good/j_data/popular_routes_j.json"

# Función para generar subrutas de longitud 2
def generate_subroutes(route):
    return [f"{route[i]}-{route[i+1]}-{route[i+2]}" for i in range(len(route) - 2)]

# Leer el archivo JSON
with open(input_file, "r") as infile:
    data = json.load(infile)

# Contador para las subrutas
subroute_counter = Counter()

# Procesar cada ruta en el archivo
for record in data:
    route = record["Route"]
    subroutes = generate_subroutes(route)
    subroute_counter.update(subroutes)

# Ordenar las rutas por frecuencia
sorted_subroutes = subroute_counter.most_common()

# Guardar los resultados en un archivo CSV
with open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    # Escribir encabezados
    writer.writerow(["Subroute", "Frequency"])
    # Escribir datos
    writer.writerows(sorted_subroutes)

print(f"Archivo de frecuencias guardado en: {output_file}")
