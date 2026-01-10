from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs

def load_molecules_from_sdf(sdf_file):
    """加载 SDF 文件中的分子"""
    suppl = Chem.SDMolSupplier(sdf_file)
    return [mol for mol in suppl if mol is not None]

def compute_fingerprints(molecules, radius=2, n_bits=2048):
    """计算分子的 Morgan 指纹"""
    fingerprints = []
    for mol in molecules:
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        fingerprints.append(fp)
    return fingerprints

def compare_fingerprints(fps1, fps2):
    """比较两个指纹列表，返回相似性矩阵"""
    similarity_matrix = []
    for fp1 in fps1:
        row = [DataStructs.TanimotoSimilarity(fp1, fp2) for fp2 in fps2]
        similarity_matrix.append(row)
    return similarity_matrix

# 输入 SDF 文件路径
sdf_file1 = "F:/docking_dataset/fold_mmp9_single_full_data/GRI977143.sdf"
sdf_file2 = "F:/docking_dataset/fold_mmp9_single_full_data/beta-Neo-endorphin.sdf"

# 加载分子
molecules1 = load_molecules_from_sdf(sdf_file1)
molecules2 = load_molecules_from_sdf(sdf_file2)

# 计算指纹
fps1 = compute_fingerprints(molecules1)
fps2 = compute_fingerprints(molecules2)

# 计算相似性
similarity_matrix = compare_fingerprints(fps2, fps1)

# 打印结果
for i, row in enumerate(similarity_matrix):
    print(f"Molecule {i+1} in file1 similarities:")
    for j, similarity in enumerate(row):
        print(f"  Similarity to Molecule {j+1} in file2: {similarity:.3f}")
