# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 20:57:47 2024

@author: ROG
"""

from rdkit import Chem
from rdkit.Chem import Draw
sdf_file1 = "F:/docking_dataset/fold_mmp9_single_full_data/GRI977143.sdf"
sdf_file2 = "F:/docking_dataset/fold_mmp9_single_full_data/beta-Neo-endorphin.sdf"
# 加载分子
large_molecule = Chem.MolFromMolFile("F:/docking_dataset/fold_mmp9_single_full_data/beta-Neo-endorphin.sdf")  # 替换为大分子路径
small_molecule = Chem.MolFromMolFile("F:/docking_dataset/fold_mmp9_single_full_data/GRI977143.sdf")  # 替换为小分子路径

# 子结构匹配
if large_molecule.HasSubstructMatch(small_molecule):
    print("The small molecule is a substructure of the large molecule.")
    match_atoms = large_molecule.GetSubstructMatch(small_molecule)
    print(f"Matched atom indices: {match_atoms}")

    # 可视化匹配结果
    matched_image = Draw.MolToImage(large_molecule, highlightAtoms=match_atoms)
    matched_image.show()
else:
    print("No match found.")
