import sqlite3
import csv
import os

os.chdir(r"D:\dungeons_and_dragons\Custom_Programs\sidekick_files\databases")

DB_STR = "equipment_master.db"

# Database connection function with foreign keys enabled
def get_connection(db_path=DB_STR):
    conn_out = sqlite3.connect(db_path)
    conn_out.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign keys are enabled
    return conn_out



# Function to upload CSV equipment data into the SQLite table
def upload_em_to_db(csv_filepath, db_path=DB_STR):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Open and read the CSV file
    with open(csv_filepath, "r", newline="", encoding="ISO-8859-1") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column headers)

        # Insert rows into the equipment_master table
        for row in reader:
            cursor.execute("""
                INSERT INTO equipment_master (id, nm, cst, wght, desc)
                VALUES (?, ?, ?, ?, ?)
            """, (int(row[0]), row[1], float(row[2]), float(row[3]), row[4]))

    # Commit and close connection
    conn.commit()
    conn.close()
    print("Equipment data successfully uploaded to the database.")

# Function to upload CSV weapon data into the SQLite table
def upload_w_to_db(csv_filepath, db_path=DB_STR):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Open and read the CSV file
    with open(csv_filepath, "r", newline="", encoding="ISO-8859-1") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column headers)

        # Insert rows into the weapon table
        for row in reader:
            cursor.execute("""
                INSERT INTO weapon (id, nm, is_mrtl, dam_amt, dam_die, dam_typ, has_fin, i_t_h, has_vers, vers_die,
                                    has_rng, norm_rng, max_rng, c_b_thrw, is_l, is_h, is_load, use_ammo, is_rch, is_spcl, is_slvd)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (int(row[0]),
                  row[1],  # nm
                  bool(int(row[2])),  # is_mrtl (convert 1/0 to Boolean)
                  int(row[3]),  # dam_amt
                  int(row[4]),  # dam_die
                  row[5],  # dam_typ
                  bool(int(row[6])),  # has_fin (convert 1/0 to Boolean)
                  bool(int(row[7])),  # i_t_h (convert 1/0 to Boolean)
                  bool(int(row[8])),  # has_vers (convert 1/0 to Boolean)
                  int(row[9]) if row[9] else None,  # vers_die (can be null)
                  bool(int(row[10])),  # has_rng (convert 1/0 to Boolean)
                  int(row[11]) if row[11] else None,  # norm_rng (can be null)
                  int(row[12]) if row[12] else None,  # max_rng (can be null)
                  bool(int(row[13])),  # c_b_thrw (convert 1/0 to Boolean)
                  bool(int(row[14])),  # is_l (convert 1/0 to Boolean)
                  bool(int(row[15])),  # is_h (convert 1/0 to Boolean)
                  bool(int(row[16])),  # is_load (convert 1/0 to Boolean)
                  bool(int(row[17])),  # use_ammo (convert 1/0 to Boolean)
                  bool(int(row[18])),  # is_rch (convert 1/0 to Boolean)
                  bool(int(row[19])),  # is_spcl (convert 1/0 to Boolean)
                  bool(int(row[20]))   # is_slvd (convert 1/0 to Boolean)
                  ))

    # Commit and close connection
    conn.commit()
    conn.close()
    print("Weapon data successfully uploaded to the database.")

def upload_a_to_db(csv_filepath, db_path=DB_STR):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Open and read the CSV file
    with open(csv_filepath, "r", newline="", encoding="ISO-8859-1") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column headers)

        # Insert rows into the equipment_master table
        for row in reader:
            cursor.execute("""
                INSERT INTO armor (id, nm, ac, ar_type, stlth, need_str)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (int(row[0]), row[1], int(row[2]), int(row[3]), bool(row[4]), int(row[5])))

    # Commit and close connection
    conn.commit()
    conn.close()
    print("Armor data successfully uploaded to the database.")

def upload_t_to_db(csv_filepath, db_path=DB_STR):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Open and read the CSV file
    with open(csv_filepath, "r", newline="", encoding="ISO-8859-1") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column headers)

        # Insert rows into the equipment_master table
        for row in reader:
            cursor.execute("""
                INSERT INTO tools (id, nm)
                VALUES (?, ?)
            """, (int(row[0]), row[1]))

    # Commit and close connection
    conn.commit()
    conn.close()
    print("Tool data successfully uploaded to the database.")

def upload_i_to_db(csv_filepath, db_path=DB_STR):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Open and read the CSV file
    with open(csv_filepath, "r", newline="", encoding="ISO-8859-1") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column headers)

        # Insert rows into the equipment_master table
        for row in reader:
            cursor.execute("""
                INSERT INTO instruments (id, nm)
                VALUES (?, ?)
            """, (int(row[0]), row[1]))

    # Commit and close connection
    conn.commit()
    conn.close()
    print("Instrument data successfully uploaded to the database.")

def upload_cur_to_db(csv_filepath, db_path=DB_STR):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Open and read the CSV file
    with open(csv_filepath, "r", newline="", encoding="ISO-8859-1") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column headers)

        # Insert rows into the equipment_master table
        for row in reader:
            cursor.execute("""
                INSERT INTO currency (id, nm, cst)
                VALUES (?, ?, ?)
            """, (int(row[0]), row[1], float(row[2])))

    # Commit and close connection
    conn.commit()
    conn.close()
    print("currency data successfully uploaded to the database.")

def upload_con_to_db(csv_filepath, db_path=DB_STR):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Open and read the CSV file
    with open(csv_filepath, "r", newline="", encoding="ISO-8859-1") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column headers)

        # Insert rows into the equipment_master table
        for row in reader:
            cursor.execute("""
                INSERT INTO containers (id, nm, lq_cap, sd_cap, 
                                      car_cap, ammo_a, amt_a, ammo_b, amt_b)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (int(row[0]),
                  row[1],
                  float(row[2]) if row[2] else None, # The containers liquid volume
                  float(row[3]) if row[3] else None, # The containers solid volume
                  float(row[4]) if row[4] else None, # the containers weight capacity
                  int(row[5]) if row[5] else None, # the id of the primary ammo type
                  int(row[6]) if row[6] else None, # the primary ammo type capacity
                  int(row[7]) if row[7] else None, # the id of the secondary ammmo type
                  int(row[8]) if row[8] else None)) # the secondary ammo type capacity

    # Commit and close connection
    conn.commit()
    conn.close()
    print("container data successfully uploaded to the database.")

def upload_char_atributes(csv_filepath):
    conn = get_connection(r"D:\dungeons_and_dragons\Custom_Programs\sidekick_files\databases\drusus_scrutatorum_database.db")
    cursor = conn.cursor()

    # Open and read the CSV file
    with open(csv_filepath, "r", newline="", encoding="ISO-8859-1") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column headers)

        for row in reader:
            cmd_str = "INSERT INTO char_att (id, atr, val) VALUES (?, ?, ?)"
            cursor.execute(cmd_str, (int(row[0]), row[1], int(row[2])))

    # Commit and close connection
    conn.commit()
    conn.close()
    print("attribute data successfully uploaded to the database.")


#############
upload_char_atributes('csv_files//char_atributes.csv')