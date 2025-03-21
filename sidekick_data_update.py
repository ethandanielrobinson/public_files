import os
import sqlite3 # Allow us to interact with SQLite files
import json # Allows us to interact with JSON files
import tkinter as tk
import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.6f} seconds.")
        return result
    return wrapper


#==============================================================================
# ACTIVE INVENTORY, WILL EVENTUALY BE PLACED IN A CHARACTER OBJECT
#==============================================================================
#==============================================================================
#### VARIABLE DEFINITIONS
#==============================================================================
use_sh = False # is a shield being used
char: 'fsu.Character' = None # initialize the character object as None for now.
skill_list: list['fsu.Skill'] = [] # initialize skill list as a list of fsu.Skill instances
cond_list: list['fsu.Condition'] = [] # intitialize condition list
char_json: str = None # the character's json file.
CMD_TEXT = """INSERT OR IGNORE INTO character_equipment (id, nm, wght, qnty)
                VALUES (?, ?, ?, ?)"""   # The command text to insert an item
# of equipment, which will be used many times.
EQUIPMENT_TYPES = ["weapon", "armor", "containers", "clothing"]
HEALTH_TXT = "UPDATE char_health SET val = ? WHERE id = ?" # define our command text
#==============================================================================
# Get the directory of the current script
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
# Set it as the working directory
os.chdir(CUR_DIR)
import function_storage_update as fsu

# Now we need to open the sidekick files
sidefiles_path = os.path.join(CUR_DIR, "sidekick_files")
print(sidefiles_path)
os.chdir(sidefiles_path)

# then link the database to that character, defining the global strings
DB_STR = "databases/equipment_master.db"

# THIS IS VERY IMPORTANT
def get_connection(db_path):
    conn_out = sqlite3.connect(db_path)
    cursor = conn_out.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign keys are enabled
    cursor.execute("PRAGMA journal_mode = DELETE;")  # Immediate disk writes

    return conn_out

import sqlite3

def get_quick_connection(db_path):
    """Returns a database connection with optimized settings."""
    conn_out = sqlite3.connect(db_path)
    cursor = conn_out.cursor()  # Always use a cursor for execution

    # Optimize database settings
    cursor.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign keys work
    cursor.execute("PRAGMA journal_mode = DELETE;")  # Immediate disk writes
    cursor.execute("PRAGMA synchronous = OFF;")  # Faster writes
    cursor.execute("PRAGMA temp_store = MEMORY;")  # Keep temp data in RAM

    return conn_out  # Caller must close it manually


# FUNCTION FOR INTIALIZATION
def remove_spaces(text: str):
    """
    A simple function to remove the last word in a string.
    Parameters:
        text (str): The input string to have its last word removed.
    Returns:
        words (str): The string with the last word removed.
    """
    words = text.split()
    if words:  # Check if the list is not empty
        return "_".join(words).lower() # remove spacing and uppercase letters
    return "" # Return empty string if the input string is empty or contains only spaces

#### ERROR FUNCTIONS ##########################################################
def display_type_error(error_str: str)->None:
    """
    A function to both display an error message and raise a TypeError.
    Parameters:
        error_str (str): What we want the error message to say
    Raises:
        TypeError: When an incorrect type of input has be entered in
            the primary function.
    """
    #fsu.error_box(error_str)
    raise TypeError(error_str)

def display_val_error(error_str: str)->None:
    """
    A function to both display an error message and raise a ValueError.
    Parameters:
        error_str (str): What we want the error message to say
    Raises:
        ValueError: When an incorrect type of input has be entered in
            the primary function.
    """
    #fsu.error_box(error_str)
    raise ValueError(error_str)

def display_imp_error(error_str: str)->None:
    """
    A function to both display an error message and raise a NotImplementedError.
    Parameters:
        error_str (str): What we want the error message to say
    Raises:
        NotImplementedError: When an incorrect type of input has be entered in
            the primary function.
    """
    #fsu.error_box(error_str)
    raise NotImplementedError(error_str)

#### DATABASE SEARCH FUNCTIONS=================================================
# Non-User Function
def ret_data(loc: str, active: bool):
    """
    Function to help streamline the database management between both active and passive.
    Stands for retrive database info. Non-User Function.
    Parameters:
        loc (str): The location we are looking for, something like "base" or "weapon"
        active (bool): Whether we ar searching the "active" (The inventory contianed in the
            Character object) or the "passive" (The inventory in the sqlite3 database).
    Returns:
        output: If searching returns the string name of the inventory table
            in the character database.
    """
    # By defining our active dictionary in this function, we ensure that it updates
    # every time the function is called.
    type_dict = {
        "base": {"act" : getattr(char, "main_inv"), "pas" : "character_equipment"},
        "weapon": {"act" : getattr(char, "weapon_inv"), "pas" : "char_weapons"},
        "armor": {"act" : getattr(char, "armor_inv"), "pas" : "char_armor"},
        "container": {"act" : getattr(char, "container_inv"), "pas" : "char_containers"},
        "clothing": {"act" : getattr(char, "clothing_inv"), "pas" : "char_clothing"}} 
    typ = "act" if active else "pas" # do we want the active or passive inventory
    return type_dict[loc][typ] # return the correct inventory
    
def check_database(in_cursor: sqlite3.Cursor, in_table: str, in_id: int)->bool:
    """
    A function to check if that specific id number is in the database. User Function
    Parameters:
        in_cursor (sqlite3.Cursor): a Cursor object that can be searched
        in_table (str): the table we wish to search, given as a key-word.
        in_id (int): A integer representing the desired objects id.
    Raises:
        TypeError: Incorrect input entered.
        NotImplementedError: Function is unable to access database.
    Returns:
        exists (bool): Does the id exist in the database or not?
    """
    # make sure we have the right data type
    if not (isinstance(in_cursor, sqlite3.Cursor) and isinstance(in_table, str) and isinstance(in_id, int)):
        display_type_error("Incorrect input entered, all arguments must be strings!")
    # Query to check if the ID exists, got from ChatGPT
    exists = False # initualize the exists function so we always get a result
    query = f"SELECT 1 FROM {in_table} WHERE id = ?" # define our query
    try:
        in_cursor.execute(query, (in_id,))
        exists = in_cursor.fetchone() is not None
    except sqlite3.Error as e:
        display_imp_error(f"Unable to access database: {e}")
    finally:
        return exists # return what we found

def find_id(in_cursor: sqlite3.Cursor, in_table: str, in_str: str)->int:
    """
    A function that searches a database table and returns an int. User Function
    Parameters:
        in_cursor (sqlite3.Cursor): The cursor connection to the database
        in_table (str): A string describing the table to be searched.
        in_str (str): A string naming the object to be found
    Raises:
        TypeError: Incorrect input entered.
        ValueError: No object with that name is found in the database.
        NotImplementedError: Unable to access database.
    Returns:
        result [0] (int): the matching id integer for the name.  0 means nothing found
    """
    if not (isinstance(in_cursor, sqlite3.Cursor) and isinstance(in_table, str) and isinstance(in_str, str)):
        display_type_error("Incorrect input entered!")
    try:
        in_cursor.execute(f"SELECT id from {in_table} WHERE nm = ?", (in_str,))
        result = in_cursor.fetchone() # get the information
    except sqlite3.Error as e:
        display_imp_error(f"Unable to access database: {e}")
    finally: # ensure that we return something
        if result:
            return result[0] # return the first thing found
        else:
            display_val_error(f"No entry found for {in_str} in {in_table}.")

def retrieve_id_list(database_name: str, table_name: str, )->list:
    """
    A function that returns a list of all id numbers in an database table.  Does not
    use a pre-defined cursor. User Function.
    Parameters:
        database_name (str): The name of the database we wish to search, ether a character db or DB_STR
        table_name (str): The name of the table we want to retrieve.
    Raises:
        TypeError: Wrong form of input.
        NotImplementedError: Unable to access database.
    Returns:
        out_list (list): A list of integers representing the id numbers of all rows in the database
        table.
    """
    # make sure we have good input wtih TypeErrors
    if not (database_name in [DB_STR, char.db]): # only certain strings are allowed, check the database master
        display_type_error("The database name must be defined.")
    if not isinstance(table_name, str):
        display_type_error("The table name must be in the form of a string.")
    # Reconnect to the character database
    conn = get_connection(database_name)
    cursor = conn.cursor()
    # Fetch all ids from the character_weapons table
    out_list = []  # Initialize out_list before the try block
    try:
        cursor.execute(f"SELECT id FROM {table_name};")
        out_list = [row[0] for row in cursor.fetchall()]  # Store names in an array of integers
    except sqlite3.Error as e:
        display_imp_error(f"Unable to access database: {e}")
    finally:
        conn.close() # Close the connection, which we want to ensure is correct
    return out_list # return the list generated

# Non-User Function
def get_equipment_type(in_cursor: sqlite3.Cursor, in_id: int):
    """
    A function that searches the database to return an equipment's type (weapon, armor, and so on).
    0 is base equipment, 1 is weapons, 2 is armor, 3 is containers, 4 is clothing.  
    Non-User type function
    Parameters:
        in_cursor (sqlite3.Cursor): The cursor object we are using to search the database
        in_id (int): The database id number of the item we wish to identify
    Returns:
        eq_type (int): An integer representing the type of equipment input.
    """
    # initialize the table as None, meaing base equipment, since if non of the sub-inventories
    # activeate, this will be what's returned
    eq_type = 0 
    
    for index, table in enumerate(EQUIPMENT_TYPES): # Equipment types is defined above
        if check_database(in_cursor, table, in_id): # check the various sub tables in the master database
            eq_type = index + 1 # and return the index (0 is base, 1 is weapons, 2 is armor, 3 is containers, and so on)
            # We need to add 1 to the index because we want 0 to be the base case
    return eq_type

def clear_table(del_curs: sqlite3.Cursor, table_name: str):
    """
    Removes all rows from the given SQLite3 table without dropping the table.
    Parameters:
        del_curs (sqlite3.Cursor): The cursor we are currently connected to.
        table_name (str): The name of the table in the database we want to clear.
    Raises:
        TypeError: Incorrect argument types.
        NotImplementedError: Unable to access the database.    
    """
    if not (isinstance(del_curs, sqlite3.Cursor) and isinstance(table_name, str)):
        display_type_error("del_curs must be a Cursor object.  table_name must be a string.")
    try:
        # Delete all rows from the table
        del_curs.execute(f"DELETE FROM {table_name};")
    except sqlite3.Error as e:
        display_type_error(f"Error clearing table: {e}")

#### CHARACTERS SEARCH FUNCTION================================================
def search_inventory(in_list: list, item_id: int):
    """
    A function to search an characters inventory, provided as a list of tuples, 
    usualy one of the inventories defined in the charachter instance, and not in the SQLite3 database.
    Parameters:
        in_list (list): The inventory we want to search.
        item_id (int): The id of the Equipment instance we want to find.
    Raises:
        TypeError: Wrong type of arguments.
    Returns:
        OUT (tuple): Is the Equipment in the inventory, the index of the Equipment (-1 if it's not there)
    """
    if not isinstance(item_id, int): # make sure the input is good
        display_type_error("Incorrect input entered!")
    for index, (object, _) in enumerate(in_list): # we need the actual Equipment instance, not the quantity
        if not isinstance(object, fsu.Equipment): # make sure the list is good.
            display_type_error("Incorrect input entered!")
        if object.id == item_id: # check if the object is an equipment instance in the inventory
            return True, index # if it is there, return true and the index
        return False, -1 # if it is not there, return false and -1

#########################################################################################
#### JSON FUNCTIONS #####################################################################
#########################################################################################
def update_JSON():
    """
    A function to update the character JSON file.
    """
    # first we define out outgoing dictionary based on the char object.
    outchar = {
        "name" : char.name,
        "image" : char.image,
        "db" : char.db,
        "color": char.color,
        "conditions" : char.conditions,
        "lang" : char.lang,
        "exhaustion" : char.exhaustion,
        "pb" : char.pb}
    # Write the updated character back to the JSON file
    with open(char_json, "w") as outfile: # Change this later
        json.dump(outchar, outfile, indent=1) # single indent, will re-write the entire file
        outfile.flush()
        outfile.close()  # Ensures the OS commits changes immediately
#########################################################################################
#### DATABASE FUNCTIONS #################################################################
#########################################################################################
# Notes on implamentation: Six functions are defined here. The print_result function is
# for development purposes--it simply lets the developer know if the database has been
# updated.  Two functions are responsible for adding new equipment to the character's
# inventory database. add_to_db directly adds an Equipment instance direclty to specified
# table.  add_eq_char_db manages this function: It makes sure that if the input Equipment
# is a Weapon Subclass for instance, both the character_equipment and char_weapons tables
# are updated, but not the char_armor table.  Since both of these functions take
# an Equipment Instance as an argument (which we will need to be defined to place in
# the active inventory contained in the Character or Container instance anyway), it's
# easy to detrimne which inventory tables should be updated just by using the isinstance
# function.  
# 
# The quantity update functions are different, howerever.  Since the Equipment
# instance is already defined in the active inventory, we don't need to define a new one
# and the function works on id nubmer alone.  For the update_qty_db this isn't as much of
# a problem, since it only updates one table at a time.  For the up_qty_char_db function
# however, which needs to know which tables to insert new data into, we use the fact that
# the changes to the active inventory should have allready been made (add_to_db also uses
# this to recreate the database if the upload fails) to dertermine which equipment
# subclass the object is in.
#
# As for the del_from_db function, we don't need a management function.  All sub-inventory
# tables are defined with ON DELETE CASCADE, pointing back to the "character_equipment"
# table.  If an item is deleted there, it should be deleted everywhere else.
#=========================================================================================
# Non-User Function, to help with printing
def print_result(in_int: int, in_str: str):
        """
        A Function to display a message depending on the numberical input:
        Parameters:
            in_int (int): The integer key we wish to display a message for.
            in_str (str): The database key we are updating.
        """
        print("Function print_result ran.")
        if in_int == 0:
            print(f"{in_str} database updated")
        elif in_int == 2:
            print(f"{in_str} database reset")
        else:
            print(f"{in_str} database error")

# Non-User Function
def add_to_db(up_curs: sqlite3.Cursor, location: str, up_obj: fsu.Equipment, up_quan: int)->int:
    """
    A Function that commits new equipment to the database, depending on its type.  Non-User Function.
    Do not use this function to initialize containers.
    Parameters:
        up_curs (sqlite.Cursor): A Cursor that forms our connection to the database.
        location (str): A string determining where in the database the equipment is to be placed. "base", "weapon", "armor" and so on, along with the contianer sub-inventories.
        up_obj (fsu.Equipment): An Equipment instance (or child) that we want to place in the database.
        up_quan (int): The quantity of that Equipment we wish to add.
    Raises:
        NotImplementedError: Unable to update database.
    Returns:
        output (int): 0 means success, 1 means container, 2 means recreated database
    """
    # The command text to insert an item.  We select the right table based on the key word
    # and ensure that we are accessing the index = 1 database title.
    cmd_str = f"INSERT INTO {ret_data(location, False)} (id, nm, qnty) VALUES (?, ?, ?)"
    try: # try to insert our information into our database
        up_curs.execute(cmd_str, (up_obj.id, up_obj.name, up_quan))
    except sqlite3.IntegrityError: # if we are unable to do that
        # if we are unable to do that, we will want to update the entire table.
        clear_table(up_curs, ret_data(location, False))
        # and grab a new one from the active database.
        for object, quantity in ret_data(location, True): # we call the active inventory defined in the character instance
            # which was probably just changed
            rep_str = f"INSERT INTO {ret_data(location, False)} (id, nm, qnty) VALUES (?, ?, ?)"
            up_curs.execute(rep_str, (object.id, object.name, quantity))
        return 2 # and return 2
    except sqlite3.Error as e: # and if an unspecified exception occurs
        display_imp_error(f"SQLite error: {e}")
    return 0 # This line is only evaluated if everything goes smoothly

# Non-User Function
def update_qty_db(up_curs: sqlite3.Cursor, location: str, item_id: int, up_quant: int)->int:
    """
    A function to update the quantity of an object in the database after it has been changed in the
    active inventory.  Non-User Function.
    Parameters:
        up_curs (sqlite.Cursor): A Cursor that forms our connection to the database.
        location (str): A string determining where in the database the equipment is to be placed. "base", "weapon", "armor" and so on, along with the contianer sub-inventories.
        up_obj (fsu.Equipment): An Equipment instance (or child) that we want to place in the database.
        up_quant (int): The quantity of that Equipment we wish to update.
    Raises:
        ValueError: No row found with the specified id.
        NotImplementedError: Unable to update database.
    Returns:
        output (int): 0 means success, 1 means failure
    """
    cmd_str = f"UPDATE {ret_data(location, False)} SET qnty = ? WHERE id = ?"
    try: # Attempt to insert the information
        up_curs.execute(cmd_str, (up_quant, item_id))
        if up_curs.rowcount == 0:
            display_val_error(f"No record found with id {item_id}, update failed.")
    except sqlite3.Error as e: # and if an exception occurs
            display_imp_error(f"SQLite error: {e}")
    return 0 # This line is only evaluated if everything goes smoothly

# Non-User Function
def del_from_db(up_curs: sqlite3.Cursor, del_id: int, inventory_str: str= "primary")->int:
    """
    A function to delete a item wholesale from the database. Non-User function.  Don't use this to
    try to delete intitialized containers.
    Parameters:
        up_curs (sqlite.Cursor): A Cursor that forms our connection to the database.
        del_id (int): The id number of the item to be deleted.
        inventory_str (str, optional): A string determining where in the database the equipment 
            is to be deleted. The default is "primary"
    Raises:
        ValueError: No row found with the specified id.
        NotImplementedError: Unable to update database.
    Returns:
        output (int): 0 means success, 1 means failure
    """
    # Ensure that if we are accessing the primary inventory our location is "base"
    location = "base" if inventory_str == "primary" else inventory_str
    # Create our command string.
    cmd_str = f"DELETE FROM {ret_data(location, False)} WHERE id = ?"
    try: # Attempt to delete the line
        up_curs.execute(cmd_str, (del_id,))
        if up_curs.rowcount == 0: # if no rows are deleted, it is assumed that
            # the update failed.
            display_val_error(f"No record found with id {del_id}, update failed.")
            return 1 # return failur key
    except sqlite3.Error as e: # and if an exception occurs
        display_imp_error(f"SQLite error: {e}")
    return 0 # This line is only evaluated if everything goes smoothly
 
# Non-User Function
def add_eq_char_db(in_curs: sqlite3.Cursor, in_o: fsu.Equipment, in_q: int, inventory_str: str = "primary")->None:
    """
    A Function to manage the add_to_db function, by ensuring that the correct information
    is inserted into the correct database tables. Non-User function.
    Parameters:
        in_curs (sqlite.Cursor): A Cursor that forms our connection to the database.
        in_o (fsu.Equipment): An Equipment instance (or child) that we want add to the character.
        in_q (int): The quantity of that Equipment we wish to add to the character.
        inventory_st (str): A string describing if we are placing the script in the primary inventory,
            or a container.
    """
    # First, for all equipment, we need to insert it into the character
    # If we are inserting the information into the character's primary inventory, which
    # means we need to keep apraised of things like the useable weapons inventory (after
    # all, you can't use a sword in your backpack, but you can use one on your belt).
    if inventory_str == "primary":
        # Place the information in the Primary Equipment Inventory
        loc = "base"
        res = add_to_db(in_curs, loc, in_o, in_q)
        print_result(res, loc) # and plase our two results in the printing function.
        # Next we need to check if equipment is in a weapon subclasss.  locs is location, subclass
        for locs, scls in [("weapon", fsu.Weapon), ("armor", fsu.Armor), ("clothing", fsu.Clothing)]:
            if isinstance(in_o, scls):
                ress = add_to_db(in_curs, locs, in_o, in_q) # stands for results, subclass
                print_result(ress, locs)
                break # end the for loop if the object subclass is found
    else:
        print("Fix This Later")

# Non-User Function
def up_qty_char_db(in_curs: sqlite3.Cursor, in_id: int, in_q: int, inventory_str: str = "primary")->None:
    """
    A Function to manage the update_qty_db function, ensuring that changes are propigated to the
    proper subclass inventories.  Requires that the active inventory has been updated first.
    Parameters:
        in_curs (sqlite.Cursor): A Cursor that forms our connection to the database.
        in_id (int): The id of the Equipment instance (or child) that we want add to the character.
        in_q (int): The quantity of that Equipment we wish to add to the character.
        inventory_st (str): A string describing if we are placing the script in the primary inventory,
            or a container.
    """
    if inventory_str == "primary":
        loc = "base" # define the base location to alter the primary location inventory
        res = update_qty_db(in_curs, loc, in_id, in_q) # update the quantity
        print_result(res, loc) # and print the result
        # We then check the subclass inventories defined in the charachter instance
        # We use the fact that the character instance should have been updated already.
        for locs in ["weapon", "armor", "clothing"]:
            lst = ret_data(locs, True) # retrive the information from the active database
            if search_inventory(lst, in_id)[0]: # we search each inventory respectably for the id
                ress = update_qty_db(in_curs, locs, in_id, in_q) # if we find the id in an inventory, we update
                print(ress, locs) # print the results
                break # and end the for loop
    else:
        print("Fix This Later")

    
# we dont need a del_eq_char_db function, since the ON DELETE CASCADE that I defined in
# in the definitions for the subclass inventories requires the tables to delete their inventory
# if the primary table is modified.

# Non-User Function
def add_skill_char_db(in_curs: sqlite3.Cursor, sk_id: int, sk_nm: str, sk_expt: bool):
    """
    A Function to save skill data to a character's data file.  Non-User Function.
    Parameters:
        in_curs (sqlite3.Cursor): The cursor we are using to search the database
        sk_id (int): The id of the skill we want to add.
        sk_nm (str): The name of the skill we want to add (for ease of use).
        sk_expt (bool): Is the skill on the expertise list.
    Raises:
        NotImplementedError: When the function is unable to implement the changes.
    """
    cmd_str = f"INSERT INTO char_skills (id, nm, expt) VALUES (?, ?, ?)"
    try:
        in_curs.execute(cmd_str, (sk_id, sk_nm, sk_expt,)) # place our three data points
    except sqlite3.Error as e: # and if an unspecified exception occurs
        display_imp_error(f"SQLite error: {e}")

#########################################################################################
####################### OLD FUNCTIONS ####################################################
#########################################################################################

# NON USER FUNCTION
def create_new_cont_table(in_cursor: sqlite3.Cursor, table_name: str)->None:
    """
    A function that creates a table in the database to store container inventory
    Parameters:
        in_cursor (sqlite3.Cursor): The current cursor connection to the database.
        table_name (str): The name of the table we want to create
    """
    cmd_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,  -- The same as the master id
            nm TEXT NOT NULL, -- the objects name
            wght REAL NOT NULL, -- the objects weight
            qnty INTEGER);"""
    in_cursor.execute(cmd_query)
    return None
    
##########################################################################
###### RETRIVAL FUNCTION #################################################
##########################################################################
# Non-User Function
def get_equipment_attr(in_cursor: sqlite3.Cursor, eq_id: int)->tuple:
    """
    A function to return the four atributes that every pieces of equipment has based on it's id:
    name, cost, weight, and description.  This function, which requires an allready existing cursor
    searches the database for the four values associated with the input id eq_id, and returns them
    as a tupple.  Non-User type function
    Parameters:
        in_cursor (sqlite.Cursor): A Cursor object than can be used to search a database.
        eq_in (int): the id of the piece of equipment we are searching for.
    Raises:
        ValueError: When an id that does not exist in the database is entered.
    Returns:
        row_out (tuple): a tupple containg the four atributes (name, cost, weight, description)
    """
    # retrive the equipment from the database
    q_t = "SELECT nm, cst, wght, desc FROM equipment_master WHERE id = ?" # Querry, temporary
    in_cursor.execute(q_t, (eq_id,)) # execute the existing cursor
    row_out = in_cursor.fetchone() # find the row
    if row_out is None: # make sure the equipment is there in row equipment
        es = f"No equipment found with id {eq_id}." # Error String
        fsu.error_box(es)
        raise ValueError(es)
    return row_out # and we return the 4 values as a tupple.

# Non-User Function
def retrieve_equipment_by_id(in_cur: sqlite3.Cursor, in_id: int):
    """
    A general purpose retrieval function that can work with all objects (it actually self identifies them).
    Replaced the prior equipment type specific retrival functions.  Returns either an Equipment object, 
    or one of its children. Non-User Function.
    Parameters:
        in_cur (sqlite3.Cursor): The Cursor object we are using to search the database.
        in_id (int): The equipment_master id of the item we wish to create an instancd for.
    Returns:
        OUT (fsu.Equipment): The item instituted as a Equipment (or child) instance.
    """
    row_e = get_equipment_attr(in_cur, in_id)  # This will also throw out an error if the equipment isn't in the database
    # If the Equipment is a weapon, this will grab the weapon data. If the equipment is not
    # a weapon, this will do nothing.
    in_cur.execute("""
        SELECT is_mrtl, dam_amt, dam_die, dam_typ, has_fin, i_t_h, has_vers, vers_die, 
                has_rng, norm_rng, max_rng, c_b_thrw, is_l, is_h, is_load, 
                use_ammo, is_rch, is_spcl, is_slvd 
        FROM weapon 
        WHERE id = ?
    """, (in_id,))
    row_we = in_cur.fetchone() # extract the weapon data in a single line
    if row_we:  # if we actualy get weapon data, its a weapon, and we can output
        return fsu.Weapon(*row_e, in_id, *row_we)
    # If the Equipment is a armor, same type
    in_cur.execute("SELECT ac, ar_type, stlth, need_str FROM armor WHERE id = ?", (in_id,))
    row_ar = in_cur.fetchone() # extract the armor specific data
    if row_ar:
        # Define the output, using row_ar to represent the armor specific data
        return fsu.Armor(*row_e, in_id, *row_ar)
    # If the Equipment is a container --------------------------------------------------------
    in_cur.execute("""
        SELECT lq_cap, sd_cap, car_cap, ammo_a, amt_a, ammo_b, amt_b 
        FROM containers 
        WHERE id = ?
    """, (in_id,))
    row_con = in_cur.fetchone() # extract the container specific data
    if row_con:
        return fsu.Container(*row_e, in_id, *row_con)
    return fsu.Equipment(*row_e, in_id) #if none of the specific types trigger, this will trigger.

# Non-User Function
def retrive_single_equip(one_id: int):
    """
    A function to retrive a single Equipment instance that does not require a initial
    Cursor object to be defined. Non-User Function
    Parameters:
        one_id (int): The id of the Equipment we are looking for.
    Returns:
        output (fsu.Equipment): The equipment (or child) object we are looking for.
    """
    conn = get_connection(DB_STR)
    one_curs = conn.cursor()
    output = retrieve_equipment_by_id(one_curs, one_id)
    conn.close() # Close the connection
    return output

# Non-User Function
def ret_skills_list(in_c: sqlite3.Cursor):
    """
    A function to retrive the raw skill information from the master database. 
    Non-User Function
    Parameters:
        in_c (sqlite3.Cursor): A cursor we can use to search the database.
    Raises:
        NotImplementedError: When the function is unable to implement the changes.
    Returns:
        out_list: A list of skill data in the form of (id, name, usual attribute, description).
    """
    try:
        in_c.execute("SELECT id, nm, usl_atr, desc FROM skills") # grab the relavant information
        out_list = [(row[0], row[1], row[2], row[3]) for row in in_c.fetchall()]
    except sqlite3.Error as e: # and if an unspecified exception occurs
        display_imp_error(f"SQLite error: {e}")
    return out_list # return our functions

# Non-User Function
def ret_cond_list(in_c: sqlite3.Cursor):
    """
    A function to retrive the raw skill information from the master database.
    Non-User Function
    Parameters:
        in_c (sqlite3.Cursor): A cursor we can use to search the database.
    Raises:
        NotImplementedError: When the function is unable to implement the changes.
    Returns:
        out_list: A list of skill data in the form of (id, name, description).
    """
    try:
        in_c.execute("SELECT id, nm, desc FROM conditions") # grab the condition info
        out_list = [(row[0], row[1], row[2]) for row in in_c.fetchall()]
    except sqlite3.Error as e: # and if an unspecified exception occurs
        display_imp_error(f"SQLite error: {e}")
    return out_list  
###############################################################################
### CHARACTER MODIFICATION FUNCTIONS ##########################################
###############################################################################
def add_equipment(in_obj: fsu.Equipment, in_qnty: int, loc: str = "primary")->None:
    """
    The master function for adding equipment.  Ensures that the equipment is added to the charachter
    instance, and that any changes are updated to the database.
    Parameters:
        in_obj (fsu.Equipment): An instance of the Equipment object we want to add to the inventory.
        in_qnty (int): How many of the specified Equipment do we want to add to the inventory.
        loc (str, optional): The inventory (either primary or a container inventory) we wish to add
            the Equipment to.
    Raises:
        TypeError: When the wrong argument types are entered.
    """
    # we first bring in the char variable as a global, to ensure we can modify the
    # character object
    global char

    # Ensure that our input is of the correct type
    if not (isinstance(in_obj, fsu.Equipment) and isinstance(in_qnty, int) and isinstance(loc, str)):
        display_type_error("Incorred input.  Please check the docstring again.")

    conn = get_connection(char.db) # Define our cursor
    curs_up = conn.cursor()

    # first we need to add the equipment to the character object.
    if char.add_to_inventory(in_obj, in_qnty): # our database update depends on the outcome
        # we only need the objects id here if the object allready exists
        up_qty_char_db(curs_up, in_obj.id, in_qnty, inventory_str=loc) 
    else:
        # We need to insert a whole new Equipment instance
        add_eq_char_db(curs_up, in_obj, in_qnty, inventory_str=loc) # ensure that we connecting to the right inventory
    
    conn.commit() # Commit and close our database.
    conn.close()

def delete_equipment(del_id: int, del_qnty: int, loc: str = "primary"):
    """
    The master function for deleting equipment.  Ensures that the equipment is deleted from the charachter
    instance, and that any changes are updated to the database.
    Parameters:
        del_id (int): The id number of the Equipment instance we wish to delete.
        in_qnty (int): How many of the specified Equipment do we want to remove from the inventory.
        loc (str, optional): The inventory (either primary or a container inventory) we wish to delete
            the Equipment from.
    Raises:
        TypeError: When the wrong argument types are entered.
    """
    global char

    # Ensure that our input is of the correct type
    if not (isinstance(del_id, int) and isinstance(del_qnty, int) and isinstance(loc, str)):
        display_type_error("Incorred input.  Please check the docstring again.")

    conn = get_connection(char.db) # Get our connection
    curs_up = conn.cursor() # define our cursor

    if char.remove_from_inventory(del_id, del_qnty):
        # if we allready have an instance of that equipment in the inventory
        up_qty_char_db(curs_up, del_id, -del_qnty, inventory_str=loc) # del_qnty must be negative here.
    else: # the item line needs to be removed wholesale
        del_from_db(curs_up, del_id, inventory_str=loc)
    
    conn.commit() # Commit and close our database.
    conn.close()

def add_cond(manual:bool = False, input: tuple = (None, None)):
    """
    A function to update the charactar object and JSON with a condition.
    Parameters:
        manual (bool, optional): Do we want to enter the information manualy or using the dialoge
            box. The default is False.
        inpt_a (tuple, optional): The condition we want to input, in the form of an (int, str) tuple,
            where the int is the condition database id, and the string is the condition name. The default is 
            (None, None)
    Raises:
        ValueError: When a manual entry is specified without a tuple.
    """
    # ensure user compatabilty
    if manual and not input: # Both must exist
        display_val_error("Input must be provided for a manual addition.")
    # first we add the condition to the char object.
    if manual:
        suc = char.add_cond_man(input)
    else:
        suc = char.add_condition(cond_list) # try to add the condition to the char object.
    if suc:
        update_JSON() # if we successufly modified the char object, we then update the JSON
        print(f"{char.name}'s condition list updated.")

def remove_cond(manual: bool = False, input: int = None):
    """
    A function to remove a condtion from the character object and JSON.
    Parameters:
        manual (bool, optional): Do we want to enter the information manualy or using the dialoge
            box. The default is False.
        inpt_a (int, optional): The condition we want to remove, in the form of the database ind integer.
            The default is None.
    Raises:
        ValueError: When a manual entry is specified without a tuple.
    """
    # ensure user compatabilty
    if manual and not input: # Both must exist
        display_val_error("Input must be provided for a manual addition.")
    if manual: #remove the condtion manualy
        suc = char.remove_cond_man(input)
    else: # remove the condition using the dialogue box.
        suc = char.remove_condition(cond_list)
    if suc:
        update_JSON() # if successful in removing a condition, update the JSON
        print(f"{char.name}'s condition list updated.")

# Non-User Function
@timing_decorator # Temporary
def add_skill_prof(inpt_a: int, expert: bool = False)->bool:
    """
    A function to help modify the character's skill list.
    Parameters:
        inpt_a (int): The id of the skill we want to add.
        expert (bool, optional): do we want to add expertise in this skill?  The default is False
    """
    global char # define the global character instance
    if expert: # if we want to add to the expertise list
        # add the skill to the expertise list if it's not allready there
        if inpt_a not in char.skills_exp: 
            char.skills_exp.append(inpt_a)
        # and if the skill is in the prof list, we remove it from there.
        if inpt_a in char.skills_prof:
            char.skills_prof.remove(inpt_a) # we want to remove that specific value.
    else: # if we don't want to add to the expertise list.
        if inpt_a not in char.skills_prof: # make sure we dont add the same skill twice
            char.skills_prof.append(inpt_a)
            print(f"{inpt_a} added to {char.name}'s skill inventory.")
    # Finaly we need to add the skill to the char_skills table in the db
    conn = get_connection(char.db)
    cur = conn.cursor()
    for skill in skill_list: # search the skill list
        if skill.id == inpt_a:
            add_skill_char_db(cur, inpt_a, skill.name, expert)
            print(f"{skill.name} {inpt_a} proficiency added to {char.name}'s inventory.")
    conn.commit()
    conn.close()
    

###############################################################################
### CHARACTER INITIALZATION FUNCTIONS #########################################
###############################################################################
def retrive_inventory_info(ch_cur: sqlite3.Cursor):
    """
    A Function to retrive initialization data (id and quantity) from a character's
    database file.
    Parameters:
        ch_cur (sqlite3.Cursor): A cursor we can use to search a database.
    Raises:
        NotImplementedError: When the function is unable to implement.
    Returns:
        out_list (list): an id-inventory list, composed of tuples in the form of 
            (item id, item quantity) which can the be used, in combination with
            the master database, to fill a character's active inventory.
    """
    # we need a function to retrive the id and qnty information from the character
    # inventory (the name is just for programer convenience)
    # Fetch all ids from the character_weapons table
    out_list = []  # Initialize out_list before the try block
    try:
        ch_cur.execute("SELECT id, qnty FROM character_equipment;") # explicetly state the inventory to search
        out_list = [(row[0], row[1]) for row in ch_cur.fetchall()]  # Store names data in an array of tuples
    except sqlite3.Error as e:
        display_imp_error(f"Unable to access database: {e}")
    return out_list # return the list generated

def retrive_atr_info(ch_cur: sqlite3.Cursor):
    """
    Function to initialize the characters atributes.
    Parameters:
        ch_cur (sqlite3.Cursor): A Cursor we can use to search a database.
    Raises:
        NotImplementedError: When the function is unable to implement.
    Returns: 
        out_list (list): a list of the six atribute values.
    """
    out_list = [] # define the outlist
    try:
        ch_cur.execute("SELECT val FROM char_att;") # explicetly state the inventory to search
        out_list = [row[0] for row in ch_cur.fetchall()] # pass the information into the list
    except sqlite3.Error as e:
        display_imp_error(f"Unable to access database: {e}")
    return out_list

# Non-User Function
def retrive_health_info(ch_cur: sqlite3.Cursor):
    """
    Function to intialize the character's health information.
    Parameters:
        ch_cur (sqlite3.Cursor): A Cursor we can use to search the database.
    Raises:
        NotImplementedError: When the function is unable to implement.
    Returns:
        out_list (list): A list of the three health values.
    """
    out_list = [] # initialize
    try:
        ch_cur.execute("SELECT val FROM char_health;") # explicitly search the database.
        out_list = [row[0] for row in ch_cur.fetchall()] # pass the information to the list
    except sqlite3.Error as e:
        display_imp_error(f"Unable to access database: {e}")
    return out_list

def retrive_skill_info(ch_cur: sqlite3.Cursor):
    """
    Function to retrive the characters skill information
    Parameters:
        ch_cur (sqlite3.Cursor): A Cursor we can use to search the database.
    Raises:
        NotImplementedError: When the function is unable to implement.
    Returns:
        out_list (list): A list of the character's skill proficiencies, by id,
            in two parts [[prof_list], [exp_list]]
    """
    out_list: list[list[int]] = [[], []]  # Initialize a list containing two lists: prof_list and exp_list
    for num, boo in [(0, False), (1, True)]: # False means proficient, True means expert
        ch_cur.execute("SELECT id FROM char_skills where expt = ?", (boo,))
        out_list[num] = [row[0] for row in ch_cur.fetchall()] # pass the inventory to the first part of the list.
    return out_list

# Non-User Function
def create_char_object(file_loc: str):
    """
    A function to set the global character instance, which will be used in the rest
    of the script. Non-User Function.
    Parameters:
        file_loc (str): The location of the character's JSON file.
    """
    global char # ensure that we can set the global
    # We do this in three stages.  Stage one--Retrive information from the characters 
    # JSON file
    with open(file_loc, "r") as infile:
        cd = json.load(infile)  # read in the JSON dictionary as cd (character dictionary)
    char = fsu.Character(**cd) # save the data in a character instance

    # Second, we retrive the information we need from the characters sqlite3 database
    conn = get_connection(char.db) # the character database
    cursor = conn.cursor()
    char.set_atributes(retrive_atr_info(cursor)) # first we set the character atributes
    char.set_health(retrive_health_info(cursor)) # then the health info
    char.set_skills(retrive_skill_info(cursor)) # and the skill information
    inv_list = retrive_inventory_info(cursor) # Then retrive our inventory list
    conn.close() # and close the connection to the character database

    #finally, we retrive class information from the master databasse
    conn = get_connection(DB_STR)
    cursor = conn.cursor()
    for item_id, q in inv_list: # item_id is id_number, q is quantity
        insert = retrieve_equipment_by_id(cursor, item_id)
        # We don't add this immediately to the char inventory since we need to close
        # the connection to the master database first.
        char.add_to_inventory(insert, q) # add directly to the inventory, don't need to save here
    conn.close()
    #### TEST AREA
    print("Function create_char_object called.")
    return char

# Non-User Function
def initialize_skills():
    """
    A function to initialize the 18 skill instances we need to make skill checks.  Non-User Function.
    """
    global skill_list

    # Start our cursor
    conn = get_connection(DB_STR)
    int_c = conn.cursor()
    # and retrive our info
    internal = ret_skills_list(int_c)
    for sk_id, sk_nm, sk_ua, sk_d in internal:
        temp = fsu.Skill(sk_id, sk_nm, sk_ua, sk_d)
        skill_list.append(temp) # and add the skill object to the skill list
    conn.close() # close the connection

def initialize_conditions():
    """
    A function to intialize the condition list.
    """
    global cond_list
    # Start our cursor
    conn = get_connection(DB_STR)
    int_c = conn.cursor()
    internal = ret_cond_list(int_c)
    for con_id, con_nm, con_d in internal:
        temp = fsu.Condition(con_id, con_nm, con_d)
        cond_list.append(temp)
    conn.close()

@timing_decorator # Temporary
def initialize_all(infile: str):
    """
    A function to combine the initialization functions
    Parameters:
        infile (str): The location of the character JSON
    """
    global char_json
    char_json = infile
    create_char_object(infile)
    initialize_skills()
    initialize_conditions()

def retrive_char():
    """
    A Function to update a the character in the graphical_sidekick.py GUI.
    Returns:
        char (fsu.Character): The currently defined global character object.
    """
    return char

def update_char():
    """
    A function to quickly return health information.  Non-User Function
    Returns:
        out (Tuple[int, int, int, List[Tuple[int, str]]]): The character's health information, 
            in the form of current health, max health, and temporary health points, followed
            by the condition list.
    """
    output = [char.cur_hp, char.max_hp, char.temp_hp, char.conditions]
    return output

def skill_names():
    """
    A function to return a list of all skills
    Returns:
        OUT (list[str]): A list contianing the names in the form of strings. 
    """
    return [skill.name for skill in skill_list]

###############################################################################
#### GAMEPLAY FUNCTIONS #######################################################
###############################################################################
def damage(dam: int):
    """
    A function that re-calculates health points after damage
    and writes the new number to the character's database.
    Parameters"
        dam (int): The damage amount.
    Raises:
        TypeError: When a variable other than an integer is passed as an argument.
    """
    # ensure correct info type
    if not isinstance(dam, int):
        display_type_error("Argument must be an integer.")
    
    # first we deal with temp_hp
    if char.temp_hp > dam:
        char.temp_hp -= dam # we simply subtract the damage
    elif char.temp_hp <= dam:
        dam -= char.temp_hp # we reduce damage by the temp_hp and set temp_hp to zero
        char.temp_hp = 0
        char.cur_hp -= dam # reduce the current hp by the remaining damage
        if char.cur_hp <= 0: # check that we haven't fallen unconsious
            char.cur_hp = 0
            add_cond(manual=True, input_a = (14, "unconscious")) # won't add it if allready unconsious.
            print('yer dead partner!') # TEMPORARY, TRADITION

    # Now we write to the SQLite3 character Database
    conn = get_quick_connection(char.db)
    cursor = conn.cursor()
    cursor.executemany(HEALTH_TXT, [(char.cur_hp, 2), (char.temp_hp, 3)])
    conn.commit()
    conn.close() # and close our database.
    #### TEST LINE
    print("Health Database Updated.")

def temp_heal(gain: int):
    """
    A function that adds temporary health points and writes
    the new number to the character's JSON file.
    Parameters:
        gain (int): The temporary hit points gained.
    Raises:
        TypeError: When a variable other than an integer is passed as an argument.
    """
    # Ensure correct argument types
    if not isinstance(gain, int):
        display_type_error("Argument must be an integer.")
    
    # add the gain
    char.temp_hp += gain # add the gain to the temp hp
    print(f"{char.name} has recived {gain} temp HP")

    # Now we write to the SQLite3 character Database
    conn = get_quick_connection(char.db)
    cursor = conn.cursor()
    cursor.execute(HEALTH_TXT, (char.temp_hp, 3))
    conn.commit()
    conn.close() # and close our database.
    #### TEST LINE
    print("Health Database Updated.")

def heal(gain: int):
    """
    A function that re-calculates health points after healing
    and writes the new number to the character's database.
    Parameters:
        gain (int): The hit points gained.
    Raises:
        TypeError: When a variable other than an integer is passed as an argument.
    """
    # Ensure correct argument types
    if not isinstance(gain, int):
        display_type_error("Argument must be an integer.")
    
    # Add the gain
    char.cur_hp += gain

    #make sure we don't go overboard
    if char.cur_hp > char.max_hp:
        char.cur_hp = char.max_hp

    # Now we write to the SQLite3 character Database
    conn = get_quick_connection(char.db)
    cursor = conn.cursor()
    cursor.execute(HEALTH_TXT, (char.cur_hp, 2))
    conn.commit()
    conn.close() # and close our database.
    #### TEST LINE
    print("Health Database Updated.")

###############################################################################
#### OBJECT SPECIFIC FUNCTIONS (for function_storage_tkinter)
###############################################################################
# Attack function
def attack(input_one: int):
    """
    Function for calling for managing the various attack functions.
    Ensures that the correct function is called from the function_storage_sidekick
    directory and that the correct attributes are input.
    Parameters:
        input_one (int): the equipment id number of the weapon being used.
    """
    if not isinstance(input_one, int): # input check
        raise TypeError("Input is of the incorrect input type.")
    # Make sure we actualy have that weapon.
    weapon_list = [weap.id for weap, _ in char.weapon_inv] # grab all the id's
    if input_one not in weapon_list:
        raise ValueError(f"Weapon ID is not in {char.name}'s inventory.")
    
    # def attack(self, free_hands: int, prof_in: int, str_score: int, dex_score:int = 10)
    for inst, _ in char.weapon_inv:
        if inst.id == input_one:
            inst.attack(2, 
                        char.pb, 
                        char.stre, 
                        dex_score = char.dext)

def return_weapon_name(in_id: int):
    """
    A function, that, when given a weapon id returns the weapons name. Non-User Function.
    Parameters:
        in_id (int): The weapon's id number
    Returns
        OUT (str): The weapon's name.
    """
    w_dict = {weapon.id: weapon.name for weapon in char.weapon_inv}  # Create a dictionary for faster lookup
    return w_dict.get(in_id)

def find_skill_mod(skill_in: fsu.Skill)->int:
    """
    A function to find the modifier for a designated skill.  Non-User function.
    Parameters:
        skill_in (fsu.Skill): The Skill object we are using.
    Returns:
        OUT (int): That skills modifier
    """
    # first we need to find the profficiency
    if skill_in.id in char.skills_prof:
        mult = 1
    elif skill_in.id in char.skills_exp:
        mult = 2
    else:
        mult = 0
    # Then we define the bonus
    atr_bonus = (getattr(char, skill_in.usual_atr) - 10) // 2
    return char.pb * mult + atr_bonus


def return_skill_name(in_id: int):
    """
    A function, that, when given a skill id returns the skill name. Non-User Function.
    Parameters:
        in_id (int): The skill's id number
    Returns:
        OUT (Tuple[str, int]): The skills's name and mod in a tuple.
    """
    skill_dict = {skill.id: skill for skill in skill_list}  # Create a dictionary for faster lookup
    temp_sk = skill_dict.get(in_id)
    return temp_sk.name, find_skill_mod(temp_sk)

def find_armor(armor_name: str, shield_in: bool):
    """
    A function that takes in the characters current armor, dextirity modifer,
    and whether they are using a shield, and returns the armor class.
    Parameters:
        armor_name (str): The name of the current armor the character is wearing.  "no_armor" means the
            character is not wearing armor.
        shield_in (bool): Whether the character is wielding a sheild at all.
    Raises:
        TypeError: Incorrect input.
        ValueError: Armor type not found in inventory
    Returns:
        armor_cl (int): The int describing the characters current armor class.
    """
    # Input check
    if not (isinstance(armor_name, str) and isinstance(shield_in, bool)):
        display_type_error("Arguments must be of correct type.")
    # bring in the global shield bool
    global use_sh
    
    # Initilize armor class
    armor_cl = 10 #base armor

    # if we get no armor, we just use 10 + the dexterity bonus.
    if armor_name == "no armor":
        armor_cl = 10 + ((char.dext - 10)//2)
    # if we don't recive the no armor input, we search the armor inventory.
    else:
        # First we need to find the armor information, which we find using a dict.
        ar_dict = {armor.name: armor for armor,_ in char.armor_inv}  # Create a dictionary for faster lookup
        armor = ar_dict[armor_name] # get the armor information
        if armor:
            armor_cl = armor.get_ac(char.dext)
        else:
            display_val_error(f"Armor not found in {char.name}'s inventory.")

    # Check for a shield
    if shield_in:
        # set the global sheild variable to be true
        use_sh = True
        armor_cl = armor_cl + 2
    else:
        # Define the sheild value as false.
        use_sh = False
    # And return the Armor Class
    return armor_cl

def skill_roll(id_in: int, normal: bool = False):
    """
    A function to call for a skill roll.
    Parameters:
        id_in (int): The database id number of the skill we want to use.
        normal (bool): Are we using the normal skill ability
    Raises:
        TypeError: Non-Integer passed as an argument.
    """
    # Ensure correct argument types
    if not isinstance(id_in, int):
        display_type_error("Argument must be an integer.")
    
    skill_dict = {skill.id: skill for skill in skill_list}  # Create a dictionary for faster lookup
    skill = skill_dict.get(id_in)  # Retrieve the skill object by id
    if skill:
        skill.normalskill(find_skill_mod(skill)) # find the modifier and roll the skill.
    else:
        display_val_error(f"Skill with id {id_in} not found.")
###############################################################################
#### TESTING AREA #############################################################
###############################################################################
