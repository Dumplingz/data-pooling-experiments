<meta name="robots" content="noindex">

# Parent Repository for all EAB experiments

This repository contains the experimental code and results in the paper "Running Functions on Pooled Data without Leakage: Comparing Solutions Over Scope, Trust, and Performance".

It has a number of submodules, each of which contains the code and results for either a group of experiments or a specific experiment. The submodules are:
- [lattigo-experiments](https://github.com/Dumplingz/lattigo-experiments.git): Experimental code and results for Lattigo.
- [eab-nn-experiments](https://github.com/Dumplingz/eab-nn-experiments.git): Experimental code and results for PyTorch and Crypten.
- [eab-nvflare-experiments](https://github.com/Dumplingz/eab-nvflare-experiments.git): Experimental code and results for NVFlare.
- [ccfjoin](https://github.com/tapansriv/ccfjoin.git): Experimental code and results for CCF.
- [datastation-escrow](https://github.com/TheDataStation/datastation-escrow/tree/447cf7146e0a9464a779c612fc6bc45105175ca7): Experimental code and results for Data Station.
- [secretflow-experiments](https://github.com/Dumplingz/secretflow-experiments.git): Experimental code and results for Secretflow.


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