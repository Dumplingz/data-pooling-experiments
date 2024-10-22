import os
import subprocess

TPCH_GEN_DIR = "./TPC-H V3.0.1/dbgen"
DATASIZES = ['1MB', '10MB', '100MB', '1GB', '10GB']

def main():
    # get working directory and create directory for generated data
    datasize_dirs = []
    cwd = os.getcwd()

    for datasize in DATASIZES:
        new_dir = f"./tpch_workdir/{datasize}"
        os.makedirs(new_dir, exist_ok=True)
        datasize_dirs += [os.path.join(cwd, new_dir)]

    # cd to dbgen directory and generate data
    os.chdir(TPCH_GEN_DIR)
    tpch_dir = os.getcwd()
    print(f"Generating data within {tpch_dir}")

    for datasize, datasize_dir in zip(DATASIZES,datasize_dirs):
        subprocess.run(["dbgen","1"])
        subprocess.run(["mv","*.tbl",datasize_dir])
    
    
if __name__ == "__main__":
    main()