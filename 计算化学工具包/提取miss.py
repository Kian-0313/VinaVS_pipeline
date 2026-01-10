# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 11:08:18 2024

@author: ROG
"""

import math
import csv
import os
import shutil
import pandas as pd
# 定义CSV文件路径
csv_file_path = "F:\\docking_dataset\\database\\Enamine_CNS_Library_plated_47360cmpds_20221006_fromMCE\\result.csv" 
# 替换为你的CSV文件路径

# 初始化一个集合来存储出现过的数字
seen_numbers = set()

# 读取CSV文件


dt=pd.read_csv(csv_file_path)
num=dt["Ligand"]

# with open(csv_file_path, mode='r', encoding='utf-8') as file:   
    # csv_reader = csv.DictReader(file)  # 使用DictReader按列名读取
    # # ligand=file['Ligand']
    # for row in csv_reader:
    #     # 假设列名为'pdbqt_column'，需要根据实际情况修改列名
    #     pdbqt_value = row["Ligand".strip()]
for pdbqt_value in num:
        
        # 提取数字部分，例如 '123.pdbqt' -> '123'
        if pdbqt_value.endswith('.pdbqt'):
            number_part = pdbqt_value.replace('.pdbqt', '')
            
            try:
                # 尝试将提取的部分转换为整数，并加入到集合中
                seen_numbers.add(int(number_part))
            except ValueError:
                # 如果无法转换为整数，跳过该行
                pass

# 定义数字范围（1到499）
all_numbers = set(range(1, 47361))

# 找出缺失的数字
missing_numbers = all_numbers - seen_numbers

missing_numbers_list = sorted(list(missing_numbers))
# 假设 missing_numbers_list 是一个包含从 0 到 420000 的数字列表

# # 创建一个字典来存储“变量”
# vars_dict = {}

# # 根据索引 i 除以 30000 向下取整的值来动态生成“变量”
# for i, num in enumerate(missing_numbers_list):
#     q = (num-1) // 30000  # 计算索引 i 除以 30000 向下取整的结果
#     var_name = f"{q}"  # 使用 f-string 动态生成变量名
    
#     # 如果字典中没有这个变量，创建一个新的列表
#     if var_name not in vars_dict:
#         vars_dict[var_name] = []
    
#     # 将数字添加到对应的变量列表中
#     vars_dict[var_name].append(num)

# 文件夹路径
# folder_path = "q"  # 假设 'q' 是目标文件夹
# 目标文件夹路径
  # 目标文件夹路径
no_file_list=[]
# 检查并复制文件
folder_path="F:/docking_dataset/database/Enamine_CNS_Library_plated_47360cmpds_20221006_fromMCE/results/"
destination_folder = "F:/docking_dataset/database/Enamine_CNS_Library_plated_47360cmpds_20221006_fromMCE/miss/" 
for filename in missing_numbers_list:
    # 形成.pdbqt文件路径
        pdbqt_filename = f"{filename}.pdbqt"
        file_path = os.path.join(folder_path, pdbqt_filename)
        
        # 检查文件是否存在
        if os.path.exists(file_path):
            # 目标路径
            destination_path = os.path.join(destination_folder, pdbqt_filename)
            
            # 复制文件
            shutil.copy(file_path, destination_path)
        else:
            no_file_list.append(file_path)
            print(f"文件 {file_path} 不存在")
            
