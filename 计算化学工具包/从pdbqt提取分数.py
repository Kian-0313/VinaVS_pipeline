# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 18:56:13 2024

@author: yqz
"""
import os
import re
import pandas as pd
import numpy
output_folder='F:\\docker_container_data\\vina\\FAM171A2\\fishA\\'
input_folder=output_folder+"results"
data=[]


for file_name in os.listdir(input_folder):
    input_file_path = os.path.join(input_folder, file_name)
    if not file_name.endswith(".pdbqt"):  # 只处理pdbqt文件
        continue

    # 处理每个输入文件
    with open(input_file_path, "r") as f:
        current_model = []
        f = f.read()
        start_recording = False

        # 使用正则表达式提取分数
        vina_results = re.findall(r"REMARK VINA RESULT:\s+(-?\d+\.\d+)", f)
        Best_Score=vina_results[0]
        vina_results = list(map(float, vina_results))
        Average_Score=numpy.mean(vina_results)
        data.append({ "Ligand":file_name,
                    "Best_Score":Best_Score,
                    "Average_Score":Average_Score   })

df = pd.DataFrame(data)

# 指定要保存的 CSV 文件名
filename = 'F:\\docker_container_data\\vina\\FAM171A2\\human'
# 将 DataFrame 保存为 CSV 文件
df.to_csv(output_folder+"results.csv", index=False)

print(f"Data has been written to {filename}")

        # 打印结果
        # for i, score in enumerate(vina_results, start=1):
                # print(f"MODEL {i}: {score}")
#         for line in f:
#             # 检查起点
#             # if line.startswith("REMARK  Name"):
#             if line.startswith("MODEL"):
#                 match=re.match(r'^MODEL\s+(\d+)', line)
#                 name=match.group(1)
#                 print(name)
#                 line=''
#                 if current_model:  # 如果已经有模型，保存当前模型
#                     global_file_count += 1
#                     output_file = os.path.join(output_folder, f"{name}.pdbqt")
#                     with open(output_file, "w") as out_f:
#                         out_f.writelines(current_model)
#                     current_model = []  # 清空以存储下一个模型
#                 start_recording = True  # 开始记录新的模型

#             # 检查终点
#             if line.startswith("TORSDOF") and start_recording:
#                 current_model.append(line)  # 添加TORSDOF行
#                 # 保存当前模型
#                 global_file_count += 1
#                 output_file = os.path.join(output_folder, f"{name}.pdbqt")
#                 with open(output_file, "w") as out_f:
#                     out_f.writelines(current_model)
#                 current_model = []  # 清空以存储下一个模型
#                 start_recording = False  # 停止记录

#             # 如果处于记录状态，将行添加到当前模型
#             if start_recording:
#                 current_model.append(line)

# print(f"文件处理完成！总共分割生成了 {global_file_count} 个模型文件，存放于文件夹：{output_folder}")

