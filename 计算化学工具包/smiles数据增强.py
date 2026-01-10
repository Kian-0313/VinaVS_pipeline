from rdkit import Chem
from rdkit.Chem import AllChem
import random
import argparse
import os

def enumerate_smiles(smiles, num_augments=5):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return []
    enumerated = set()
    for _ in range(num_augments):
        # 打乱原子顺序
        atoms = list(mol.GetAtoms())
        random.shuffle(atoms)
        # 重新构建分子
        new_order = [atom.GetIdx() for atom in atoms]
        mol = Chem.RenumberAtoms(mol, new_order)
        # 生成非标准 SMILES
        new_smiles = Chem.MolToSmiles(mol, canonical=False)
        enumerated.add(new_smiles)
    return list(enumerated)

def augment_smi_file(input_file, output_file, num_augments):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            parts = line.strip().split()
            if not parts:
                continue
            smiles = parts[0]
            name = parts[1] if len(parts) > 1 else ''
            augmented = enumerate_smiles(smiles, num_augments)
            # outfile.write(f"{smiles}\n")
            for idx, aug_smiles in enumerate(augmented):
                outfile.write(f"{aug_smiles}\n")

if __name__ == "__main__":

    # parser = argparse.ArgumentParser(description="SMILES Data Augmentation Script")
    # parser.add_argument("input_file", help="Path to the input .smi file")
    # parser.add_argument("--output_file", help="Path to the output .smi file")
    # parser.add_argument("--num_augments", type=int, default=10, help="Number of augmentations per molecule")
    # args = parser.parse_args()

    # 如果未提供输出文件路径，则自动生成

    input_file="F:/docker_container_data/ChemTSv2/data/2019PubChemQC_can_nocharge.smi"

    base, ext = os.path.splitext(input_file)

    output_file = f"{base}_enhanced{ext}"

    augment_smi_file(input_file, output_file, 5)











