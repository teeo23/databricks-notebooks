from pyspark.sql import SparkSession
from collections import defaultdict

# Define the root directory
root_dir = "/mnt/lab/unrestricted/"

# Initialize a dictionary to store folder sizes
folder_sizes = []

# Function to calculate total size of a folder (including subfolders)
def calculate_folder_size(path):
    total_size = 0
    try:
        files = dbutils.fs.ls(path)  # List all items in the directory
        for file in files:
            if file.isDir():
                # Recursively calculate the size of all subfolders
                total_size += calculate_folder_size(file.path)
            else:
                total_size += file.size  # Add file size
    except Exception as e:
        print(f"Error accessing {path}: {e}")
    return total_size  # Return size in bytes

# Process each top-level folder in the root directory
try:
    top_level_folders = dbutils.fs.ls(root_dir)  # List all top-level items
    for folder in top_level_folders:
        if folder.isDir():
            print(f"Calculating size for: {folder.path}")
            size_in_bytes = calculate_folder_size(folder.path)  # Get size in bytes
            size_in_gb = size_in_bytes / (1024 ** 3)  # Convert bytes to GB
            folder_sizes.append({"Folder": folder.path, "Size_GB": size_in_gb})
except Exception as e:
    print(f"Error accessing {root_dir}: {e}")

# Create a Spark DataFrame from the results
df = spark.createDataFrame(folder_sizes)

# Order by size in descending order
df = df.orderBy(df["Size_GB"].desc())

# Display the table (allows CSV download)
display(df)
