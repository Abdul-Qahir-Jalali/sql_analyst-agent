"""
Convert MySQL database to SQLite - Simplified version
"""
import mysql.connector
import sqlite3
import yaml

# Load config
with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

db_config = config['database']

print("Connecting to MySQL...")
mysql_conn = mysql.connector.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password'],
    database=db_config['database']
)

print("Creating SQLite database...")
sqlite_conn = sqlite3.connect("retail_analytics.db")

mysql_cur = mysql_conn.cursor()
sqlite_cur = sqlite_conn.cursor()

# Get tables
mysql_cur.execute("SHOW TABLES")
tables = [t[0] for t in mysql_cur.fetchall()]

print(f"Found tables: {tables}\n")

for table in tables:
    print(f"Converting {table}...")
    
    # Get all data first
    mysql_cur.execute(f"SELECT * FROM {table}")
    rows = mysql_cur.fetchall()
    
    if not rows:
        print(f"  Skipping empty table")
        continue
    
    # Get column info
    mysql_cur.execute(f"DESCRIBE {table}")
    cols = mysql_cur.fetchall()
    
    # Create table
    col_defs = []
    for col in cols:
        name = col[0]
        dtype = str(col[1])
        
        sql_type = "TEXT"
        if "int" in dtype.lower():
            sql_type = "INTEGER"
        elif "decimal" in dtype.lower() or "float" in dtype.lower():
            sql_type = "REAL"
        
        pk = " PRIMARY KEY" if col[3] == "PRI" else ""
        col_defs.append(f"{name} {sql_type}{pk}")
    
    create_sql = f"CREATE TABLE {table} ({', '.join(col_defs)})"
    sqlite_cur.execute(create_sql)
    
    # Insert data
    placeholders = ','.join(['?' for _ in cols])
    insert_sql = f"INSERT INTO {table} VALUES ({placeholders})"
    
    # Convert decimal to float for SQLite
    clean_rows = []
    for row in rows:
        clean_row = []
        for val in row:
            if hasattr(val, '__float__'):  # Decimal type
                clean_row.append(float(val))
            else:
                clean_row.append(val)
        clean_rows.append(tuple(clean_row))
    
    sqlite_cur.executemany(insert_sql, clean_rows)
    print(f"  ✓ Copied {len(rows)} rows")

sqlite_conn.commit()
sqlite_conn.close()
mysql_conn.close()

print("\n✅ Done! Created: retail_analytics.db")
