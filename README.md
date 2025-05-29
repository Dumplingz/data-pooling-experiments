# Parent Repository for all EAB experiments


## TPC-H Setup
1. Add unzipped TPC-H generation files to this directory
2. Change the variables in `makefile.suite` to 
    ```
    CC      = gcc
    DATABASE= DB2
    MACHINE = LINUX
    WORKLOAD = TPCH
    ```
3. Make while in the `TPC-H V3.0.1/dbgen` directory: `make -f makefile.suite`
4. Run the following command to generate the data while in the root directory of the project: `python generate_tpch_data.py `
5. The data will be generated in the tpch_workdir directory under each tpch database size (e.g. `tpch_workdir/1GB/customer.tbl`)
6. Clone the submodules `git submodule update --init`
7. Clone any other experimental repositories into this directory.
