# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 17:51:15 2025

@author: ethan
"""
import os # Allows us to change directories

# Get the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the current working directory to the script's directory
os.chdir(script_dir)

import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
import function_storage_update as fss
os.chdir(script_dir) # ensure we are in the correct folder.
import sidekick_data_update as sd

# Printing information
# List of the abreviations for all the atributes.  VERY USEFUL
atributetitle = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

# list of light weapons for marking
weapons_light = ["club", "dagger", "handaxe", "light hammer", "sickle",
                 "scimitar", "shortsword", "hand crossbow"]

LAB_OPTIONS_ONE = {
                "bg": "#FFFFFF",
                "fg": "#202020",
                "bd" : 3,
                "padx": 10,
                "pady": 10,
                "justify" : tk.CENTER,
                "relief" : tk.SOLID}


#### FRAME GENERATING FUNCTIONS
def padded_frame(root, pad: int, column_number: int, color: str):
    """
    A function to produce a padded frame (the outer columns, which are meant to be empty, have a fixed
    width).
    Parameters:
        root: The root window or master frame instance.
        pat (int): The amount of padding we want in pixels
        column_number (int):  The number of filled columns we expect the frame to have.
        color (str): The color of the frame expressed as a string.
    Raises:
        TypeError: Argument other than an integer or string entered.
    Returns:
        output (tk.Frame): A Frame object output.
    """
    if not (isinstance(column_number, int) and isinstance(color, str)): # ensure correct input
        raise TypeError("Argument must be an correct.")
    
    output = tk.Frame(root, bg = color, pady = 10)
    out_col = column_number + 1
    for num in [0, out_col]: # iterate over the array.
        output.columnconfigure(num, minsize=pad)
    return output


# Function 1
def atribute_click(button_input, num_input):
    at_mod = (num_input - 10) // 2
    output = fss.rolltwenty(0) + at_mod # calculate the roll.
    fss.create_info_box("Atribute Roll", f"You rolled a {output}.")
    
# Function 2
def dam_click():
    """
    A function to call for the damage function in sidekick data update.
    """
    # Use simpledialog to prompt for input
    user_string = simpledialog.askstring("Damage Input", "Combat Damage:")
    user_input = int(user_string) # Ensure that our input is an int
    
    # Check to make sure user input something
    if user_input:
        sd.damage(user_input)
    else:
        sd.damage(0)

def temp_click():
    """
    A function to manage the temp_heal function in sidekick data update
    """
    # Use simpledialog to prompt for input
    user_string = simpledialog.askstring("Temporary Health Input",
                                         "Temp HP Amount:")
    user_input = int(user_string) # Ensure that our input is an int
    
    # Check to make sure user input something
    if user_input:
        sd.temp_heal(user_input)
    else:
        sd.temp_heal(0)

# Function 3       
def hea_click():
    """
    A function to manage the heal function in sidekick data update.
    """
    # Use simpledialog to prompt for input
    user_string = simpledialog.askstring("Healing Input", "Healing Amount:")
    user_input = int(user_string) # Ensure that our input is an int
        
    # Check User input
    if user_input:
        sd.heal(user_input)
    else:
        sd.heal(0)

# Function 4
def weapon_click(type_in):
    """
    Function to manage the attack function from sidekick data update.
    """
    sd.attack(type_in)

# Function 5
def titlelabel(win: tk.Frame, var: tk.StringVar, color: str):
    """
    Function that creates a title label, ensuring only Frame and StringVar are used.
    Parameters:
        win (tk.Frame): The primary window.
        var (tk.StringVar): The StringVar we want to put in the label.
        color (str): The background color.
    Raises:
        TypeError: Incorrect input.
    """
    
    # Ensure correct argument types
    if not (isinstance(win, tk.Frame) and isinstance(var, tk.StringVar) and isinstance(color, str)):
        raise TypeError("Argument incorrect")

    # Create the label
    to_show = tk.Label(win, 
                        textvariable=var,
                        bg = color,
                        bd=5,
                        font=("Times New Roman", 24, "bold"),
                        fg="#FFFFFF",
                        padx=15,
                        pady=15,
                        justify=tk.CENTER,
                        relief=tk.RAISED
                    )
    return to_show

def atlabel(win: tk.Frame, var: tk.StringVar):
    """Function that creates a title label, 
    ensuring only Frame and StringVar are used."""
    
    # Ensure correct argument types
    if not isinstance(win, tk.Frame):
        raise TypeError("Argument must be a Frame instance, Error 2")
    
    if not isinstance(var, tk.StringVar):
        raise TypeError("Argument must be a StringVar, Error 2")

    # Create the label
    to_show = tk.Label(win, 
                        textvariable=var,
                        bg="#000000",
                        height = 1, # in characters, not pixels
                        width=3, # in characters, not pixels
                        bd=3,
                        font=("Times New Roman", 12, "bold"),
                        fg="#FFFFFF",
                        padx = 5,
                        pady = 5,
                        justify=tk.CENTER,
                        relief=tk.SOLID
                    )
    return to_show

def create_atlabels(root, text_array):
    """
    Creates a list of Tkinter Label widgets using StringVar.

    :param root: The parent Tkinter widget (usually a Tk() or Frame instance).
    :param text_array: List of strings to be displayed in the labels.
    :return: List of tuples (StringVar, Label).
    """
    labels = []
    for text in text_array:
        var = tk.StringVar(value=text)  # Create a StringVar with the text
        label = atlabel(root, var)  # Bind the StringVar to the Label
        labels.append((var, label))  # Store both in a tuple

    return labels  # Returns a list of (StringVar, Label) pairs

def create_atvalues(root, int_array):
    """
    Creates a list of Tkinter Button widgets where each prints a unique index (0-5).

    :param root: The parent Tkinter widget (usually a Tk() or Frame instance).
    :param int_array: List of ints to be displayed in the buttons.
    :return: List of tuples (IntVar, Label).
    
    Modified with the help of chatGPT
    """
    buttons = []
    for index, num in enumerate(int_array):  # Use enumerate to track index
        var = tk.IntVar(value=num)  # Create a IntVar with the text
        # Create a Button with a lambda to pass `num` correctly
        button = tk.Button(root, 
                            textvariable=var,
                            # Pass the index (0-5) and the value
                            command=lambda i=index, n_i = num: atribute_click(i, n_i),  
                            bg="#FFFFFF",
                            height=1,  # in characters, not pixels
                            width=2,
                            bd=3,
                            font=("Times New Roman", 18, "bold"),
                            cursor="hand2",
                            fg="#000000",
                            padx=5,
                            pady=5,
                            justify=tk.CENTER,
                            relief=tk.SOLID
                        )  
        buttons.append((var, button))  # Store both in a tuple

    return buttons  # Returns a list of (IntVar, Label) pairs

def create_modvalues(root, int_array):
    """
    Creates a list of Tkinter Label widgets using IntVar.

    :param root: The parent Tkinter widget (usually a Tk() or Frame instance).
    :param int_array: List of ints to be displayed in the labels.
    :return: List of tuples (IntVar, Label).
    """
    labels = []
    for num in int_array:
        numstring = str(num) # turn the number into a string
        if num > 0:
            numstring = "+" + numstring # add a + to positive numbers
        var = tk.StringVar(value=numstring)  # Create a StringVar with the integer
        label = tk.Label(root, textvariable = var,
                         bg="#000000",
                         height = 1, # in characters, not pixels
                         width=3, # in characters, not pixels
                         bd=3,
                         font=("Times New Roman", 10, "bold"),
                         fg="#FFFFFF",
                         padx = 5,
                         justify=tk.CENTER,
                         relief=tk.SOLID)  # Bind the StringVar to the Label
        labels.append((var, label))  # Store both in a tuple

    return labels  # Returns a list of (StringVar, Label) pairs

def health_labels(root : tk.Frame, cur_health: tk.IntVar, max_health: tk.IntVar, color: str):
    """
    A Function to create the Health Labels for the GUI.
    Parameters:
        root (tk.Frame): The root frame we are placing the label in.
        cur_health (tk.IntVar): An IntVar object contianing the current health.
        mas_health (tk.IntVar): An IntVar Object contianing the max health.
        color (str): The background color of the frame.
    Returns:
        labels (Tuple[tk.Label]): a tuple containing the health labels.
    """
    labels = []
    # Current Health Label
    label_cur = tk.Label(root, 
                         textvariable = cur_health,
                         height=1, # in characters, not pixels
                         width=2,
                         font=("Times New Roman", 18, "bold"),
                         **LAB_OPTIONS_ONE)
    labels.append((cur_health, label_cur)) 
    # We also need a divider label
    div_label = tk.Label(root, 
                         text = " / ",
                         bg=color,
                         height=1,  # in characters, not pixels
                         width=1,
                         font=("Times New Roman", 36, "bold"),
                         fg="#FFFFFF",
                         justify=tk.CENTER)
    labels.append((" / ",div_label))
    # Stores both the var and the label in a tupple ^
    # And Finaly, the total health label
    label_max = tk.Label(root,
                         textvariable = max_health,
                         height=1, # in characters, not pixels
                         width=2,
                         font=("Times New Roman", 18, "bold"),
                         **LAB_OPTIONS_ONE)
    labels.append((max_health, label_max)) 
    return labels

def temphealthindicator(root: tk.Frame, in_int: tk.IntVar):
    """
    A function to create the temp health label.
    Parameters:
        root (tk.Frame): The frame we are placing the widget in.
        in_int (tk.IntVar): An IntVar contianing the temp health value.
    Return
        label_temp (tk.Label): The label widget.
    """
    label_temp = tk.Label(root,
                     textvariable = in_int,
                     bg="#FFFFFF",
                     height=1, # in characters, not pixels
                     width=2,
                     bd=3,
                     font=("Times New Roman", 18, "bold"),
                     fg="#275D38",
                     padx=5,
                     pady=5,
                     justify=tk.CENTER,
                     relief=tk.SOLID)
    return label_temp

def longlabel(win: tk.Frame, var: tk.StringVar):
    """
    Function that creates a general label, ensuring only Frame and StringVar are used.
    Parameter:
        win (tk.Frame): The root frame.
        var (tk.StringVar): StringVar containing the text.
    Raises:
        TypeError: Incorrect Arguments
    Returns:
        to_show (tk.Label): The label widget.
    """
    
    # Ensure correct argument types
    if not isinstance(win, tk.Frame):
        raise TypeError("Argument must be a Frame instance, Error 1")
    
    if not isinstance(var, tk.StringVar):
        raise TypeError("Argument must be a StringVar, Error 1")

    # Create the label
    to_show = tk.Label(win, 
                        textvariable=var,
                        bg="#FFFFFF",
                        bd=5,
                        font=("Times New Roman", 12, "bold"),
                        fg="#202020",
                        padx=15,
                        pady=5,
                        justify=tk.CENTER,
                        relief=tk.SOLID
                    )
    return to_show
    
def damagebutton(win: tk.Frame, var: tk.StringVar):
    """
    Parameters
    ----------
    win : tk.Frame
        DESCRIPTION.
    var : tk.StringVar
        DESCRIPTION.

    Raises
    ------
    TypeError
        DESCRIPTION.

    Returns
    -------
    to_show : TYPE
        DESCRIPTION.

    """
    # Ensure correct argument types
    if not isinstance(win, tk.Frame):
        raise TypeError("Argument must be a Frame instance, Error 10A")
    
    if not isinstance(var, tk.StringVar):
        raise TypeError("Argument must be a StringVar, Error 10B")
        
    # Create the buttons
    to_show = tk.Button(win,
                        textvariable=var,
                        command = dam_click,
                        width = 8, # in characters
                        font=("Times New Roman", 10, "bold"),
                        bg = "#CCCCCC",
                        cursor="hand2")
    return to_show

def tempbutton(win: tk.Frame, var: tk.StringVar):
    """
    A function to create the button that adds temporary health points
    
    Parameters
    ----------
    win : tk.Frame
        The frame the button is being placed in.
    var : tk.StringVar
        The text we wish to display on the button.

    Raises
    ------
    TypeError
        An error for entering the wrong class of input.

    Returns
    -------
    to_show : tk.Button
        the tk.Button object, ready to place.

    """
    # Ensure correct argument types
    if not isinstance(win, tk.Frame):
        raise TypeError("Argument must be a Frame instance, Error 10A")
    
    if not isinstance(var, tk.StringVar):
        raise TypeError("Argument must be a StringVar, Error 10B")
        
    # Create the buttons
    to_show = tk.Button(win,
                        textvariable=var,
                        command = temp_click,
                        width = 8, # in characters
                        font=("Times New Roman", 10, "bold"),
                        bg = "#CCCCCC",
                        cursor="hand2",
                        wraplength= 75) # tells the text to wrap if it gets too long
    return to_show

def healbutton(win: tk.Frame, var: tk.StringVar):
    """
    Parameters
    ----------
    win : tk.Frame
        DESCRIPTION.
    var : tk.StringVar
        DESCRIPTION.

    Raises
    ------
    TypeError
        DESCRIPTION.

    Returns
    -------
    to_show : tk.Button
        The Tkinter object for a healing button.
    """
    # Ensure correct argument types
    if not isinstance(win, tk.Frame):
        raise TypeError("Argument must be a Frame instance, Error 11A")
    
    if not isinstance(var, tk.StringVar):
        raise TypeError("Argument must be a StringVar, Error 11B")
        
    # Create the buttons
    to_show = tk.Button(win,
                        textvariable=var,
                        command = hea_click,
                        width = 8,  # in characters
                        font=("Times New Roman", 10, "bold"),
                        bg = "#CCCCCC",
                        cursor="hand2")
    return to_show

# Function 13
def weaponbutton(root: tk.Frame, vars: list[tuple]):
    """
    A function to create the weapon button array.
    Parameters:
        root (tk.Frame): the frame the button is placed in.
        vars (list[tuple]): a list of tuples, in the form of (StringVar, int, bool)
            where int is the equipment id of the weapon, and the bool is the weapons
            in_light bool.
    Raises:
        TypeError: Error for incorect input.
    Returns:
        weapons (list[tk.Label]): an array of Tk.Weapon objects.
    """
    #check that we have the correct window
    if not isinstance(root, tk.Frame):
        raise TypeError("Argument must be a Frame instance, Error weaponbuttonA")
        
    weapons: list[tk.Label] = []
    for w_SV, w_id, w_light in vars:
        if not (isinstance(w_SV, tk.StringVar) and isinstance(w_id, int) and isinstance(w_light, bool)):
            raise TypeError("Incorrect Argument")
        # if the weapon is light, we modify the StringVar
        if w_light in weapons_light:
            new_str = w_SV.get() + " (l)" # Add an (l) to indicate a light weapon
            w_SV.set(new_str) # set this new string to be the var StringVar
        
        # We pass the weapon's id number into the weapon_click function.
        weapon = tk.Button(root,
                          textvariable=w_SV,
                          command = lambda t=w_id: weapon_click(t),
                          bg = "#CCCCCC",
                          height=1,  # in characters, not pixels
                          width=15,
                          bd=3,
                          cursor="hand2",
                          font=("Times New Roman", 12, "italic"),
                          fg = "#202020",
                          justify=tk.CENTER,
                          relief=tk.RAISED
                          )
        weapons.append((w_SV,weapon))
    return weapons

def equipcheck(root: tk.Frame, incolor: str = "#FFFFFF", fontcolor: str = "#000000"):
    """
    A function that creates a background-variable checkbox and returns
    the user's choice.

    Parameters
    ----------
    root : tk.Frame
        The base frame the widget is being placed in.
    incolor : str, optional
        The desired background color for the widget. The default is "#FFFFFF".
    fontcolor: str, optional
        The desired text color for the widget.  The default is "#000000".

    Raises
    ------
    TypeError
        Error for incorrect input.

    Returns
    -------
    use : tk.BooleanVar
        The variable linked to the checkbox, allowing access to its state.
    outcheck : tk.Checkbutton
        The checkbutton widget itself.
    """
    if not isinstance(root, tk.Frame):
        raise TypeError("Argument must be a Frame instance, Error equipcheckA")
    
    if not isinstance(incolor, str):
        raise TypeError("Argument must be a string object, Error equipcheckB")
    
    if not isinstance(fontcolor, str):
        raise TypeError("Argument must be a string object, Error equipcheckC")
    
    use = tk.BooleanVar()
    use.set(False)  # Default value

    outcheck = tk.Checkbutton(root, 
                              text="Equip Shield?",
                              bg=incolor,
                              font=("Times New Roman", 12),
                              fg=fontcolor,
                              indicatoron=0,  # make it an indecator button
                              bd = 3,
                              cursor = "hand2",
                              variable=use)
    
    return (use, outcheck)  # Return the BooleanVar, not just its initial value

    
# Next Function
def armordrop(root: tk.Frame, vars: list[str]):
    """
    A function to create the armor dropdown widget.
    Parameters
    ----------
    root : tk.Frame
        The root frame.
    vars : list[str]
        A list of equipment strings.

    Raises
    ------
    TypeError
        Error for incorrect entry.

    Returns
    -------
    selected_option : tk.StringVar
        The StringVar that holds the current armor.
    dropdown : tk.OptionMenu
        the dropdown widget itself.

    """
    # check that we have the correct window
    if not isinstance(root, tk.Frame):
        raise TypeError("Argument must be a Frame instance, Error armordropA")
    
    # check that we have the correct strings
    for index, var in enumerate(vars):
        # Check that we have a string
        if not isinstance(var, str):
            raise TypeError("Argument must be a string instance, Error armordropB")
        
    # We need to add the none option.
    vars.insert(0, "no armor")
    
    # Initialize Tkinter string variable
    # able to store any string value
    selected_option = tk.StringVar()
    selected_option.set(vars[0]) # Set the selected_option to the first outfit
    
    # Function to update the label when the menu selection changes
    #def update_label(*args):
        #print(f"You have selected {selected_option.get()}")

    # Create an OptionMenu (Dropdown Menu)
    dropdown = tk.OptionMenu(root, selected_option, *vars)

    # Bind the StringVar to automatically update when the menu choice changes
    #selected_option.trace_add("write", update_label)
    
    # and return both the dropdown and the current variable
    return (selected_option, dropdown)

# Got some help from chatGPT
def armorlabel(win: tk.Frame, var: tk.StringVar, inbool: tk.BooleanVar):
    """
    Function that creates the Armor Class Label, 
    ensuring only Frame, StringVar, and BooleanVar are used, 
    and updates dynamically.
    Parameters:
        win (tk.Frame): The base frame the dynamic label is to be placed in.
        var (tk.IntVar): The StringVar that holds the current armor name.  As we
            are dealing with direct user input, we use strings and not integers.
        inbool (tk.BooleanVar): The BooleanVar describing if the character is using a shield.
    Raises
        TypeError: When the incorrect type of information is entered.
    Returns:
        to_show (tk.Label): A Label object displaying the armor class.
    """
    
    # Ensure correct argument types
    if not (isinstance(win, tk.Frame) and isinstance(var, tk.StringVar) and isinstance(inbool, tk.BooleanVar)):
        sd.display_type_error("All arguments must be of the correct type.")

    # Create an IntVar to store the armor value
    armor_num = tk.IntVar()

    # Function to update armor_num when var changes
    def update_armor(*args):
        # Update the armor value based on changes to the armor
        # and shield.
        armor_num.set(sd.find_armor(var.get(), inbool.get())) 
        
    # Bind the update function to var's changes
    var.trace_add("write", update_armor)
    # and to inbool's changes as well
    inbool.trace_add("write", update_armor)

    # Initialize the value
    update_armor()

    # Create the label
    to_show = tk.Label(win, 
                       textvariable=armor_num,
                       font=("Times New Roman", 18, "bold"),
                       **LAB_OPTIONS_ONE)
    
    return to_show

def skillbutton(root: tk.Frame, vars: list, color: str):
    """
    A function to create a tkinter skill button.    

    Parameters
    ----------
    root : tk.Frame
        The frame in which we want to create this button.
    vars : list
        a list of StringVar objects to place on the button.
    color: str
        The background color.
    Raises:
        TypeError: Incorrect input objects.

    Returns:
        skills: a list of buttons to be placed by graphical_sidekick.py.

    """
    #check that we have the correct window
    if not (isinstance(root, tk.Frame) and isinstance(color, str)):
        raise TypeError("Incorrect input, Error skillbuttonA")
    
    skills = []
    for var in vars:
        # Ensure that we have a StringVar object
        if not isinstance(var, tk.IntVar):
            raise TypeError("Argument must be a IntVar class, Error skillbuttonB")

        # TEST AREA
        id_sk = var.get() # get the int from the IntVar

        skillname, skillbonus = sd.return_skill_name(id_sk)
        if skillbonus < 0:
            text = skillname + " (" + str(skillbonus) + ")" # for negative modifers
        else:
            text = skillname + " (+" + str(skillbonus) + ")"
        # we need to retrive the skill to use as a var
        but_txt = tk.StringVar(value = text)

        #and create the array of buttons
        skill = tk.Button(root,
                          textvariable=but_txt,
                          command = lambda t=id_sk: sd.skill_roll(t),
                          bg = "#FFFFFF",
                          height = 1, # In charachters
                          width = 16, # In charachters
                          cursor = "hand2",
                          font=("Times New Roman", 12, "italic"),
                          fg=color,
                          justify=tk.CENTER,
                          relief=tk.RAISED
                          )
        skills.append((var, skill))
    return skills

def cond_effects(root: tk.Frame, st_in: tk.StringVar):
    """
    Parameters
    ----------
    root : tk.Frame
        The root frame the objects are placed in.
    st_in : tk.StringVar
        the input StringVar.

    Raises
    ------
    TypeError
        When an incorrect object is entered.

    Returns
    -------
    effects : list
        an array of Tk Labels.

    """
    #check that we have the correct window
    if not isinstance(root, tk.Frame):
        raise TypeError("Argument must be a Frame instance, Error cond_effectsA")
    
    if not isinstance(st_in, tk.StringVar):
        raise TypeError("Argument must be a StringVar instance, Error cond_effectsB")
    
    # and create the icons
    con_ic = tk.Message(root,
                      textvariable = st_in,
                      bg = "#FFFFFF",
                      width = 200)
    
    return con_ic

def conbutton(root: tk.Frame, color: str):
    """
    Function to create tkinter windows for the tkinter window.
    Parameters:
        root (tk.Frame): The root frame we are placing the widget in.
        color (str): The hex code of the color we we want the text to be.
    Raises:
        TypeError: Incorrect Argument.
    Returns:
        buttons (list[tk.Button]): A list of Button widgets.
    """
    #check that we have the correct window
    if not (isinstance(root, tk.Frame) and isinstance(color, str)):
        raise TypeError("Incorrect input")
       
    buttons = []
    #and create the array of buttons
    buttona = tk.Button(root,
                        text = "Add Condition",
                        command = lambda: sd.add_cond(),
                        bg = "#FFFFFF",
                        height = 1,
                        width = 16,
                        cursor = "hand2",
                        font=("Times New Roman", 12, "bold"),
                        fg=color,
                        justify=tk.CENTER,
                        relief=tk.RAISED)
    buttonb = tk.Button(root,
                        text = "Remove Condition",
                        command = lambda: sd.remove_cond(),
                        bg = "#FFFFFF",
                        height = 1,
                        width = 16,
                        cursor = "hand2",
                        font=("Times New Roman", 12, "bold"),
                        fg=color,
                        justify=tk.CENTER,
                        relief=tk.RAISED)
    buttons.append(buttona)
    buttons.append(buttonb)
    
    return buttons # as a tupple

def add_eq_window(color: str):
    """
    A function to open the equipment modificaiton pane.
    Parameters:
        color (str): The character's primary color, expressed as a hex code.
    Raises:
        KeyError: When the entered equipment is not in the master dictionary.
    """
    # retrive equpment as a dictionary
    eq_dict = sd.retrive_equipment_master()

    def commit(in_stv: tk.StringVar):
        """
        A fucnction to commmit the equipment to the inventory
        Parameters:
            in_stv (tk.StringVar): the StringVar object taken from the combobox.
        Raises:
            KeyError: Equipment entered is not in the master database.
        """
        in_str = in_stv.get() # get the string
        try: # Attempt to retrive the id from the dict.
            print(f"Added {in_str}")
            in_id = eq_dict[in_str]
            in_equipment = sd.retrive_single_equip(in_id)
            sd.add_equipment(in_equipment, 1)
            eq_win.destroy() # close the window.
        except KeyError:
            fss.error_box("Equipment not defined? Did you want to create a custom object?")

    eq_win = tk.Tk() # Create the Tk window
    eq_win.title("Add Equipment")

    # Window Construction
    user_lab = tk.Label(eq_win, text = "Choose equipment to add:", font = ("Times New Roman", 12), height = 1, # In charachters
                        justify=tk.CENTER)
    # then create the menu
    choice = tk.StringVar()
    conchosen = ttk.Combobox(eq_win, width = 20, textvariable = choice)
    conchosen['values'] = list(eq_dict.keys()) # Retrieve the keys of the dictionary as a list
    # And the commit button
    com_but = tk.Button(eq_win, text = "Commit equipment to inventory", font = ("Times New Roman", 12),
                        command = lambda c = choice: commit(c),
                        height = 1, cursor = "hand2", bg = color, fg = "#FFFFFF", justify=tk.CENTER,relief=tk.RAISED)
    
    # And populate the window
    user_lab.pack(padx = 5, pady = 5)
    conchosen.pack(padx = 5, pady = 5)
    com_but.pack(padx = 5, pady = 5)
    eq_win.mainloop() # run the window

    #### TESTING AREA ################################################################################################



