import json
import csv
from collections import Counter

# Generates the most popular routes based on the frequency of each subroute, allowing repetitions
# and with three displacements
# Change the input and output file paths to match the desired files
# The input has to be the one generated in code 2_route_for_id.py

# Ruta de entrada y salida
input_file = "/home/mmarcrv/Data4good/g_data/id_to_route.json"
output_file = "/home/mmarcrv/Data4good/g_data/popular_routes_3_repetition.json"

# Función para generar subrutas de longitud 4
def generate_subroutes(route):
    return [f"{route[i]}-{route[i+1]}-{route[i+2]}-{route[i+3]}" for i in range(len(route) - 3)]

# Leer el archivo JSON
with open(input_file, "r", encoding="utf-8") as infile:
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
with open(output_file, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    # Escribir encabezados
    writer.writerow(["Subroute", "Frequency"])
    # Escribir datos
    writer.writerows(sorted_subroutes)

print(f"Archivo de frecuencias guardado en: {output_file}")

