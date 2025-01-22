import pandas as pd
import json

# this code creates two different datasets containing the more repeated routes divided in two
# one dataset contains the routes with the same coordinates as origin and destination and the other with different coordinates

# Input
input_file = "/home/mmarcrv/Data4good/g_data/movement_id_data.csv"
# Output files
same_coords_top100_file = "/home/mmarcrv/Data4good/j_data/same_coords_j.csv"
different_coords_top100_file = "/home/mmarcrv/Data4good/j_data/different_coords_j.csv"
combined_df = pd.read_csv(input_file)

# Verificar que las columnas necesarias existen
required_columns = ['Origin Coordinates', 'Destination Coordinates']
if not all(col in combined_df.columns for col in required_columns):
    raise ValueError(f"El archivo debe contener las columnas: {required_columns}")

# Paso 2: Separar en DataFrames diferentes
same_coords_df = combined_df[
    combined_df['Origin Coordinates'] == combined_df['Destination Coordinates']
].copy()

different_coords_df = combined_df[
    combined_df['Origin Coordinates'] != combined_df['Destination Coordinates']
].copy()

# Paso 3: Calcular frecuencias de desplazamientos
# Desplazamientos con mismas coordenadas
same_coords_freq = same_coords_df.groupby(
    ['Origin Coordinates', 'Destination Coordinates']
).size().reset_index(name='Frequency')

# Desplazamientos con diferentes coordenadas
different_coords_freq = different_coords_df.groupby(
    ['Origin Coordinates', 'Destination Coordinates']
).size().reset_index(name='Frequency')

# Ordenar por frecuencia descendente
same_coords_freq = same_coords_freq.sort_values(by='Frequency', ascending=False).head(100)
different_coords_freq = different_coords_freq.sort_values(by='Frequency', ascending=False).head(100)

same_coords_freq.to_csv(same_coords_top100_file, index=False)
different_coords_freq.to_csv(different_coords_top100_file, index=False)

# Paso 5: Informar sobre los resultados
print(f"Top 100 desplazamientos con mismas coordenadas guardados en: {same_coords_top100_file}")
print(f"Top 100 desplazamientos con diferentes coordenadas guardados en: {different_coords_top100_file}")

# Opcional: Mostrar las rutas más frecuentes
print("\nTop 100 desplazamientos con mismas coordenadas:")
print(same_coords_freq)

print("\nTop 100 desplazamientos con diferentes coordenadas:")
print(different_coords_freq)
