import psycopg2
import os
import glob

# Read password
with open(os.path.join("secrets", "psql.pass"), "r") as f:
    password = f.read().strip()

# Connection string (Python 2/3 compatible)
conn_string = (
    "host=hadoop-04.uni.innopolis.ru "
    "port=5432 "
    "user=team19 "
    "dbname=team19_projectdb "
    "password=" + password
)

# Paths
sql_create = os.path.join("sql", "create_tables.sql")
csv_dir = os.path.join("data", "monthly_trips")
csv_files = sorted(glob.glob(os.path.join(csv_dir, "2023-*.csv")))

copy_sql = """
COPY citibike_trips FROM STDIN WITH (FORMAT CSV, HEADER true, DELIMITER ',');
"""

def main():
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    
    # 1. Create table
    with open(sql_create, "r") as f:
        cur.execute(f.read())
    conn.commit()
    print("Table created (or re-created).")
    
    # 2. Load each CSV
    for csv_path in csv_files:
        file_name = os.path.basename(csv_path)
        print("Loading {} ...".format(file_name))
        with open(csv_path, "r") as f:
            cur.copy_expert(copy_sql, f)
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM citibike_trips;")
        total = cur.fetchone()[0]
        print("  Total rows so far: {}".format(total))
    
    # 3. Final count
    cur.execute("SELECT COUNT(*) FROM citibike_trips;")
    final_count = cur.fetchone()[0]
    print("All data loaded. Total rows: {}".format(final_count))
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
