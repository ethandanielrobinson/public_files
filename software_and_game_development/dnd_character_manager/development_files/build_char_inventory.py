import os
import sqlite3 # Allow us to interact with SQLite files
import json # Allows us to interact with JSON files
import tkinter as tk

# FUNCTION FOR INTIALIZATION
def remove_spaces(text: str):
    """
    A simple function to remove all spaces and convert the string to lowercase

    Parameters
    ----------
    text : str
        The input string to have its last word removed.

    Returns
    -------
    words: str
        the output string with the last word removed.

    """
    words = text.split()
    if words:  # Check if the list is not empty
        return "_".join(words).lower() # replace spacing and uppercase letters
    return "" # Return empty string if the input string is empty or contains only spaces

# Get the directory of the current script--all this is mostly boilerplate
current_dir = os.path.dirname(os.path.abspath(__file__))
# Set it as the working directory
os.chdir(current_dir)

os.chdir(r"D:\dungeons_and_dragons\Custom_Programs\sidekick_files")
with open("filia_kosta.json", "r") as infile:
    CHAR = json.load(infile)
# then link the database to that character

CH_STR = CHAR["db"]
DB_STR = "equipment_master.db"

# THIS IS VERY IMPORTANT
def get_connection(db_path):
    conn_out = sqlite3.connect(db_path)
    conn_out.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign keys are enabled
    return conn_out

###################################################################################
# CREATE TABLES
conn = get_connection("databases/filia_kosta_database.db")
cursor = conn.cursor()

# Clear the inventory?
new_table = False
if new_table:
    for text in ["character_equipment", "char_weapons", "char_armor", "char_containers"]:
        cursor.execute(f"DROP TABLE IF EXISTS {text}")

query_a = """
    CREATE TABLE IF NOT EXISTS character_equipment (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- the objects name
        qnty INTEGER);
    """
query_b = """
    CREATE TABLE IF NOT EXISTS char_weapons (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- The objects name
        qnty INTEGER, -- the objects quantity
        FOREIGN KEY (id) REFERENCES character_equipment(id) ON DELETE CASCADE);"""

query_c = """
    CREATE TABLE IF NOT EXISTS char_armor (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- the armor's name
        qnty INTEGER, -- the armor's quantity
        FOREIGN KEY (id) REFERENCES character_equipment(id) ON DELETE CASCADE);"""

query_d = """
    CREATE TABLE IF NOT EXISTS char_clothing (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- the article of clothings name
        qnty INTEGER, -- the quantity of clothing
        FOREIGN KEY (id) REFERENCES character_equipment(id) ON DELETE CASCADE);"""

query_e = """
    CREATE TABLE If NOT EXISTS char_containers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Intialized ID, THIS IS DIFFERENT FROM THE original ID
        nm TEXT NOT NULL, -- the container's name
        tbl TEXT, -- the name of the attached equipment table
        tot_wght REAL NOT NULL);"""


query_f = """
    CREATE TABLE IF NOT EXISTS char_att (
        id INTEGER PRIMARY KEY,
        atr TEXT NOT NULL, -- The characters atribute key
        val INTEGER NOT NULL);"""

query_g = """
    CREATE TABLE IF NOT EXISTS char_health (
        id INTEGER PRIMARY KEY,
        typ TEXT NOT NULL, -- the type of health data,
        val INTEGER NOT NULL);"""

query_h = """
    CREATE TABLE IF NOT EXISTS char_skills (
        id INTEGER PRIMARY KEY,
        nm STRING NOT NULL,  -- The skill name
        expt BOOLEAN NOT NULL)
"""

cursor.execute(query_a)
cursor.execute(query_b)
cursor.execute(query_c)
cursor.execute(query_d)
cursor.execute(query_e)
cursor.execute(query_f)
cursor.execute(query_g)
cursor.execute(query_h)

conn.commit()
conn.close()