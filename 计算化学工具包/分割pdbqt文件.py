import os
import re
# 输入文件夹路径
input_folder = "F:/docking_dataset/database/Enamine_CNS_Library_plated_47360cmpds_20221006_fromMCE/"  # 包含多个待分割文件的文件夹
output_folder = "F:/docking_dataset/database/Enamine_CNS_Library_plated_47360cmpds_20221006_fromMCE/name"  # 输出文件夹

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 初始化全局计数器
global_file_count = 0

# 遍历输入文件夹中的所有文件
for file_name in os.listdir(input_folder):
    input_file_path = os.path.join(input_folder, file_name)
    if not file_name.endswith(".pdbqt"):  # 只处理pdbqt文件
        continue

    # 处理每个输入文件
    with open(input_file_path, "r") as f:
        current_model = []
        start_recording = False

        for line in f:
            # 检查起点
            # if line.startswith("REMARK  Name"):
            if line.startswith("MODEL"):    
                match=re.match(r'^MODEL\s+(\d+)', line)
                name=match.group(1)
                print(name)
                line=''                
                if current_model:  # 如果已经有模型，保存当前模型
                    global_file_count += 1
                    output_file = os.path.join(output_folder, f"{name}.pdbqt")
                    with open(output_file, "w") as out_f:
                        out_f.writelines(current_model)
                    current_model = []  # 清空以存储下一个模型
                start_recording = True  # 开始记录新的模型

            # 检查终点
            if line.startswith("TORSDOF") and start_recording:
                current_model.append(line)  # 添加TORSDOF行
                # 保存当前模型
                global_file_count += 1
                output_file = os.path.join(output_folder, f"{name}.pdbqt")
                with open(output_file, "w") as out_f:
                    out_f.writelines(current_model)
                current_model = []  # 清空以存储下一个模型
                start_recording = False  # 停止记录

            # 如果处于记录状态，将行添加到当前模型
            if start_recording:
                current_model.append(line)

print(f"文件处理完成！总共分割生成了 {global_file_count} 个模型文件，存放于文件夹：{output_folder}")
