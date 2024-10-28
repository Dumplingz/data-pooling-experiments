import duckdb
import os
import sys
import time

if __name__ == '__main__':
    # Experiment setups
    num_MB = sys.argv[1]

    num_trials = int(sys.argv[2])
    
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
    
    # run setup queries
    conn = duckdb.connect()
    conn.execute(table_query)
    conn.execute(load_query)

    # run trials
    for _ in range(num_trials):
        start_time = time.perf_counter()
        res = conn.execute(join_query).fetchall()
        end_time = time.perf_counter()
        for r in res:
            print(res)
            # break
        print(f"Time taken: {end_time - start_time}")