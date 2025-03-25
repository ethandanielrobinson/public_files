# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 17:29:33 2025

@author: ethan
"""
#%% Intialization
#=============================================================================
# Program to better help me manage sidekick characters, as there is currently
# No effective way to do this on dndbeyond.com
#=============================================================================
# Boilerplate imports
import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from time import sleep
from time import time
from typing import List, Tuple
import os # Allows us to change directories

# Get the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
# Change the current working directory to the script's directory
os.chdir(script_dir)

# And import our two suplementary files
import tkinter_function_storage as tfs # must come first
import sidekick_data_update as sd
import function_storage_update as fsu


# Now we need to open the sidekick files
sidefiles_path = os.path.join(script_dir, "sidekick_files")
print(sidefiles_path)
os.chdir(sidefiles_path)

character: fsu.Character = None # Initilize the Character object
char_names = ["filia_kosta", "drusus_scrutatorum", "agripina_exotoria"]
in_name = 2
sd.initialize_all(f"{char_names[in_name]}.json") # needed to use the sd file.

#%% Function Definitions
def load_character():
    """Loads the latest character data from the JSON file."""
    global character
    character = sd.retrive_char()  # Update the Character.
    if character is None:
        raise ValueError("Failed to load character. Please check the JSON file.")

load_character()
print(f"Loaded {character.name}")

# Define the absolute file path
def get_file_path(file_name, sub_dir=""):
    """
    Returns the absolute path of a file within the sidefiles directory.
    Parameters:
        file_name (str): The name of the file.
        sub_dir (str): Optional subdirectory within sidefiles_path.
    Returns:
        str: The absolute path of the file.
    """
    return os.path.join(sidefiles_path, sub_dir, file_name)

char_json_path = get_file_path(f"{char_names[in_name]}.json")
char_db_path = get_file_path(f"{char_names[in_name]}_database.db", "databases")
print(char_json_path)
print(char_db_path)

#%%
class FileHandler(FileSystemEventHandler):
    """
    A Class to update the local file data if the JSON or SQLite3 Database is changed.
    Parameters:
        FileSystemEventHandler: The Parent Class.
    """
    def __init__(self, ui_update_callback):
        super().__init__()
        self.ui_update_callback = ui_update_callback  # Store callback function
    
    last_modified_time = 0  # Store the last modification time
    
    def on_modified(self, event):
        if event.src_path == os.path.abspath(char_json_path) or event.src_path == os.path.abspath(char_db_path):
            current_time = time()
            
            # Ignore duplicate triggers within 0.5 seconds
            if current_time - self.last_modified_time > 0.5:
                self.last_modified_time = current_time
                print(f"File Changed: {event.src_path}. Reloading...")
                # And grab the updated information.
                character.cur_hp, character.max_hp, character.temp_hp, character.conditions = sd.update_char()
                self.ui_update_callback(main_win)


def add_string(vars: list[str]):
    """
    A function to turn a list of strings into a single string separated by commas.
    Parameters:
        vars (list[str]): A list of strings.
    Returns:
        output (str): The list of strings in a comma-separated single string.
    """
    output = "" # initialize the empty string
    len_con = len(vars) - 1 # the minus one is to get the index correct
    spacer = ', '
    for index, text in enumerate(vars):
        output += text
        if index < len_con:
            output += spacer
    return output
    


def start_observer(ui_update_callback):
    observer = Observer()
    handler = FileHandler(ui_update_callback)

    # Monitor both the character JSON file's directory and the databases directory
    observer.schedule(handler, path=sidefiles_path, recursive=False)  # Watches the JSON file directory
    observer.schedule(handler, path=os.path.join(sidefiles_path, "databases"), recursive=False)  # Watches the database directory
    
    observer.start()
    return observer


# EQUIPMENT BUTTON ===========================================================
def equipment_press(in_root: tk.Tk):
    """
    Function that defines what to do when the add equipment button is pressed.
    Parameters:
        in_root (tk.Tk): The primary character window.
    """
    global character # define our global character
    in_root.destroy() # Destroy current char window
    tfs.add_eq_window(character.color) # open equipment modification pane
    character = sd.retrive_char()
    main_win, update_ui= create_main_window()

    # Start the observer in a background thread
    observer = start_observer(update_ui)
    observer_thread = threading.Thread(target=observer.join, daemon=True)
    observer_thread.start()


    main_win.mainloop()


def create_main_window():
    
    def _safe_update_ui():
        """
        This function runs on the main Tkinter thread.
        """
        global character
        hit_points_current.set(character.cur_hp)
        hit_points_max.set(character.max_hp)
        hit_points_temp.set(character.temp_hp)
        cond_current.set(add_string([cond[1] for cond in character.conditions]))  
        print(f"Updated UI: {character.name}, HP: {character.cur_hp}/{character.max_hp}")

    def _update_ui(root: tk.Tk):
        """
        A function to manage the update_ui function.
        """
        root.after(0, _safe_update_ui)

    #create main window
    window = tk.Tk()
    window.config(bg = "#FFFFFF") # Set the background of the window to be BYU slate grey

    window.title(character.name) # Window Name

    ###############################################################################
    #### CREATING THE DATA ########################################################
    ###############################################################################

    #------------------------------------------------------------------------------
    #### FRAME 1
    #------------------------------------------------------------------------------

    # Make sure we have the correct name
    name_var = tk.StringVar()
    name_var.set(character.name)

    # List of the abreviations for all the atributes.  VERY USEFUL
    atributetitle = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    atributelist = ["stre", "dext", "cons", "inte", "wisd", "char"]

    # Initialize the list of atrubute ints, then fill it with the corrct
    # date from the charachter dictionary.  Atributes Visible is the name
    at_vis = []
    for atr in atributelist:
        statone = getattr(character, atr) # grab the atributes from the character.
        at_vis.append(statone)
        
    # Generate the correct modifiers to be placed below the atributes
    at_mod = [] # Initialize the array
    for n in range(6):
        modone = at_vis[n] # Get the correct data
        modtwo = (modone - 10) // 2 # find the modifier
        at_mod.append(modtwo) # add to list

    # Bring in the charachter image (from Geeks to Geeks)
    # adding image (remember image should be PNG and not JPG)
    # Ensure the image file exists and is accessible
    image_path = os.path.join(sidefiles_path, character.image)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    window.img_a = tk.PhotoImage(file=image_path)  # Store reference in the window object
    window.img = window.img_a.subsample(3, 3)

    #------------------------------------------------------------------------------
    #### FRAME 2
    #------------------------------------------------------------------------------

    # Create IntVar objects for hit points
    hit_points_max = tk.IntVar(value = character.max_hp)
    hit_points_current = tk.IntVar(value = character.cur_hp)
    hit_points_temp = tk.IntVar(value = character.temp_hp)

    # Import weapons
    wea_array = []
    for weapon, _ in character.weapon_inv: #check the weapon inventory and add the names
        tkweaponstr = tk.StringVar(value = weapon.name)
        weapon_id = weapon.id # an int
        weapon_l = bool(weapon.is_light) # FIX LATER
        wea_array.append((tkweaponstr, weapon_id, weapon_l))

    armor_list = [armor.name for armor, _ in character.armor_inv] # creates a list of strings to create the armor list

    # we also need to check if the character has a shield
    has_shield = True if character.search_inventory(2) else False

    #------------------------------------------------------------------------------
    #### FRAME 3
    #------------------------------------------------------------------------------

    # Combine both the expterise skill list and the proficiancy skill list
    # Then putting them into an array of StringVars
    skill_list = []
    skill_insts = sd.skill_list # the total list of skills from the sd file.
    for skill in skill_insts:
        skill_var = tk.IntVar(value = skill.id)
        skill_list.append(skill_var)

    # Conditions display
    cond_str = add_string([cond[1] for cond in character.conditions])
    cond_current = tk.StringVar(value = cond_str)        

    ###############################################################################
    #### CREATING THE FRAMES ######################################################
    ###############################################################################
    #### MASTER FRAMES ============================================================
    master_1_color = "#92734A"
    master_1 = tk.Frame(window, bg = master_1_color) # Atributes and Photo
    master_1.grid(row = 0, column=0, sticky="nesw")

    # Weapons and Armor Class
    master_2_color = character.color
    master_2 = tk.Frame(window, bg = master_2_color)
    master_2.grid(row=0, column=1, sticky="nesw")

    # Skill Pane
    master_3_color = "#92734A"
    master_3 = tk.Frame(window, bg = master_3_color)
    master_3.grid(row=0, column=2, sticky="nesw")
    #### SUB FRAMES ===============================================================
    # master_1 --------------------------------------------------------------------
    atribute_frame = tfs.padded_frame(master_1, 25, 6, master_1_color) # Create the atribute Frame
    # master_2 --------------------------------------------------------------------
    health_frame = tk.Frame(master_2, bg = master_2_color, padx = 10, pady = 10) # Create the Health Frame
    hp_frame = tk.Frame(health_frame, bg = master_2_color) # sub-sub-frame--------------------------------
    weapon_frame = tk.Frame(master_2, bg = master_2_color, padx = 10, pady = 10) # Create the Weapon Frame
    armor_frame = tk.Frame(master_2, bg = master_2_color, padx = 10, pady = 10) # Create the Equipment Frame
    # master_3 --------------------------------------------------------------------
    skill_frame = tk.Frame(master_3, bg = master_3_color, padx = 10, pady = 10) # Create the skill frame
    condition_frame = tk.Frame(master_3, bg = master_3_color, padx = 10, pady = 10) # Create the Condition Frame
    equipment_frame = tk.Frame(master_3, bg = master_3_color, padx = 10, pady = 10) # Create the equipment frame
    ###############################################################################
    #### CREATING THE LABELS ######################################################
    ###############################################################################

    #------------------------------------------------------------------------------
    #### Master 1
    #------------------------------------------------------------------------------
    # and generate the name label
    name = tfs.titlelabel(master_1, name_var, character.color)

    # and the Array of Atribute Labels---------------------------------------------
    atributelabel = tfs.create_atlabels(atribute_frame, atributetitle)

    # And create the atributes label (lab stands for label)
    valuebutton = tfs.create_atvalues(atribute_frame, at_vis)

    # We use a new function, create_modvalues
    modlabels = tfs.create_modvalues(atribute_frame, at_mod)
        
    # setting image with the help of label ----------------------------------------
    imglabel_one = tk.Label(master_1, image=window.img, bg=character.color)

    #------------------------------------------------------------------------------
    #### Master 2
    #------------------------------------------------------------------------------
    # generate the total health and current health labels
    he_str = tk.StringVar()
    he_str.set("Health")
    healthtitle = tfs.longlabel(health_frame, he_str)
    healthlabels = tfs.health_labels(hp_frame, hit_points_current, hit_points_max, character.color)
    # Temp Health Points value
    tempvalue = tfs.temphealthindicator(health_frame, hit_points_temp) 
    # Create the temp health points label
    templabel = tfs.longlabel(health_frame, tk.StringVar(value = "Temp Health"))

    # and the damage controls
    damage_str = tk.StringVar(value = "DAMAGE")
    dambutton = tfs.damagebutton(health_frame, damage_str)
    temp_hp_str = tk.StringVar(value = "TEMP HP")
    temp_hp_button = tfs.tempbutton(health_frame, temp_hp_str)
    heal_str = tk.StringVar(value = "HEAL")
    heabutton = tfs.healbutton(health_frame, heal_str)

    # Now for the Weapons title-----------------------------------------------------
    we_str = tk.StringVar()
    we_str.set("Weapons")
    wea_title = tfs.longlabel(weapon_frame, we_str)

    # And the Weapons list
    wea_list = tfs.weaponbutton(weapon_frame, wea_array)

    # Next the Armor title------------------------------------------------------------
    ar_str = tk.StringVar()
    ar_str.set("Armor Class")
    ar_title = tfs.longlabel(armor_frame, ar_str)

    # datatype of menu text 
    ar_but_list = tfs.armordrop(armor_frame, armor_list)

    # and a checkbox for the shield that will only be placed if the character has a sheild
    shield_check = tfs.equipcheck(armor_frame, incolor = "#CCCCCC", fontcolor = "#202020")

    #------------------------------------------------------------------------------
    #### Skill Frame
    #-----------------------------------------------------------------------------
    sk_lab = tk.StringVar()
    sk_lab.set("Skill List")
    sk_title = tfs.longlabel(skill_frame, sk_lab)

    # And create the skill buttons themselves (Skill Button List)
    sk_but_list = tfs.skillbutton(skill_frame, skill_list, character.color)

    # Create a label for the conditions frame ------------------------------------
    con_str = tk.StringVar()
    con_str.set("Conditions")
    con_title = tfs.longlabel(condition_frame, con_str)

    # The buttons to add and remove a condition
    con_but = tfs.conbutton(condition_frame, character.color)

    # and create the icons to go into the frame.
    con_array = tfs.cond_effects(condition_frame, cond_current)


    # The equipment management pane -----------------------------------------------
    eq_str = tk.StringVar()
    eq_str.set("Equipment")
    eq_title = tfs.longlabel(equipment_frame, eq_str)

    eq_but = tk.Button(equipment_frame, text = "Open Equipment Panel", command = lambda w=window: equipment_press(w), 
                    font = ("Times New Roman", 12, "bold"), fg="#FFFFFF", 
                    bg=character.color, padx = 5, pady = 5, cursor="hand2")

    # And the exit button
    exit_but = tk.Button (master_3, 
                        text = "EXIT", 
                        command = window.destroy,
                        font = ("Times New Roman",12),
                        fg = "#FFFFFF",
                        bg = "#CC0000",
                        width = 6,
                        cursor = "hand2")

    ###############################################################################
    #### PLACING THE LABELS #######################################################
    ###############################################################################

    #==============================================================================
    #### 1st Master Frame
    # (row = 0) Character Name
    # (row = 1) Character Atributes
    # (row = 1) Character Image
    #==============================================================================

    # and Print out the labels, starting with Row 0
    name.grid(row = 0, column = 0, pady = 5)

    # Atributes frame, remember column 0 and column 8 are empty and set at 25 px --
    #--- We use a for loop to place all the correct labels
    # ROW 0
    for n in range(6):
        colid = n + 1 # Column ID
        atributelabel[n][1].grid(row = 0, column = colid)

    # ROW 1
    for n in range(6):
        colid = n + 1 # Column ID
        valuebutton[n][1].grid(row = 1, column = colid, padx = 5) # ensure seperation

    # ROW 2
    for n in range(6):
        colid = n + 1 # Column ID
        modlabels[n][1].grid(row = 2, column = colid)
    #------------------------------------------------------------------------------
    atribute_frame.grid(row = 1, column = 0) # add the atribute frame to the master

    # And back to the master frame ------------------------------------------------
    imglabel_one.grid(row = 2, column = 0)
    #-----------------------------------

    #==============================================================================
    #### 2nd Master Frame
    # (row = 0) Character Health
    # (row = 1) Character Weapons
    # (row = 2) Character Armor
    #==============================================================================

    # Health Frame, 3 Columns -----------------------------------------------------
    # ROW 0
    healthtitle.grid(row = 0, column = 0, columnspan = 3, pady = 5)

    # ROW 1
    # Our health information -- we want a third level frame for this
    for n in range(3):
        healthlabels[n][1].grid(row = 0, column = n)
    hp_frame.grid(row = 1, column = 0, columnspan = 3) # we need to remember to place the actual hp frame

    # ROW 2
    # place the health modification buttons
    dambutton.grid(row = 2, column = 0)
    temp_hp_button.grid(row = 2, column = 1)
    heabutton.grid(row = 2, column = 2)

    # ROW 3
    # Place the temporary health values
    tempvalue.grid(row = 3, column = 0, pady = 5)
    templabel.grid(row = 3, column = 1, columnspan = 2, pady = 5)
    #----------------------------------------------------------------------------
    health_frame.grid(row = 0, column = 0) # add the health frame

    # Weapon Frame, 1 Column ----------------------------------------------------
    # R0W 0
    wea_title.grid(row = 0, column = 0, pady = 5)

    # Now we need to know how many weapons we have
    length_a = len(character.weapon_inv) # should work fine, even with the tupples

    # Weapon Rows
    for n in range(length_a):
        active_ros = n + 1
        wea_list[n][1].grid(row = active_ros, column = 0)
    #----------------------------------------------------------------------------
    weapon_frame.grid(row = 1, column = 0) # add the weapon frame
    
    # Armor Frame, 1 Column -----------------------------------------------------
    # Row 0
    ar_title.grid(row = 0, column = 0, pady = 5)

    # Row 1
    ar_but_list[1].grid(row = 1, column = 0, pady = 5)

    # Row 2
    ar_row = 2 # set the armor row to 2
    if has_shield:
        shield_check[1].grid(row = 2, column = 0, pady = 5)
        ar_row = 3 # set the armor row to 3    

    #Row 3 (Row 2 if no shield)
    #******************************************
    # we have to take some special time here to 
    # ensure that the correct armor value is there
    # as well as checking if we have a shield
    #*************************************************
    # We grab the StringVar from the armor button list 
    # (it's the first value of the tupple)
    armorval = tfs.armorlabel(armor_frame, ar_but_list[0], shield_check[0])
    armorval.grid(row = ar_row, column = 0, pady = 5)
    #----------------------------------------------------------------------------
    armor_frame.grid(row = 2, column = 0) # add the armor frame

    #==============================================================================
    #### 3rd Master Frame
    # (row = 0) Character Skills
    # (row = 1) Character Conditions
    # (row = 2) Character Equipment
    #==============================================================================

    # Skill Frame, 2 Columns ------------------------------------------------------
    # Row 0
    sk_title.grid(row = 0, column = 0, columnspan=2, pady = 5)

    length_b = len(sd.skill_list) // 2 # The total number of skills in 5e is 18
    # so this number should be 9

    # Row 1-9
    for n in range(length_b):
        act_row = n + 1 # the one is for the title.
        sk_a = n*2 # stands for skill A
        sk_b = (n*2) + 1 # stands for skill B
        sk_but_list[sk_a][1].grid(row = act_row, column = 0)
        sk_but_list[sk_b][1].grid(row = act_row, column = 1)
    #----------------------------------------------------------------------------
    skill_frame.grid(row = 0, column = 0) # add the skill frame

    # Conditions Frame, 2 Columns -----------------------------------------------
    # Row 0, conditions lable
    con_title.grid(row = 0, column = 0, columnspan = 2, pady = 5)

    # Row 1, And the condition buttons
    con_but[0].grid(row = 1, column = 0)
    con_but[1].grid(row = 1, column = 1)

    # Row 2, Conditions text
    con_array.grid(row = 2, column = 0, columnspan = 2, pady = 5)
    #---------------------------------------------------------------------------- 
    condition_frame.grid(row = 1, column = 0) # add the condition frame

    # Equipment Frame, 1 Column -------------------------------------------------
    # Row 0
    eq_title.grid(row=0, column=0, pady = 5)

    # Row 1
    eq_but.grid(row = 1, column = 0)
    #----------------------------------------------------------------------------
    equipment_frame.grid(row = 2, column = 0) # add the equipment frame

    # back to the master
    exit_but.grid(row = 3, column = 0, pady = 5)

    return window, _update_ui

#%% And start up our window
if __name__ == "__main__":
    main_win, update_ui= create_main_window()

    # Start the observer in a background thread
    observer = start_observer(update_ui)
    observer_thread = threading.Thread(target=observer.join, daemon=True)
    observer_thread.start()


    main_win.mainloop()
    # Cleanup observer when the Tkinter window closes
    observer.stop()
    observer.join()
if character is not None:
    print(f"The current health is {character.cur_hp}")
else:
    print("Character data is not loaded. Unable to display current health.")
    print(f"An error occurred: {e}")

