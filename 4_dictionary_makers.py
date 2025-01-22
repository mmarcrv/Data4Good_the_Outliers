import pandas as pd
import json
import re
from collections import defaultdict
from collections import Counter

# This code creates more dictionaries that map each coordinate to a list of labels and a count of the number of labels
# the input has to be the one generated in code 1_extraction_of_data.py

# Archivos de entrada y salida
input_file = "/home/mmarcrv/Data4good/j_data/markers_j.json"
output_file = "j_data/grouped_markers_j.json"


# Function to fix and clean the Geo Location string
def fix_json_string_with_triples(input_string):
    fixed_string = re.sub(r'^"""|"""$', '', input_string)
    fixed_string = fixed_string.replace('""', '"')
    fixed_string = re.sub(r'(?<!")(\b\w+\b)(?=:)', r'"\1"', fixed_string)
    fixed_string = re.sub(r'(?<=:)(\b\w+\b)(?!")', r'"\1"', fixed_string)
    fixed_string = fixed_string.replace(",}", "}")
    fixed_string = fixed_string.replace(",]", "]")
    fixed_string = re.sub(r'"(-?\d+\.\d+)"', r'\1', fixed_string)
    fixed_string = re.sub(r'"(-?\d+)"', r'\1', fixed_string)
    return fixed_string

# Function to process a single JSON string into markers dictionary
def process_json(data, decimals=1):
    try:
        data = json.loads(data)
        markers = []
        for marker in data.get("markers", []):
            label = marker.get("label", "")
            location = marker.get("location", {})
            if label and location:
                lat = round(location.get("lat", 0), decimals)
                lon = round(location.get("lon", 0), decimals)
                if lat and lon:
                    coord_str = f"{lat},{lon}"  # Use rounded coordinates
                    markers.append((coord_str, label))
        return markers
    except Exception as e:
        raise ValueError(f"Error processing JSON data: {e}")

# Function to process CSV and create a grouped markers dictionary
def process_csv(file_path, decimals=1):
    df = pd.read_csv(file_path)
    grouped_markers = defaultdict(lambda: {"labels": set(), "count": 0})

    for index, row in df.iterrows():
        geo_location = row["Geo Location"]
        if pd.isna(geo_location):
            continue
        if index % 1000 == 0:
            print(f"Processing row {index}...")
        geo_location = geo_location.strip()
        if geo_location.startswith('"') and geo_location.endswith('"'):
            geo_location = geo_location[1:-1]
        try:
            cleaned_json = fix_json_string_with_triples(geo_location)
            json_objects = cleaned_json.split('}{')
            if len(json_objects) > 1:
                json_objects[0] += '}'
                for i in range(1, len(json_objects) - 1):
                    json_objects[i] = '{' + json_objects[i] + '}'
                json_objects[-1] = '{' + json_objects[-1]
                for json_obj in json_objects:
                    markers = process_json(json_obj, decimals)
                    for coord_str, label in markers:
                        grouped_markers[coord_str]["labels"].add(label)
                        grouped_markers[coord_str]["count"] += 1
            else:
                markers = process_json(cleaned_json, decimals)
                for coord_str, label in markers:
                    grouped_markers[coord_str]["labels"].add(label)
                    grouped_markers[coord_str]["count"] += 1
        except Exception as e:
            print(f"Error processing row {index}: {e}")

    # Convert sets to lists for easier JSON serialization
    for coord_str in grouped_markers:
        grouped_markers[coord_str]["labels"] = list(grouped_markers[coord_str]["labels"])
    
    return grouped_markers

# Example usage
file_path = "/home/mmarcrv/Data4good/j_data/jewish_victims_movement.csv"  # Replace with your file path
grouped_markers = process_csv(file_path, decimals=1)

# Print the resulting grouped markers dictionary
print("\nGrouped Markers Dictionary:")
for coord_str, data in list(grouped_markers.items())[:10]:  # Show first 10 entries
    print(f"{coord_str}: {data}")

# Save results to JSON
with open(output_file, "w") as f:
    json.dump(grouped_markers, f, indent=4)

print(f"Grouped markers successfully saved to {output_file}")


