# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:20:01 2024

@author: ROG
"""
import pandas as pd
import os
from rdkit import Chem 
from rdkit.Chem import AllChem
import subprocess
#import threading
from multiprocessing import Process
import shutil
import time
import sys


cmd=""
num=sys.argv[1]
for i in range(int(num)):
    if i!=0:
        cmd=cmd+" & "
    cmd=cmd+"python plc1.py "+str(i)
      

result = subprocess.run(cmd, shell=True,capture_output=False,text=False)

#print("命令输出:", result.stdout)
