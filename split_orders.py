import os

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
    first_file_path = out_path + "/" + out_file + '1.csv'
    with open(first_file_path, 'w') as first_output_file:
        first_output_file.writelines(first_file_content)

    # Create the second output file
    second_file_path = out_path + "/" + out_file + '2.csv'
    with open(second_file_path, 'w') as second_output_file:
        second_output_file.writelines(second_file_content)