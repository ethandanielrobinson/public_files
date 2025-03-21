import json
import os # Allows us to change directories
os.chdir(r'D:\dungeons_and_dragons\Custom_Programs')
import tkinter_function_storage as tfs
import sidekick_data as sd

# First open the sidekick file
os.chdir(r'D:\dungeons_and_dragons\Custom_Programs\sidekick_files')

with open("drusus_scruatorum.json", "r") as infile:
    drusus = json.load(infile)
    
with open("filia_kosta.json","r") as infile:
    char = json.load(infile)

char['class'] = 'Warrior'

char['condition'] = ['unconscious']

char['current_hp'] = 40

char['hp'] = 40

# Define equipment as a nest
char['equipment'] = {}

char['equipment']['armor'] = ['chain shirt', 'common clothes']
char['equipment']['weapons'] = ['spear', 'longsword']
char['equipment']['other'] = ['shield', 'bottle']

char['exhastion'] = 0

char['hit_dice'] = 6

char['hit_dice_remaining'] = 6

char['languages'] = ['common', 'elvish']

char['level'] = 4

char['name'] = 'Filia Kosta'

char['prof_bonus'] = 2

char['saving_throws'] = ['STR']

# Define Skills a nest
char['skills'] = {}

char['skills']['expertise'] = []

char['skills']['prof'] = ["intimidation", 'perception']

# Define stats as a nest
char['stats'] = {}

char['stats']['STR'] = 14

char['stats']['DEX'] = 13

char['stats']['CON'] = 12

char['stats']['INT'] = 10

char['stats']['WIS'] = 11

char['stats']['CHA'] = 10

char['image'] = "filia_kosta.png"

char['temp_hp'] = 0

# Write the updated character back to the JSON file
with open("filia_kosta.json", "w") as outfile:
    json.dump(char, outfile, indent=2)
    print('done')