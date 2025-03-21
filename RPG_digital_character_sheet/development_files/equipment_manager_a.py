import sqlite3
import os
import csv
os.chdir(r"D:\dungeons_and_dragons\Custom_Programs\sidekick_files\databases")

# TO DO =======================================================================
#==============================================================================

#==============================================================================
# GLOBAL VARIABLES
DB_STR = "equipment_master.db"
#==============================================================================

#==============================================================================
# FUNCTION DEFINITIONS
#==============================================================================
# Next a function to retrieve an item from the database and store it in an equipment
# object.
# Database connection function with foreign keys enabled
def get_connection(db_path):
    conn_out = sqlite3.connect(db_path)
    conn_out.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign keys are enabled
    return conn_out

def check_database(cursor_in: sqlite3.Cursor, table_name: str, item_name: str):
    """
    Returns if an object is in a list

    Parameters
    ----------
    cursor_in: sqlite.Cursor
        The cursor object storing the database we want to search.
    table_name: str
        The name of the table we want to search.
    item_name: str
        The item we are looking for.
    
    Raises
    ------
    ValueError
        If the input is not the correct type.
    
    Returns
    -------
    bool
        Is the object in the table or not.
    
    """
    # Ensure good input--------------------------------------
    if not isinstance(cursor_in, sqlite3.Cursor):
        raise ValueError("Must input a valid cursor object!")
    if not isinstance(table_name, str):
        raise ValueError("Table name must be a valid string!")
    if not isinstance(item_name, str):
        raise ValueError("Item name must be a valid string!")
    
    # Check to see if the item is in the database
    query = f"SELECT 1 FROM {table_name} WHERE nm = ? LIMIT 1"
    cursor_in.execute(query, (item_name,))
    return cursor_in.fetchone() is not None

def retrive_equipment(in_text: str):
    """
    A function to retrieve equipment from the master equipment database.
    
    Parameters
    ----------
    in_text : str
        The name of the equipment to retrieve.
    
    Returns
    -------
    output: Equipment
        The equipment object.

    """
    # make sure the input is good
    if not isinstance(in_text, str):
        raise ValueError("The input must be a string.")
    
    # Create a connection to the database
    conn = get_connection(DB_STR)
    cursor = conn.cursor()

    # Retrieve the equipment from the database
    cursor.execute("SELECT id, cst, wght, desc FROM equipment_master WHERE nm = ?", (in_text,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise ValueError(f"No equipment found with name {in_text}.")
    
    # select out output, which is row[0] is the id, row[1] is the cost, row[2] 
    # is the weight, and row[3] is the description.
    id_out = int(row[0])
    cost_out = float(row[1])
    weight_out = float(row[2])
    desc_out = row[3]

    output = In_equipment(in_text, cost_out, weight_out, desc_out, id_out)

    print(f"Aquired {in_text} from master inventory, with cost {cost_out} and weight {weight_out}.")
    return output

def retrive_weapon(in_text: str):
    """
    Retrieve weapon information from the database based on the provided weapon name.
    Args:
        in_text (str): The name of the weapon to retrieve.
    Returns:
        In_weapon: An instance of the In_weapon class containing the weapon's details.
    Raises:
        ValueError: If the input is not a string or if no equipment is found with the given name.
    """
    # make sure the input is good
    if not isinstance(in_text, str):
        raise ValueError("The input must be a string.")
    
    # Create a connection to the database
    conn = get_connection(DB_STR)
    cursor = conn.cursor()

    # Retrieve the equipment from the database, first from equipment_master
    cursor.execute("SELECT id, cst, wght, desc FROM equipment_master WHERE nm = ?", (in_text,))
    eq_row = cursor.fetchone() # extract the data
    if eq_row is None: # make sure thre is some equipment there
        raise ValueError(f"No equipment found with name {in_text}.")
    id_o = eq_row[0]
    cost_o = eq_row[1] # Get the cost
    weight_o = eq_row[2] # Get the weight
    desc_o = eq_row[3] # Get the description

    # Then retreive the equipment from the weapon table
    cursor.execute("""
        SELECT is_mrtl, dam_die, dam_typ, has_fin, i_t_h, has_vers, vers_die, 
               has_rng, norm_rng, max_rng, c_b_thrw, is_l, is_h, is_load, 
               use_ammo, is_rch, is_spcl, is_slvd 
        FROM weapon 
        WHERE id = ?
    """, (id_o,))
    we_row = cursor.fetchone() # extract the weapon data
    if we_row is None: # make sure the line isn't empty
        raise ValueError(f"No equipment found with name {in_text}")
    mar_o = we_row[0] # Is the weapon martial?
    dam_die_o = we_row[1] # How many faces on the damage die?
    dam_typ_o = we_row[2] # What type of damage?
    has_fin_o = we_row[3] # Does the weapon have the finnesse property
    two_hand_o = we_row[4] # Does the weapon need two hands
    has_vers_o = we_row[5] # Does the weapon have the versatile property
    vers_die_o = we_row[6] # If the weapon has the versatile property, what is the die
    has_rng_o = we_row[7] # Is the weapon ranged?
    norm_o = we_row[8]# what is the normal range of a ranged weapon
    max_o = we_row[9] # what is the maximum range of a ranged weapon
    throw_o = we_row[10] # Can the weapon be thrown?
    light_o = we_row[11] # is the weapon light?
    heavy_o = we_row[12] # is the weapon heavy?
    load_o = we_row[13] # Does the weapon have the loading property
    ammo_o = we_row[14] # Does the weapon require amunition?
    reach_o = we_row[15] # Does the weapon have reach?
    special_o = we_row[16] # Does the weapon have special properties?
    silvered_o = we_row[17] # Is the weapon silvered

    # And load or data into a In_weapon class
    output = In_weapon(in_text, 
                       cost_o, 
                       weight_o, 
                       desc_o, 
                       dam_die_o, 
                       dam_typ_o,
                       is_martial=mar_o,
                       has_finesse=has_fin_o,
                       is_two_handed=two_hand_o,
                       has_verstile=has_vers_o,
                       damage_die_versatile=vers_die_o,
                       has_range=has_rng_o,
                       normal_range=norm_o,
                       max_range=max_o,
                       has_thrown=throw_o,
                       is_light=light_o,
                       is_heavy=heavy_o,
                       is_loading=load_o,
                       uses_ammunition=ammo_o,
                       has_reach=reach_o,
                       is_special=special_o,
                       is_silvered=silvered_o)
    
    return output

def retrive_armor(in_text: str):
    """
    Retrieve armor information from the database based on the provided armor name.

    Args:
        in_text (str): The name of the armor to retrieve.
    Returns:
        In_armor: An instance of the In_armor class containing the armor's details.
    Raises:
        ValueError: If the input is not a string or if no equipment is found with the given name.
    """
    # make sure the input is good
    if not isinstance(in_text, str):
        raise ValueError("The input must be a string.")
    
    # Create a connection to the database
    conn = get_connection(DB_STR)
    cursor = conn.cursor()

    # Retrieve the equipment from the database, first from equipment_master
    cursor.execute("SELECT id, cst, wght, desc FROM equipment_master WHERE nm = ?", (in_text,))
    eq_row = cursor.fetchone() # extract the data
    if eq_row is None: # make sure thre is some equipment there
        raise ValueError(f"No equipment found with name {in_text}.")
    id_o = eq_row[0]
    cost_o = eq_row[1] # Get the cost
    weight_o = eq_row[2] # Get the weight
    desc_o = eq_row[3] # Get the description

    # Then retreive the equipment from the weapon table
    cursor.execute("""
        SELECT ac, ar_type, stlth, need_str
        FROM armor
        WHERE id = ?
    """, (id_o,))
    ar_row = cursor.fetchone() # extract the weapon data
    a_class, a_type, stealth, needed_str = ar_row

    output = In_armor(in_text, cost_o, weight_o, desc_o, a_class, a_type, 
                      stealth_good=stealth, str_required=needed_str)
    return output

def modify_table(database_in: str, table_in: str, column_in: str, id: int, new_value):
    """
    Modifies a specific column value for a given item in the specified table.

    Parameters
    ----------
    database_in: str
        The name of the database to update.
    table_in : str
        The name of the table to update.
    column_in : str
        The column to be updated.
    id : int
        The id of the item to be updated.
    new_value : any
        The new value to set for the specified column.

    Returns
    -------
    None
    """
    conn = get_connection(database_in)
    cursor = conn.cursor()

    query = f"""
        UPDATE {table_in}
        SET {column_in} = ?
        WHERE id = ?
    """
    cursor.execute(query, (new_value, id))
    conn.commit()
    conn.close()
    print(f"Updated {id} in {table_in}, set {column_in} to {new_value}.")

def get_next_id(cursor, table_name: str, id_column: str = "id"):
    """
    Retrieves the next available ID for the specified SQLite table.
    Function developed with help from chatGPT.

    Parameters:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        table_name (str): The name of the table.
        id_column (str, optional): The name of the ID column (default is "id").

    Returns:
        int: The next available ID (highest existing ID + 1), or 1 if the table is empty.
    """
    cursor.execute(f"SELECT MAX({id_column}) FROM {table_name}")
    result = cursor.fetchone()
    
    return (result[0] + 1) if result and result[0] is not None else 1  # Start at 1 if table is empty


#==============================================================================
# CLASS DEFINITIONS
#==============================================================================
# now we are going to uses classes, defining the weapon class as a the child of the equipment class.
class In_equipment:
    def __init__(self, name: str, cost: float, weight: float, description: str, id: int = None):
        """
        Initializes the equipment class

        Parameters
        ----------
        name : str
            The name of the equipment.
        cost : float
            The cost of the equipment.
        weight : float
            The weight of the equipment.
        description : str
            A description of the equipment.
        id : int, optional
            The unique identifier for the equipment (default is None).
            
        Raises
        ------
        ValueError
            If the input is not the correct type.   
        
        Returns
        -------
        None.
        """
        # We ensure that we get the correct type of data
        if not isinstance(name, str):
            raise ValueError("The name must be a string.")
        if not isinstance(cost, float):
            raise ValueError("The cost must be a float.")
        if not isinstance(weight, float):
            raise ValueError("The weight must be a float.")
        if not isinstance(description, str):
            raise ValueError("The description must be a string.")
        
        # and then define our class variables bassed on the input given
        self.name = name
        self.cost = cost
        self.weight = weight
        self.description = description
        self.id = id # initial id definition

        # we find an available id if the id space is blank
        if self.id is None:
            conn = get_connection(DB_STR) # open the database
            cursor_check = conn.cursor() # asign a cursor
            self.id = get_next_id(cursor_check, "equipment_master") # get an acceptable id
            conn.close()

        return None

    def add_equipment_to_master (self):
        """
        A function to add equipment to the character's inventory in the database.

        Returns
        -------
        None.

        """
        
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # Insert the equipment into the database
        cursor.execute("""
        INSERT INTO equipment_master (id, nm, cst, wght, desc)
        VALUES (?, ?, ?, ?, ?)
        """, (self.id, self.name, self.cost, self.weight, self.description))
        conn.commit()
        conn.close()
        print(f"Added {self.name} to master inventory.")

    def delete_equipment_from_master(self):
        """
        A function to delete equipment from the master equipment database.

        Returns
        -------
        None.

        """
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # Delete the equipment from the database
        cursor.execute("DELETE FROM equipment_master WHERE nm = ?", (self.name,))
        conn.commit()
        conn.close()
        print(f"Deleted {self.name} from master inventory.")

class In_weapon(In_equipment):
    def __init__(self,
                 name: str, # the name of the weapon as a string
                 cost: float, # the cost of the weapon in gold pieces
                 weight: float, # the weight of the weapon in pounds
                 description: str, # a string describing the weapon
                 damage_die: int, # the number of sides on the damage die
                 damage_type: str, # the type of damage the weapon deals
                 is_martial: bool = False, # whether the weapon is a martial weapon
                 has_finesse: bool = False, # whether the weapon has the finesse property
                 is_two_handed: bool = False, # whether the weapon is two-handed
                 has_verstile: bool = False, # whether the weapon is versatile
                 damage_die_versatile: int = 0, # the number of sides on the versatile damage die
                 has_range: bool = False, # whether the weapon has a range
                 normal_range: int = 0, # the normal range of the weapon
                 max_range: int = 0, # the maximum range of the weapon
                 has_thrown: bool = False, # whether the weapon can be thrown efficiently
                 is_light: bool = False, # whether the weapon is light
                 is_heavy: bool = False, # whether the weapon is heavy
                 is_loading: bool = False, # whether the weapon has the loading property
                 uses_ammunition: bool = False, # whether the weapon uses ammunition
                 has_reach: bool = False, # whether the weapon has the reach property
                 is_special: bool = False, # whether the weapon is a special weapon
                 is_silvered: bool = False # whether the weapon is silvered
                 ):
        
        """
        Initializes a weapon class object
        """
        # Call the parent constructor using super()
        super().__init__(name, cost, weight, description)
        self.damage_die = damage_die 
        self.damage_type = damage_type
        self.is_martial = is_martial
        self.has_finesse = has_finesse
        self.is_two_handed = is_two_handed
        self.has_verstile = has_verstile
        self.damage_die_versatile = damage_die_versatile
        self.has_range = has_range
        self.normal_range = normal_range
        self.max_range = max_range
        self.has_thrown = has_thrown
        self.is_light = is_light
        self.is_heavy = is_heavy
        self.is_loading = is_loading
        self.uses_ammunition = uses_ammunition
        self.has_reach = has_reach
        self.is_special = is_special
        self.is_silvered = is_silvered

        # We then make sure to Enforce dependency: on versatilty
        if self.has_verstile and self.damage_die_versatile == 0:
            raise ValueError("A versatile weapon must have a versatile damage die!")
        
        # And on ranged weapons
        if (self.has_range or self.has_thrown) and (self.normal_range == 0 or self.max_range == 0):
            raise ValueError("A ranged weapon must have both a maximum and normal range!")

        # Ensure that the weapon cannot be both heavy and light
        if self.is_heavy and self.is_light:
            raise ValueError("A weapon cannot be both heavy and light!")
        
        return None

    def add_weapon_to_database(self):
        """
        Adds a weapon to the database.
        This method first checks if the weapon is already present in the master 
        database. If the weapon is not present, it adds the weapon to the master 
        database. Then, it inserts the weapon into the weapons database with all 
        its attributes.
        Attributes:
            self (object): The weapon object containing all the necessary attributes 
                           to be added to the database.
        Database Tables:
            equipment_master: The master table containing all equipment details.
        Returns:
            None
        """
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # First we check if the weapon is in the master database and add if it isn't
        # We add it
        in_database = check_database(cursor, "equipment_master", self.name)
        if not in_database:
            self.add_equipment_to_master()
        else:
            conn.close() # close the database
            return None #end the function
        
        # then we add the weapon to the weapons database
        # Insert the equipment into the database
        cursor.execute("""
        INSERT INTO weapon (
            id, is_mrtl, dam_die, dam_typ, has_fin, i_t_h, has_vers, vers_die, 
            has_rng, norm_rng, max_rng, c_b_thrw, is_l, is_h, is_load, use_ammo, 
            is_rch, is_spcl, is_slvd
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """, (
            self.id, self.is_martial, self.damage_die, self.damage_type, 
            self.has_finesse, self.is_two_handed, self.has_verstile, 
            self.damage_die_versatile, self.has_range, self.normal_range, 
            self.max_range, self.has_thrown, self.is_light, self.is_heavy, 
            self.is_loading, self.uses_ammunition, self.has_reach, self.is_special, 
            self.is_silvered
        ))
        conn.commit()
        conn.close()
        print(f"Added {self.name} to weapons inventory.")

        return None

    def delete_weapon_from_inventory(self):
        """
        Deletes a weapon from the inventory database.
        This method connects to the SQLite database specified by `DB_STR`, 
        deletes the weapon with the name stored in `self.name` from the 
        `equipment_master` table, commits the transaction, and closes the 
        connection. It also prints a confirmation message indicating the 
        deletion of the weapon.
        Returns:
            None
        """

        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # first we need to get the id from equipment_master list
        # Retrieve the equipment from the database
        cursor.execute("SELECT id FROM equipment_master WHERE nm = ?", (self.name,))
        id_delete = cursor.fetchone()

        # make sure that the weapon is in the list.
        if id_delete is None:
            raise ValueError(f"No equipment found with name {self.name}.")

        # Delete the weapon from the weapons table
        cursor.execute("DELETE FROM weapon WHERE id = ?", (id_delete[0],))
        conn.commit()

        # Delete the equipment from the equipment_master table
        cursor.execute("DELETE FROM equipment_master WHERE id = ?", (id_delete[0],))
        conn.commit()
        conn.close()
        print(f"Deleted {self.name} from master inventory.")

        return None
    
    def get_damage_die(self):
        return self.damage_die
    
    def get_damage_type(self):
        return self.damage_type
    
    def get_martial(self):
        return self.is_martial

    def get_versitile(self):
        outdie = 0 # initialize the outdie
        if self.has_verstile:
            outdie = self.damage_die_versatile # set the outdie to the value if true
        
        return self.has_verstile, outdie

class In_armor(In_equipment):
    def __init__(self,
                 name: str, # the name of the weapon as a string
                 cost: float, # the cost of the weapon in gold pieces
                 weight: float, # the weight of the weapon in pounds
                 description: str, # a string describing the weapon
                 armor_class: int, # an int describing the armor class bonus
                 armor_type: int, # an int describing the armor type 1-Light Armor 2-Medium Armor, and 3-Heavy Armor
                 stealth_good: bool = True, # a bool describing if the armor is an effective at stealth
                 str_required: int = 0): # the minimum STR score needed to wear this armor
        """
        Initialize a new piece of equipment.
            Args:
                name (str): The name of the weapon.
                cost (float): The cost of the weapon in gold pieces.
                weight (float): The weight of the weapon in pounds.
                description (str): A description of the weapon.
                armor_class (int): The armor class bonus provided by the armor.
                armor_type (int): The type of armor (1 for Light Armor, 2 for Medium Armor, 3 for Heavy Armor).
                stealth_good (bool, optional): Indicates if the armor is effective for stealth. Defaults to True.
                str_required (int, optional): The minimum STR score needed to wear this armor. Defaluts to 0.
        """
        # Call the parent constructor using super()
        super().__init__(name, cost, weight, description)
        self.armor_class = armor_class
        self.armor_type = armor_type
        self.stealth_good = stealth_good
        self.str_required = str_required
    
    def add_armor(self):
        """
        Adds a armor to the database.
        This method first checks if the armor is already present in the master 
        database. If the armor is not present, it adds the armor to the master 
        database. Then, it inserts the armor into the armor database with all 
        its attributes.
        Attributes:
            self (object): The weapon armor containing all the necessary attributes 
                           to be added to the database.
        Database Tables:
            equipment_master: The master table containing all equipment details.
            armor: the armor table
        Returns:
            None
        """
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # First we check if the armor is in the master database and add if it isn't
        # We add it
        in_database = check_database(cursor, "equipment_master", self.name)
        if not in_database:
            self.add_equipment_to_master()
        else:
            temp_equip = retrive_equipment(self.name) # Load the equipment in a temporary equipment object
            self.id = temp_equip.get_id() # get the updated id
        
        # then we add the weapon to the weapons database
        # Insert the equipment into the database
        cursor.execute("""
        INSERT INTO armor (id, nm, ac, ar_type, stlth, need_str)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (self.id, self.name, self.armor_class, self.armor_type, 
              self.stealth_good, self.str_required))
        conn.commit() # commit the database
        conn.close() # close the database
        print(f"Added {self.name} to armor inventory.") # print confermation
        return None
    
    def delete_armor(self):
        """
        Deletes an armor entry from the database.
        This method deletes an armor entry from both the `armor` table and the 
        `equipment_master` table in the database. It first retrieves the ID of the 
        armor entry from the `equipment_master` table using the armor's name. If 
        the armor entry is found, it deletes the entry from both tables. If the 
        armor entry is not found, it raises a ValueError.
        Raises:
            ValueError: If no equipment is found with the specified name.
        Returns:
            None
        """
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # first we need to get the id from equipment_master list
        # Retrieve the equipment from the database
        cursor.execute("SELECT id FROM equipment_master WHERE nm = ?", (self.name,))
        id_delete = cursor.fetchone()

        # make sure that the weapon is in the list.
        if id_delete is None:
            raise ValueError(f"No equipment found with name {self.name}.")

        # Delete the weapon from the weapons table
        cursor.execute("DELETE FROM armor WHERE id = ?", (id_delete[0],))
        conn.commit()

        # Delete the equipment from the equipment_master table
        cursor.execute("DELETE FROM equipment_master WHERE id = ?", (id_delete[0],))
        conn.commit()
        conn.close()
        print(f"Deleted {self.name} from master inventory.")

        return None

class In_tool(In_equipment):
    def __init__(self, name: str, cost: float, weight: float, description: str):
        super().__init__(name, cost, weight, description) # we only need this line

    def add_tool_to_database(self):
        """
        Adds a tool to the database.
        This method first checks if the tool is already present in the master 
        database. If the tool is not present, it adds the tool to the master 
        database. Then, it inserts the tool into the tool database with all 
        its attributes.
        Attributes:
            self (object): The tool object containing all the necessary attributes 
                           to be added to the database.
        Database Tables:
            equipment_master: The master table containing all equipment details.
            tools: the tool table
        Returns:
            None
        """
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # First we check if the tool is in the master database and add if it isn't
        # We add it
        in_database = check_database(cursor, "equipment_master", self.name)
        if not in_database:
            self.add_equipment_to_master()
        else:
            temp_equip = retrive_equipment(self.name) # Load the equipment in a temporary equipment object
            self.id = temp_equip.get_id() # get the updated id

        # then we add the weapon to the weapons database
        # Insert the equipment into the database
        cursor.execute("""
        INSERT INTO tools (id, nm)
        VALUES (?, ?)
        """, (self.id, self.name))
        conn.commit() # commit the database
        conn.close() # close the database
        print(f"Added {self.name} to tools inventory.") # print confermation
        return None
    
    def delete_tool_from_database(self):
        """
        Deletes an tool entry from the database.
        This method deletes an tool entry from both the `tool` table and the 
        `equipment_master` table in the database. It first retrieves the ID of the 
        tool entry from the `equipment_master` table using the tool's name. If 
        the tool entry is found, it deletes the entry from both tables. If the 
        tool entry is not found, it raises a ValueError.
        Raises:
            ValueError: If no equipment is found with the specified name.
        Returns:
            None
        """
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # first we need to get the id from equipment_master list
        # Retrieve the equipment from the database
        cursor.execute("SELECT id FROM equipment_master WHERE nm = ?", (self.name,))
        id_delete = cursor.fetchone()

        # make sure that the weapon is in the list.
        if id_delete is None:
            raise ValueError(f"No equipment found with name {self.name}.")

        # Delete the tool from tools table
        cursor.execute("DELETE FROM tools WHERE id = ?", (id_delete[0],))
        conn.commit()

        # Delete the equipment from the equipment_master table
        cursor.execute("DELETE FROM equipment_master WHERE id = ?", (id_delete[0],))
        conn.commit()
        conn.close()
        print(f"Deleted {self.name} from both tools and master inventories.")

        return None
    
class In_instrument(In_tool):
    def __init__(self, name: str, cost: float, weight: float, description: str):
        super().__init__(name, cost, weight, description) # we only need this line

    def add_instrument(self):
        super().add_tool_to_database()
        # then we add the weapon to the instrument database
        # Insert the equipment into the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO instruments (id, nm)
        VALUES (?, ?)
        """, (self.id, self.name))
        conn.commit() # commit the database
        conn.close() # close the database
        print(f"Added {self.name} to instrument inventory.") # print confermation
        return None
    
    def delete_instrument(self):
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # first we need to get the id from equipment_master list
        # Retrieve the equipment from the database
        cursor.execute("SELECT id FROM equipment_master WHERE nm = ?", (self.name,))
        id_delete = cursor.fetchone()

        # make sure that the weapon is in the list.
        if id_delete is None:
            raise ValueError(f"No equipment found with name {self.name}.")

        # Delete the tool from instruments table-> it will casede to the other two
        cursor.execute("DELETE FROM instruments WHERE id = ?", (id_delete[0],))
        cursor.execute("DELETE FROM tools WHERE id = ?", (id_delete[0],))
        cursor.execute("DELETE FROM equipment_master WHERE id = ?", (id_delete[0],))
        conn.commit()
        conn.close()
        print(f"Deleted {self.name} from all inventories.")

        return None

class In_coin(In_equipment):
    def __init__(self, name: str, cost: float, weight: float, description: str):
        super().__init__(name, cost, weight, description) # we only need this line

    def add_coin(self):
        """
        Adds a coin type to the database.
        This method first checks if the coin is already present in the master 
        database. If the coin is not present, it adds the coin to the master 
        database. Then, it inserts the coin into the tool database with all 
        its attributes.
        Attributes:
            self (object): The coin object containing all the necessary attributes 
                           to be added to the database.
        Database Tables:
            equipment_master: The master table containing all equipment details.
            currency: the coin table
        Returns:
            None
        """
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # First we check if the tool is in the master database and add if it isn't
        # We add it
        in_database = check_database(cursor, "equipment_master", self.name)
        if not in_database:
            self.add_equipment_to_master()
        else:
            temp_equip = retrive_equipment(self.name) # Load the equipment in a temporary equipment object
            self.id = temp_equip.get_id() # get the updated id

        # then we add the weapon to the weapons database
        # Insert the equipment into the database
        cursor.execute("""
        INSERT INTO currency (id, nm, cst)
        VALUES (?, ?, ?)
        """, (self.id, self.name, self.cost))
        conn.commit() # commit the database
        conn.close() # close the database
        print(f"Added {self.name} to currency inventory.") # print confermation
        return None

class In_container(In_equipment):
    def __init__(self, name: str, 
                 cost: float, 
                 weight: float, 
                 description: str,
                 file: str = None, # the location of the contents database
                 lq_cap: float = None, # the containers liquid capacity, in ounces
                 sd_cap: float = None, # the containers solic capacity, in cubic feet
                 car_cap: float = None, # the containers carying capacity, in pounds
                 ammo_a: str = None, # can the container be used as a quiver?
                 amt_a: int = None, # and how much can it hold?
                 ammo_b: str = None,# can it be used for more than one type of ammo?
                 amt_b: int = None): # how much of that can it hold?
        """
        Initializes a object of the In_container type
        """
        super().__init__(name, cost, weight, description)
        self.file = file
        self.lq_cap = lq_cap
        self.sd_cap = sd_cap
        self.car_cap = car_cap
        self.ammo_a = ammo_a
        self.amt_a = amt_a
        self.ammo_b = ammo_b
        self.amt_b = amt_b

    def add_container(self):
        """
        Adds a container type to the database.
        This method first checks if the container is already present in the master 
        database. If the container is not present, it adds the container to the master 
        database. Then, it inserts the container into the containers database with all 
        its attributes.
        Attributes:
            self (object): The container object containing all the necessary attributes 
                           to be added to the database.
        Database Tables:
            equipment_master: The master table containing all equipment details.
            containers: the container table
        Returns:
            None
        """
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # First we check if the tool is in the master database and add if it isn't
        # We add it
        in_database = check_database(cursor, "equipment_master", self.name)
        if not in_database:
            self.add_equipment_to_master()
        else:
            temp_equip = retrive_equipment(self.name) # Load the equipment in a temporary equipment object
            self.id = temp_equip.get_id() # get the updated id

        # then we add the weapon to the weapons database
        # Insert the equipment into the database
        cursor.execute("""
        INSERT INTO containers (id, nm, file, lq_cap, sd_cap, car_cap, ammo_a, amt_a, ammo_b, amt_b)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.id, self.name, self.file, self.lq_cap, self.sd_cap, self.car_cap,
              self.ammo_a, self.amt_a, self.ammo_b, self.amt_b))
        conn.commit() # commit the database
        conn.close() # close the database
        print(f"Added {self.name} to containers inventory.") # print confermation
        return None

    
class In_amunition(In_equipment):
    def __init__(self, name: str, cost: float, weight: float, description: str):
        """
        Initializes a object of the In_ammunition type
        """
        super().__init__(name, cost, weight, description)

    def add_ammo(self):
        """
        Adds a amunition type to the database.
        This method first checks if the amunition is already present in the master 
        database. If the amunition is not present, it adds the amunition to the master 
        database. Then, it inserts the amunition into the ammunition database with all 
        its attributes.
        Attributes:
            self (object): The amunition object containing all the necessary attributes 
                           to be added to the database.
        Database Tables:
            equipment_master: The master table containing all equipment details.
            amunition: the amunition table
        Returns:
            None
        """
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # First we check if the tool is in the master database and add if it isn't
        # We add it
        in_database = check_database(cursor, "equipment_master", self.name)
        if not in_database:
            self.add_equipment_to_master()
        else:
            temp_equip = retrive_equipment(self.name) # Load the equipment in a temporary equipment object
            self.id = temp_equip.id # get the updated id

        # then we add the weapon to the amunition database
        # Insert the equipment into the database
        cursor.execute("""
        INSERT INTO ammunition (id, nm)
        VALUES (?, ?)
        """, (self.id, self.name))
        conn.commit() # commit the database
        conn.close() # close the database
        print(f"Added {self.name} to ammunition inventory.") # print confermation
        return None
        
class in_food(In_equipment):
    def __init__(self, name: str, cost: float, weight: float, description: str, day_good: float):
        """
        Initializes a object of the In_ammunition type
        """
        super().__init__(name, cost, weight, description)
        self.day_good = day_good

    def add_food(self):
        """
        Adds a food type to the database.
        This method first checks if the food is already present in the master 
        database. If the food is not present, it adds the food to the master 
        database. Then, it inserts the food into the foodstuff database with all 
        its attributes.
        Attributes:
            self (object): The food object containing all the necessary attributes 
                           to be added to the database.
        Database Tables:
            equipment_master: The master table containing all equipment details.
            foodstuff: the food table
        Returns:
            None
        """
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # First we check if the tool is in the master database and add if it isn't
        # We add it
        in_database = check_database(cursor, "equipment_master", self.name)
        if not in_database:
            self.add_equipment_to_master()
        else:
            temp_equip = retrive_equipment(self.name) # Load the equipment in a temporary equipment object
            self.id = temp_equip.id # get the updated id

        # then we our food to the food database
        # Insert the equipment into the database
        cursor.execute("""
        INSERT INTO foodstuff (id, nm, day)
        VALUES (?, ?, ?)
        """, (self.id, self.name, self.day_good))
        conn.commit() # commit the database
        conn.close() # close the database
        print(f"Added {self.name} to foodstuff inventory.") # print confermation
        return None

class In_article(In_equipment):
    def __init__(self, name: str, cost: float, weight: float, description: str, type: int, blocks_other: bool):
        """
        Initializes a object of the In_article type
        """
        super().__init__(name, cost, weight, description)
        self.type = type
        self.blocks_other = blocks_other

    def add_clothing(self):
        """
        Adds a article type to the database.
        This method first checks if the article is already present in the master 
        database. If the article is not present, it adds the article to the master 
        database. Then, it inserts the article into the clothing database with all 
        its attributes.
        Attributes:
            self (object): The article object containing all the necessary attributes 
                           to be added to the database.
        Database Tables:
            equipment_master: The master table containing all equipment details.
            clothing: the article table
        Returns:
            None
        """
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # First we check if the tool is in the master database and add if it isn't
        # We add it
        in_database = check_database(cursor, "equipment_master", self.name)
        if not in_database:
            self.add_equipment_to_master()
        else:
            temp_equip = retrive_equipment(self.name) # Load the equipment in a temporary equipment object
            self.id = temp_equip.id # get the updated id

        # then we our article to the clothing database
        # Insert the equipment into the database
        cursor.execute("""
        INSERT INTO clothing (id, nm, loc, only)
        VALUES (?, ?, ?, ?)
        """, (self.id, self.name, self.type, self.blocks_other))
        conn.commit() # commit the database
        conn.close() # close the database
        print(f"Added {self.name} to clothing inventory.") # print confermation
        return None

class In_liquid():
    def __init__(self, name: str, cost: float, id: int = None):
        """
        A function to initialize a liquid
        """
        # We ensure that we get the correct type of data
        if not isinstance(name, str):
            raise ValueError("The name must be a string.")
        if not isinstance(cost, float):
            raise ValueError("The cost must be a float.")
        
        self.name = name
        self.cost = cost
        self.id = id

        # we find an available id if the id space is blank
        if self.id is None:
            conn = get_connection(DB_STR) # open the database
            cursor_check = conn.cursor() # asign a cursor
            self.id = get_next_id(cursor_check, "liquids") # get an acceptable id
            conn.close()

        return None
    
    def add_liquid(self):
        """
        A function to add a liquid to the liquid inventory in the database.

        Returns
        -------
        None.

        """
        
        # Create a connection to the database
        conn = get_connection(DB_STR)
        cursor = conn.cursor()

        # Insert the equipment into the database
        cursor.execute("""
        INSERT INTO liquids (id, nm, cst)
        VALUES (?, ?, ?)
        """, (self.id, self.name, self.cost))
        conn.commit()
        conn.close()
        print(f"Added {self.name} to liquid inventory.")
        

############### FUNCTIONS ############################################################################
def retrive_equipment_by_id(database_name: str, table_name: str, in_id: int)->In_equipment:
    """
    Retrieve equipment details from the database by its ID.
    Args:
        database_name (str): The name of the database file.
        table_name (str): The name of the table containing equipment data.
        in_id (int): The ID of the equipment to retrieve.
    Returns:
        In_equipment: An instance of In_equipment containing the retrieved equipment details.
    Raises:
        ValueError: If the input types are incorrect or if no equipment is found with the given ID.
    Example:
        equipment = retrive_equipment_by_id("equipment.db", "equipment_table", 1)
    """
    # make sure we have good input
    if not isinstance(database_name, str):
        raise ValueError("The database name must be in the form of a string.")
    if not isinstance(table_name, str):
        raise ValueError("The table name must be in the form of a string.")
    if not isinstance(in_id, int):
        raise ValueError("The id entered must be an integer")
    
    # initialize our cursor
    # Create a connection to the database
    conn = get_connection(database_name)
    cursor = conn.cursor()

    # Retrieve the equipment from the database
    cursor.execute(f"SELECT nm, cst, wght, desc FROM {table_name} WHERE id = ?", (in_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise ValueError(f"No equipment found with id {in_id}.")
    
    # select out output, which is row[0] is the id, row[1] is the cost, row[2] 
    # is the weight, and row[3] is the description.
    name_out = row[0]
    cost_out = row[1]
    weight_out = row[2]
    desc_out = row[3]

    output = In_equipment(name_out, cost_out, weight_out, desc_out, id=in_id)

    print(f"Aquired {name_out} from master inventory, with cost {cost_out} and weight {weight_out}.")
    return output

def retrive_weapon_by_id(database_name: str, 
                         primary_table_name: str, 
                         secondary_table_name: str, 
                         in_id: int)->In_weapon:
    """
    Retrieve weapon details from the database by its ID.
    Args:
        database_name (str): The name of the database file.
        primary_table_name (str): The name of the table containing equipment data.
        secondary_table_name (str): The name of the table containing weapon data.
        in_id (int): The ID of the weapon to retrieve.
    Returns:
        In_weapon: An instance of In_weapon containing the retrieved weapon details.
    Raises:
        ValueError: If the input types are incorrect or if no weapon is found with the given ID.
    Example:
        equipment = retrive_weapon_by_id(DB_STR, equipment_master, weapons, 79)
    """
    # make sure we have good input
    if not isinstance(database_name, str):
        raise ValueError("The database name must be in the form of a string.")
    if not isinstance(primary_table_name, str):
        raise ValueError("The primary table name must be in the form of a string.")
    if not isinstance(secondary_table_name, str):
        raise ValueError("The secondary table name must be in the form of a string.")
    if not isinstance(in_id, int):
        raise ValueError("The id entered must be an integer")
    
    # initialize our cursor
    # Create a connection to the database
    conn = get_connection(database_name)
    cursor = conn.cursor()

    # Retrieve the equipment from the database
    cursor.execute(f"SELECT nm, cst, wght, desc FROM {primary_table_name} WHERE id = ?", (in_id,))
    row_e = cursor.fetchone() # find the row
    if row_e is None: # make sure the equipment is there in row equipment
        raise ValueError(f"No equipment found with id {in_id}.")
    name_out, cost_out, weight_out, desc_out = row_e # define our equipment variabls

    # Retrieve thew weapons data
    cursor.execute("""
        SELECT is_mrtl, dam_die, dam_typ, has_fin, i_t_h, has_vers, vers_die, 
               has_rng, norm_rng, max_rng, c_b_thrw, is_l, is_h, is_load, 
               use_ammo, is_rch, is_spcl, is_slvd 
        FROM weapons 
        WHERE id = ?
    """, (in_id,))
    # Define the row and create
    we_row = cursor.fetchone() # extract the weapon data
    conn.close() # close the database

    if we_row is None: # make sure the line isn't empty
        raise ValueError(f"No weapon found with id {in_id}")
    mar_o = we_row[0] # Is the weapon martial?
    dam_die_o = we_row[1] # How many faces on the damage die?
    dam_typ_o = we_row[2] # What type of damage?
    has_fin_o = we_row[3] # Does the weapon have the finnesse property
    two_hand_o = we_row[4] # Does the weapon need two hands
    has_vers_o = we_row[5] # Does the weapon have the versatile property
    vers_die_o = we_row[6] # If the weapon has the versatile property, what is the die
    has_rng_o = we_row[7] # Is the weapon ranged?
    norm_o = we_row[8]# what is the normal range of a ranged weapon
    max_o = we_row[9] # what is the maximum range of a ranged weapon
    throw_o = we_row[10] # Can the weapon be thrown?
    light_o = we_row[11] # is the weapon light?
    heavy_o = we_row[12] # is the weapon heavy?
    load_o = we_row[13] # Does the weapon have the loading property
    ammo_o = we_row[14] # Does the weapon require amunition?
    reach_o = we_row[15] # Does the weapon have reach?
    special_o = we_row[16] # Does the weapon have special properties?
    silvered_o = we_row[17] # Is the weapon silvered


    # And load or data into a In_weapon class
    output = In_weapon(name_out, cost_out, weight_out, desc_out, dam_die_o, dam_typ_o,
                       is_martial=mar_o, has_finesse=has_fin_o, is_two_handed=two_hand_o,
                       has_verstile=has_vers_o, damage_die_versatile=vers_die_o,
                       has_range=has_rng_o, normal_range=norm_o, max_range=max_o,
                       has_thrown=throw_o, is_light=light_o, is_heavy=heavy_o,
                       is_loading=load_o, uses_ammunition=ammo_o, has_reach=reach_o,
                       is_special=special_o, is_silvered=silvered_o)
    return output # return the In_weapon object

def retrive_armor_by_id(database_name: str, 
                         primary_table_name: str, 
                         secondary_table_name: str, 
                         in_id: int)->In_weapon:
    """
    Retrieve armor details from the database by its ID.
    Args:
        database_name (str): The name of the database file.
        primary_table_name (str): The name of the table containing equipment data.
        secondary_table_name (str): The name of the table containing armor data.
        in_id (int): The ID of the armor to retrieve.
    Returns:
        In_armor: An instance of In_armor containing the retrieved armor details.
    Raises:
        ValueError: If the input types are incorrect or if no armor is found with the given ID.
    Example:
        equipment = retrive_armor_by_id(DB_STR, equipment_master, armor, 79)
    """
    # make sure we have good input
    if not isinstance(database_name, str):
        raise ValueError("The database name must be in the form of a string.")
    if not isinstance(primary_table_name, str):
        raise ValueError("The primary table name must be in the form of a string.")
    if not isinstance(secondary_table_name, str):
        raise ValueError("The secondary table name must be in the form of a string.")
    if not isinstance(in_id, int):
        raise ValueError("The id entered must be an integer")
    
    # initialize our cursor
    # Create a connection to the database
    conn = get_connection(database_name)
    cursor = conn.cursor()
    
    # Retrieve the equipment from the database
    cursor.execute(f"SELECT nm, cst, wght, desc FROM {primary_table_name} WHERE id = ?", (in_id,))
    row_e = cursor.fetchone() # find the row
    if row_e is None: # make sure the equipment is there in row equipment
        raise ValueError(f"No equipment found with id {in_id}.")
    name_out, cost_out, weight_out, desc_out = row_e # define our equipment variabels

    # the retrieve the armor specific information
    cursor.execute(f"""
        SELECT ac, ar_type, stlth, need_str 
        FROM {secondary_table_name} WHERE id = ?""", (in_id,))
    # Define the row and create
    ar_row = cursor.fetchone() # extract the weapon data
    conn.close() # close the database
    if ar_row is None: # make sure the line isn't empty
        raise ValueError(f"No weapon found with id {in_id}")
    arm_class, arm_type, g_s, n_s = ar_row # g_s: good for stealth, n_s: needed strength

    # and place this all in the In_armor constructor
    output = In_armor(name_out, cost_out, weight_out, desc_out,
                      arm_class, arm_type, stealth_good=g_s, str_required=n_s)
    return output # and return the output

def retrive_id(database_name: str, table_name: str, name_in: str)->int:
    # make sure we have good input
    if not isinstance(database_name, str):
        raise ValueError("The database name must be in the form of a string.")
    if not isinstance(table_name, str):
        raise ValueError("The table name must be in the form of a string.")
    if not isinstance(name_in, str):
        raise ValueError("The name entered must be a string.")

    # initialize our cursor
    # Create a connection to the database
    conn = get_connection(database_name)
    cursor = conn.cursor()

    # Retrieve the equipment from the database
    cursor.execute(f"SELECT id FROM {table_name} WHERE nm = ?", (name_in,))
    output = cursor.fetchone()
    conn.close()
    return output[0]
    
def delete_object(in_str: str):
    """
    Deletes an object entry from the database.
    This method deletes an object entry from the `equipment_master` table in the database. 
    It first retrieves the ID of the object entry from the `equipment_master` table using 
    the objects's name. If the objects entry is found, it deletes the entry from the `equipment_master`
    table, and triggers the ON CASCADE DELETE ability.
    Parameters:
        in_str (str): the name of the object to be deleted
    Raises:
        ValueError: If no equipment is found with the specified name.
    Returns:
        None
    """
    # Check input
    if not isinstance(in_str, str):
        raise TypeError("Input must be in the form of a string")
    # Create a connection to the database
    conn = get_connection(DB_STR)
    cursor = conn.cursor()
    # first we need to get the id from equipment_master list
    # Retrieve the equipment from the database
    cursor.execute("SELECT id FROM equipment_master WHERE nm = ?", (in_str,))
    id_delete = cursor.fetchone()
    print(f"The deleted id is: {id_delete[0]}")
    # make sure that the weapon is in the list.  We need to search by name
    # since the defined object may not have the same id
    if id_delete is None:
        raise ValueError(f"No equipment found with name {in_str}.")
    # Delete the equipment from the equipment_master table
    cursor.execute("DELETE FROM equipment_master WHERE id = ?", (id_delete[0],))
    conn.commit()
    conn.close()
    print(f"Deleted {in_str} from all inventories.")
    # and exit the function
    return None

def delete_liquid(in_str: str):
    """
        Deletes an object entry from the database.
        This method deletes an object entry from the `equipment_master` table in the database. 
        It first retrieves the ID of the object entry from the `equipment_master` table using 
        the objects's name. If the objects entry is found, it deletes the entry from the `equipment_master`
        table, and triggers the ON CASCADE DELETE ability.
        Parameters:
            in_str (str): the name of the object to be deleted
        Raises:
            ValueError: If no equipment is found with the specified name.
        Returns:
            None
        """
        # Check input
    if not isinstance(in_str, str):
        raise TypeError("Input must be in the form of a string")
    # Create a connection to the database
    conn = get_connection(DB_STR)
    cursor = conn.cursor()
    # first we need to get the id from equipment_master list
    # Retrieve the equipment from the database
    cursor.execute("SELECT id FROM liquids WHERE nm = ?", (in_str,))
    id_delete = cursor.fetchone()
    print(f"The deleted id is: {id_delete[0]}")
    # make sure that the weapon is in the list.  We need to search by name
    # since the defined object may not have the same id
    if id_delete is None:
        raise ValueError(f"No liquid found with name {in_str}.")
    # Delete the equipment from the equipment_master table
    cursor.execute("DELETE FROM liquids WHERE id = ?", (id_delete[0],))
    conn.commit()
    conn.close()
    print(f"Deleted {in_str} from all inventories.")
    # and exit the function
    return None

def insert_condition(in_curs: sqlite3.Cursor, in_id: int, in_name: str, in_desc: str):
    """
    Inserts a condition into the master database.
    Parameters:
        in_curs (sqlite3.Cursor): The cursor we are using.
        in_id (int): The item id we want to use.
        in_name (str): The condition name we want to use.
        in_desc (str): A short description of the condition.
    """
    cmdtext = "INSERT OR IGNORE INTO conditions (id, nm, desc) VALUES (?, ?, ?)"
    in_curs.execute(cmdtext, (in_id, in_name, in_desc,))
    print(f"Inserted {in_name} into conditions at position {in_id}")
def insert_skill(in_curse: sqlite3.Cursor, in_id: int, in_name:str, in_attr: str, in_desc: str):
    """
    Inserts a condition into the master database.
    Parameters:
        in_curs (sqlite3.Cursor): The cursor we are using.
        in_id (int): The item id we want to use.
        in_name (str): The name of the skill.
        in_attr (str): The skills usual atribute.
        in_desc (str): A short description of the skill.
    """
    cmdtext = "INSERT OR IGNORE INTO skills (id, nm, usl_atr, desc) VALUES (?, ?, ?, ?)"
    in_curse.execute(cmdtext, (in_id, in_name, in_attr, in_desc))
    print(f"Inserted {in_name} into skills at position {in_id}")

############## APPLICATION SPACE ##############################################
#==============================================================================
#
#==============================================================================