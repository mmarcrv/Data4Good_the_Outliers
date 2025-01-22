import json
from collections import Counter

# Map the locations to a single name, chosen by the most common name
# The input file has to be the one generated in code 4_dictionary_makers.py

# Archivos de entrada y salida
input_file = "/home/mmarcrv/Data4good/g_data/grouped_markers.json"
output_file = "/home/mmarcrv/Data4good/j_data/dicc_coor_name_freq_j.json"


def process_labels(input_file, output_file):
    # Leer el archivo de entrada
    with open(input_file, 'r') as infile:
        data = json.load(infile)
    
    output = {}

    # Procesar cada entrada
    for coord, details in data.items():
        labels = details["labels"]
        count = details["count"]

        # Encontrar el nombre más repetido
        most_common_label = Counter(labels).most_common(1)[0][0]

        # Formar el nuevo formato
        output[coord] = {
            "labels": most_common_label,
            "count": count
        }

    # Escribir el resultado en el archivo de salida
    with open(output_file, 'w') as outfile:
        json.dump(output, outfile, indent=4)




# Llamar a la función
process_labels(input_file, output_file)

print(f"Archivo procesado. La salida está en '{output_file}'.")


