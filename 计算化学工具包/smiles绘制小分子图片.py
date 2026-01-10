# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 09:53:15 2025

@author: yqz
"""

from rdkit import Chem
from rdkit.Chem import Draw
import pandas as pd
import math

# # 定义SMILES字符串列表
# smiles_list = [
#     "CCO",  # 乙醇
#     "CC(=O)O",  # 乙酸
#     "c1ccccc1",  # 苯
# ]
file_path='F:\\docker_container_data\\SBMolGen-vina\\mol_3D_pose_trial1\\min\\min_score_data.xlsx'
df = pd.read_excel(file_path)
df = df.sort_values(by='per')
print(df)
smi=df['smiles']
smiles_list=smi[:]
save_path="F:\\docker_container_data\\SBMolGen-vina\\mol_3D_pose_trial1\\per_with_compensate_c2_t1\\pic"
# 批量绘制分子结构并保存为图片
for i, smile in enumerate(smiles_list):
    mol = Chem.MolFromSmiles(str(smile))
    if mol:  # 检查 SMILES 是否合法
        img = Draw.MolToImage(mol, size=(300, 300))
        img.save(save_path+f"\\molecule_{i+1}.png")
    else:
        print(f"无效的 SMILES 字符串: {smile}")

print("二维结构图片已保存。")


# 批量绘制分子结构，12个一组
group_size = 12
num_groups = math.ceil(len(smiles_list) / group_size)

for group_idx in range(num_groups):
    # 获取当前组的 SMILES 列表
    group_smiles = smiles_list[group_idx * group_size:(group_idx + 1) * group_size]

    # 转换为分子对象
    mols = [Chem.MolFromSmiles(smile) for smile in group_smiles]

    # 绘制并保存为图片
    img = Draw.MolsToGridImage(
        mols,
        molsPerRow=4,  # 每行 4 个
        subImgSize=(200, 200)
    )

    # 保存图片
    img.show()



















