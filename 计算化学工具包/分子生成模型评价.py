# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 16:43:45 2025

@author: yqz
"""

from rdkit import Chem
from rdkit.Chem import AllChem, QED, Crippen
from rdkit.Chem import Descriptors, DataStructs
import numpy as np
import pandas as pd


def read_smi_file(filepath):
    with open(filepath, 'r') as f:
        smiles_list = []
        for line in f:
            line = line.strip()
            if line:
                smiles = line.split()[0]  # 取每行第一个字段
                smiles_list.append(smiles)
    return smiles_list



def analyze_generated_smiles(smiles_list, train_set=None):
    result = {}

    # 1. Validity
    valid_mols = [Chem.MolFromSmiles(s) for s in smiles_list if Chem.MolFromSmiles(s)]
    result['validity'] = len(valid_mols) / len(smiles_list)
    print(result['validity'])
    # 2. Uniqueness
    unique_smiles = set([Chem.MolToSmiles(mol) for mol in valid_mols])
    result['uniqueness'] = len(unique_smiles) / len(valid_mols)
    print(result['uniqueness'])
    # 3. Novelty
    if train_set:
        novel_smiles = [s for s in unique_smiles if s not in train_set]
        result['novelty'] = len(novel_smiles) / len(unique_smiles)
    print(result['novelty'])
    # 4. Diversity
    fps = [AllChem.GetMorganFingerprintAsBitVect(mol, 2) for mol in valid_mols]
    sims = []
    for i in range(len(fps)):
        for j in range(i+1, len(fps)):
            sims.append(DataStructs.TanimotoSimilarity(fps[i], fps[j]))
    result['diversity'] = 1 - np.mean(sims) if sims else 0.0
    print(result['diversity'])
    # # 5. QED, SA, logP 等
    # result['avg_qed'] = np.mean([QED.qed(mol) for mol in valid_mols])
    # result['avg_sa'] = np.mean([calculateScore(mol) for mol in valid_mols])
    # result['avg_logp'] = np.mean([Crippen.MolLogP(mol) for mol in valid_mols])

    return result


train_smiles_list = read_smi_file("F:/ai_drug_gen_method/ChemTSv2-master/data/ChEMBL_220K.smi")


data=pd.read_csv(("F:\\ai_drug_gen_method\\ChemTSv2-master\\result\\cdk2\\3setting_cdk2_vina_binary_per_syn_samemodel\\result_C1.0.csv"))
gener_smiles=data['smiles']
result = analyze_generated_smiles(gener_smiles,train_smiles_list)


print(result)

































