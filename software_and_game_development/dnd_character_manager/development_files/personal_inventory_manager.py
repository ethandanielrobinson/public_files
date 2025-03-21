#%%
import sqlite3
import json
import os
os.chdir(r"D:\dungeons_and_dragons\Custom_Programs\development_files")
import equipment_manager_a as eme

os.chdir(r"D:\dungeons_and_dragons\Custom_Programs\sidekick_files")
with open("drusus_scruatorum.json", "r") as infile:
    char = json.load(infile)

os.chdir(r"D:\dungeons_and_dragons\Custom_Programs\sidekick_files\databases")

# may be useful
def remove_spaces(text: str):
    """
    A simple function to remove the last word in a string

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
        return "_".join(words).lower() # remove spacing and uppercase letters
    return "" # Return empty string if the input string is empty or contains only spaces

# then link the database to that character
char_name = remove_spaces(char["name"])
CH_STR = f"{char_name}_inventory.db"
DB_STR = "equipment_master.db"

# Reconnect to the master database
new_id = eme.retrive_id(DB_STR, "equipment_master", "leather")
new_armor= eme.retrive_armor_by_id(DB_STR, "equipment_master", "armor", new_id)

# Reconnect to the character database
conn = sqlite3.connect(CH_STR)
cursor = conn.cursor()
cursor.execute("""
        INSERT INTO character_equipment (id, nm, wght, qnty)
        VALUES (?, ?, ?, ?)
        """, (new_id, new_armor.name, new_armor.weight, 1,))

print(f"Added {new_armor.name} to character inventory.")

cursor.execute("""
        INSERT INTO character_armor (id, nm, qnty)
        VALUES (?, ?, ?)
        """, (new_id, new_armor.name, 1))

print(f"Added {new_armor.name} to character armors.")

# Commit and close connection
conn.commit()
conn.close()



# %%
