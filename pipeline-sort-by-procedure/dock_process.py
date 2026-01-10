# -*- coding: utf-8 -*-
from pathlib import Path
import os
import subprocess
import sys

# 1. Threading Configuration from Command Line
# q: the index of the current process/thread
# step: the total number of parallel processes running
q = int(sys.argv[1])
step = int(sys.argv[2])

# 2. Parse config.txt
config_file = "./config.txt"
config = {}

if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key.strip()] = value.strip()
else:
    print(f"Error: {config_file} not found.")
    sys.exit(1)

# Extract paths and settings
ligands_dir = config.get("ligand_dir")
project_name = config.get("project_name")
vina_path = config.get("vina_path")
vina_config_path = config.get("vina_config_path")

# Get CPU per Vina task from config; default to 1 as requested
# This ensures that each 'batch' process only takes up the specified amount of cores
vina_cpu = config.get("cpu_nums", "1")

output_dir = f"./{project_name}/result"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# 3. Get file list and slice it for this specific process
folder_path = Path(ligands_dir)
file_list = [file.name for file in folder_path.iterdir() if file.is_file()]

# Distribute files: this process handles every 'step'-th file starting from index 'q'
file_list = file_list[q::step]

# 4. Batch Docking Loop
print(f"Process {q} starting. Handling {len(file_list)} ligands.")

for ligand in file_list:
    ligand_path = os.path.join(ligands_dir, ligand)
    output_path = os.path.join(output_dir, ligand)

    # Construct Vina command with dynamic CPU count from config
    # We use the 'vina_cpu' variable read from config.txt
    command = f'"{vina_path}" --config "{vina_config_path}" --ligand "{ligand_path}" --out "{output_path}" --cpu {vina_cpu}'
    
    print(f"Process {q} docking: {ligand}")
    
    # Execute Vina
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if process.returncode != 0:
        print(f"Error running Vina for {ligand}: {process.stderr}")
        continue

print(f"Process {q} task completed.")