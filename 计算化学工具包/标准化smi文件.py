from rdkit import Chem
from rdkit.Chem import MolStandardize
import sys

# # 初始化标准化器
# normalizer = MolStandardize.normalize.Normalizer()
# fragment_remover = MolStandardize.fragment.LargestFragmentChooser()
# uncharger = MolStandardize.charge.Uncharger()

def get_largest_fragment(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    frags = Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True)
    if not frags:
        return None
    largest = max(frags, key=lambda m: m.GetNumAtoms())
    return Chem.MolToSmiles(largest, isomericSmiles=True)

def normalize_smi_file(input_file, output_file):
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        count_in, count_out = 0, 0
        for line in fin:
            count_in += 1
            smi = line.strip()
            if not smi:
                continue
            norm_smi = get_largest_fragment(smi)
            if norm_smi:
                fout.write(norm_smi + '\n')
                count_out += 1
        print(f"✅ 共读取 {count_in} 个分子，输出 {count_out} 个主碎片 SMILES")

if __name__ == "__main__":
    # if len(sys.argv) != 3:
        # print("用法: python normalize_standardize_smi.py 输入文件.smi 输出文件.smi")
        # sys.exit(1)

    _in="F:\docker_container_data\ChemTSv2\data\Enamine_CNS_47360.smi"
    _out="F:\docker_container_data\ChemTSv2\data\Enamine_CNS_47360_standared.smi"

    normalize_smi_file(_in, _out)
