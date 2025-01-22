import pandas as pd
import json

# This file generates a dictionary that maps each ID to a list of coordinates representing the route of the ID
# Change the input file path to the path of the CSV file containing the data
# the input has to be the file generated in code 1_extraction_of_data.py

# Cargar el archivo CSV
input_file = "/home/mmarcrv/Data4good/j_data/movement_id_data_j.csv"
output_file = "/home/mmarcrv/Data4good/j_data/id_to_route_j.json"

df = pd.read_csv(input_file)

# Crear una lista para las rutas de cada TD
routes = []

# Agrupar por TD
grouped = df.groupby("ID")

for ID, group in grouped:

    # Crear la lista de coordenadas, asegurándonos de que no se repitan las consecutivas
    route = [group.iloc[0]["Origin Coordinates"]]  # Comenzar con el origen inicial
    route += group["Destination Coordinates"].tolist()  # Agregar todos los destinos
    
    # Añadir al resultado final
    routes.append({"ID": ID, "Route": route})

# Guardar en un archivo JSON
with open(output_file, "w") as outfile:
    json.dump(routes, outfile, indent=4)

print(f"Archivo de rutas guardado en: {output_file}")



