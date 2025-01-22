import pandas as pd
import json
import re

# File paths
file_path = "/home/mmarcrv/Data4good/Data4Good_Arolsen_Archives_50k.csv"  # Replace with your file path
output_file = "updated_processed_data.csv"  # Output file with coordinates
output_markers_dic = "/home/mmarcrv/Data4good/markers.json"  # Output markers dictionary file

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

# Function to process a single JSON string into DataFrame and markers dictionary
def process_json(data):
    try:
        data = json.loads(data)
        paths = data.get("paths", [])
        if paths:
            df_paths = pd.DataFrame(paths)
            if not all(col in df_paths.columns for col in ["fromLabel", "toLabel"]):
                raise ValueError(f"Missing expected columns in paths: {df_paths.columns}")
            df_paths = df_paths[["fromLabel", "toLabel"]].rename(columns={
                "fromLabel": "Origin",
                "toLabel": "Destination"
            })
        else:
            df_paths = pd.DataFrame(columns=["Origin", "Destination"])

        markers = {}
        for marker in data.get("markers", []):
            label = marker.get("label", "")
            location = marker.get("location", {})
            if label and location:
                markers[label] = location

        birthplace_marker = next((m for m in data.get("markers", []) if m.get("type") == "Birth Place"), None)
        if birthplace_marker:
            birthplace = birthplace_marker.get("label")
            df_paths["Birth Place"] = birthplace
        else:
            df_paths["Birth Place"] = None

        return df_paths, markers

    except Exception as e:
        raise ValueError(f"Error processing JSON data: {e}")

# Function to process CSV and handle multiple JSON objects per row
def process_csv(file_path):
    df = pd.read_csv(file_path)
    combined_df = pd.DataFrame()
    combined_markers = {}

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
                    df_paths, markers = process_json(json_obj)
                    df_paths["ID"] = row["ID"]
                    combined_df = pd.concat([combined_df, df_paths], ignore_index=True)
                    for label, location in markers.items():
                        if label not in combined_markers:
                            combined_markers[label] = location
            else:
                df_paths, markers = process_json(cleaned_json)
                df_paths["ID"] = row["ID"]
                combined_df = pd.concat([combined_df, df_paths], ignore_index=True)
                for label, location in markers.items():
                    if label not in combined_markers:
                        combined_markers[label] = location

        except Exception as e:
            print(f"Error processing row {index}: {e}")

    return combined_df, combined_markers

# Function to get the coordinates from the dictionary based on the name
def get_coordinates(name, markers):
    if name in markers:
        lat = round(markers[name]["lat"], 1)
        lon = round(markers[name]["lon"], 1)
        return f"{lat},{lon}"
    return None

# Function to process the CSV and update it with coordinates
def process_csv_with_coordinates(file_path, output_file):
    combined_df, combined_markers = process_csv(file_path)

    origins = []
    destinations = []

    for index, row in combined_df.iterrows():
        origin_name = row["Origin"]
        destination_name = row["Destination"]

        origin_coords = get_coordinates(origin_name, combined_markers)
        destination_coords = get_coordinates(destination_name, combined_markers)

        if origin_coords and destination_coords:
            origins.append(origin_coords)
            destinations.append(destination_coords)
        else:
            origins.append(None)
            destinations.append(None)

    combined_df["Origin Coordinates"] = origins
    combined_df["Destination Coordinates"] = destinations
    combined_df = combined_df.dropna(subset=["Origin Coordinates", "Destination Coordinates"])

    combined_df.to_csv(output_file, index=False)
    print(f"Processed data successfully saved to {output_file}")

    with open(output_markers_dic, "w") as f:
        json.dump(combined_markers, f, indent=4)
    print(f"Markers dictionary successfully saved to {output_markers_dic}")

# Example usage
process_csv_with_coordinates(file_path, output_file)