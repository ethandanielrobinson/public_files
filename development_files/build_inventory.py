import sqlite3
import os

os.chdir(r"D:\dungeons_and_dragons\Custom_Programs\sidekick_files\databases")

DB_STR = "equipment_master.db"

def get_connection(str_in: str):
    conn_out = sqlite3.connect(str_in)
    conn_out.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign keys are enabled
    return conn_out

conn = get_connection(DB_STR)
cursor = conn.cursor()

equipment_str = """
    CREATE TABLE IF NOT EXISTS equipment_master (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- item name
        cst REAL NOT NULL, -- item cost
        wght REAL NOT NULL, -- item weight
        desc TEXT);"""
cursor.execute(equipment_str)

weapon_str = """
    CREATE TABLE IF NOT EXISTS weapon (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- weapon name
        is_mrtl BOOLEAN NOT NULL, -- is the weapon martial?
        dam_amt INTEGER NOT NULL, -- how many damage dice?
        dam_die INTEGER NOT NULL, -- what type of damage dice?
        dam_typ TEXT NOT NULL, -- what type of damage dealt
        has_fin BOOLEAN, -- does the weapon have finnese?
        i_t_h BOOLEAN, -- does the weapon require two hands?
        has_vers BOOLEAN, -- does the weapon have versatility?
        vers_die INTEGER, -- what is the versatility die?
        has_rng BOOLEAN, -- is the weapon ranged?
        norm_rng INTEGER, -- what is the normal ranged?
        max_rng INTEGER, -- what is the maximum range?
        c_b_thrw BOOLEAN, -- can the weapon be thrown?
        is_l BOOLEAN, -- is the weapon light?
        is_h BOOLEAN, -- is the weapon heavy?
        is_load BOOLEAN, -- does the weapon have loading?
        use_ammo BOOLEAN, -- does the weapon use ammunition?
        is_rch BOOLEAN, -- does the weapon have reach?
        is_spcl BOOLEAN, -- Is the weapon special?
        is_slvd BOOLEAN,  -- is the weapon silvered?
        FOREIGN KEY (id) REFERENCES equipment_master(id) ON DELETE CASCADE);"""
cursor.execute(weapon_str)

armor_str = """
    CREATE TABLE IF NOT EXISTS armor (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- armor name
        ac INTEGER NOT NULL, -- armor class bonus
        ar_type INTEGER NOT NULL, -- what type is the armor?
        stlth BOOLEAN, -- is the armor good for stealth?
        need_str INTEGER NOT NULL, -- what is the required strength score?
        FOREIGN KEY (id) REFERENCES equipment_master(id) ON DELETE CASCADE);"""
cursor.execute(armor_str)

tool_str = """
    CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- tool-set name
        FOREIGN KEY (id) REFERENCES equipment_master(id) ON DELETE CASCADE);"""
cursor.execute(tool_str)

instruments_str = """
    CREATE TABLE IF NOT EXISTS instruments (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- instrument name
        FOREIGN KEY (id) REFERENCES tools(id) ON DELETE CASCADE);"""
cursor.execute(instruments_str)

currency_str = """
    CREATE TABLE IF NOT EXISTS currency (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- coinage name
        cst REAL NOT NULL, -- coinage value
        FOREIGN KEY (id) REFERENCES equipment_master(id) ON DELETE CASCADE);"""
cursor.execute(currency_str)

containers_str = """
    CREATE TABLE IF NOT EXISTS containers (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- container name
        lq_cap REAl, -- container liqid capacity, in ounces
        sd_cap REAL, -- container solid capacity, in cubic feet
        car_cap REAL, -- container carying capcity, in lbs.
        ammo_a INTEGER, -- if the container can be used as a quiver, what type of ammo can it hold?
        amt_a INTEGER, -- and how much of it?
        ammo_b INTEGER, -- can it hold a second type of ammunition?
        amt_b INTEGER, -- and how much of that type?
        FOREIGN KEY (id) REFERENCES equipment_master(id) ON DELETE CASCADE);"""
cursor.execute(containers_str)

ammunition_str = """
    CREATE TABLE IF NOT EXISTS ammunition (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- container name
        FOREIGN KEY (id) REFERENCES equipment_master(id) ON DELETE CASCADE);"""
cursor.execute(ammunition_str)

foodstuff_str = """
    CREATE TABLE IF NOT EXISTS foodstuff(
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- foodstuff name
        day REAL, -- how many days the food last?
        FOREIGN KEY (id) REFERENCES equipment_master(id) ON DELETE CASCADE);"""
cursor.execute(foodstuff_str)

cursor.execute("DROP TABLE clothing")

clothing_str = """
    CREATE TABLE IF NOT EXISTS clothing (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- article of clothing name
        loc INTEGER NOT NULL, -- where on the body the piece of clothing is worn, according to the guide,
        only BOOLEAN NOT NULL, -- Does the article of clothing block other pieces on that body part?
        FOREIGN KEY (id) REFERENCES equipment_master(id) ON DELETE CASCADE);"""
cursor.execute(clothing_str)

liquids_str = """
    CREATE TABLE IF NOT EXISTS liquids (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- the liquids name
        cst REAL NOT NULL);"""
cursor.execute(liquids_str)

conditions_str = """
    CREATE TABLE IF NOT EXISTS conditions (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- The conditions name
        desc TEXT);
"""
cursor.execute(conditions_str)

skills_str = """
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY,
        nm TEXT NOT NULL, -- The skill's name
        usl_atr TEXT NOT NULL, -- The skill's usual atributes
        desc TEXT);
"""
cursor.execute(skills_str)

conn.commit()
conn.close()

