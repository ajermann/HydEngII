import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime


image_path = "Classified/HYDO2_250524_all_roi_2/Fish_confirmed_human/"


dict = {'name': [], 'folder': [], 'timestamp': []}

# Iterate over images in Fish_confirmed_human
for image_file in os.listdir(image_path):
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
        image_filepath = os.path.join(image_path, image_file)
        
        # Extract filename
        dict['name'].append(image_file)

        fol_num = image_file.split('_')[4]
        dict['folder'].append(fol_num)

        # extract timestamp from metadata file
        timestamp_path = f"../Group_4_HYDO2/ROIs_250524_post/full_video_reduced_{fol_num}/ROIs_250524/metadata_250524.csv"

        if not os.path.exists(timestamp_path):
            print(f"Warning: Metadata file not found: {timestamp_path}")
            dict['timestamp'].append(None)
            continue

        with open(timestamp_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['image_name'] == image_file:
                    timestamp = row['utc_timestamp']
                    dict['timestamp'].append(timestamp)
                    print(f"Timestamp: {timestamp}")
                    break


# Filter out timestamps within 5 seconds of the previous one
indices_to_remove = []
for i in range(1, len(dict['timestamp'])):
    if dict['timestamp'][i] is not None and dict['timestamp'][i-1] is not None:
        try:
            current_time = datetime.fromisoformat(dict['timestamp'][i])
            previous_time = datetime.fromisoformat(dict['timestamp'][i-1])
            time_diff = (current_time - previous_time).total_seconds()
            
            if time_diff < 10:
                indices_to_remove.append(i)
                print(f"Removing index {i}: timestamp {dict['timestamp'][i]} is only {time_diff:.2f}s after previous")
        except ValueError as e:
            print(f"Error parsing timestamp at index {i}: {e}")

# Remove indices in reverse order to avoid index shifting
for i in reversed(indices_to_remove):
    dict['name'].pop(i)
    dict['folder'].pop(i)
    dict['timestamp'].pop(i)

print(f"\nRemoved {len(indices_to_remove)} entries with timestamps too close together")
print(f"Remaining entries: {len(dict['name'])}")


output_path = "output/fish.csv"
pd.DataFrame(dict).to_csv(output_path, index=False)
print(f"Saved CSV to: {output_path}")


print('Done! Check the output folder for the generated CSV file.')