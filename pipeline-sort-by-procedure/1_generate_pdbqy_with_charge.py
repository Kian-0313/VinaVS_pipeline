from meeko import MoleculePreparation
from rdkit import Chem
from rdkit.Chem import AllChem
import os
import pandas as pd

def from_smi_2_pdbqt(smi, ID, output_path):
    """
    Converts a single SMILES string to a PDBQT file with 3D coordinates.
    """
    # Define output file path
    output_file_name = os.path.join(output_path, f"{ID}.pdbqt")
    
    # Skip processing if the file already exists
    if os.path.exists(output_file_name):
        return

    # 1. Desalting / Fragment Selection
    # If the SMILES contains multiple fragments (separated by '.'), pick the most likely organic one
    if '.' in smi:
        parts = smi.split('.')
        organic_parts = []
        for part in parts:
            mol_temp = Chem.MolFromSmiles(part)
            if mol_temp is not None:
                # Check for carbon atoms or a minimum size to identify organic molecules
                has_carbon = any(atom.GetSymbol() == 'C' for atom in mol_temp.GetAtoms())
                if has_carbon or mol_temp.GetNumAtoms() > 3:
                    organic_parts.append(part)
        # Use the longest string among organic fragments as the main molecule
        smiles_to_use = max(organic_parts, key=len) if organic_parts else smi
    else:
        smiles_to_use = smi

    # 2. RDKit Processing
    mol = Chem.MolFromSmiles(smiles_to_use)
    if mol is None:
        print(f" [Skip] SMILES parsing failed: ID={ID}, SMILES={smi}")
        return 

    try:
        # Add Hydrogens (crucial for docking)
        mol = Chem.AddHs(mol)
        
        # Generate 3D Coordinates
        # Use ETKDGv3: A robust conformer generation algorithm
        params = AllChem.ETKDGv3() 
        params.randomSeed = 42
        if AllChem.EmbedMolecule(mol, params) == -1:
            # Fallback to random coordinates if ETKDG fails
            AllChem.EmbedMolecule(mol, useRandomCoords=True, randomSeed=42)
        
        # Force field optimization (Universal Force Field)
        AllChem.UFFOptimizeMolecule(mol)
        
        # 3. Convert to PDBQT using Meeko
        preparator = MoleculePreparation()
        preparator.prepare(mol)
        pdbqt_string = preparator.write_pdbqt_string()
        
        # Save to local disk
        with open(output_file_name, "w") as f:
            f.write(pdbqt_string)
            
    except Exception as e:
        print(f" [Error] 3D generation or conversion failed: ID={ID}, Reason={e}")

def batch_process_smiles(input_file, output_path):
    """
    Batch processes molecules from CSV, SMI, or TXT files.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    file_ext = os.path.splitext(input_file)[-1].lower()
    molecules = [] # List of tuples: (smiles, id)

    # 1. Identify file format and extract data
    if file_ext == '.csv':
        print(f"Reading CSV file: {input_file}")
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='gbk') # Handle Windows-specific encoding
            
        for _, row in df.iterrows():
            # Assumes columns named 'SMILES' and 'ID'
            molecules.append((str(row['SMILES']), str(row['ID'])))
            
    elif file_ext in ['.smi', '.txt']:
        print(f"Reading {file_ext} file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line: continue
                
                parts = line.split()
                smi = parts[0]
                # If the .smi file has a name in the second column, use it; otherwise use line index
                mol_id = parts[1] if len(parts) > 1 else f"mol_{i}"
                molecules.append((smi, mol_id))
    else:
        print(f"Unsupported file format: {file_ext}")
        return

    # 2. Iterative processing
    print(f"Task Started: {len(molecules)} molecules found.")
    for smi, ID in molecules:
        from_smi_2_pdbqt(smi, ID, output_path)
    
    print("Batch processing complete.")

# --- Example Usage ---
#input_path = "C:\\Users\\17534\\Desktop\\mol.smi"
"""csv mode need row named 'SMILES' and 'ID' """
#input_path = "C:\\Users\\17534\\Desktop\\mol.csv"  

#output_dir = "C:\\Users\\17534\\Desktop\\3D_conformation"
#batch_process_smiles(input_path, output_dir)