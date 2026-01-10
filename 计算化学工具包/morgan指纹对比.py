# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 20:56:31 2024

@author: ROG
"""

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import TanimotoSimilarity

# 读取 SDF 文件中的分子
def load_molecules(sdf_file):
    supplier = Chem.SDMolSupplier(sdf_file)
    molecules = [mol for mol in supplier if mol is not None]
    return molecules

# 比较两个 SDF 文件中的分子指纹相似性
def compare_fingerprints(sdf_file1, sdf_file2):
    mols1 = load_molecules(sdf_file1)
    mols2 = load_molecules(sdf_file2)

    # 计算所有分子指纹
    fps1 = [AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048) for mol in mols1]
    fps2 = [AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048) for mol in mols2]

    # 比较相似性
    for i, fp1 in enumerate(fps1):
        for j, fp2 in enumerate(fps2):
            similarity = TanimotoSimilarity(fp1, fp2)
            print(f"Similarity between molecule {i+1} in File1 and molecule {j+1} in File2: {similarity:.2f}")

# 使用示例
sdf_file1 = "F:/docking_dataset/fold_mmp9_single_full_data/GRI977143.sdf"
sdf_file2 = "F:/docking_dataset/fold_mmp9_single_full_data/beta-Neo-endorphin.sdf"
compare_fingerprints(sdf_file1, sdf_file2)