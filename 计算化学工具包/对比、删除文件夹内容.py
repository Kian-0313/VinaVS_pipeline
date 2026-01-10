# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 13:55:59 2025

@author: yqz
"""

import os

folder_A = "F:\\docker_container_data\\vina\\FAM171A2\\fishA\\results"
folder_B = "F:\\docker_container_data\\vina\\FAM171A2\\fishA\\ligands"

files_in_A = os.listdir(folder_A)
files_in_B = os.listdir(folder_B)


files_to_delete = list(set(files_in_A) & set(files_in_B))


for file in files_to_delete:
    file_path = os.path.join(folder_B, file)
    if os.path.isfile(file_path):
        os.remove(file_path)

