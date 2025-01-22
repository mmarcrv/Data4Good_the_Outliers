import pandas as pd
import json
import numpy as np

# Code that does a statistical study that helped to understand the data and what
# we could do with it

# the input has to be the file generated in code 2_route_for_id.py

# Cargar el archivo JSON
input_file = "/home/mmarcrv/Data4good/g_data/id_to_route.json"
with open(input_file, "r") as infile:
    data = json.load(infile)

# Convertir el archivo JSON en un DataFrame
df = pd.DataFrame(data)

# Calcular el número de desplazamientos (número de coordenadas - 1)
df["Number of Movements"] = df["Filtered Route"].apply(lambda x: len(x) - 1)

# Calcular estadísticas descriptivas
mean_movements = df["Number of Movements"].mean()
std_movements = df["Number of Movements"].std()
quartiles = df["Number of Movements"].quantile([0.25, 0.5, 0.75]).to_dict()

# Crear un resumen de estadísticas
summary = {
    "Mean": mean_movements,
    "Standard Deviation": std_movements,
    "Quartiles": {
        "Q1 (25%)": quartiles[0.25],
        "Median (50%)": quartiles[0.5],
        "Q3 (75%)": quartiles[0.75]
    }
}

# Mostrar resultados
print("Estadísticas del número de desplazamientos por persona:")
print(json.dumps(summary, indent=4))

# Guardar estadísticas en un archivo JSON
output_stats_file = r"C:\Users\emmac\Downloads\estudio_ruta3.csv"
with open(output_stats_file, "w") as outfile:
    json.dump(summary, outfile, indent=4)

print(f"Archivo de estadísticas guardado en: {output_stats_file}")
