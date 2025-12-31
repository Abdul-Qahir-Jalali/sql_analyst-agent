"""
Export retail_analytics database to SQL file for PlanetScale migration
"""
import mysql.connector
import yaml
from datetime import datetime

def load_config():
    with open("config.yaml", 'r') as f:
        return yaml.safe_load(f)

def export_database():
    config = load_config()
    db_config = config['database']
    
    print("=" * 60)
    print("EXPORTING DATABASE TO SQL FILE")
    print("=" * 60)
    
    # Connect to database
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    cursor = conn.cursor()
    
    # Create export file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"retail_analytics_export_{timestamp}.sql"
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        print(f"\nFound {len(tables)} tables: {', '.join(tables)}")
        print(f"\nExporting to: {filename}\n")
        
        for table in tables:
            print(f"Exporting table: {table}...")
            
            # Get CREATE TABLE statement
            cursor.execute(f"SHOW CREATE TABLE {table}")
            create_stmt = cursor.fetchone()[1]
            f.write(f"\n-- Table: {table}\n")
            f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
            f.write(f"{create_stmt};\n\n")
            
            # Get all data
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            if rows:
                # Get column names
                cursor.execute(f"DESCRIBE {table}")
                columns = [col[0] for col in cursor.fetchall()]
                
                f.write(f"-- Data for table: {table}\n")
                f.write(f"INSERT INTO `{table}` (`{'`, `'.join(columns)}`) VALUES\n")
                
                for i, row in enumerate(rows):
                    # Escape values properly
                    values = []
                    for val in row:
                        if val is None:
                            values.append('NULL')
                        elif isinstance(val, str):
                            # Escape single quotes and backslashes
                            escaped = val.replace('\\', '\\\\').replace("'", "\\'")
                            values.append(f"'{escaped}'")
                        else:
                            values.append(str(val))
                    
                    row_str = f"({', '.join(values)})"
                    if i < len(rows) - 1:
                        f.write(f"{row_str},\n")
                    else:
                        f.write(f"{row_str};\n\n")
                
                print(f"  ✓ Exported {len(rows)} rows")
            else:
                print(f"  ✓ Table is empty")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print(f"✅ Export completed successfully!")
    print(f"📁 File saved: {filename}")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Create a PlanetScale account")
    print("2. Create a new database")
    print("3. Import this SQL file")
    print("=" * 60)

if __name__ == "__main__":
    export_database()
