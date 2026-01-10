from meeko import MoleculePreparation
from rdkit import Chem
from rdkit.Chem  import AllChem
import os
import shutil
import time
import sys
import pandas as pd

# dt=pd.read_csv("F:/docking_dataset/zinc/output_MW200-350/smi_MW200-350.csv")
# smiles=dt["smiles"]
# for i in range(len(smiles)):
#  compound = smiles[i]
# # 定义一个 SMILES 字符串
#  smiles_string = compound  
def from_smi_2_pdbqt(smi,ID,output_path):
    

    # 检查输出文件是否已存在
    output_file_name = os.path.join(output_path, f"{ID}.pdbqt")
    if os.path.exists(output_file_name):
        print(f"文件 {output_file_name} 已存在，跳过处理。")
        return

    # 如果包含点号，选择有机部分
    if '.' in smi:
        parts = smi.split('.')
        organic_parts = []

        for part in parts:
            mol_temp = Chem.MolFromSmiles(part)
            if mol_temp is not None:
                # 简单判断：如果包含碳原子或者是有机特征原子
                has_carbon = any(atom.GetSymbol() == 'C' for atom in mol_temp.GetAtoms())
                if has_carbon or mol_temp.GetNumAtoms() > 3:  # 或者原子数较多
                    organic_parts.append(part)

        if organic_parts:
            # 使用最长的有机部分
            smiles_to_use = max(organic_parts, key=len)
            # print(f"使用最长的有机部分: {smiles_to_use}")
        else:
            smiles_to_use = smi
    else:
        smiles_to_use = smi


    
    # 使用 RDKit 将 SMILES 转换为 RDKit 分子对象
    mol = Chem.MolFromSmiles(smiles_to_use)
    if mol is None:
        print("SMILES 解析失败，请检查输入是否正确。")
    mol = Chem.AddHs(mol)  # 补充氢原子
    AllChem.EmbedMolecule(mol)  # 为分子生成 3D 坐标
    AllChem.UFFOptimizeMolecule(mol)  # 使用 UFF 力场优化分子几何
     
     
     
    # 转换为 PDBQT 格式 
    preparator = MoleculePreparation()
    preparator.prepare(mol)  # 使用 RDKit 分子对象进行预处理
    pdbqt_string = preparator.write_pdbqt_string()  # 生成 PDBQT 格式的字符串
    print(pdbqt_string)
    # 打印或保存结果
    output_file_name=os.path.join(output_path,f"{ID}.pdbqt")
    with open(output_file_name, "w") as f:
        f.write(pdbqt_string)
    # print("生成成功")
    

input_path="C:\\Users\\17534\\Desktop\\"

#df=pd.read_csv(os.path.join(input_path,"47360_Molecular_property.csv"))
# df=pd.read_excel(os.path.join(input_path,"Drug_Repurposing_Library_3000.xlsx"),sheet_name="Compound List")
df=pd.read_csv(os.path.join(input_path,"filtered_clusters.csv"))
output_path=os.path.join(input_path,"3D_conformation")
# 确保文件夹存在
os.makedirs(output_path, exist_ok=True)


smi_list=df["SMILES"]
id_list=df["ID"]

for smi,ID in zip(smi_list,id_list):
        try:
            from_smi_2_pdbqt(smi,ID,output_path)
        except:
            print(smi,ID)
            continue








