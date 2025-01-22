import pandas as pd

# Create a new CSV file with only Jewish victims, use this to filter the data

# File paths
input_file = "/home/mmarcrv/Data4good/Data4Good_Arolsen_Archives_50k.csv"
output_file = "jewish_victims_movement.csv"

# Load the dataset
data = pd.read_csv(input_file)

# Filter rows where the religion is "Jewish"
jewish_victims = data[data['Religion'] == 'Jewish']

# Save the filtered data to a new CSV file
jewish_victims.to_csv(output_file, index=False)

print(f"Filtered data saved to {output_file}")
