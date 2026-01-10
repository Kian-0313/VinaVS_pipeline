from rdkit import Chem
from rdkit.Chem import Descriptors
import csv

# === 配置区 ===
input_file = 'F:\\docking_dataset\\database\\Enamine_CNS_Library_plated_47360cmpds_20221006_fromMCE\\47360.smi'   # 输入的 .smi 文件
output_file = 'F:\\docking_dataset\\database\\Enamine_CNS_Library_plated_47360cmpds_20221006_fromMCE\\47360_Molecular_property.csv'  # 输出文件
delimiter = '\t'  # xsv 分隔符

# === 定义要计算的性质 ===
properties = {
    "MolWt": Descriptors.MolWt,
    "LogP": Descriptors.MolLogP,
    "NumHDonors": Descriptors.NumHDonors,
    "NumHAcceptors": Descriptors.NumHAcceptors,
    "TPSA": Descriptors.TPSA,
    "NumRotatableBonds": Descriptors.NumRotatableBonds,
    "RingCount": Descriptors.RingCount,
    "HeavyAtomCount": Descriptors.HeavyAtomCount   # ✅ 新增这一行
}

# === 读取 .smi 文件并处理 ===
results = []
with open(input_file, 'r') as f:
    for line in f:
        parts = line.strip().split()
        if not parts:
            continue
        smi = parts[0]
        name = parts[1] if len(parts) > 1 else ''
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            print(f"⚠️  无法解析 SMILES：{smi}")
            continue
        prop_values = {prop: fn(mol) for prop, fn in properties.items()}
        results.append({
            "Name": name,
            "SMILES": smi,
            **prop_values
        })

# === 写入 xsv 文件 ===
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys(), delimiter=delimiter)
    writer.writeheader()
    writer.writerows(results)

print(f"✅ 共导出 {len(results)} 个分子的性质至 {output_file}")
