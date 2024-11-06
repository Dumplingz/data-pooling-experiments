import duckdb
import os
import sys
import time
import csv

if __name__ == '__main__':
    # Experiment setups
    num_MB = sys.argv[1]

    num_trials = int(sys.argv[2])
    
    total_start = time.perf_counter()
    # get agent des
    agent_des = []
    for agent in ["1", "2"]:
        agent_des.append(f"../tpch_workdir/{num_MB}/split0.5/orders{agent}.tbl")

    table_query = """
    CREATE TABLE ORDERS1  ( O_ORDERKEY       INTEGER NOT NULL,
                O_CUSTKEY        INTEGER NOT NULL,
                O_ORDERSTATUS    CHAR(1) NOT NULL,
                O_TOTALPRICE     DECIMAL(15,2) NOT NULL,
                O_ORDERDATE      DATE NOT NULL,
                O_ORDERPRIORITY  CHAR(15) NOT NULL,  
                O_CLERK          CHAR(15) NOT NULL, 
                O_SHIPPRIORITY   INTEGER NOT NULL,
                O_COMMENT        VARCHAR(79) NOT NULL);

    CREATE TABLE ORDERS2  ( O_ORDERKEY       INTEGER NOT NULL,
                O_CUSTKEY        INTEGER NOT NULL,
                O_ORDERSTATUS    CHAR(1) NOT NULL,
                O_TOTALPRICE     DECIMAL(15,2) NOT NULL,
                O_ORDERDATE      DATE NOT NULL,
                O_ORDERPRIORITY  CHAR(15) NOT NULL,  
                O_CLERK          CHAR(15) NOT NULL, 
                O_SHIPPRIORITY   INTEGER NOT NULL,
                O_COMMENT        VARCHAR(79) NOT NULL);
    """

    load_query = f"""
    COPY ORDERS1 FROM '{agent_des[0]}' DELIMITER '|';
    COPY ORDERS2 FROM '{agent_des[1]}' DELIMITER '|';
    """

    join_query = """
    SELECT COUNT(*) FROM ORDERS1 o1 JOIN ORDERS2 o2 ON o1.o_custkey = o2.o_custkey;
    """

    full_query = """
CREATE TABLE ORDERS1  ( O_ORDERKEY       INTEGER NOT NULL,
            O_CUSTKEY        INTEGER NOT NULL,
            O_ORDERSTATUS    CHAR(1) NOT NULL,
            O_TOTALPRICE     DECIMAL(15,2) NOT NULL,
            O_ORDERDATE      DATE NOT NULL,
            O_ORDERPRIORITY  CHAR(15) NOT NULL,  
            O_CLERK          CHAR(15) NOT NULL, 
            O_SHIPPRIORITY   INTEGER NOT NULL,
            O_COMMENT        VARCHAR(79) NOT NULL);

CREATE TABLE ORDERS2  ( O_ORDERKEY       INTEGER NOT NULL,
            O_CUSTKEY        INTEGER NOT NULL,
            O_ORDERSTATUS    CHAR(1) NOT NULL,
            O_TOTALPRICE     DECIMAL(15,2) NOT NULL,
            O_ORDERDATE      DATE NOT NULL,
            O_ORDERPRIORITY  CHAR(15) NOT NULL,  
            O_CLERK          CHAR(15) NOT NULL, 
            O_SHIPPRIORITY   INTEGER NOT NULL,
            O_COMMENT        VARCHAR(79) NOT NULL);

COPY ORDERS1 FROM '{de1_filepath}' DELIMITER '|';
COPY ORDERS2 FROM '{de2_filepath}' DELIMITER '|';

SELECT COUNT(*) FROM ORDERS1 o1 JOIN ORDERS2 o2 ON o1.o_custkey = o2.o_custkey;"""
    
    query = full_query.format(de1_filepath=agent_des[0], de2_filepath=agent_des[1])
    # run setup queries
    conn = duckdb.connect()
    # conn.execute(table_query)
    # conn.execute(load_query)
    
    # create exp directory
    os.makedirs(f"experiments/join", exist_ok=True)

    # run trials
    for _ in range(num_trials):
        start_time = time.perf_counter()
        # res = conn.execute(join_query).fetchall()
        res = conn.execute(query).fetchall()
        end_time = time.perf_counter()
        total_time = end_time - start_time
        for r in res:
            print(res)
            # break
        print(f"Time taken: {total_time}")
        with open(f"experiments/join/{num_MB}.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([total_time])

    total_end = time.perf_counter()
    print(total_end - total_start)