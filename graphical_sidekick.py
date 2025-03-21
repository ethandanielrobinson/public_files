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
import json
from time import sleep
from time import time
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
char_names = ["filia_kosta", "drusus_scrutatorum"]
in_name = 0
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
        FileSystemEventHandler: The input.
    """
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
                update_ui()


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
    

def update_ui():
    window.after(0, _safe_update_ui)

def _safe_update_ui():
    """This function runs on the main Tkinter thread."""
    hit_points_current.set(character.cur_hp)
    hit_points_max.set(character.max_hp)
    hit_points_temp.set(character.temp_hp)
    cond_current.set(add_string([cond[1] for cond in character.conditions]))  
    print(f"Updated UI: {character.name}, HP: {character.cur_hp}/{character.max_hp}")


def start_observer():
    observer = Observer()
    handler = FileHandler()

    # Monitor both the character JSON file's directory and the databases directory
    observer.schedule(handler, path=sidefiles_path, recursive=False)  # Watches the JSON file directory
    observer.schedule(handler, path=os.path.join(sidefiles_path, "databases"), recursive=False)  # Watches the database directory
    
    observer.start()

    try:
        while True:
            sleep(1)  # Keep the observer running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Start the observer in a background thread
observer_thread = threading.Thread(target=start_observer, daemon=True)
observer_thread.start()

#create main window
window = tk.Tk()
window.config(bg = "#FFFFFF") # Set the background of the window to be BYU slate grey

window.title(character.name) # Window Name



#%% CREATING THE DATA =========================================================

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
img_a = tk.PhotoImage(file = character.image)
img = img_a.subsample(3, 3)

#------------------------------------------------------------------------------
#### FRAME 2
#------------------------------------------------------------------------------

# Create IntVar objects for hit points
hit_points_max = tk.IntVar(value=character.max_hp)
hit_points_current = tk.IntVar(value=character.cur_hp)
hit_points_temp = tk.IntVar(value=character.temp_hp)

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
cond_current = tk.StringVar()
cond_str = add_string([cond[1] for cond in character.conditions])
cond_current.set(cond_str)        

#%% CREATING THE MASTER FRAMES ================================================
a_and_p = tk.Frame(window, bg = "#7C878E") # Atributes and Photo
a_and_p.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Weapons and Armor Class
we_and_ac = tk.Frame(window, bg = character.color)
we_and_ac.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Skill Pane
skill_fr = tk.Frame(window, bg = "#7C878E")
skill_fr.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

#%% CREATING THE LABELS =======================================================

#------------------------------------------------------------------------------
#### Atributes and Photo
#------------------------------------------------------------------------------
# and generate the name label
name = tfs.titlelabel(a_and_p, name_var, character.color)

# and the Array of Atribute Labels
atributelabel = tfs.create_atlabels(a_and_p, atributetitle)

# And create the atributes label (lab stands for label)
valuebutton = tfs.create_atvalues(a_and_p, at_vis)

# We use a new function, create_modvalues
modlabels = tfs.create_modvalues(a_and_p, at_mod)

# Create an array of spacing frame
width_space = 15
height_space = 15
spacers = []
for n in range(8):
    spacer = tk.Frame(a_and_p, 
                      width = width_space, 
                      height = height_space, 
                      bg = "#7C878E")
    spacers.append(spacer)
    
# setting image with the help of label
imglabel_one = tk.Label(a_and_p, image = img, bg = character.color)

#------------------------------------------------------------------------------
#### Weapons and Armor Class
#------------------------------------------------------------------------------
# generate the total health and current health labels
he_str = tk.StringVar()
he_str.set("Health")
healthtitle = tfs.longlabel(we_and_ac, he_str)
healthlabels = tfs.health_labels(we_and_ac, hit_points_current, hit_points_max, character.color)
# Temp Health Points value
tempvalue = tfs.temphealthindicator(we_and_ac, hit_points_temp) 
# Create the temp health points label
templabel = tfs.longlabel(we_and_ac, tk.StringVar(value = "Temp Health"))

# and the damage controls
damage_str = tk.StringVar(value = "DAMAGE")
dambutton = tfs.damagebutton(we_and_ac, damage_str)
temp_hp_str = tk.StringVar(value = "TEMP HP")
temp_hp_button = tfs.tempbutton(we_and_ac, temp_hp_str)
heal_str = tk.StringVar(value = "HEAL")
heabutton = tfs.healbutton(we_and_ac, heal_str)

# Now for the Weapons title
we_str = tk.StringVar()
we_str.set("Weapons")
wea_title = tfs.longlabel(we_and_ac, we_str)

# And the Weapons list
wea_list = tfs.weaponbutton(we_and_ac, wea_array)

# Next the Armor title
ar_str = tk.StringVar()
ar_str.set("Armor Class")
ar_title = tfs.longlabel(we_and_ac, ar_str)

# datatype of menu text 
ar_but_list = tfs.armordrop(we_and_ac, armor_list)

# and a checkbox for the shield that will only be placed if the character has a sheild
shield_check = tfs.equipcheck(we_and_ac, incolor = "#CCCCCC", 
                              fontcolor = "#202020")

#------------------------------------------------------------------------------
#### Skill Frame
#-----------------------------------------------------------------------------
sk_lab = tk.StringVar()
sk_lab.set("Skill List")
sk_title = tfs.longlabel(skill_fr, sk_lab)

# And create the skill buttons themselves (Skill Button List)
sk_but_list = tfs.skillbutton(skill_fr, skill_list, character.color)

# Create a label for the conditions frame
con_str = tk.StringVar()
con_str.set("Conditions")
con_title = tfs.longlabel(skill_fr, con_str)

# The buttons to add and remove a condition
con_but = tfs.conbutton(skill_fr, character.color)

# and create the icons to go into the frame.
con_array = tfs.cond_effects(skill_fr, cond_current)


# And the exit button
exit_but = tk.Button (skill_fr, 
                      text = "EXIT", 
                      command = window.destroy,
                      font = ("Times New Roman",12),
                      fg = "#FFFFFF",
                      bg = "#CC0000",
                      width = 6,
                      cursor = "hand2")

#%% PLACING THE LABELS ========================================================

#------------------------------------------------------------------------------
#### 1st Frame
#------------------------------------------------------------------------------

# and Print out the labels, starting with Row 0
name.grid(row = 0, column = 0, columnspan = 8, pady = 15)

# ROW 1
spacers[0].grid(row = 1, column = 0)
#--- We use a for loop to place all the correct labels
for n in range(6):
    colid = n + 1 # Column ID
    atributelabel[n][1].grid(row = 1, column = colid)
#-----------------------------------------------------
spacers[1].grid(row = 1, column = 7)

# ROW 2
spacers[2].grid(row = 2, column = 0)
#------------------------------------
for n in range(6):
    colid = n + 1 # Column ID
    valuebutton[n][1].grid(row = 2, column = colid)
#------------------------------------
spacers[3].grid(row = 2, column = 7)

# ROW 3
spacers[4].grid(row = 3, column = 0)
#-----------------------------------
for n in range(6):
    colid = n + 1 # Column ID
    modlabels[n][1].grid(row = 3, column = colid)
#-----------------------------------
spacers[5].grid(row = 3, column = 7)

# ROW 4

spacers[6].grid(row = 3, column = 0)
#-----------------------------------
imglabel_one.grid(row = 4, column = 1, columnspan = 6, pady = 10)
#-----------------------------------
spacers[7].grid(row = 3, column = 7)

#------------------------------------------------------------------------------
#### 2nd Frame
#-----------------------------------------------------------------------------

# ROW 0
healthtitle.grid(row = 0, column = 0, columnspan = 3, pady = 15)

# ROW 1
# Our health information
for n in range(3):
    xspace = 0; # ensure that the actual 2 numbers have the propper buffer
    if n in [0,2]:
        xspace = 5
    healthlabels[n][1].grid(row = 1, column = n, padx = xspace, pady = 10)

# ROW 2
# place the health modification button
dambutton.grid(row = 2, column = 0)
temp_hp_button.grid(row = 2, column = 1)
heabutton.grid(row = 2, column = 2)

# ROW 3
# Place the temporary health values
tempvalue.grid(row = 3, column = 0, pady = 5)
templabel.grid(row = 3, column = 1, columnspan = 2, pady = 5)

# R0W 4
wea_title.grid(row = 4, column = 0, columnspan = 3, pady = 15)

# Now we need to know how many weapons we have
length_a = len(character.weapon_inv) # should work fine, even with the tupples

# Row More
add_row = 5 #This is a counter for the armor class row

for n in range(length_a):
    active_ros = n + 5
    wea_list[n][1].grid(row = active_ros, column = 0, columnspan = 3)
    add_row = active_ros + 1
    
# ROW add_row ----------
ar_title.grid(row = add_row, column = 0, columnspan= 3, pady = 15)

# ROW add_row + 1 -----
current_row = add_row + 1
ar_but_list[1].grid(row = current_row, column = 0, columnspan = 3)

# ROW add 1
if has_shield:
    current_row += 1 # Update the current row
    shield_check[1].grid(row = current_row, column = 0, columnspan = 3, pady = 5)

#ROW next
current_row += 1 # Update the current row
#----------------------------------------------------------------------------
# we have to take some special time here to 
# ensure that the correct armor value is there
# as well as checking if we have a shield
#----------------------------------------------------------------------------
# We grab the StringVar from the armor button list 
# (it's the first value of the tupple)
armorval = tfs.armorlabel(we_and_ac, ar_but_list[0], shield_check[0])
armorval.grid(row = current_row, column = 1, padx = 5, pady = 5)

#------------------------------------------------------------------------------
#### 3rd Frame
#------------------------------------------------------------------------------

sk_title.grid(row = 0, column = 0, columnspan=2, padx = 15, pady = 15)

length_b = len(sd.skill_list) // 2 # The total number of skills in 5e is 18
# so this number should be 9

for n in range(length_b):
    act_row = n + 1 # the one is for the title.
    sk_a = n*2 # stands for skill A
    sk_b = (n*2) + 1 # stands for skill B
    sk_but_list[sk_a][1].grid(row = act_row, column = 0, padx = 0)
    sk_but_list[sk_b][1].grid(row = act_row, column = 1, padx = 0)
    
# update act_row
act_row = act_row + 1
# place conditions label
con_title.grid(row = act_row, column = 0, columnspan = 2, padx = 20, pady = 5)

# place the buttons
act_row = act_row + 1 # update act_row
con_but[0].grid(row = act_row, column = 0, pady = 5)
con_but[1].grid(row = act_row, column = 1, pady = 5)

# and Place our conditions frame
act_row = act_row + 1 # update act_row
con_array.grid(row = act_row, column = 0, columnspan = 2, padx = 20, pady = 5)

act_row = act_row + 1 # update act_row
exit_but.grid(row = act_row, column = 0, columnspan = 2, padx = 20, pady = 5)
#%% And start up our window

window.mainloop()
if character is not None:
    print(f"The current health is {character.cur_hp}")
else:
    print("Character data is not loaded. Unable to display current health.")
    print(f"An error occurred: {e}")

