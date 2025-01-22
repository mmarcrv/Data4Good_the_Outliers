import json
import csv
from collections import Counter

# Generates the most popular routes based on the frequency of each subroute, allowing repetitions
# and with two displacements
# Change the input and output file paths to match the desired files
# The input has to be the one generated in code 2_route_for_id.py

# Input and output file paths
input_file = "/home/mmarcrv/Data4good/g_data/id_to_route.json"
output_file = "/home/mmarcrv/Data4good/g_data/popular_routes_2_with_repetition.json"

# Function to generate subroutes of length 2
def generate_subroutes(route):
    return [f"{route[i]}-{route[i+1]}-{route[i+2]}" for i in range(len(route) - 2)]

# Read the JSON file
with open(input_file, "r") as infile:
    data = json.load(infile)

# Counter for the subroutes
subroute_counter = Counter()

# Process each route in the file
for record in data:
    route = record["Route"]
    subroutes = generate_subroutes(route)
    subroute_counter.update(subroutes)

# Sort the routes by frequency
sorted_subroutes = subroute_counter.most_common()

# Write the sorted subroutes to the output file
with open(output_file, "w") as outfile:
    json.dump(sorted_subroutes, outfile, indent=4)

print(f"Processed data successfully saved to {output_file}")
