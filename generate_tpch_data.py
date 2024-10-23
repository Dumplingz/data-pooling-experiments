import os
import subprocess
import csv

TPCH_GEN_DIR = "./TPC-H V3.0.1/dbgen"
DATASIZES = ['1MB', '10MB', '100MB', '1GB', '10GB']
# DATASIZES = ['1MB', '10MB']
SPLIT_RATIOS = [0.09,0.5]

def select_custkey(file_name, out_file):
    """
    Selects the custkey column from the input file and writes it to the output file
    """
    custkey_column = []
    with open(file_name, 'r') as input_file:
        # Read the content of the input file
        content = csv.reader(input_file, delimiter='|')
        # print(content)
        for row in content:
            custkey_column.append(row[1])
            # print(row[1])

        # Extract the custkey column from the content
        # custkey_column = [line.split('|')[1] for line in content]
        # print(custkey_column)
    with open(out_file, 'w') as first_output_file:
        writer = csv.writer(first_output_file, delimiter=',')
        for custkey in custkey_column:
            writer.writerow([custkey])


# split 1MB ... 10GB orders.csv into two files of size ratio "ratio"
def split_file(file_name, out_file, ratio):
    full_file_path = "./" + file_name
    out_path = f"./split{ratio}"
    # create directory if it does not exist
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # Get the size of the file in bytes
    num_lines = sum(1 for _ in open(full_file_path, 'r'))

    # Calculate the size of the first file based on the ratio
    first_file_size = int(num_lines * ratio)

    # Open the input file for reading
    with open(full_file_path, 'r') as input_file:
        # Read the content of the input file
        content = input_file.readlines()

        # Split the content into two parts based on the first file size
        first_file_content = content[:first_file_size]
        second_file_content = content[first_file_size:]

    # Create the first output file
    first_file_path = out_path + "/" + out_file + '1.tbl'
    with open(first_file_path, 'w') as first_output_file:
        first_output_file.writelines(first_file_content)

    # Create the second output file
    second_file_path = out_path + "/" + out_file + '2.tbl'
    with open(second_file_path, 'w') as second_output_file:
        second_output_file.writelines(second_file_content)

# generate tpch data and put it into the directory specified
def generate_data(datasize, directory, datasize_dict):
    # get working directory
    cwd = os.getcwd()
    # cd to dbgen directory and generate data
    os.chdir(TPCH_GEN_DIR)
    tpch_dir = os.getcwd()
    print(f"Generating data within {tpch_dir} of size {str(datasize_dict[datasize])}")

    subprocess.run(["./dbgen","-s",str(datasize_dict[datasize])])
    print("Moving data to",directory)
    subprocess.run(f"mv *.tbl {directory}", shell=True)

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

    # generate data for each datasize
    for datasize, datasize_dir in zip(DATASIZES, datasize_dirs):
        # check if tbl data already exists
        if os.path.exists(os.path.join(datasize_dir,"customer.tbl")):
            print(f"Data already exists for '.tbl' files of datasize {datasize}. Skipping data generation.")
        else:
            generate_data(datasize, datasize_dir, datasize_dict)

    # split orders table for each datasize
    cwd = os.getcwd()
    for data_size, datasize_dir in zip(DATASIZES, datasize_dirs):
        print(f"Trying to split orders for size {data_size} in directory {datasize_dir}.")
        if all([os.path.exists(os.path.join(datasize_dir,f"split{ratio}/orders1.tbl")) for ratio in SPLIT_RATIOS]):
            print(f"Data already split for orders on {data_size}. Skipping data splitting.")
            continue
        os.chdir(datasize_dir)
        for ratio in SPLIT_RATIOS:
            split_file("orders.tbl", "orders", ratio)
    # cd back to working directory
    os.chdir(cwd)
    
    # select custkey from the split orders table
    for data_size, datasize_dir in zip(DATASIZES, datasize_dirs):
        print(f"Trying to extract custkey for size {data_size} in directory {datasize_dir}")
        if all([os.path.exists(os.path.join(datasize_dir,f"split{ratio}/orders1.csv")) for ratio in SPLIT_RATIOS]):
            print(f"Custkey already extracted on {data_size}. Skipping.")
            continue
        os.chdir(datasize_dir)
        for ratio in SPLIT_RATIOS:
            select_custkey(f"split{ratio}/orders1.tbl", f"split{ratio}/orders1.csv")
            select_custkey(f"split{ratio}/orders2.tbl", f"split{ratio}/orders2.csv")


if __name__ == "__main__":
    main()