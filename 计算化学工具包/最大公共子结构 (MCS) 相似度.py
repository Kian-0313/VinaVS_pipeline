from rdkit import Chem
from rdkit.Chem import Draw
import pandas as pd
import math
from rdkit import Chem
from rdkit.Chem import AllChem, QED, Crippen
from rdkit.Chem import Descriptors, DataStructs
import numpy as np
import pandas as pd
from rdkit.Chem import rdFMCS


# 两个 SMILES
smiles1 = "c1ccc2c(c1)[nH]cc2"         # 吲哚
smiles2 = "c1ccc2c(c1)occ2"        # 苯并咪唑
smiles_list=[smiles1,smiles2]
mol1 = Chem.MolFromSmiles(smiles1)
mol2 = Chem.MolFromSmiles(smiles2)

# 计算相似度
fp1 = AllChem.GetMorganFingerprintAsBitVect(mol1, 2, nBits=256)
fp2 = AllChem.GetMorganFingerprintAsBitVect(mol2, 2, nBits=256)
sim = DataStructs.TanimotoSimilarity(fp1, fp2)
print(f"Tanimoto 相似度: {sim:.4f}")

# 最大公共子结构 (MCS) 相似度

mcs_result = rdFMCS.FindMCS([mol1, mol2])
mol1_atoms = mol1.GetNumAtoms()
mol2_atoms = mol2.GetNumAtoms()
mcs_atoms = mcs_result.numAtoms
print(f"MCS SMARTS: {mcs_result.smartsString}")
print(f"匹配原子数: {mcs_result.numAtoms}")
print(f"匹配键数: {mcs_result.numBonds}")
structure_sim = mcs_atoms / min(mol1_atoms, mol2_atoms)
print(f"MCS相似度: {structure_sim}")


# 转换为分子对象
mols = [Chem.MolFromSmiles(smile) for smile in smiles_list]

# 绘制并保存为图片
img = Draw.MolsToGridImage(
    mols,
    subImgSize=(200, 200)
)

# 保存图片
img.show()
