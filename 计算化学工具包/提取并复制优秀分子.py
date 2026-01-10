# -*- coding: utf-8 -*
"""
Created on Sat Dec  7 21:01:57 2024

@author: ROG
"""

import os
import shutil
import pandas as pd
import csv
import re
# 输入文件夹路径
input_folder = "F:\\hpc_data\\61-base04-c1.5\\3D_pose"


def sort_and_copy(key_word,data,num):
    id_list=[]


    '''排序并获取排序后的文件名'''
    data_sort_key_word = data.sort_values(by=key_word,ascending=False)
    if num!=0:
        record = data_sort_key_word[0:num]
    select_file_id = list(record["generated_id"])
    reward        = list(record["reward"])

    print(select_file_id,reward)
    '''创建输出文件夹（如果不存在）'''
    destination_folder=destination_path+key_word
    os.makedirs(destination_folder, exist_ok=True)

    '''复制文件到目标文件夹'''
    for file_id,score in zip(select_file_id,reward):
        print(file_id)
        score=round(score,3)
        file_name=f'mol_{file_id}_out.pdbqt'
        input_file_path = os.path.join(input_folder, file_name)
        destination_file_name=destination_folder+f'\\{score}_{file_name}'
        try:
         shutil.copy(input_file_path, destination_file_name)
        except:
            print("复制失败")

    record.to_csv(destination_path+'\\'+key_word+'.csv', index=True)


def copy_with_per_heavyatom(key_word,data,num):

    '''排序并获取排序后的文件名'''
    data_sort_key_word = data.sort_values(by=key_word)
    if num!=0:
        record = data_sort_key_word[0:num]
    else:
        record=data_sort_key_word

    select_file_name = record["Ligand"]
    heavy_atom_list  = record["HeavyAtomCount"]
    per_score        = record["per"]


    '''创建输出文件夹（如果不存在）'''
    destination_folder=destination_path+key_word
    os.makedirs(destination_folder, exist_ok=True)

    '''复制文件到目标文件夹'''
    for file_name,hvyatom,per in zip(select_file_name,heavy_atom_list,per_score):
        file_name=str(file_name)+".pdbqt"
        per = round(per, 3)
        input_file_path = os.path.join(input_folder, file_name)
        destination_file_name=destination_folder+f'\\{hvyatom}_{per}_{file_name}'
        shutil.copy(input_file_path, destination_file_name)


destination_path="F:\\hpc_data\\61-base04-c1.5\\"

df = pd.read_csv(destination_path+"result_C1.5.csv")

# for i in  range(15):
#     df = pd.read_csv(f'F:/docking_dataset/27w_docking_results/15个结果日志/{i}.txt', sep='\t')
#     destination_path = f"F:\\docking_dataset\\27w_docking_results\\每个日志中优秀的300个分子\\{i}_rank\\"  # 输出文件夹
# df = pd.read_csv("F:\\docking_dataset\\database\\Enamine_CNS_Library_plated_47360cmpds_20221006_fromMCE\\combined_file.csv")



sort_and_copy("reward",df,100)
# copy_with_per_heavyatom("per",df_per, 0)
    # sort_and_copy("Average_Score", 100)
    # sort_and_copy("diff", 100)






