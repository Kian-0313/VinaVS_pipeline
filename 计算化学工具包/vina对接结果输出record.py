# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 21:46:38 2024

@author: ROG
"""

import os
import re
import pandas as pd
# 输入文件夹路径

root_folder = "F:\\njs_prot_structure_and_degree_to_njs\\CAFP20_or_Bug22_CAFP20\\"  # 包含多个待分割文件的文件夹
input_folder=root_folder+"results"

# 创建输出文件夹（如果不存在）
# os.makedirs(output_folder, exist_ok=True)

record=[]
# 遍历输入文件夹中的所有文件
for file_name in os.listdir(input_folder):
    input_file_path = os.path.join(input_folder, file_name)
    if not file_name.endswith(".pdbqt"):  # 只处理pdbqt文件
        continue

    # 处理每个输入文件
    with open(input_file_path, "r") as f:

        data = f.read()  # 读取文件内容为字符串
        # 使用正则表达式提取 "REMARK VINA RESULT:" 后的第一个数字
        vina_results = re.findall(r'REMARK VINA RESULT:\s*(-?\d+\.\d+)', data)
        # 将字符串转换为浮动数值
        numbers = [float(num) for num in vina_results]
        # 计算最优值,平均值,diff
        try:
            Best_Score=vina_results[0]
            average = sum(numbers) / len(numbers)
            diff=float(Best_Score)-average
        except:
            Best_Score=10
            average=10
            diff=10
        # 输出结果
        record.append([file_name,Best_Score,average,diff])


record_df = pd.DataFrame(record, columns=['Ligand', 'Best_Score', 'Average_Score','diff'])
record_df.to_csv(input_folder+"record.csv")






