import sqlite3
import csv
import os

os.chdir(r"D:\dungeons_and_dragons\Custom_Programs\sidekick_files\databases")

DB_STR = "drusus_scrutatorum_database.db"

# Database connection function with foreign keys enabled
def get_connection(db_path=DB_STR):
    conn_out = sqlite3.connect(db_path)
    conn_out.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign keys are enabled
    return conn_out

conn = get_connection(DB_STR)
cursor = conn.cursor()

table_name = "char_atributes"

cursor.execute(f"SELECT * FROM {table_name}")
rows = cursor.fetchall()

with open(f"csv_files\{table_name}.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([desc[0] for desc in cursor.description])  # Write headers
    writer.writerows(rows)  # Write data

conn.close()
