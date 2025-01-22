import json
import csv
from collections import Counter

# Count the number of times each city appears in the routes
# The input files are the ones generated in code 3_compute_popular_routes.py and code 5_map_coord_to_label.py

# File paths
routes_file = "/home/mmarcrv/Data4good/j_data/id_to_route_j.json"
dicc_file = "/home/mmarcrv/Data4good/g_data/dicc_coor_name_freq.json"
output_csv = "/home/mmarcrv/Data4good//j_data/top_frequent_cities_j.csv"

# Load the JSON files
with open(routes_file, "r") as rf:
    routes_data = json.load(rf)

with open(dicc_file, "r") as df:
    dicc_data = json.load(df)

# Count the frequencies of each coordinate in routes.json
coordinate_counter = Counter()
for route in routes_data:
    coordinate_counter.update(route["Route"])

# Merge the counts with the city information
city_frequencies = []
for coord, count in coordinate_counter.items():
    if coord in dicc_data:
        city_info = dicc_data[coord]
        city_frequencies.append({
            "Coordinate": coord,
            "City": city_info["labels"],
            "Frequency": count
        })

# Sort the cities by frequency (descending) and take the top 50
sorted_cities = sorted(city_frequencies, key=lambda x: x["Frequency"], reverse=True)[:50]

# Write the result to a CSV file
with open(output_csv, "w", newline="") as csvfile:
    fieldnames = ["Coordinate", "City", "Frequency"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(sorted_cities)

print(f"Top 50 cities saved to {output_csv}")
