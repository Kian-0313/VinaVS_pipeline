#数据预处理，生成3D结构
python 1_generate_pdbqt_with_charge.py
#分配任务，用于并行 python 2_distribution_dock_task.py <task_num> vina_cpu默认占用1，可自行调整
python 2_distribution_dock_task.py 1
#提取对接数据
python  3_from_vina_2record.py