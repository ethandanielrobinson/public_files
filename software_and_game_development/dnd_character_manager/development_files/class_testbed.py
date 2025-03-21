

import sqlite3
import os
os.chdir(r"D:\dungeons_and_dragons\Custom_Programs\sidekick_files\test_files")

# define a function to add a character to the database
def add_character(name, char_class, char_species, str_a, dex_a, con_a, int_a, wis_a, cha_a):
    conn = sqlite3.connect("test_2.db") # Grab the database
    cursor = conn.cursor() # initialize the cursor
    cursor.execute("""
        INSERT INTO characters (name, class, species, strength, dexterity, constitution, intelligence, wisdom, charisma)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, char_class, char_species, str_a, dex_a, con_a, 
        int_a, wis_a, cha_a))

    conn.commit() # commit the changes
    conn.close()

# Define a function to add equipment to the database
def add_equipment(nm, is_l, is_h):
    conn = sqlite3.connect("test_2.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO equipment (name, is_light, is_heavy) VALUES (?, ?, ?)", 
                   (nm, is_l, is_h))
    conn.commit()
    conn.close()
    print(f"Weapon '{nm}' added.")

# Function to add a spell to the database
def add_spell(name, level, school, casting_time, range, components, duration, is_ritual, description):
    conn = sqlite3.connect("test_2.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO spells (name, level, school, casting_time, range, components, duration, is_ritual, description) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, level, school, casting_time, range, components, duration, is_ritual, description))
    conn.commit()
    conn.close()
    print(f"Spell '{name}' added.")

# Function to add an ability to the database
def add_ability(name, description):
    conn = sqlite3.connect("test_2.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO abilities (name, description) VALUES (?, ?)", 
                   (name, description))
    conn.commit()
    conn.close()
    print(f"Ability '{name}' added.")

# Function to add equipment to a character
def assign_equipment_to_character(character_name, weapon_name):
    conn = sqlite3.connect("test_2.db")
    cursor = conn.cursor()
    
    # Get IDs
    cursor.execute("SELECT id FROM characters WHERE name = ?", (character_name,))
    char_id = cursor.fetchone()
    
    cursor.execute("SELECT id FROM equipment WHERE name = ?", (weapon_name,))
    weapon_id = cursor.fetchone()

    if char_id and weapon_id:
        cursor.execute("INSERT INTO character_weapons (character_id, weapon_id) VALUES (?, ?)", 
                       (char_id[0], weapon_id[0]))
        conn.commit()
        print(f"Weapon '{weapon_name}' assigned to '{character_name}'.")
    else:
        print("Character or weapon not found.")

    conn.close()

def assign_spell_to_character(character_name, spell_name):
    conn = sqlite3.connect("test_2.db")
    cursor = conn.cursor()
    
    # Get IDs
    cursor.execute("SELECT id FROM characters WHERE name = ?", (character_name,))
    char_id = cursor.fetchone()
    
    cursor.execute("SELECT id FROM spells WHERE name = ?", (spell_name,))
    spell_id = cursor.fetchone()

    if char_id and spell_id:
        cursor.execute("INSERT INTO character_spells (character_id, spell_id) VALUES (?, ?)", 
                       (char_id[0], spell_id[0]))
        conn.commit()
        print(f"Spell '{spell_name}' assigned to '{character_name}'.")
    else:
        print("Character or spell not found.")

    conn.close()

def get_character_sheet(character_name):
    conn = sqlite3.connect("test_2.db")
    cursor = conn.cursor()

    # Get Character Info
    cursor.execute("SELECT * FROM characters WHERE name = ?", (character_name,))
    character = cursor.fetchone()

    if not character:
        print("Character not found.")
        return

    char_id, name, char_class, level, species, strength, dex, con, int_, wis, cha = character

    print(f"\n===== {name} | Level {level} {species} {char_class} =====")
    print(f"STR: {strength}  DEX: {dex}  CON: {con}  INT: {int_}  WIS: {wis}  CHA: {cha}\n")

    # Get Weapons
    cursor.execute("""
    SELECT equipment.name, equipment.is_light, equipment.is_heavy
    FROM equipment
    JOIN character_weapons ON equipment.id = character_weapons.weapon_id 
    WHERE character_weapons.character_id = ?
    """, (char_id,))
    weapons = cursor.fetchall()
    
    print("Weapons:")
    for w in weapons:
        print(f"- {w[0]}, Is the weapon light: {w[1]}, Is the weapon heavy: {w[2]})")

    # Get Spells
    cursor.execute("""
    SELECT spells.name, spells.level, spells.school, spells.casting_time, spells.range, spells.components, spells.duration, spells.is_ritual, spells.description
    FROM spells 
    JOIN character_spells ON spells.id = character_spells.spell_id 
    WHERE character_spells.character_id = ?
    """, (char_id,))
    spells = cursor.fetchall()

    print("\nSpells:")
    for s in spells:
        print(f"- {s[0]} (Level {s[1]}, {s[2]}) - {s[3]}, {s[4]}")
        print(f"  {s[5]} - {s[6]} - Ritual: {s[7]}")
        print(f"  {s[8]}\n")

    conn.close()

get_character_sheet("Filia Kosta")
# %%
