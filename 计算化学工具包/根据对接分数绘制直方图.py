# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 12:30:12 2024

@author: yqz
"""

import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV 文件


# 检查数据

# 绘制直方图
column_name = "Best_Score"  # 替换为你要绘制直方图的列名
for i in range(1):
        
        # file_path = f"F:/docking_dataset/郑州超算/batch/27w分子txt日志/{i}.txt"  # 替换为你的 CSV 文件路径
        file_path='F:/docking_dataset/database/Enamine_CNS_Library_plated_47360cmpds_20221006_fromMCE/result.csv'
        output_path='F:/docking_dataset/database/Enamine_CNS_Library_plated_47360cmpds_20221006_fromMCE/'
        # data = pd.read_csv(file_path,sep='\t')
        data = pd.read_csv(file_path)
        plt.figure( dpi=1200) 
        
        # 绘制直方图并获取统计值
        counts, bins, patches = plt.hist(data[column_name], bins=30, color='blue', edgecolor='black')
        
        # 显示频次
        for count, x in zip(counts, bins[:-1]):  # bins[:-1] 是每个 bin 的左边界
            plt.text(x + (bins[1] - bins[0]) / 2, count, str(int(count)), ha='center', va='bottom', fontsize=6)
       
        # 设置坐标轴上的边界点
        plt.xticks(bins, rotation=45,fontsize=6)  # 显示每个 bin 的边界点并旋转 45 度以防止重叠
       
        # 添加标题和标签
        plt.title(f'{column_name} totality')
        plt.xlabel(column_name)
        plt.ylabel('Frequency')
        plt.tight_layout()  # 增加整体边距
        # plt.savefig(output_path, dpi=1200, bbox_inches='tight')  # 保存高分辨率图片
        plt.savefig(output_path, dpi=1200)  # 保存高分辨率图片
        plt.show()
