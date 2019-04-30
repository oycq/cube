import os
from multiprocessing import Process

def start_solver():
    os.system("cd ../solver \n python3 my_solver.py")
    
solver_process = Process(target=start_solver)
solver_process.daemon=True
solver_process.start()