import os
import subprocess

TPCH_GEN_DIR = "./TPC-H V3.0.1/dbgen"
# DATASIZES = ['1MB', '10MB', '100MB', '1GB', '10GB']
DATASIZES = ['1MB', '10MB']

def generate_data(datasize, datasize_dir, datasize_dict):
    # get working directory
    cwd = os.getcwd()
    # cd to dbgen directory and generate data
    os.chdir(TPCH_GEN_DIR)
    tpch_dir = os.getcwd()
    print(f"Generating data within {tpch_dir}")

    subprocess.run(["./dbgen",str(datasize_dict[datasize])])
    print("Moving data to",datasize_dir)
    subprocess.run(f"mv *.tbl {datasize_dir}", shell=True)

    # cd back to working directory
    os.chdir(cwd)

def main():
    datasize_dict = {'1MB': 0.001, '10MB': 0.01, '100MB': 0.1, '1GB': 1, '10GB': 10}

    # get working directory and create directory for generated data
    datasize_dirs = []
    cwd = os.getcwd()

    # create directories for each datasize
    for datasize in DATASIZES:
        new_dir = f"./tpch_workdir/{datasize}"
        os.makedirs(new_dir, exist_ok=True)
        datasize_dirs += [os.path.join(cwd, new_dir)]

    for datasize, datasize_dir in zip(DATASIZES, datasize_dirs):
        # check if tbl data already exists
        if os.path.exists(os.path.join(datasize_dir,"customer.tbl")):
            print(f"Data already exists for .tbl files of datasize {datasize}. Skipping data generation.")
        else:
            generate_data(datasize, datasize_dir, datasize_dict)    
    
    
if __name__ == "__main__":
    main()