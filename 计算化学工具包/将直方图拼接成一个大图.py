# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 12:57:25 2024

@author: yqz
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 图像文件路径列表
image_files = [f"F:/docking_dataset/27w_docking_results/best300_every_batch/{i}.png" for i in range(15)]  # 替换为实际路径
output_path= 'F:/docking_dataset/27w_docking_results/best300_every_batch/all_in.png'
# 创建子图网格（3 行 5 列）
rows, cols = 3, 5
plt.figure( dpi=600)
fig, axes = plt.subplots(rows, cols, figsize=(15, 9))

# 遍历子图并加载图像
for i, ax in enumerate(axes.flat):
    if i < len(image_files):
        img = mpimg.imread(image_files[i])  # 加载第 i 张图像
        ax.imshow(img)
        ax.axis('off')
    else:
        ax.axis('off')  # 关闭多余子图

# 调整整体布局
plt.tight_layout()
plt.savefig(output_path, dpi=600, bbox_inches='tight')
plt.show()