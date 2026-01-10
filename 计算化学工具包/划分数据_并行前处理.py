# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:24:25 2024

@author: ROG
"""

import pandas as pd
import os

# 输入文件路径
input_file = r"./output_MW200-350/smi_MW200-350.csv"

# 读取 CSV 文件
df = pd.read_csv(input_file,header=None)

df_shuffled = df.sample(frac=1).reset_index(drop=True)

# 计算每一份的大小（行数）
num_parts = 20
part_size = len(df) // num_parts  # 每份的行数，整除

# 如果有余数，调整最后一部分的大小
remainder = len(df) % num_parts

# 输出文件夹路径
output_folder = r"./output_MW200-350/split"
os.makedirs(output_folder, exist_ok=True)  # 如果文件夹不存在，创建文件夹

# 分割并保存每个部分
start_row = 0
for i in range(num_parts):
    # 计算当前部分的结束行
    end_row = start_row + part_size + (1 if i < remainder else 0)  # 如果有余数，前几个部分多一个行
    part_df = df_shuffled.iloc[start_row:end_row]
    part_df.columns = ['smiles']
    # 输出文件路径
    output_file = os.path.join(output_folder, f"{i+1}.csv")
    part_df.to_csv(output_file, index=False)  # 保存为新的 CSV 文件
    start_row = end_row  # 更新开始行数

print(f"CSV 文件已分成 {num_parts} 份，并保存到 {output_folder}")
