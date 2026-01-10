# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 15:57:25 2025

@author: yqz
"""

import os
import re
import pandas as pd

# 存放 PDBQT 文件的文件夹路径
folder_path = "F:\\docking_dataset\\database\\Enamine_CNS_Library_plated_47360cmpds_20221006_fromMCE\\name"  # 替换为你的文件夹路径

# 存储结果
data = []

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith(".pdbqt"):
        # 提取序号（假设文件名是 {序号}.pdbqt）
        file_id = filename.split(".")[0]

        # 读取文件的第一行
        with open(os.path.join(folder_path, filename), "r") as f:
            first_line = f.readline().strip()

        # 提取 REMARK 中的 Zxxxxxx 编号
        match = re.search(r"REMARK\s+Name\s*=\s*([A-Za-z0-9]+)", first_line)
        if match:
            z_number = match.group(1)
        else:
            z_number = "N/A"

        data.append({"File_ID": int(file_id), "Z_Number": z_number})

# 生成 DataFrame 并保存为 Excel
df = pd.DataFrame(data)
df.to_excel("output.xlsx", index=False)
print("提取完成，结果已保存到 output.xlsx")
