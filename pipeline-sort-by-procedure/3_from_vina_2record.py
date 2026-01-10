# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 21:46:38 2024

@author: ROG
"""

import os
import re
import pandas as pd
from datetime import datetime

def analyze_docking_results(input_folder, output_path):
    """
    Parses PDBQT files in a folder and saves an analysis report to a CSV file.
    
    :param input_folder: Path to the directory containing .pdbqt result files.
    :param output_path: Full path (including filename) for the output CSV.
    """
    # 1. Validate the input directory
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' not found.")
        return

    print(f"Analyzing files in: {input_folder}")

    record = []
    
    # 2. Iterate through all files
    for file_name in os.listdir(input_folder):
        if not file_name.endswith(".pdbqt"):
            continue

        file_path = os.path.join(input_folder, file_name)
        
        try:
            with open(file_path, "r") as f:
                content = f.read()
                
                # Regex to extract numerical scores from "REMARK VINA RESULT:"
                # Extracts the first column (binding affinity)
                vina_results = re.findall(r'REMARK VINA RESULT:\s*(-?\d+\.\d+)', content)
                scores = [float(val) for val in vina_results]

                if not scores:
                    continue

                # Data calculation
                best_score = scores[0]  # Vina lists the best pose first
                average_score = sum(scores) / len(scores)
                score_diff = best_score - average_score

                # Extract ligand ID from filename
                ligand_id = os.path.splitext(file_name)[0]
                record.append([ligand_id, best_score, average_score, score_diff])

        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            continue

    # 3. Create DataFrame and export
    if record:
        df = pd.DataFrame(record, columns=['Ligand', 'Best_Score', 'Average_Score', 'Score_Diff'])
        
        # Sort by Best_Score (ascending - lowest energy first)
        df = df.sort_values(by='Best_Score', ascending=True)
        
        # Ensure the directory for the output path exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        df.to_csv(output_path, index=False)
        print(f"Success! Report generated with {len(df)} entries.")
        print(f"Output saved to: {output_path}")
    else:
        print("No valid docking results were found in the specified folder.")

# --- Manual Execution ---
if __name__ == "__main__":
    target_results = ""
    target_output = ""
    
    analyze_docking_results(target_results, target_output)