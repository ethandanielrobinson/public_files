# TO DO
# The way this works is that the classes are defined here.  They are not filled with information
# from the database; that happens in the sidekick_data.py script.

import tkinter as tk
from tkinter import ttk
import time
import numpy as np
import os
from typing import List, Tuple, Dict
import math

# Make sure we are in the files directory
# script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the current working directory to the script's directory
# os.chdir(script_dir)
# Get the directory of the current script
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
# Set it as the working directory
os.chdir(CUR_DIR)
# Set the seed to the current time
seed_value = int(time.time() * 1000)
rng = np.random.default_rng(seed_value)

# CONSTANT DEFINITION
BUTTON_OPTIONS_BLUE = {
                "bg": "#2850A3",
                "font": ("Times New Roman", 10, "bold"),
                "fg": "#FFFFFF",
                "cursor": "hand2"}
BUTTON_OPTIONS_RED = {
                "bg": "#CC0000",
                "font": ("Times New Roman", 10, "bold"),
                "fg": "#FFFFFF",
                "cursor": "hand2"}
# Label options normal
LABEL_OP_NOR = { 
                "font": ("Times New Roman", 10),
                "fg": "#000000"}
LABEL_OP_RED = { 
                "font": ("Times New Roman", 10),
                "fg": "#FF0000"}


#=========================================================================
# define a dict to help manage ability scores
ABILITY_DICT = {1: "STR", 2: "DEX", 3: "CON", 4: "INT", 5: "WIS", 6: "CHA"}
#=========================================================================
def xnor(in_a = None, in_b = None)->bool:
    """
    A function that returns an exclusive or (either both are true or both are false)
    Parameters:
        in_a: Our first input. The default is None.
        in_b: Our second input. The default is None.
    Returns:
        output (bool): True if both exist or neither exist, false if one does and the other doesn't
    """
    out_a = True if in_a else False # check if we have a input
    out_b = True if in_b else False # check if we have b input
    return True if out_a == out_b else False # only return True if out_a and out_b are the same

def list_xnor(in_list: list):
    """
    A function that checks a list of inputs and returns true if they are all true or all false,
    but returns false if some are true and some are false.
    Parameters:
        in_list (list): A list of variables, can be of mixed type
    Returns:
        OUT (bool): Is the list all of one type?
    """
    # we define a count for each true element in the list.  If the count equals the length of the list 
    # (meaning everything in the list is true) or 0 (meaning everything in the list is false), we return
    # True. If it is not one of those two numbers, we return False.
    count = 0
    # we check each element in the list
    for elem in in_list:
        if elem:
            count += 1
    if (count == len(in_list) or count == 0):
        return True
    else:
        return False

def remove_last_word(text: str):
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
        words.pop()
        return " ".join(words)
    return "" # Return empty string if the input string is empty or contains only spaces

def format_spell_text(in_str: str) -> str:
    """
    A function to format the raw text we get from the database into a more readable format.
    Parameters:
        in_str (str): The raw text that we want to format.
    Raises:
        TypeError: Argument other than string entered.
    Returns:
        out_str (str): The formatted string.
    """
    # check our input
    if not isinstance(in_str, str):
        raise TypeError("Argument other than string entered.")
    
    # Remove any line breaks that were added for database ease of maitanince
    temp_str = in_str.replace('\n', '').replace('\r', '')

    # format our input string, using the dollar sign for a line break
    # (since fantasy and sci-fi worlds generaly don't use USD).
    out_str = temp_str.replace("$", "\n")

    return out_str

def choose_char(vars: list):
    """
    A function to help us choose a character from a list
    
    Parameters
    ----------
    vars : list
        A list of charachter name strings.

    Raises
    ------
    ValueError
        Incorrect input (input is not a string).

    Returns
    -------
    output : string
        The selected character name as a string.

    """
    output = '' # The empty string
    
    # create window
    cha_win = tk.Tk()
    cha_win.title("Character Selector")
    cha_win.configure(bg = "#FCF5E5")
    
    # and a label
    cha_lab = tk.Label(cha_win, 
                       text = "Please Select a Character:",
                       font = ("Times New Roman", 16),
                       bg = "#FCF5E5")
    cha_lab.pack(padx = 15, pady = 5)
    
    # and define our string return function
    def returnstring(str_in):
        nonlocal output
        output = str_in
    
    # And a frame for the buttons
    but_fram = tk.Frame(cha_win, bg = "#FCF5E5")
    
    for var in vars:
        if not isinstance(var, str):
            raise TypeError("Argument must be a string, Error choose_char_A")
        
        # create and place the buttons
        button = tk.Button(but_fram, 
                           text = var, 
                           command = lambda v = var: [returnstring(v), cha_win.destroy()],
                           width = 15,
                           bg = "#0062B8",
                           font=("Times New Roman", 12, "bold"),
                           fg = "#FFFFFF",
                           cursor="hand2")
        button.pack(padx=5)
    
    but_fram.pack(padx = 5, pady = 5)
    
    cha_win.grab_set()  # Makes popup modal (forces user to interact with it first)
    cha_win.wait_window()  # Pauses execution until popup is closed
    
    return output

# A searching function
def find_in_first_entries(lst, num):
    """
    A function to search an inventory and return the first instance of an object by id. Non-User Function
    Parameters:
        lst: A list of tupples, usualy an inventory with both Equipment instance and then quantity
        num: The id of the object we are looking for.
    Returns:
        tuple: Is the Equipment in the inventory, the index of the Equipment (-1 if it's not there)
    """
    for index, (object, _,) in enumerate(lst):
        if object.id == num: # checks if the id is the same as the input
            return True, index  # Return True and the index where it was found
    return False, -1  # Return False and -1 if not found

# we create a general purpose error message box
def error_box(error_string: str):
    """
    A function to create a window to display an error message

    Parameters
    ----------
    error_string : str
        The message to display.

    Returns
    -------
    None.

    """
    # create errorbox window
    er_win = tk.Toplevel()
    er_win.title("Error")
    
    # and create a label
    error_lab = tk.Label(er_win, 
                         text = error_string, 
                         fg = "#CC0000",
                         font=("Times New Roman", 10, "bold"),
                         wraplength= 100)
    error_lab.pack(padx = 5, pady = 5)
    
    # plus an exit button
    error_but = tk.Button(er_win, text = "Exit", command = er_win.destroy, width = 6, **BUTTON_OPTIONS_RED)
    error_but.pack(padx = 5, pady = 5)
    
    er_win.grab_set()  # Makes popup modal (forces user to interact with it first)
    er_win.wait_window()  # Pauses execution until popup is closed
    
    # And return none
    return None

def create_info_box(title: str, to_display: str)->None:
    """
    A function to create a info-box to inform the user.
    Parameters:
        title (str): What we want the box to be titled.
        to_display (str): The string we want the box to say.
    Raises:
        TypeError: Incorrect input entered.
    """
    # check input
    if not (isinstance(title, str) and isinstance(to_display, str)):
        raise TypeError ("Incorrect input entered.")
    # create window
    pop = tk.Toplevel()
    pop.title(title)
    pop.geometry("300x100")

    in_lab = tk.Label(pop, text=to_display, **LABEL_OP_NOR)
    in_lab.pack(padx = 5, pady = 5)

    ex_but = tk.Button(pop, text = "Exit", command = pop.destroy, width = 6, **BUTTON_OPTIONS_RED)
    ex_but.pack(padx = 5, pady = 5)

    pop.grab_set()  # Makes popup modal (forces user to interact with it first)
    pop.wait_window()  # Pauses execution until popup is closed

def set_dimensions_pop(root, wind_width: int = 300):
    """
    A function to help set the dimensions of a popup window.

    Parameters:
        root: the Toplevel window we are setting the dimensions for.  Can be either a
            tk.Tk or tk.Toplevel
        wind_width (int, optional): The width we want the window to be. The default
            is 300 pixels.
    Raises:
        TypeError: When the root window is not of tk.Tk or tk.Toplevel type.
    """
    if not (isinstance(root, tk.Tk) or isinstance(root,tk.Toplevel)):
        error_box("The root window must be a tk window type!")
        raise TypeError("The root window must be a tk window type!")
    root.update_idletasks()  # Let Tkinter compute the default dimensions
    root.geometry(f"{wind_width}x{root.winfo_height()}")  # Set only width explicitly after a short delay

def add_to_list(base: list, current: list):
    """
    A function to add data to a list using a tkinter window, 
    """
    # Create the pop-up window
    pop = tk.Toplevel()
    pop.title("Add A Condition")
    pop.geometry('350x250')
    
    # Our output function
    output = current
    
    # Define the add_check button
    def add_check(in_strv: tk.StringVar):
        stringraw = in_strv.get()
        nonlocal output
        # ensure that the condition we are adding is not current
        if stringraw not in current:
            output.append(stringraw)
        else:
            error_box("Condition already current")
        return None
    
    # Label creation
    poplabel = tk.Label(pop,
                        text = "Select Condition :",
                        font = ("Times New Roman", 10))
    poplabel.pack(padx = 15, pady = 5)
    
    # then create the menu
    choice = tk.StringVar()
    conchosen = ttk.Combobox(pop, width = 20, textvariable = choice)
    conchosen['values'] = base
    conchosen.pack(pady = 5)
    
    # and the button to return the value of the menu
    but = tk.Button(pop,
                    text = "Confirm Choice",
                    command = lambda c = choice: [add_check(c), pop.destroy()],
                    font = ("Times New Roman", 10, "bold"),
                    width = 15,
                    bg = "#0062B8",
                    fg = "#FFFFFF",
                    cursor="hand2")
    but.pack()
    
    pop.grab_set()  # Makes popup modal (forces user to interact with it first)
    pop.wait_window()  # Pauses execution until popup is closed
    
    return output

def remove_to_list(current: list):
    
    # Create the pop-up window
    pop = tk.Toplevel()
    pop.title("Remove A Condition")
    pop.geometry('350x250')
    
    # Our output function
    output = current
    
    # Define the add_check button
    def sub_check(in_strv: tk.StringVar):
        stringraw = in_strv.get()
        nonlocal output
        output.remove(stringraw)
        return None
    
    # Label creation
    poplabel = tk.Label(pop,
                        text = "Select Condition :",
                        font = ("Times New Roman", 10))
    poplabel.pack(padx = 15, pady = 5)
    
    # then create the menu
    choice = tk.StringVar()
    conchosen = ttk.Combobox(pop, width = 20, textvariable = choice)
    conchosen['values'] = current
    conchosen.pack(pady = 5)
    
    # and the button to return the value of the menu
    but = tk.Button(pop,
                    text = "Confirm Choice",
                    command = lambda c = choice: [sub_check(c), pop.destroy()],
                    font = ("Times New Roman", 10),
                    width = 15,
                    bg = "#0062B8",
                    fg = "#FFFFFF",
                    cursor="hand2")
    but.pack()
    
    pop.grab_set()  # Makes popup modal (forces user to interact with it first)
    pop.wait_window()  # Pauses execution until popup is closed
    
    return output

def rolltwenty(advantage: int):
    """
    A function to simulate the rolling of a d20
    as part of a skill check

    Parameters
    ----------
    advantage : int
        the integer that determines whether we roll with advangtage,
        disadvantage, or not.  Greater than zero means advantage, 
        less than zero means disadvantage, zero means a normal roll.

    Returns
    -------
    value : int
        the value of the skill check without any modifiers.

    """
    # The advantage number works as thus.  if the number is greater than zero,
    # The system assumes the roll has advantage.  If the number is less than
    # zero, the system assume the roll has disadvantage
    if advantage < 0:
        val_array = rng.integers(1,20,2)
        #### TEST SPACE--------------------------------------------------------
        print(val_array)
        #----------------------------------------------------------------------
        value = min(val_array)
        print(f"The roll was {value} with disadvantage")
    elif advantage > 0:
        val_array = rng.integers(1,20,2)
        #### TEST SPACE--------------------------------------------------------
        print(val_array)
        #----------------------------------------------------------------------
        value = max(val_array)
        print(f"The roll was {value} with advantage")
    else:
        value = rng.integers(1,20)
        print(f"The roll was {value}")
    return value

def rolldamage(in_mod: int, die_max: int, die_amount: int):
    """
    A function to simulate the attack roll in an attack
    magical or otherwise.

    Parameters
    ----------
    in_mod : int
        The modifier applied to the attack.
    die_max : int
        The type of die, expressed in a maximum.  for instance,
        a d10 would be expressed as 10.
    die_amount : int
        How many individual dice do we want to roll.

    Returns
    -------
    damage : int
        The damage output expressed as an int.

    """
    dam_array = rng.integers(1, die_max, die_amount)
    damage = sum(dam_array)
    #### TEST SPACE -----------------------------------------------------------
    print(f"The raw damage was {damage} on {die_amount}d{die_max}")
    # -------------------------------------------------------------------------
    damage += in_mod
    return damage

class Equipment:
    def __init__(self, name: str, cost: float, weight: float, description: str, id: int):
        """
        Initializes the equipment class, which has several child classes

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
        id : int
            The unique identifier for the equipment.
            
        Raises
        ------
        ValueError
            If the input is not the correct type.   
        
        Returns
        -------
        None.
        """
        # and then define our class variables bassed on the input given
        self.name = name
        self.cost = float(cost)
        self.weight = float(weight)
        self.description = description
        self.id = id # initial id definition
        # We ensure that we get the correct type of data
        if not isinstance(self.name, str):
            raise ValueError("The name must be a string.")
        if not isinstance(self.cost, float):
            raise ValueError("The cost must be a float.")
        if not isinstance(self.weight, float):
            raise ValueError("The weight must be a float.")
        if not isinstance(self.description, str):
            raise ValueError("The description must be a string.")
        return None
    
class Weapon(Equipment):
    def __init__(self,
                 name: str, # the name of the weapon as a string
                 cost: float, # the cost of the weapon in gold pieces
                 weight: float, # the weight of the weapon in pounds
                 description: str, # a string describing the weapon
                 id: int, # the id from the master database
                 is_martial: bool, # whether the weapon is a martial weapon
                 damage_amount: int, # The number of damage dice rolled
                 damage_die: int, # the number of sides on the damage die
                 damage_type: str, # the type of damage the weapon deals
                 has_finesse: bool = False, # whether the weapon has the finesse property
                 is_two_handed: bool = False, # whether the weapon is two-handed
                 has_verstile: bool = False, # whether the weapon is versatile
                 damage_die_versatile: int = None, # the number of sides on the versatile damage die
                 has_range: bool = False, # whether the weapon has a range
                 normal_range: int = None, # the normal range of the weapon
                 max_range: int = None, # the maximum range of the weapon
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
        super().__init__(name, cost, weight, description, id)
        self.is_martial = is_martial
        self.damage_amount = damage_amount
        self.damage_die = damage_die 
        self.damage_type = damage_type
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


        # We then make sure to Enforce dependency: on versatilty------------------------------
        if self.has_verstile and self.damage_die_versatile is None:
            raise ValueError("A versatile weapon must have a versatile damage die!")      
        # And on ranged weapons---------------------------------------------------------------
        if (self.has_range or self.has_thrown) and (self.normal_range is None or self.max_range is None):
            raise ValueError("A ranged weapon must have both a maximum and normal range!")
        # Ensure that the weapon cannot be both heavy and light-------------------------------
        if self.is_heavy and self.is_light:
            raise ValueError("A weapon cannot be both heavy and light!")
        # Ensure that the weapon cannot have both range and finesse (how would that even work?)
        if self.has_range and self.has_finesse:
            raise ValueError("A weapon cannot have both range and the finesse property!")

        return None
    
    def ask_range(self):
        """
        A function to ask the user for the target's range
        Raises:
            ValueError: Input must be an integer.
        Returns:
            long_range (bool): Is the target at long range or not. None means the 
                target is out of range.
        """
        # initialize our variables.  ran is the target's range
        ran = None 
        
        #create a window asking for the targets range
        ranpop = tk.Toplevel()
        ranpop.title("Range Window")
        ranpop.geometry("300x200") # set the geometry to 300x200
        
        # We define what to do when the submit button is pressed
        def submit():
            try:
                nonlocal ran
                ran = int(ran_str.get())
                ranpop.destroy()
            except ValueError:
                error_label.config(text="Please enter a valid integer", fg="red")
        
        # Range Label ---- Asks for user input
        ran_lab_one = tk.Label(ranpop, text = "Enter distance to target in feet:")
        ran_lab_one.pack(padx = 5, pady = 5)
        
        # Initialize Entry Stringvar
        ran_str = tk.StringVar()
        # defining a function for the submit button that will get
        # what's in the entry box and print it to the correct string.
        
        # Now we create our entry box
        # Range Entry
        ran_entry = tk.Entry(ranpop, textvariable = ran_str, width = 10)
        ran_button = tk.Button(ranpop, 
                               text = "Submit", 
                               command = submit,
                               width = 8,
                               **BUTTON_OPTIONS_BLUE)
        # Create our error labe, even if its not visible
        error_label = tk.Label(ranpop, text="", fg="red")
        
        # and place these objects into our window
        ran_entry.pack(pady = 5)
        ran_button.pack(pady = 5)
        error_label.pack(pady = 5)
        
        ranpop.grab_set()  # Makes popup modal (forces user to interact with it first)
        ranpop.wait_window()  # Pauses execution until popup is closed
        
        # target is at normal range --------------------------------------------------
        if ran <= self.normal_range: 
            long_range = False
        # target is at long range ----------------------------------------------------
        elif self.normal_range < ran <= self.max_range: 
            long_range = True
        # target is out of range -----------------------------------------------------
        else: 
            long_range = None
            
        return long_range
    
    def attack_roll(self, is_range: bool, hands_free: int) -> Tuple[int, bool, bool]:
        """
        A fuction to simulate the attack roll using the global rolltwenty function.
        Parameters:
            is_range (bool): Is the attack a ranged attack or not.
            hands_free (int): How many free hands does the character have?
        Returns:
            result (Tuple[int, bool, bool]): The raw result of the attack roll with no modifier, 
                folloed by first if versatility is being used, and then finesse.
        """
        # Define our advantage_num
        result = None
        get_vers = None
        get_fin = None
        
        # Define a function on what to do on a button press
        def button_press(int_in: int):
            nonlocal result, get_vers, get_fin # bring in our non_local variables
            # Set the get_vers bool to the checkbox so we can effect
            # other class functions
            get_vers = use_vers.get()
            # Set the get_fin bool to the checkbox so we can effect the other
            # class function
            get_fin = use_fin.get()
            result = rolltwenty(int_in), get_vers, get_fin
            rollpop.destroy()
            
        # create a roll options screen
        rollpop = tk.Toplevel()
        rollpop.title("Roll Options")

        
        # Create a label to ask the user for input
        rol_lab = tk.Label (rollpop, text = "Are you attacking with Advantage or Disadvantage?")
        rol_lab.pack(padx = 5, pady = 5) # place the label in rollpop
        
        # add a button if the weapon has Finnesse --------------------------
        # initilize the bool to false in the base case
        use_fin = tk.BooleanVar()
        use_fin.set(False)
        # add a button if the weapon has versitality --------------------------
        # initilize the bool to false in the base case
        use_vers = tk.BooleanVar()
        use_vers.set(False)
        
        # If the weapon has finesse, we can create and place the box
        if self.has_finesse:
            # Create the Checkbox to decide if attacking with finnese
            fin_check = tk.Checkbutton(rollpop,
                                       text="Attack with finesse?",
                                       variable = use_fin)
            fin_check.pack(pady = 5)
        
        # if the weapon has versatility, we can create and place the box
        if self.has_verstile and (hands_free == 2) and not is_range: # can't use versatility at range
            # Create the Checkbutton to decide if using versatility (two hands)
            ver_check = tk.Checkbutton(rollpop, 
                                       text="Attack with two hands?", 
                                       variable=use_vers)
            ver_check.pack(pady=5)
        if is_range == None:
            button = tk.Button(rollpop,
                               text = "Attack with Disadvantage?",
                               command = lambda: button_press(-1),
                               width = 26,
                               **BUTTON_OPTIONS_BLUE)
            button.pack(padx = 5)
        else:
            # We create the three buttons using a for loop
            # over a tupple, as seen bellow
            for num, lab in [(0, "Normal"),(1, "Advantage"), (-1, "Disadvantage")]:
                button = tk.Button(rollpop,
                                text = lab,
                                command = lambda n = num: button_press(n),
                                width = 12,
                                **BUTTON_OPTIONS_BLUE)
                button.pack(padx = 5) # and place the button in the window

        # finaly we place the logo
        img_a = tk.PhotoImage(file = r"D:\dungeons_and_dragons\Custom_Programs\sidekick_files\images\illustrator_tokens\32w\blue_symbol_32_px.png")
        
        # setting image with the help of label
        imglabel = tk.Label(rollpop, 
                            image = img_a,
                            bd= 5,
                            relief=tk.SOLID)
        imglabel.pack(pady = 5)
        
        rollpop.grab_set()  # Makes popup modal (forces user to interact with it first)
        rollpop.wait_window()  # Pauses execution until popup is closed
        
        return result
    
    def damage_roll(self, mod_in: int, using_versatility: bool, critical: bool):
        """
        A function to simulate the damage in an weapon attack roll.

        Parameters
        ----------
        mod_in: int
            the modifier that we wish to apply to the damage bool.
        using_versatility : bool
            Are we attacking with versatility?
        critical : bool
            Was the attack a critical hit?

        Returns
        -------
        damage : int
            The damage of the whole role as an integer.

        """
        #### MAY NEED TO CHANGE THIS LATER
        die_type = self.damage_die_versatile if using_versatility else self.damage_die
        attack_dice = self.damage_amount

        # make sure to check for criticality
        attack_dice *= 2 if critical else 1
        
        # generate the damage value based on the attack
        dam_val = rolldamage(mod_in, die_type, attack_dice)
            
        # And generate the damage window
        dam_pop = tk.Toplevel()
        dam_pop.title("Damage Window")
        
        # The user info label
        dam_str = f"The damage rolled was {str(dam_val)} {self.damage_type} damage!"
        dam_lab = tk.Label(dam_pop, text = dam_str)
        dam_lab.pack(padx = 5, pady = 5)
        
        # And the exit button
        exit_but = tk.Button(dam_pop, 
                             text = "Exit",
                             command = dam_pop.destroy,
                             width = 6,
                             **BUTTON_OPTIONS_RED)
        exit_but.pack(pady = 5)
        
        dam_pop.grab_set()  # Makes popup modal (forces user to interact with it first)
        dam_pop.wait_window()  # Pauses execution until popup is closed
        
        return dam_val
        
    def ask_throw(self):
        """
        A function adding a throw option to weapons like spears or daggers
        that can be thrown as a ranged attack.

        Returns
        -------
        in_bool : bool
            The user input on whether to throw the weapon or not.

        """
        # define our output
        out_bool = None
        # we define what to do when the button is pressed
        def button_press_th(in_bool: bool):
            nonlocal out_bool
            thrpop.destroy()
            out_bool = in_bool
        
        # First we create a window asking for the attack mode.
        thrpop = tk.Toplevel()
        thrpop.title("Attack Mode Window")
        thrpop.geometry("300x200")
        
        # And a label asking for user input
        thrlab = tk.Label(thrpop, text = "How would you like to attack?")
        thrlab.pack(padx = 5, pady  =5)
        
        # and finaly two attack buttons, using a for loop
        for mode, textin in [(False,"Melee"), (True,"Thrown")]:
            thrbut = tk.Button(thrpop, 
                               text = textin,
                               command=lambda m=mode: button_press_th(m),
                               width = 12,
                               **BUTTON_OPTIONS_BLUE)
            thrbut.pack(padx = 5) # and place the button
        
        thrpop.grab_set()  # Makes popup modal (forces user to interact with it first)
        thrpop.wait_window()  # Pauses execution until popup is closed
        
        return out_bool  
    
    def attack(self, free_hands: int, prof_in: int, str_score: int, dex_score:int = 10):
        """
        The attack function itself, which controls the usages of the
        other functions.
        Parameters:
            free_hands (int): How many hands free does the character have?
            prof_in (int): The character's proficiency bonus.
            str_score (int): The character's strength score.
            dex_score (int, optional): The character's dexterity score. The default is 10.
        """
        # Define our damage and roll variables
        damage = 0 # define damage as zero to start, we can change this
        roll = None
        str_mod = (str_score-10)//2 # calculate the strength modifier
        dex_mod = (dex_score-10)//2 # calculate the dexterity modifier

        # First we need to check if we have enough hands free.
        if self.is_two_handed and (free_hands < 2) :
            error_box("You don't have the hands free to attack with that!")
            return 1
        # Then we need to check if the weapon is thrown or not
        range_attack = False # is the attack being made at range.
        # At default we want it to be false
        
        if self.has_range:
            range_attack = True # if the weapon is ranged, the attack is automatically ranged
        elif self.has_thrown: # here we need to ask the user if the attack is ranged or not.
            range_attack = self.ask_throw()
        
        # check to see if we are at long range for ranged weapons
        if range_attack:
            range_bool = self.ask_range() # True is long range, false is normal range
            # we quit the attack if the target is out of range
            if range_bool == None:
                error_box("Target is out of range, no attack.")
                return 2
            elif range_bool:
                roll = self.attack_roll(None, free_hands)
            else: # an attack in range
                # roll our attack dice, which returns a tuple
                roll = self.attack_roll(True, free_hands)
        else: # A meele attack
            # roll our attack dice, wich returns a tupple
            roll = self.attack_roll(False, free_hands)
        
        #### Total Roll
        # define total_roll as as seperate so we can check for crits
        # set the modifier to be either dex or str.  We use the first element
        # of the roll tupple, wich is the roll value itself.
        # TEST SPACE--------------------------------------------------------
        if roll[2] or self.has_range:
            mod = dex_mod # Define the damage modifier to be the dex mod
            a_mod = prof_in + mod # Attack modifiers is dex + prof
            print(f'The attack modifier is +{a_mod}')
            total_roll = roll[0] + a_mod
        else:
            mod = str_mod # Define the damage modifier to be the str mod
            a_mod = prof_in + mod # attack modifier is str + mod
            print(f'The attack modifier is +{a_mod}')
            total_roll = roll[0] + a_mod
        # And make sure to check for criticality (True if the roll = 20,
        # false otherwise)
        crit = roll[0] == 20
        
        # At which point we open the hit window
        hit_pop = tk.Toplevel()
        hit_pop.title("Attack Window")
        
        # And create a label informing the user of the attack roll
        # attack_lab stands for attack label
        attack_text = "Your attack roll was " + str(total_roll) + " !"
        attack_lab = tk.Label(hit_pop, text = attack_text)
        attack_lab.pack(padx = 5, pady = 5)
        
        # Plus a label asking the user for input (a hit label)
        hit_lab = tk.Label(hit_pop, text = "Did the attack succeed?")
        hit_lab.pack(padx = 5, pady = 5)
        
        # Before we provide some buttons for them to answer
        def on_yes_button_click():
            nonlocal damage
            hit_pop.destroy()
            # and enter our damage data
            using_fin = roll[2]
            using_ver = roll[1]
            damage = self.damage_roll(mod, using_ver, crit)

        yes_but = tk.Button(hit_pop, 
                            text = "Yes", 
                            command = on_yes_button_click,
                            width = 6,
                            **BUTTON_OPTIONS_BLUE)
        no_but = tk.Button(hit_pop,
                           text = "No",
                           command = hit_pop.destroy,
                           width = 6,
                           **BUTTON_OPTIONS_RED)
        yes_but.pack()
        no_but.pack()
        
        hit_pop.grab_set()  # Makes popup modal (forces user to interact with it first)
        hit_pop.wait_window()  # Pauses execution until popup is closed
        
        #### TEST SPACE--------------------------------------------------------
        print(f"The result of the roll was {total_roll} with {damage} {self.damage_type} damage.")
        #----------------------------------------------------------------------
        
        return None

class Armor(Equipment):
    def __init__(self,
                 name: str, # the name of the weapon as a string
                 cost: float, # the cost of the weapon in gold pieces
                 weight: float, # the weight of the weapon in pounds
                 description: str, # a string describing the weapon
                 id: int, # the id integer from the master database
                 armor_class: int, # the armor classs bonus of the armor
                 armor_type: int, # whether the armor is 1: light, 2: medium, or 3: heavy
                 stealth_friendly: bool, # whether the armor is stealth freindly
                 required_str: int): # the strength required to don the armor
        """
        Initializes a armor class object
        """
        # Call the parent constructor using super()
        super().__init__(name, cost, weight, description, id)
        self.armor_class = armor_class
        self.armor_type = armor_type
        self.stealth_friendly = stealth_friendly
        self.required_str = required_str
        return None
    
    def get_ac(self, dex_scr: int)->int:
        """
        A function to return the armor class of an equiped suit of armor,
        taking into acount the dexterity modifier of the charachter in
        question

        Parameters
        ----------
        dex_scr: int
            The characters dexterity score.
        
        Raises
        ------
        ValueError
            Raised when something other than string is entered in dex_scr
        TypeError
            Raised when an incorrect armor type is entered (an int above 2)

        Returns
        -------
        ac: int
            The characters complete armor class
        """
        if not isinstance(dex_scr, int):
            raise ValueError("Dexterity score must be an integer.")
        
        ac = None # initialize ac
        dex_mod = (dex_scr - 10) // 2
        # and calculate the armor class
        if self.armor_type == 1: # Light Armor
            ac = self.armor_class + dex_mod # ac is armor_class + dex_mod
        elif self.armor_type == 2: # Medium Armor
            d_bonus = 2 if dex_mod > 2 else dex_mod # set d_bonus to be no more than 2
            ac = self.armor_class + d_bonus # we use d_bonus here
        elif self.armor_class == 3: # Heavy Armor
            ac = self.armor_class
        else: # if something goes wrong
            raise TypeError("Incorrect armor type entered.")
        return ac
    
    def is_heavy(self)->bool:
        """
        Returns if the armor is of the heavy type.

        Returns
        -------
        bool
            is the armor heavy or not (is self.armor_type 3)!
        """
        if self.armor_type == 3:
            return True
        else:
            return False

class Ammunition(Equipment):
    def __init__(self, name: str, cost: float, weight: float, description: str, id: int):
        """
        Intializes an Ammunition type object.
        Parameters:
            name (str): the name of the ammo as a string.
            cost (float): the cost of the ammo in gold pieces.
            weight (float): the weight of the ammo in pounds.
            description (str): a string describing the ammo.
            id (int): the id integer from the master database.
        Returns:
            Ammunition: an Ammunition type object
        """
        # Call the parent constructor using super()
        super().__init__(name, cost, weight, description, id)

class Clothing(Equipment):
    def __init__(self, name: str, cost: float, weight: float, description: str, id: int,
                    location: int, exclusive: bool):
        """
        Intializes an Clothing type object.
        Parameters:
            name (str): the name of the article as a string.
            cost (float): the cost of the article in gold pieces.
            weight (float): the weight of the article in pounds.
            description (str): a string describing the article.
            id (int): the id integer from the master database.
            location (int): Where on the body is this article of clothing worn? See
                guide for details.
            exclusive (bool): Can any other article of clothing be worn in the same spot?
        Returns:
            Clothing: a Clothing type object.
        """
        # Call the parent constructor using super()
        super().__init__(name, cost, weight, description, id)
        self.location = location
        self.exclusive = exclusive
        # MAY ADD A WORN BOOL IN THE FUTURE

class Container(Equipment):
    def __init__(self, 
                 name: str, 
                 cost: float, 
                 weight: float, 
                 description: str, 
                 id: int,
                 wet_volume: float = None, 
                 dry_volume: float = None, 
                 capacity: float = None,
                 ammo_type_a: int = None, 
                 amount_a: int = None, 
                 ammo_type_b: int = None, 
                 amount_b: int = None):
        """
        Intializes an Container type object.
        Parameters:
            name (str): The name of the article as a string.
            cost (float): The cost of the article in gold pieces.
            weight (float): The weight of the article in pounds.
            description (str): A string describing the article.
            id (int): The id integer from the master database.
            liquid_volume (float, optional): The total liquid volume of the container, expressed
                in ounces as a float. The default is None.
            solid_volume (float, optional): The total solid volume of the container, expressed
                in cubic feet as a float. The default is None. 
            capacity (float, optional): The total weight capacity of the container, expressed
                in pounds as a float. The default is None.
            ammo_type_a (int, optional): If the container can be used as a magazine, what type
                of amunition can it hold, expressed as that amunitions id number. The default
                is None.
            amount_a (int, optional): If the container can be used as magazine, how much ammo
                can it hold? The default is None.
            ammo_type_b: If the container is a magazine, can it hold another type of ammunition?
                Expressed as that ammo's id number. The default is None.
            amount_b (int, optional): How much of this secondary ammunition can the container hold?
                The default is None.
            
        Returns:
            Container: an Container type object.
        """
        # Call the parent constructor using super()
        super().__init__(name, cost, weight, description, id)
        self.wet_volume = wet_volume
        self.dry_volume = dry_volume
        self.capacity = capacity
        self.ammo_type_a = ammo_type_a
        self.amount_a = amount_a
        self.ammo_type_b = ammo_type_b
        self.amount_b = amount_b
        self.inventory = [] # and initilize a list which will become the items inventory
        # The self.inventory list will contain Equipment type objects.
        self.inv_weight = 0.0 # the total weight of the containers inventory.
        # whether the cointainer is currently carying dry or wet goods.  True means dry,
        # False means wet.
        self.config = True
        self.file = None # the table name of the contaienrs table in the database
        self.file_id = None # the id inside the "character_containers" table in the character database
        # We also need to ensure some dependecies, which is difficult since python doesnt
        if not xnor(self.ammo_type_a, self.amount_a): # will return true if both exists
            raise ValueError("A magazine must have both a ammunition type and a capacity")
        if not xnor(self.ammo_type_b, self.amount_b): # will return true if both exists
            raise ValueError("A magazine must have both a ammunition type and a capacity")
    #======================================================================================
    #======================================================================================
    def get_inv_weight(self):
        """
        A functiont to return the inventory weight of the object.
        Returns:
            inv_weight (float): The total weight of the containers inventory.
        """
        inv_weight = 0 # initialize inv_weight
        for item, quantity in self.inventory:
            inv_weight += item.weight * quantity # add the item to the weight multiplied by the quantity
        return inv_weight
    
    def add_to_container(self, in_item: Equipment, in_qty, by_volume: bool = False)->int:
        """
        A function to add solid goods to the container.  Remember that we have to capacities
        to juggle here: The dry goods volume (dry_volume) and the carying capcity (capacity).
        For now, we will consider the size of objects to be negligeble, as none of our equipment
        has a size atribute yet.

        Parameters:
            in_item (Equipment): an instance of the Equipment item that we wish to add
            in_qty: the quantity of the item to add. Could be an int or a float.
            in_name (str): the name of the item to add.
            by_volume (bool, optional): is that quantity expressed by volume (cubic feet) or by count?
                False means by count, True by quantity.  The default is False.
        Raises:
            TypeError: One of the Arguments is of the wrong type.
        Returns:
            output (int): Is 1 if unssuccessful, is 0 if successful.
        """
        # Ensure that we have the right input
        if not isinstance(in_item, Equipment):
            raise TypeError ("Item name must be an Equipment instance.")
        if not isinstance(by_volume, bool):
            raise TypeError("Variable by_volume must be a bool")
        
        # first we check if the bag is empty
        if self.inventory == []:
            self.config = True # if the container is empty, it can be reconfigured for dry goods
        else: # if it's not empty, we need to check that it's not being used for wet goods.
            if not self.config:
                print(f"You are currenty using this {self.name} to store wet goods.")
                return 1
        #Now, if we are adding by quantity
        if by_volume:
            # we first make sure that the incoming quantity is real
            in_qty = float(in_qty) # make sure that a float has been input
            print ("Fix This Later")
            return 1
        else:
            # we first make sure that the incoming quantity is an int
            if not isinstance(in_qty, int):
                raise TypeError("Input quantity must be an integer if not filling by volume.")
            # We need to check if we are not overloading our inventory
            new_wght = self.inv_weight + (in_item.weight * in_qty) # our new weight
            if new_wght > self.capacity:
                print(f"Item cannot be added to {self.name}.")
                return 1
            # in_inventory is wether the item is in our inventory, idx is the index of where it is
            # if its ther and is -1 if its not. 
            in_inventory, idx = find_in_first_entries(self.inventory, in_item.id)
            # if the item is already in the inventory, we just need to change the quantity
            if in_inventory:
                self.inventory[idx][1] += in_qty # we simply increse the quantyity, 
                print(f"Aditional {in_item.name} added to inventory, quantity: {self.inventory[idx][1]}.")
            # if its not there, we want to add it.
            # Now we want to store our items as tww integers and a float: 
            # one for the items id (easier than storing names),
            # one for the quantity.  
            # and one for the item weight.
            # We will express this information as a nested list of (id, quantity, name, and weight)
            else:
                self.inventory.append([in_item, in_qty])
                print(f"{in_item.name} added to inventory.")
            self.inv_weight = new_wght
            return 0
    
    def remove_from_container(self, in_item: int, in_qty, by_volume: bool = False)->int:
        """
        A function to remove solid goods to the container.  Remember that we have to capacities
        to juggle here: The dry goods volume (dry_volume) and the carying capcity (capacity).
        For now, we will consider the size of objects to be negligeble, as none of our equipment
        has a size atribute yet.

        Parameters:
            in_item (int): the id of the item to remove.
            in_qty: the quantity of the item to remove.
            by_volume (bool): is that quantity expressed by volume (cubic feet) or by count?
                False means by count, True by quantity.
        Raises:
            TypeError: One of the Arguments is of the wrong type.
        Returns:
            output (int): Is 1 if unssuccessful, is 0 if successful.
        """
        # Ensure that we have the right input
        if not isinstance(in_item, int):
            raise TypeError ("Item name must be an id integer.")
        if not isinstance(by_volume, bool):
            raise TypeError("Variable by_volume must be a bool")
        # Next we want to check if the item is currently in our inventory. We define a function
        # to help us search.
        #Now, if we are removing by quantity
        if by_volume:
            # we first make sure that the incoming quantity is real
            in_qty = float(in_qty) # make sure that a float has been input
            print ("Fix This Later")
            return 1
        else: #remove an item by count
            # we first make sure that the incoming quantity is an int
            if not isinstance(in_qty, int):
                raise TypeError("Input quantity must be an integer if not removing by volume.")
            # then we check that the object is actualy in the container
            in_inventory, idx = find_in_first_entries(self.inventory, in_item)
            if in_inventory:
                new_qty = self.inventory[idx][1] - in_qty
                if new_qty <= 0:
                    new_qty = 0 # Set new_qty to zero and remove all instances
                    self.inventory.pop(idx) # remove the item tupple itself
                    print(f"All items of id {in_item} removed from {self.name}.")
                else:
                    # We need to replace the entire tuple
                    self.inventory[idx][1] = new_qty
                    print(f"Removed {in_qty} of id {in_item} from {self.name}")
                return 0 # and return 0
            else:
                print(f"Item {in_item} not found in {self.name} inventory.")
                return 1
    
    def initialize(self, tab_id_in: int)->None:
        """
        A function to initialize a container.  This function is exclusivly used in the initialize_cont
        fucntion in the sidekick_data_update.py file.
        Parameters:
            tab_id_in (int): The id of the container in the "character_containers" database.
        Raises
            TypeError: When input other than an Integer is entered.
        """
        if not isinstance(tab_id_in, int):
            raise TypeError ("Input must be an int!")
        self.file_id = tab_id_in # update the containers id number to the new directory
        self.file = self.name + "_" + str(tab_id_in) # generate the file string, changing the int to a string
        return None
    
    # HAS NOT BEEN UPDATED
    def add_window(self, in_list: list)->None:
        """
        Creates a window to implement the add_to_container_function.
        
        Parameters:
            in_list (list): a list of three elemented tuples, usualy containing much of the information
                found in the "equipment_master" table in the "equipment_master.db" database.  It's a big
                list, so we'll want to avoid calling this function all that much, but I don't want to
                manage my database connections in this script.
        """
        # Create a dictionary to map names to a tuple of (ID, weight, quantity)
        item_dict = {{item.name: (item.id, item.weight) for item in in_list}} 
        name_list = list(item_dict.keys())
        # Create the main popup
        addpop = tk.Toplevel()
        addpop.title(f"Add item to {self.name}")
        # Create a label asking the user for input
        user_lab = tk.Label (addpop, text = f"What are you adding to the {self.name}?", **LABEL_OP_NOR)
        user_lab.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        #label each entry
        for index, txt in enumerate(["Item: ", "Quantity: "]):
            cur_row = index + 1 # ensure that we have the current row
            entry_lab = tk.Label(addpop, text = txt, width = 10, **LABEL_OP_NOR)
            entry_lab.grid(row=cur_row, column=0, pady = 5)
        # then create the item selection menu
        item_ch = tk.StringVar()
        itemchosen = ttk.Combobox(addpop, width = 20, textvariable = item_ch)
        itemchosen['values'] = name_list
        itemchosen.grid(row=1, column=1, pady = 5)
        # Function to get the selected item ID
        def get_selected_item_info(name_str: str):
            return item_dict.get(name_str, None)
        # and the quantity box
        qty_ch = tk.StringVar()
        # defining a function for the submit button that will get
        # what's in the entry box and print it to the correct string.
        # Now we create our entry box
        qty_entry = tk.Entry(addpop, textvariable = qty_ch, width = 20)
        qty_entry.grid(row=2, column=1, pady = 5)
        # we define the ent_but_press function
        def ent_but_press():
            id_out, wgt_out = get_selected_item_info(item_ch.get())
            qty_out = qty_ch.get()
            # make sure the inputs are of the correct type
            # remember, the self.add_to_container contains an int.  
            suc_int = self.add_to_container(int(id_out), int(qty_out), item_ch.get(), float(wgt_out))
            if suc_int == 0:
                print(f'Item {item_ch.get()} added to inventory.') # TEST PRINTING
            else:
                error_box(f'Unable to add {item_ch.get()} to inventory.')
            # And destroy the primary window
            addpop.destroy()
        # and finaly add the entry button
        ent_but = tk.Button(addpop, 
                            text = "ENTER",
                            command=ent_but_press,
                            width = 6,
                            **BUTTON_OPTIONS_BLUE)
        ent_but.grid(row=3, column = 0, columnspan=2, pady = 5) # and place the button
        addpop.grab_set()  # Makes popup modal (forces user to interact with it first)
        addpop.wait_window()  # Pauses execution until popup is closed
    
    # HAS NOT BEEN UPDATED
    def remove_window(self)->None:
        """
        A function to open an window to remove an item from a container using the 
        remove_from_container function.
        """
        # remember, self.invetory is stored as (id, quantity, name, weight)
        item_dict = {entry[2]: entry[0] for entry in self.inventory} # we only need the id here
        name_list = list(item_dict.keys())
        # Create the main popup -----------------
        rempop = tk.Toplevel()
        rempop.title(f"Add item to {self.name}")
        # Create a label asking the user for input
        user_lab = tk.Label (rempop, text = f"Which item would you like to remove from the {self.name}", **LABEL_OP_NOR)
        user_lab.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        #label each entry, this is mostly the same as last time
        for index, txt in enumerate(["Item: ", "Quantity: "]):
            cur_row = index + 1 # ensure that we have the current row
            entry_lab = tk.Label(rempop, text = txt, width = 10, **LABEL_OP_NOR)
            entry_lab.grid(row=cur_row, column=0, pady = 5)
        # THIS IS THE BIT THAT's DIFFERENT
        item_ch = tk.StringVar()
        itemchosen = ttk.Combobox(rempop, width = 20, textvariable = item_ch)
        itemchosen['values'] = name_list
        itemchosen.grid(row=1, column=1, pady = 5)
        # Function to get the selected item ID
        def get_selected_item_info(name_str: str):
            return item_dict.get(name_str, None)
        # and the quantity box
        qty_ch = tk.StringVar()
        # defining a function for the submit button that will get
        # what's in the entry box and print it to the correct string.
        # Now we create our entry box
        qty_entry = tk.Entry(rempop, textvariable = qty_ch, width = 20)
        qty_entry.grid(row=2, column=1, pady = 5)
        def ent_but_press():
            id_out = int(get_selected_item_info(item_ch.get()))
            qty_out = int(qty_ch.get())
            # make sure the inputs are of the correct type
            # remember, the self.add_to_container contains an int.  
            suc_int = self.remove_from_container(id_out, qty_out) # ensure our arguments are of the correct type
            if suc_int == 0:
                print(f'Item {item_ch.get()} removed from {self.name}') # TEST PRINTING
            else:
                error_box(f'Unable to remove {item_ch.get()} from {self.name}.')
            # And destroy the primary window
            rempop.destroy()
        # and finaly add the entry button
        ent_but = tk.Button(rempop, 
                            text = "ENTER",
                            command=ent_but_press,
                            width = 6,
                            **BUTTON_OPTIONS_BLUE)
        ent_but.grid(row=3, column = 0, columnspan=2, pady = 5) # and place the button
        rempop.grab_set()  # Makes popup modal (forces user to interact with it first)
        rempop.wait_window()  # Pauses execution until popup is closed

##########################################################################################
#### SKILL CLASSES #######################################################################
##########################################################################################
class Skill:
    def __init__(self, id: int, name: str, usual_atr: str, desc: str):
        """
        Initialzes a skill instance, which stores the information required to use a skill.
        Parameters:
            id (int): The id number of the skill in the skill_master table.
            name (str): The name of the skill.
            usual_atr (str): The atribute the skill is usualy associated with.
            desc (str): The text description of the skill.
        """
        self.id = id # the skills id in the skill master tamble
        self.name = name # The name of the skill
        self.usual_atr = usual_atr # the attribute skill usualy associated with the skill.
        self.desc = desc # The text description of the skill
    
    def normalskill(self, bonus: int):
        """
        A function to simulate making a skill check
        Parameters:
            bonus (int): The bonus we want to apply to the roll.
        """
        # Define the advantage integer
        result = None
        # and the criticality bool
        crit_suc = None
        
        # define what to do when our button is pressed, so we can change the value
        def button_result(in_a):
            nonlocal result
            nonlocal crit_suc
            roll = rolltwenty(in_a)
            crit_suc = True if roll == 20 else False # Define if the roll was critical
            result = roll + bonus #the roll plus the bonus
        
        # Create a popup window for for advantage
        adv_pop = tk.Toplevel()
        adv_pop.title("Advantage Window")
        
        adv_title = tk.Label(adv_pop, text = "Do you have Advantage or Disadvantage?")
        adv_title.pack(padx = 5, pady = 5)
        
        # Define the normal button ------------------------------------------------
        nor_but = tk.Button(adv_pop,
                            text = "Normal Roll",
                            command = lambda: [button_result(0),
                                            adv_pop.destroy()],
                            width = 12,
                            **BUTTON_OPTIONS_BLUE)
        nor_but.pack(padx = 5)
        # Define the Advantage button ---------------------------------------------
        ad_but = tk.Button(adv_pop,
                            text = "Advantage",
                            command = lambda: [button_result(1),
                                            adv_pop.destroy()],
                            width = 12,
                            **BUTTON_OPTIONS_BLUE)
        ad_but.pack(padx = 5)
        # Define the Disadvantage button ------------------------------------------
        dis_but = tk.Button(adv_pop,
                            text = "Disadvantage",
                            command = lambda: [button_result(-1),
                                            adv_pop.destroy()],
                            width = 12,
                            **BUTTON_OPTIONS_BLUE)
        dis_but.pack(padx = 5)

        # finaly we place the logo
        img_a = tk.PhotoImage(file = r"D:\dungeons_and_dragons\Custom_Programs\sidekick_files\images\illustrator_tokens\32w\blue_symbol_32_px.png")
        # setting image with the help of label
        imglabel = tk.Label(adv_pop, image = img_a)
        imglabel.pack(pady = 5)
        
        adv_pop.grab_set()  # Makes adv_pop modal (forces user to interact with it first)
        adv_pop.wait_window()  # Pauses execution until adv_pop is closed
        
        # and display the correct roll
        res_pop = tk.Toplevel() # For result popup
        res_pop.title("Result Window")
        
        # create a string to display
        text_res = "The result of your roll is " + str(result)
        res_lab = tk.Label(res_pop, text = text_res, **LABEL_OP_NOR) # Stands for Result Label
        res_lab.pack(padx = 5, pady = 5)

        if crit_suc: # Create the critical success label
            text_crit = "CRITICAL SUCCESS!"
            res_lab = tk.Label(res_pop, text = text_crit, **LABEL_OP_RED)
            res_lab.pack(padx=5, pady=5)

        # and an exit button
        ex_but = tk.Button(res_pop, 
                        text = "EXIT", 
                        command = res_pop.destroy,
                        width = 6,
                        **BUTTON_OPTIONS_RED)
        ex_but.pack(padx = 5, pady = 5)
        
        # and return nothing
        return None

    def roll_skill(self, in_prof: int, in_atribute: int )->None:
        """
        Rolls a skill check depending on the character's input.
        Parameters:
            in_prof (int): The character's proficiency bonus.
            in_atribute (int): The character's atribute score.
        """
        mod = (in_atribute - 10) // 2
        self.normalskill(in_prof + mod)
        return None
    
##########################################################################################
#### SKILL CLASSES #######################################################################
##########################################################################################
class Condition:
    def __init__(self, in_id: int, name: str, description: str):
        """
        Initializes a Container instance.
        Parameters:
            in_id (int): The id of the condition in the equipment_master conditions table
            name (str): The name of the conditoion
            description (str): The condition description string.
        """
        self.id = in_id
        self.name = name
        self.description = description

##########################################################################################
#### SPELL CLASSES #######################################################################
##########################################################################################
class Spell:
    def __init__(self, in_id: int, name: str, school: str, level: int, cast_time: int,
                 range: int, duration: int, description: str, v_comp: bool = False, 
                 s_comp: bool = False, m_comp: bool = False, m_comp_desc: str = None, 
                 m_comp_cost: float = None, req_concentration: bool = False, 
                 is_ritual: bool = False):
        """
        A class to contain all the information needed to initialize a spell.
        Parameters:
            id (int): The id we want the spell to have in the spell_master table.
            name (str): The name of the spell.
            school (str): What school of magic is the spell in (necromancy, for example)
            level (int): What level is the spell (0 is a cantrip)
            cast_time (int): How long does it take to cast the spell, expressed in seconds.
                Six seconds is one action.
            range (int): What is the spell's range, in feet. 0 means the target is self.
            duration (int): The duration of the spell, expressed in seconds.
            description (str): The text description of the spell.
            v_comp (bool, optional): Does the spell require verbal components? The default is
                False.
            s_comp (bool, optional): Does the spell require somatic components? The default is
                False.
            m_comp (bool, optional): Does the spell require material components? The default is
                False.
            m_comp_desc (str, optional): If the spell requires material compenents, what are they?
                The default is None.
            m_comp_cost (float, optional): If the spell requires material compoents, do they have
                a specific cost in gold pieces? The default is None.
            req_concentration (bool, optional): Does the spell require concentration? The default
                is False.
            is_ritual (bool, optional): Can the spell be cast as a ritual? The default is False.
        Raises:
            ValueError: When values without the proper depencencies are entered as arguments.
        Returns:
            OUT (Spell): An instance of the Spell class.
        """
        self.id = in_id # the spells id number for the database
        self.name = name # the spell's name
        self.school = school # the spell's school
        self.level = level # the spell's level
        self.cast_time = cast_time # the spell's cast time in seconds
        self.range = range # the spell's range in feet.  0 means the target is self.
        self.duration = duration # the spells duration in seconds
        self.desc = format_spell_text(description) # The spell's text description, properly formated
        # The following atributes are optional ---------------------------------------------
        self.v_comp = v_comp # does the spell require verbal components
        self.s_comp = s_comp # does the spell require somatic components
        self.m_comp = m_comp # does the spell require material components
        self.m_comp_desc = m_comp_desc # description of the material components?
        # do the material components have a cost? We ensure this number is a float.
        self.req_con = req_concentration # Does the spell require concentration?
        self.m_comp_cost = float(m_comp_cost) if m_comp_cost is not None else None 
        self.is_ritual = is_ritual # can the spell be cast as a ritual?
        
    def cast_base_spell(self) -> bool:
        """
        A function to cast a basic (non-attack, non-modifiying) spell.
        Returns:
            out_bool (bool): Whether the spell was cast.
        """
        out_bool = None # Define our out_bool to be None
        def button_press(in_b: bool) -> None:
            """
            An internal function to determine what to do when the button is pressed.
            Parameters:
                in_b (bool): The bool we wanted to return.
            """
            nonlocal out_bool
            out_bool = in_b # set our out_bool
            pop.destroy() # close the window

        # create a window to display information
        pop = tk.Toplevel()
        pop.title("Normal Spell Cast")

        name_txt = f"{self.name} spell information:"
        name_lab = tk.Label(pop, text=name_txt, font=("Times New Roman", 12, "bold"))
        name_lab.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)

        # We create a label to display the spell information, wraplength is in pixels, not characters
        spell_lab = tk.Label(pop, text = self.desc, wraplength=400, bd=5, relief=tk.RIDGE, 
                             justify=tk.LEFT, **LABEL_OP_NOR, pady=2) # we want to pad the groove a bit
        spell_lab.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)

        # And create buttons to ask for user input.
        yes_but = tk.Button(pop, text="Cast Spell", command=lambda: button_press(True), width=10, **BUTTON_OPTIONS_BLUE)
        no_but = tk.Button(pop, text="Exit", command=lambda: button_press(False), width=10, **BUTTON_OPTIONS_RED)
        # And place them
        yes_but.grid(row = 2, column = 0, pady = 5)
        no_but.grid(row = 2, column = 1, pady = 5)

        pop.grab_set()  # Makes popup modal (forces user to interact with it first)
        pop.wait_window()  # Pauses execution until popup is closed

        # and return the bool
        return out_bool

class Attack_Spell(Spell):
    def __init__(self, in_id: int, name: str, school: str, level: int, cast_time: int,
                 range: int, duration: int, description: str, v_comp: bool = False, 
                 s_comp: bool = False, m_comp: bool = False, m_comp_desc: str = None, 
                 m_comp_cost: float = None, req_concentration: bool = False, 
                 is_ritual: bool = False, effect_shape: str = None, effect_length: int = None, 
                 origin_self: bool = False, save_type: int = None, save_suc: float = None, 
                 damage_die_amount: int = None, damage_die_type: int = None, damage_bonus: int = None, 
                 damage_type: str = None):
        """
        A function to intialize an Attack_Spell object.
        Parameters:
            id (int): The id we want the spell to have in the spell_master table.
            name (str): The name of the spell.
            school (str): What school of magic is the spell in (necromancy, for example)
            level (int): What level is the spell (0 is a cantrip)
            cast_time (int): How long does it take to cast the spell, expressed in seconds.
                Six seconds is one action.
            range (int): What is the spell's range, in feet. 0 means the target is self.
            duration (int): The duration of the spell, expressed in seconds.
            description (str): The text description of the spell.
            v_comp (bool, optional): Does the spell require verbal components? The default is
                False.
            s_comp (bool, optional): Does the spell require somatic components? The default is
                False.
            m_comp (bool, optional): Does the spell require material components? The default is
                False.
            m_comp_desc (str, optional): If the spell requires material compenents, what are they?
                The default is None.
            m_comp_cost (float, optional): If the spell requires material compoents, do they have
                a specific cost in gold pieces? The default is None.
            req_concentration (bool, optional): Does the spell require concentration? The default
                is False.
            is_ritual (bool, optional): Can the spell be cast as a ritual? The default is False.
            effect_shape (str, optional): If the spell is an area attack, what shape of area does
                it effect. The default is None, which means it isn't an area attack.
            effect_length (int, optional): How long is the effect area, in feet? The default is
                None.
            origin_self (bool, optional): Is the area of effect's origin the player? The default is
                False.
            save_type (int, optional): Does the spell require the target to make a saving throw?
                If it does, give the id of the attribute. 7 means the spell automaticaly hits, such
                as a Magic Missle. The default is None, meaning no save required.
            save_suc (float, optional): If the save is successful, what fraction of damage can the
                target ignore. 1.0 means all damage. The default is None.
            damage_die_amount (int, optional): The number of damage dice to roll in the base case.
                The default is None.
            damage_die_type (int, optional): The number of sides on the damage die, expressed in 1dn
                notation. The default is None.
            damage_bonus (int, optional): The bonus we add to the damage roll. The default is None.
            damage_type (str, optional): The type of damage, expressed as a string. The default is
                None.
        Raises:
            ValueError: When Arguments with incorrect dependecies are entered.
        Returns:
            OUT (Attack_Spell): The Attack_Spell instance.
        """
        # Call the parent constructor using super()
        super().__init__(in_id, name, school, level, cast_time, range, duration, description,
                         v_comp, s_comp, m_comp, m_comp_desc, m_comp_cost, req_concentration,
                         is_ritual)
        self.effect_shape = effect_shape # what is the effect shape
        self.effect_length = effect_length # what is the effect length.
        self.origin = origin_self # Is the origin of the spell the player.
        self.save_type = save_type # What is the id of the save atribute? 7 means automatic hit.
        self.save_suc = save_suc # What percentage of damage does the saving throw allow you to avoid?
        self.damage_die_amount = damage_die_amount # amount of damage dice to roll
        self.damage_die_type = damage_die_type # sides on the damage dice, in 1dn notation
        self.damage_bonus = damage_bonus # Any bonus we add to the damage roll (say, for magic missle)
        self.damage_type = damage_type # type of damage, say "bludgeoning"

        # We need to define some dependencies
        if not xnor(self.m_comp, self.m_comp_desc): # We need a description for material components
            raise ValueError("All material components must have a description.")
        if not (xnor(self.damage_die_type, self.damage_type)): # we need damage for an attack
            raise ValueError("All attacks must have both a damage die and a damage type")
        if self.save_type != 7 and not (xnor(self.save_type, self.save_suc)):
            raise ValueError ("A defined save must have both a attribute and an effect.")
        if not (xnor(self.effect_shape, self.effect_length)):
            raise ValueError("A defined effect must have a size.")
        if not(list_xnor([self.effect_length, self.effect_shape, self.origin])):
            raise ValueError("A defined effect must have a size and origin.")
    
    def ask_range(self) -> bool:
        """
        A function to ask the user for a range input.
        Raises:
            ValueError: Input needs to be an integer.
        Returns:
            outbool (bool): Is the target in range or not.
        """
        # initialize our variables.  ran is the target's range
        ran = None
        outbool = False
        
        #create a window asking for the targets range
        ranpop = tk.Toplevel()
        ranpop.title("Range Window")
        ranpop.geometry("300x200") # set the geometry to 300x200
        
        # We define what to do when the submit button is pressed
        def submit():
            try:
                nonlocal ran
                ran = int(ran_str.get())
                ranpop.destroy()
            except ValueError:
                error_label.config(text="Please enter a valid integer", fg="red")
        
        # Range Label ---- Asks for user input
        ran_lab_one = tk.Label(ranpop, text = "Enter distance to target in feet:")
        ran_lab_one.pack(padx = 5, pady = 5)
        
        # Initialize Entry Stringvar
        ran_str = tk.StringVar()
        # defining a function for the submit button that will get
        # what's in the entry box and print it to the correct string.
        
        # Now we create our entry box
        # Range Entry
        ran_entry = tk.Entry(ranpop, textvariable = ran_str, width = 10)
        ran_button = tk.Button(ranpop, 
                               text = "Submit", 
                               command = submit,
                               width = 8,
                               **BUTTON_OPTIONS_BLUE)
        # Create our error labe, even if its not visible
        error_label = tk.Label(ranpop, text="", fg="red")
        
        # and place these objects into our window
        ran_entry.pack(pady = 5)
        ran_button.pack(pady = 5)
        error_label.pack(pady = 5)
        
        ranpop.grab_set()  # Makes popup modal (forces user to interact with it first)
        ranpop.wait_window()  # Pauses execution until popup is closed
        
        # If target is in range, set outbool to True.
        if ran <= self.range:
            outbool = True
        # And return our outbool.
        return outbool

    def attack_roll(self) -> int:
        """
        A fuction to simulate a spell attack roll using the global rolltwenty function.
        Returns:
            result (int): The raw result of the attack roll with no modifier.
        """
        # Define our advantage_num
        result = None
        # Define a function on what to do on a button press
        def button_press(int_in: int):
            nonlocal result # bring in our non_local variables
            # get the result
            result = rolltwenty(int_in)
            rollpop.destroy()
            
        # create a roll options screen
        rollpop = tk.Toplevel()
        rollpop.title("Spell Roll Options")

        
        # Create a label to ask the user for input
        rol_lab = tk.Label (rollpop, text = "Are you attacking with Advantage or Disadvantage?")
        rol_lab.pack(padx = 5, pady = 5) # place the label in rollpop
        
        # We create the three buttons using a for loop, and place them in a frame
        but_frame = tk.Frame(rollpop)
        # over a tupple, as seen bellow
        for num, lab in [(0, "Normal"),(1, "Advantage"), (-1, "Disadvantage")]:
            button = tk.Button(but_frame, text = lab, command = lambda n = num: button_press(n), 
                               width = 12, **BUTTON_OPTIONS_BLUE)
            button.pack() # and place the button in the frame
        but_frame.pack(padx=5, pady=5) # and place the frame

        # finaly we place the logo
        image_file = os.path.join(CUR_DIR, "sidekick_files", "images", "illustrator_tokens", 
                                  "32w", "blue_symbol_32_px.png")
        img_a = tk.PhotoImage(file = image_file)
        
        # setting image with the help of label
        imglabel = tk.Label(rollpop, 
                            image = img_a,
                            bd= 5,
                            relief=tk.SOLID)
        imglabel.pack(pady = 5)
        
        rollpop.grab_set()  # Makes popup modal (forces user to interact with it first)
        rollpop.wait_window()  # Pauses execution until popup is closed
        
        return result

    def attack_result_info(self, attack_result: int) -> bool:
        """
        A function to display the attack roll result and ask the user if it hit.
        Parameters:
            attack_result (int): The modified attack roll
        Returns:
            attack_successful (bool): is the attack successful or not?
        """
        # Define the attack results window
        atkpop = tk.Toplevel()
        atkpop.title("Spell Attack Results Window")

        attack_successful: bool = False # initialize our successful attack as false

        # Place the user input label
        res_txt = f"You rolled a {attack_result} on your attack roll."
        res_lab = tk.Label(atkpop, text=res_txt, **LABEL_OP_NOR)
        res_lab.pack(padx=5, pady=5)

        # Plus a label asking the user for input (a hit label)
        hit_lab = tk.Label(atkpop, text = "Did the attack succeed?", **LABEL_OP_NOR)
        hit_lab.pack(padx = 5, pady = 5)
        
        # Before we provide some buttons for them to answer
        def on_yes_button_click():
            nonlocal attack_successful
            attack_successful = True
            atkpop.destroy()

        # define a frame for the buttons
        butfram = tk.Frame(atkpop)
        yes_but = tk.Button(butfram, 
                            text = "Yes", 
                            command = on_yes_button_click,
                            width = 6,
                            **BUTTON_OPTIONS_BLUE)
        no_but = tk.Button(butfram,
                           text = "No",
                           command = atkpop.destroy,
                           width = 6,
                           **BUTTON_OPTIONS_RED)
        yes_but.pack()
        no_but.pack()
        butfram.pack(padx=5, pady=5)
        
        atkpop.grab_set()  # Makes popup modal (forces user to interact with it first)
        atkpop.wait_window()  # Pauses execution until popup is closed

        return attack_successful # and return the attack successful bool

    def damage_roll(self, is_c: bool, red: float) -> None:
        """
        A function to actualy roll the damage dice.
        Parameters:
            is_c (bool): Is the roll a critical one?
            red (float): The amount we wish to reduce the damage by.
        Returns:
            dam (int): The damage dealt.
        """
        dice_amount = self.damage_die_amount

        # make sure to check for criticality
        dice_amount *= 2 if is_c else 1
        
        # The bonus damage is the damage bonus, if it exists. If it doesn't, we set to be zero.
        bonus_dam = self.damage_bonus if self.damage_bonus is not None else 0

        # generate the damage value based on the attack, the amount of dice to roll
        # and any specified bonsus (like for magic missle)
        raw_dam = rolldamage(bonus_dam, self.damage_die_type, dice_amount)
        # We acount for the possibility of reduction
        dam = int(math.floor(raw_dam * (1.0 - red)))
        return dam

    def damage_window(self, is_crit: bool, display_txt: str) -> None:
        """
        A Function to call for a damage roll on a spell attack
        Parameters:
            is_crit (bool): Did we roll a critical on the roll.
            display_txt (str): Additional text about the target we wish to display.
                None means no special text.
        Returns:
            out_dam (int): The spells damage.
        """
        # We don't need to worry about damage reduction here, so we set it to zero
        # we then use the damage_roll function defined above.
        dam_val = self.damage_roll(is_crit, 0.0)
            
        # And generate the damage window
        dampop = tk.Toplevel()
        dampop.title("Damage Window")

        # if we rolled a critical, we notify the player
        if is_crit:
            crit_lab = tk.Label(dampop, text="CRITICAL!", **LABEL_OP_RED)
            crit_lab.pack(padx = 5, pady = 5)
        
        # The user info label
        dam_str = f"The damage rolled was {str(dam_val)} {self.damage_type} damage!"
        dam_lab = tk.Label(dampop, text = dam_str, **LABEL_OP_NOR)
        dam_lab.pack(padx = 5, pady = 5)

        # Display target info, if nessicary
        if display_txt:
            disp_lab = tk.Label(dampop, text = display_txt, **LABEL_OP_RED)
            disp_lab.pack(padx = 5, pady = 5)
        
        # And the exit button
        exit_but = tk.Button(dampop, 
                             text = "Exit",
                             command = dampop.destroy,
                             width = 6,
                             **BUTTON_OPTIONS_RED)
        exit_but.pack(padx=5, pady = 5)
        
        dampop.grab_set()  # Makes popup modal (forces user to interact with it first)
        dampop.wait_window()  # Pauses execution until popup is closed
        
        return dam_val
        
    def get_targets(self) -> List[str]:
        """
        A function to get the user input for targets for an area-attack spell
        Returns:
            target_list (List[str]): The names of the targets as a list of strings.
        """
        target_list: List[str] = [] # initialise the target list.
        list_raw: str = None # the display string
        list_display = tk.StringVar() # define list dislpay as a StringVar
        list_display.set("No current targets.") # and define the inital state

        def reset_display(in_target: str):
            """
            A function to reset the dislpayed list of names
            Parameters:
                in_target (str): The name of the target we want to add to the display
            """
            nonlocal list_raw
            nonlocal list_display
            if list_raw == None:
                list_raw = in_target # if the list_raw is empty, we just add the name
            else:
                list_raw = list_raw + ", " + in_target # we add to the string, using a comma
            list_display.set(list_raw) # Update list_display

        def button_press():
            # Define our non-local variables
            nonlocal target_list
            nonlocal list_display
            new_target = target.get()
            if new_target not in target_list: # check if the name is already in the list
                target_list.append(new_target) # add the target to the list
                reset_display(new_target) # reset the display

        tarpop = tk.Toplevel()
        tarpop.title = "Attack Targeting Window"

        # Label the current target, row 0
        q_lab = tk.Label(tarpop, text="Current Targets:", **LABEL_OP_NOR)
        q_lab.grid(row = 0, column = 0, columnspan=2)

        # list the current targets, row 1
        tarlab = tk.Label(tarpop, textvariable=list_display, bd = 5, relief=tk.RIDGE, **LABEL_OP_NOR)
        tarlab.grid(row = 1, column = 0, columnspan=2)

        #and ask the user for input, row 2
        target = tk.StringVar()
        a_lab = tk.Label(tarpop, text = "Target:", **LABEL_OP_NOR)
        # And the user entry
        a_entry = tk.Entry(tarpop, textvariable = target, width = 20)
        a_lab.grid(row=2, column=0)
        a_entry.grid(row=2, column=1)

        # And the user control buttons, row 3
        add_button = tk.Button(tarpop, text="Add To List", command=button_press, width = 15, **BUTTON_OPTIONS_BLUE)
        com_button = tk.Button(tarpop, text="Confirm Targets", command=tarpop.destroy,
                               width=15, **BUTTON_OPTIONS_BLUE)
        add_button.grid(row=3, column=0)
        com_button.grid(row=3, column=1)

        tarpop.grab_set()  # Makes popup modal (forces user to interact with it first)
        tarpop.wait_window()  # Pauses execution until popup is closed

        return target_list # return the target list
    
    def get_targets_special(self) -> Dict[str, int]:
        """
        A special version of get_targets that allows the list to contain multiple instances of the
        same target for independently targeted spells like Magic Missle.
        Returns:
            target_list (Dict[str, int]): The names and occurences of the targets stored as a dict, with the
                names as the key.
        """
        target_list: Dict[str, int] = {} # initialise the target dict..
        list_raw: str = None # the display string
        list_display = tk.StringVar() # define list dislpay as a StringVar
        list_display.set("No current targets.") # and define the inital state

        def reset_display(in_target: str):
            """
            A function to reset the dislpayed list of names
            Parameters:
                in_target (str): The name of the target we want to add to the display
            """
            nonlocal list_raw
            nonlocal list_display
            if list_raw == None:
                list_raw = in_target # if the list_raw is empty, we just add the name
            else:
                list_raw = list_raw + ", " + in_target # we add to the string, using a comma
            list_display.set(list_raw) # Update list_display

        def button_press():
            # Define our non-local variables
            nonlocal target_list
            nonlocal list_display
            new_target = target.get()
            if new_target not in target_list.keys(): # check if the name is already in the list keys
                target_list[new_target] = 1 # we define a new entry
                reset_display(new_target) # reset the display
            else: # if the target is in the list
                target_list[new_target] += 1 # we itterate by one.
                reset_display(new_target)

        tarpop = tk.Toplevel()
        tarpop.title = "Attack Targeting Window"

        # We want an info label informing the user that the same target can be attacked multiple times
        # for this type of spell.
        info_txt = "As this spell is independently targteted, the same target can be entered multiple times."
        info_lab = tk.Label(tarpop, text = info_txt, wraplength=250, **LABEL_OP_RED)
        info_lab.grid(row=0, column=0, columnspan=2, padx = 5, pady = 5)

        # Label the current target, row 1
        q_lab = tk.Label(tarpop, text="Current Targets:", **LABEL_OP_NOR)
        q_lab.grid(row = 1, column = 0, columnspan=2)

        # list the current targets, row 2
        tarlab = tk.Label(tarpop, textvariable=list_display, bd = 5, relief=tk.RIDGE, **LABEL_OP_NOR)
        tarlab.grid(row = 2, column = 0, columnspan=2)

        #and ask the user for input, row 3
        target = tk.StringVar()
        a_lab = tk.Label(tarpop, text = "Target:", **LABEL_OP_NOR)
        # And the user entry
        a_entry = tk.Entry(tarpop, textvariable = target, width = 20)
        a_lab.grid(row=3, column=0)
        a_entry.grid(row=3, column=1)

        # And the user control buttons, row 4
        add_button = tk.Button(tarpop, text="Add To List", command=button_press, width = 15, **BUTTON_OPTIONS_BLUE)
        com_button = tk.Button(tarpop, text="Confirm Targets", command=tarpop.destroy,
                               width=15, **BUTTON_OPTIONS_BLUE)
        add_button.grid(row=4, column=0)
        com_button.grid(row=4, column=1)

        tarpop.grab_set()  # Makes popup modal (forces user to interact with it first)
        tarpop.wait_window()  # Pauses execution until popup is closed

        return target_list # return the target list

    def force_saving_throw(self, dif: int, target_list: List[str]) -> Dict[str, bool]:
        """
        A function to manage our saving throws.
        Parameters:
            dif (int): The DC of the saving throw
            target_list (List[str]): A list of all the creatures effected by the spell
        Returns:
            out_list (Dict[str, bool]): A list of all the creatures hit by the spell.
        """
        out_list = {n: False for n in target_list}
        # 1) instantiate one IntVar per name, default 0 (failed)
        var_dict = {n: tk.IntVar(value=0) for n in target_list}

        def on_choice(in_name: str):
            # read the IntVar and update out_list
            out_list[in_name] = bool(var_dict[in_name].get())

        respop = tk.Toplevel()
        respop.title("Saving Throw Results")

        tk.Label(
            respop,
            text=(
                f"For each name below, select if they passed or failed the "
                f"{ABILITY_DICT[self.save_type]} DC {dif} saving throw."
            ),
            **LABEL_OP_NOR
        ).pack(padx=5, pady=5)

        for name in target_list:
            frm = tk.Frame(respop, bg="#DDDDDD")
            tk.Label(frm, text=name, **LABEL_OP_NOR).grid(row=0, column=0)

            # 2) give each button a value
            yes = tk.Radiobutton(
                frm,
                text="passed",
                variable=var_dict[name],
                value=1,
                command=lambda n=name: on_choice(n)
            )
            no = tk.Radiobutton(
                frm,
                text="failed",
                variable=var_dict[name],
                value=0,
                command=lambda n=name: on_choice(n)
            )

            yes.grid(row=0, column=1)
            no.grid(row=0, column=2)
            frm.pack(padx=5, pady=3)

        tk.Button(
            respop,
            text="Confirm",
            pady=10,
            command=respop.destroy,
            **BUTTON_OPTIONS_BLUE
        ).pack(padx=5, pady=5)

        respop.grab_set()
        respop.wait_window()

        return out_list

    def save_damage_roll(self, in_dict: Dict[str, bool]) -> None:
        """
        A function to roll damage dice for multiple targets.
        Parameters:
            in_dict (Dict[str, bool]): A dict object containing the relevant information.
                The str is the target's name. The bool is whether the target was successful
                in it's saving throw or not.
        """
        # We first create a window
        dampop = tk.Toplevel()
        dampop.title("Save Damage Result Window")

        # And define what the user is seeing.
        usr_txt = "The following targets were damaged as such"
        usr_lab = tk.Label(dampop, text=usr_txt, **LABEL_OP_NOR)
        usr_lab.pack(padx=5, pady=5)

        # Before automaticaly generating a result label for each target.
        for target_name, suc in in_dict.items():
            # We define name_dam, using an if/else statement
            name_dam = self.damage_roll(False, self.save_suc) if suc else self.damage_roll(False, 0.0)
            # create a label to display this information
            name_txt = f"Target {target_name} has recived {name_dam} {self.damage_type} damage."
            name_lab = tk.Label(dampop, text=name_txt, bg="#DDDDDD", **LABEL_OP_NOR)
            name_lab.pack(padx=5, pady=3) # place the label
        
        # and create a button to exit and place it using pack
        exit_but = tk.Button(dampop, text = "EXIT", width=6, command=dampop.destroy, **BUTTON_OPTIONS_RED)
        exit_but.pack(padx=5, pady=5)

        dampop.grab_set()  # Makes popup modal (forces user to interact with it first)
        dampop.wait_window()  # Pauses execution until popup is closed

    def auto_damage_roll(self, in_dict: Dict[str, int]) -> None:
        """
        A function to automaticaly damage multiple targets for spells such as magic missle.
        Parameters:
            in_dict (Dict[str, int]): The dictionary containing the targeting information, in the 
                form of name: attack amount.
        """
        dampop = tk.Toplevel()
        dampop.title("Attack Damage Result Window")

        # And define what the user is seeing.
        usr_txt = "The following targets were damaged as such"
        usr_lab = tk.Label(dampop, text=usr_txt, **LABEL_OP_NOR)
        usr_lab.pack(padx=5, pady=5)

        # Before automaticaly generating a result label for each target.
        for target_name, amt in in_dict.items():
            # We define name_dam, using the rolldamage master function
            name_dam = 0 # We initialize roll damage
            for n in range(amt): # we want to roll the correct number of times, but we need to start at zero
                name_dam += self.damage_roll(False, 0.0)
            # create a label to display this information
            name_txt = f"Target {target_name} has recived {name_dam} {self.damage_type} damage."
            name_lab = tk.Label(dampop, text=name_txt, bg="#DDDDDD", **LABEL_OP_NOR)
            name_lab.pack(padx=5, pady=3) # place the label

        # and create a button to exit and place it using pack
        exit_but = tk.Button(dampop, text = "EXIT", width=6, command=dampop.destroy, **BUTTON_OPTIONS_RED)
        exit_but.pack(padx=5, pady=5)

        dampop.grab_set()  # Makes popup modal (forces user to interact with it first)
        dampop.wait_window()  # Pauses execution until popup is closed

    def singular_attack(self, cm: int):
        """
        A function to manage the function calls for a singular spell attack against a single target.
        Parameters:
            cm (int): The cast modifier for the spell
        Returns:
            OUT (Tuple[bool, int]): A tuple containing the criticality bool first and the modified roll second.
        """
        # Define our damage and roll variables
        roll = self.attack_roll()
        cr = True if roll == 20 else False # check for criticality
        rm = roll + cm # calculate the modified roll
        return cr, rm

    def cast_spell_attack(self, prof_bonus: int, relavant_score: int, spcl_txt: str = None) -> bool:
        """
        A function to cast an attack spell.
        Parameters:
            prof_bonus (int): The character's proficiency bonus.
            relevant_score (int): The relative atribute score, such as intelligence or charisma.
            spcl_txt (str, optional): Any special instructions we wish to give the player. The
                default is None. This option is generaly used for Special_Attack_Spells, but is
                defined here for convenience.
        Returns:
            out_b (bool): Whether the spell is cast or not.
        """
        # We define the spell modifier
        spell_mod = ((relavant_score - 10) // 2)
        cast_mod = prof_bonus + spell_mod # Define our casting modifier
        in_range = True # is the target in range, which we assume to be true

        # first we need to ask the user if they wish to cast the spell
        # Which does not require outside information.
        out_b = self.cast_base_spell() # display the spell information.
        if out_b:

            damage = 0 # define damage as zero to start, we can change this

            # We condsider three different scenarios
            # 1) An attack roll (save_type is None)
            if self.save_type == None:
                            # if we are using a ranged spell, we need the target's range
                # Anything over 5 feet is considered a ranged spell.
                if self.range > 5:
                    in_range = self.ask_range()

                # if the target is in range, we can attack.
                if in_range:
                    # Get the details from my spell attack
                    critical, roll_modified = self.singular_attack(cast_mod)
                    # And display the attack window
                    if critical:
                        damage = self.damage_window(critical, spcl_txt) # pass the criticality bool to the damage roll function
                    else:
                        if self.attack_result_info(roll_modified):
                            damage = self.damage_window(critical, spcl_txt) # pass the criticality bool to the damage roll function
                        else:
                            error_box("Failed to hit target!") # we failed to hit our target

                #### TEST LINE
                print(f"You rolled {roll_modified} and dealt {damage} {self.damage_type} damage.")
            
            # 2) Force a save roll (save_type is None)
            elif self.save_type in {1,2,3,4,5,6}:
                st_dificulty = 8 + cast_mod # set the dificulty of the saving throw.

                # First we need to find out how many targets we are attacking using the targeting window.
                targets = self.get_targets()
                # We pass these targets into the Saving Roll Window
                target_dict = self.force_saving_throw(st_dificulty, targets)
                # And generate the damage window.
                self.save_damage_roll(target_dict)
                #### TEST LINE
                print("Damage dealt to various targets.")
            
            # 3) An auto hitting spell, similar to magic missle.
            elif self.save_type == 7:
                # like before, we need to get targets
                targets = self.get_targets_special()
                # This time, we can place them direclty into the auto_damage_roll function
                # since no saving throw is needed.
                self.auto_damage_roll(targets)
                #### TEST LINE
                print("Successfuly cast Magic Missile")
            else:
                error_box("Target out of range!") # target is out of range.

        else:
            print(f"{self.name} not cast.")

        return out_b

class Special_Spell(Spell):
    def __init__(self, in_id: int, name: str, school: str, level: int, cast_time: int,
                 range: int, duration: int, description: str, v_comp: bool = False, 
                 s_comp: bool = False, m_comp: bool = False, m_comp_desc: str = None, 
                 m_comp_cost: float = None, req_concentration: bool = False, 
                 is_ritual: bool = False, indicator: int = None, special_text: str = ""):
        """
        A child class to contain the specific information needed for special type spells (spells that
        require special rules to function correclty, such as magic missle.)
        Parameters:
            id (int): The id we want the spell to have in the spell_master table.
            name (str): The name of the spell.
            school (str): What school of magic is the spell in (necromancy, for example)
            level (int): What level is the spell (0 is a cantrip)
            cast_time (int): How long does it take to cast the spell, expressed in seconds.
                Six seconds is one action.
            range (int): What is the spell's range, in feet. 0 means the target is self.
            duration (int): The duration of the spell, expressed in seconds.
            description (str): The text description of the spell.
            v_comp (bool, optional): Does the spell require verbal components? The default is
                False.
            s_comp (bool, optional): Does the spell require somatic components? The default is
                False.
            m_comp (bool, optional): Does the spell require material components? The default is
                False.
            m_comp_desc (str, optional): If the spell requires material compenents, what are they?
                The default is None.
            m_comp_cost (float, optional): If the spell requires material compoents, do they have
                a specific cost in gold pieces? The default is None.
            req_concentration (bool, optional): Does the spell require concentration? The default
                is False.
            is_ritual (bool, optional): Can the spell be cast as a ritual? The default is False.
            indicator (int, optional): The indicator of what type of special spell this is (such as unique 
                effect or such). The default is None, meaning a unique spell. 0 means an spell that imparts
                some effect to the target, such as "ray of frost."
            special_text (str, optional): Any specific text we want the spell dialogue box to display.
                The default is the empty string.
        Returns:
            OUT (Special_Spell): The Special_Spell instance.
        """
        # Call the parent constructor using super()
        super().__init__(in_id, name, school, level, cast_time, range, duration, description,
                         v_comp, s_comp, m_comp, m_comp_desc, m_comp_cost, req_concentration,
                         is_ritual)
        self.indicator = indicator # The indicator (special spell type)
        self.special_text = special_text # and specific text we want to display.
    
    def cast_special_spell(self) -> None:
        """
        A funciton to cast a special type spell.
        Returns:
            out_b (bool): Whether the spell is cast or not.
        """
        # first, we cast the spell as usual.  The specific special atributes of the spell should
        # be contained in the spell's text description.
        out_b = self.cast_base_spell()
        if out_b:
            error_txt = "You have selecte a spell whose atributes are not built into they system yet!"
            error_box(error_txt)

        return out_b

class Special_Attack_Spell(Attack_Spell):
    def __init__(self, in_id: int, name: str, school: str, level: int, cast_time: int,
                 range: int, duration: int, description: str, v_comp: bool = False,
                 s_comp: bool = False, m_comp: bool = False, m_comp_desc: str = None, 
                 m_comp_cost: float = None, req_concentration: bool = False, 
                 is_ritual: bool = False, effect_shape: str = None, effect_length: int = None, 
                 origin_self: bool = False, save_type: int = None, save_suc: float = None, 
                 damage_die_amount: int = None, damage_die_type: int = None, damage_bonus: int = None, 
                 damage_type: str = None, indicator: int = None, special_text: str = ""):
        """
        A function to intialize an Special_Attack_Spell object.
        Parameters:
            id (int): The id we want the spell to have in the spell_master table.
            name (str): The name of the spell.
            school (str): What school of magic is the spell in (necromancy, for example)
            level (int): What level is the spell (0 is a cantrip)
            cast_time (int): How long does it take to cast the spell, expressed in seconds.
                Six seconds is one action.
            range (int): What is the spell's range, in feet. 0 means the target is self.
            duration (int): The duration of the spell, expressed in seconds.
            description (str): The text description of the spell.
            v_comp (bool, optional): Does the spell require verbal components? The default is
                False.
            s_comp (bool, optional): Does the spell require somatic components? The default is
                False.
            m_comp (bool, optional): Does the spell require material components? The default is
                False.
            m_comp_desc (str, optional): If the spell requires material compenents, what are they?
                The default is None.
            m_comp_cost (float, optional): If the spell requires material compoents, do they have
                a specific cost in gold pieces? The default is None.
            req_concentration (bool, optional): Does the spell require concentration? The default
                is False.
            is_ritual (bool, optional): Can the spell be cast as a ritual? The default is False.
            effect_shape (str, optional): If the spell is an area attack, what shape of area does
                it effect. The default is None, which means it isn't an area attack.
            effect_length (int, optional): How long is the effect area, in feet? The default is
                None.
            origin_self (bool, optional): Is the area of effect's origin the player? The default is
                False.
            save_type (int, optional): Does the spell require the target to make a saving throw?
                If it does, give the id of the attribute. 7 means the spell automaticaly hits, such
                as a Magic Missle. The default is None, meaning no save required.
            save_suc (float, optional): If the save is successful, what fraction of damage can the
                target ignore. 1.0 means all damage. The default is None.
            damage_die_amount (int, optional): The number of damage dice to roll in the base case.
                The default is None.
            damage_die_type (int, optional): The number of sides on the damage die, expressed in 1dn
                notation. The default is None.
            damage_bonus (int, optional): The bonus we add to the damage roll. The default is None.
            damage_type (str, optional): The type of damage, expressed as a string. The default is
                None.
            indicator (int, optional): The indicator of what type of special spell this is (such as unique 
                effect or such). The default is None, meaning a unique spell. 0 means an spell that imparts
                some effect to the target, such as "ray of frost."
            special_text (str, optional): Any specific text we want the spell dialogue box to display.
                The default is the empty string.
        Raises:
            ValueError: When Arguments with incorrect dependecies are entered.
        Returns:
            OUT (Attack_Spell): The Attack_Spell instance.
        """
        # Call the parent constructor using super()
        super().__init__(in_id, name, school, level, cast_time, range, duration, description,
                         v_comp, s_comp, m_comp, m_comp_desc, m_comp_cost, req_concentration,
                         is_ritual)
        self.effect_shape = effect_shape # what is the effect shape
        self.effect_length = effect_length # what is the effect length.
        self.origin = origin_self # Is the origin of the spell the player.
        self.save_type = save_type # What is the id of the save atribute? 7 means automatic hit.
        self.save_suc = save_suc # What percentage of damage does the saving throw allow you to avoid?
        self.damage_die_amount = damage_die_amount # amount of damage dice to roll
        self.damage_die_type = damage_die_type # sides on the damage dice, in 1dn notation
        self.damage_bonus = damage_bonus # Any bonus we add to the damage roll (say, for magic missle)
        self.damage_type = damage_type # type of damage, say "bludgeoning"
        self.indicator = indicator # The indicator (special spell type)
        self.special_text = special_text # and specific text we want to display.

    def cast_special_spell_attack(self, prof_bonus: int, relavant_score: int) -> bool:
        """
        A function to cast a special attack spell
        Parameters:
            prof_bonus (int): The character's proficiency bonus
            relavant_score (int): The character's spellcasting ability score.
        Returns:
            out_b (bool): Whether the spell is cast or not.
        """
        # first, we cast the spell as usual.  The specific special atributes of the spell should
        # be contained in the spell's text description.
        out_b = False
        if self.indicator == 0: # Spell forces a condition upon a target with a successful hit.
            out_b = self.cast_spell_attack(prof_bonus, relavant_score, spcl_txt=self.special_text)
        elif self.indicator == 1: # Spell creates multiple beams when leveled up
            out_b = self.cast_spell_attack(prof_bonus, relavant_score)
        else:
            error_box("Spell id not recognized, Error cssa_1.")

        return out_b


##########################################################################################
#### CHARACTER CLASSES ###################################################################
##########################################################################################
class Character:
    def __init__(self, name:str, image:str, db: str, color: str, lang: list[str],
                  exhaustion: int, pb: int = 0):
        """
        Initialialzes the character class, which stores the information neccisary to create
        and control a character.
        Parameters:
            name (str): The name of the character.
            image (str): The location of the character's image file expressed as a string.
            db (str): The location of the character's database file expressed as a string.
            color (str): The character's color code (blue, red, green, orange)
            conditions (list[(int, str)]): A list of tuples (id, name) describing any active conditons
                on the character.
            lang (list[str]): Languages the character speaks.
            exhaustion (int): A integer representing the character's exhaustion.
            pb (int, optional): The character's proficiency bonus. The defualt is 0
        """
        self.name = name # intialize the name of the character
        self.image = image # The image location
        self.db = db # the database location
        self.color = color # the character's color code.
        self.lang = lang
        self.exhaustion = exhaustion # The characer's exaustion level.
        self.pb = pb # the proficiency bonus
        # ABILITY SCORES
        self.stre: int = None # the strength score, defined later
        self.dext: int = None # the dexterity score, defined later
        self.cons: int = None # the constitution score, defined later
        self.inte: int = None # the intelligence score, defined later
        self.wisd: int = None # the wisdom score, defined later
        self.char: int = None # the charisma score, defined later
        # HEALTH DATA
        self.max_hp: int = None # the character's max hp, defined later
        self.cur_hp: int = None # the character's current hp , defined later
        self.temp_hp: int = None # the charater's temporary hp, defined later
        self.max_hd: int = None # the character's max hit dice, defined later
        self.cur_hd: int = None # the character's current hit dice, defined later
        self.hd_type: int = None # the number of sides on the character's hit dice, defined later
        # CONDITION DATA
        self.conditions : Dict[int, Condition] = {} # An inventory dict for the conditions.
        # INVENTORY DATA
        self.main_inv: List[Tuple[Equipment, int]] = [] # initialize the main inventory
        self.weapon_inv: List[Tuple[Weapon, int]] = [] # initialize the weapon inventory
        self.armor_inv: List[Tuple[Armor, int]] = [] # initilize the armor inventory
        self.container_inv: list[Container] = [] # initilize the container inventory
        self.clothing_inv: List[Tuple[Clothing, int]] = [] # intitialize the clothing inventory
        # SKILL DATA
        self.skills_prof: list[int] = [] # defined in the skills functions
        self.skills_exp : list[int] = [] # the expertise list (for characters that have that)
        # SPELL DATA
        self.spell_list: Dict[int, Spell] = {} # the spells the character has prepared, stored in a dict
        self.atk_spell_list: List[int] = []
        # The character's available spell slots. The first number is availble slots, the second number is total slots.
        # The keys are the corresponding spell level.
        self.spell_slots: Dict[int, List[int]] = {1: [0,0], 2: [0,0], 3: [0,0], 4: [0,0], 5: [0,0], 
                                            6: [0,0], 7: [0,0], 8: [0,0], 9: [0,0]}

    def set_atributes(self, in_list: list):
        """
        A Function to set the character's atributes.
        Parameters:
            in_list (list): A list of six integers, with the order 
                (STR, DEX, CON, INT, WIS, CHA) determing the scores 
                of each atribute
        Raises:
            ValueError: When a list other than size six is entered.
        """
        if len(in_list) == 6: #ensure that we got the correct length list
            attributes = ['stre', 'dext', 'cons', 'inte', 'wisd', 'char']
            for attr, value in zip(attributes, in_list): # use a handy zip
                setattr(self, attr, value) # use a setatttr function to set the atributes
        else:
            raise ValueError("Input did not contain 6 elements.")

    def set_health(self, in_list: list):
        """
        A Function to set the character's health information.
        Parameters:
            in_list (list): A list of six integers, in the order of (max health, current health,
                temporary health) to set each atribute.
        Raises:
            ValueError: When a list other than six items is entered
        """
        if len(in_list) == 6: # ensure the correct info
            h_list = ["max_hp", "cur_hp", "temp_hp", "max_hd", "cur_hd", "hd_type"] # define a list of atributes
            for att, val in zip(h_list, in_list): # zip the information together
                setattr(self, att, val) # use a setatttr function to set the atributes
        else:
            raise ValueError("Input did not contain 6 elements.")
        
    def set_skills(self, in_list: list[list[int]]):
        """
        A function to set the character's skill information.
        Parameters:
            in_list (list[list[int]]): A nested list of ints representing first the proficiency id's
                then the expertise id's
        Raises:
            ValueError: When a list of other than 2 items is entered.
        """
        if len(in_list) == 2: # ensure the correct info
            self.skills_prof = in_list[0] # set the prof list
            self.skills_exp = in_list[1] # set the exp list.
        else:
            raise ValueError("Input did not contain 2 elements.")

    def set_spell_slots(self, in_list: List[Tuple[int, int]]):
        """
        A funciton to set the character's spell slots.
        Parameters:
            in_list (List[Tuple[int, int]]): A list of integers representing the number of spell slots available.
        Raises:
            ValueError: When a list other than 9 entries is entered.
        """
        if len(in_list) != 9: # ensure the correct
            raise ValueError("Input did not contain 9 elements.")
        # Then use the for loop to set the spell slots
        for idx, (num_a, num_b) in enumerate(in_list): # changes from a tuple to a nested list
            self.spell_slots[idx + 1] = [num_a, num_b] # Set the available and total slots to the same number

    def add_cond_man(self, in_con: Condition) -> Condition:
        """
        A function to add a condition to a character object in the form of condition object.
        Parameters:
            in_info (tuple): A tuple containing the database id number of the condition, along with the name.
        Returns:
            OUT (Condition): Returns the added condition if succesful. Returns None if not.
        """
        # First we check if that condition is already in the database (we don't need to specify keys)
        if in_con.id in self.conditions:
            print(f"{self.name} already is {in_con.name}.")
            return None
        else:
            # Otherwise
            print(f"{self.name} now is {in_con.name}.")
            self.conditions[in_con.id] = in_con
            return in_con
            
    def remove_cond_man(self, del_id: int) -> Condition:
        """
        A function to remove a condition from a characer.  Input comes in the form of an integer, the id
        of the condition we want to delete.
        Parameters:
            del_id (int): The database id of the condition we want to delete.
        Returns:
            OUT (condition): Returns the removed condition if successful. Returns None if not.
        """
        temp = self.conditions.pop(del_id, None)  # Remove and return the condition if it exists
        if temp == None:
            print(f"{self.name} is not that conditon.")
        else: # We successfuly removed the condition.
            print(f"{self.name} is no longer {temp.name}.")
        return temp

    def add_to_inventory(self, in_inst: Equipment, in_quantity: int)->bool:
        """
        A function to add a piece of equipment to the character's inventory.
        Parameters:
            in_inst (Equipment): An instance of the Equipment class or one of it's children
            in_quantity (int): An integer representing the quantity of that Equipment class
                to be added
        Returns:
            OUT (Tuple[bool, int]): True if the objects was already in the instance, False if it was not.  The
                second element of the tuple is the new quantity.
        """
        # We define an interior function to help us update lists
        def add_elements(inpt_lst: list, in_i: Equipment, in_q: int):
            """
            A function to add a piece of equipment to a list, either updating the quantity
            or adding a new entry.  Returns the updated list.  Interior function.
            Parameters:
                inpt_lst (list): The inventory list we wish to update.
                in_i (Equipment): The ingoing Equipment instance.
                in_q (in_q): The quantity of "in_i" we want to add.
            Returns:
                OUT (Tuple[bool, int, List[Tuple[Equipment, int]]]): A tuple.  
                    The first part of the tuple is whether the object was found in the list.  
                    The second part is updated quantity.  The third one is the new list.
            """
            found, idx = find_in_first_entries(inpt_lst, in_i.id)
            if found:
                inpt_lst[idx][1] += in_q
                n_qnty: int = inpt_lst[idx][1]
            else:
                inpt_lst.append([in_i, in_q])
                n_qnty :int = in_q
            return found, n_qnty, inpt_lst
        
        exists, new_qnty, self.main_inv = add_elements(self.main_inv, in_inst, in_quantity)
        # Then check the weapon list
        if isinstance(in_inst, Weapon):
            self.weapon_inv = add_elements(self.weapon_inv, in_inst, in_quantity)[2] # want the third element of the 
            # tuple
        # check the armor inventory
        if isinstance(in_inst, Armor):
            self.armor_inv = add_elements(self.armor_inv, in_inst, in_quantity)[2]
        # check the container inventory
        if isinstance(in_inst, Container):
            self.container_inv = add_elements(self.container_inv, in_inst, in_quantity)[2]
        # check the clothing inventory
        if isinstance(in_inst, Clothing):
            self.clothing_inv = add_elements(self.container_inv, in_inst, in_quantity)[2]
        return exists, new_qnty

    def remove_from_inventory(self, item_id: int, del_qty: int)->bool:
        """
        A function to remove an item from a character's inventory.
        Parameters:
            item_id (int): The id of the item we want to remove.
            del_qty (int): The quantity of the item we want to remove.
        Raises:
            ValueError: Object is not found in inventory.
        Returns:
            OUT (Tuple[bool, int]): False if the object line was deleted, True if not.  The second element is the remaining quantity
        """
        # search for the id in the index
        def delete_elements(in_list: List[Tuple[Equipment, int]], in_i: int, in_qty: int):
            """
            List must be of 2 element tuples. An internal function.
            Parameters:
                in_list (List[Tuple[Equipment, int]]): An inventory list.
                in_i (int): the id of the object we are looking for
                in_qty (int): the quantity we want to remove
            Returns:
                OUT (Tuple[bool, int, Tuple[Equipment, int]]): The first element of the tuple is wether the object still exists in
                    the inventory (True) or not (False).  The second element is is the updated quanitity.  The third
                    is the updated list.
            """
            ex = True #initialise exist
            n_qty = -1 # initillize this as -1, will only return this if the object is not in the inventory
            found, idx = find_in_first_entries(in_list, in_i)
            if found:
                in_list[idx][1] -= in_qty # calculate our new quantity
                n_qty = in_list[idx][1]
                if in_list[idx][1] <= 0: # check if the quantity is zero
                    in_list.pop(idx) # if it is zero, remove the element
                    ex = False # set exists to false
            return ex, n_qty, in_list # and return the list
        
        exists, new_qnty, self.main_inv = delete_elements(self.main_inv, item_id, del_qty) # Check main inventory
        self.weapon_inv = delete_elements(self.weapon_inv, item_id, del_qty)[2] # Check weapon inventory
        self.armor_inv = delete_elements(self.armor_inv, item_id, del_qty)[2] # Check armor inventory
        self.container_inv = delete_elements(self.container_inv, item_id, del_qty)[2] # Check contianer inventory
        self.clothing_inv = delete_elements(self.clothing_inv, item_id, del_qty)[2] # Check clothing inventory
        return exists, new_qnty

    def search_inventory(self, in_id: int):
        """
        A function that searches the inventory for a specific id.
        Parameters:
            in_id (int): The id of the equipment we are searching for.
        Returns:
            OUT (bool): If the equipment is in the list or not.
        """
        # we first create an list of all equipment id's
        id_list = [eq.id for eq, _ in self.main_inv]
        if in_id in id_list:
            return True
        else:
            return False

    def add_condition(self, base: list[Condition]) -> Condition:
        """
        A function to add data to a list using a tkinter window.
        Parameters:
            base (list[Condition]): a list of Condition objects defined over in the sidekick data update
                file. Usualy contains all the pre-defined condition objects.
        Returns:
            output (Condition): Returns the Condition if successfuly added. Returns None if not.
        """
        output = None # initialize output
        # Preprocess the base list into a dictionary for fast lookups--faster than a linear search
        # We use the name as the dictionary key since that is what will be used in the entry box
        condition_map = {condition.name: condition for condition in base}
        # Filter out conditions that are already in self.conditions
        display_list = [condition.name for condition in base if condition.id not in self.conditions]

        # Define the add_check button
        def add_check(in_strv: tk.StringVar):
            nonlocal output
            c_name = in_strv.get()
            if c_name in condition_map:
                condition = condition_map[c_name]
                # We want to make sure we can't add the same condition twice
                if condition.id not in self.conditions: # We only add if the condition is not already current
                    output = self.add_cond_man(condition) # we now can add manual to the character.
                else:
                    error_box(f"{self.name} is already {condition.name}.")
            else:
                error_box("Invalid condition selected")
            pop.destroy() # Close the window here 

        # Create the pop-up window
        pop = tk.Toplevel()
        pop.title("Add A Condition")
        pop.geometry('350x250')
        
        # Label creation
        poplabel = tk.Label(pop,
                            text = "Select Condition :",
                            **LABEL_OP_NOR)
        poplabel.pack(padx = 15, pady = 5)
        
        # then create the menu
        choice = tk.StringVar()
        conchosen = ttk.Combobox(pop, width = 20, textvariable = choice)
        conchosen['values'] = display_list
        conchosen.pack(pady = 5)
        
        # and the button to return the value of the menu
        but = tk.Button(pop,
                        text = "Confirm Choice",
                        command = lambda c = choice: add_check(c),
                        width = 15,
                        **BUTTON_OPTIONS_BLUE)
        but.pack()
        
        pop.grab_set()  # Makes popup modal (forces user to interact with it first)
        pop.wait_window()  # Pauses execution until popup is closed
        return output # Finaly return the output when finshed

    def remove_condition(self, base: list[Condition])->Condition:
        """
        A function to remove a condition from a list using a tkinter window.
        Parameters:
            base (list[Condition]): a list of Condition objects defined in another window
        Returns:
            output (Condition): Returns the Condition if it is removed. Returns None if not.
        """
        output = None
        # Preprocess the base list into a dictionary for fast lookups--faster than a linear search
        condition_map = {condition.name: condition for condition in base}
        # Filter out conditions that are already in self.conditions
        display_list = [cond.name for cond in self.conditions.values()] # access the values of the condition dict

        # Define the rem_check button
        def rem_check(in_strv: tk.StringVar):
            nonlocal output
            c_name = in_strv.get()
            if c_name in condition_map:
                condition = condition_map[c_name]
                output = self.remove_cond_man(condition.id) # We use the handy previously defined function
            else:
                error_box("Invalid condition selected")
            pop.destroy() # Close the window

        # Create the pop-up window
        pop = tk.Toplevel()
        pop.title("Remove a Condition")
        pop.geometry('350x250')

        # Label creation
        poplabel = tk.Label(pop,
                            text = "Select Condition :",
                            **LABEL_OP_NOR)
        poplabel.pack(padx = 15, pady = 5)

         # then create the menu
        choice = tk.StringVar()
        conchosen = ttk.Combobox(pop, width = 20, textvariable = choice)
        conchosen['values'] = display_list
        conchosen.pack(pady = 5)
        
        # and the button to return the value of the menu
        but = tk.Button(pop,
                        text = "Confirm Choice",
                        command = lambda c = choice: rem_check(c),
                        width = 15,
                        **BUTTON_OPTIONS_BLUE)
        but.pack()

        pop.grab_set()  # Makes popup modal (forces user to interact with it first)
        pop.wait_window()  # Pauses execution until popup is closed
        return output # return the output

    def add_spell(self, spell_inst: Spell) -> bool:
        """
        A function to add a spell to the characters spell dictionary.
        Parameters:
            spell_inst (Spell): The spell we are trying to add to the character's spell list. Is a
                Spell or child instance.
        Returns:
            OUT (bool): True if the spell was added, False if it was not added.
        """
        # We will first want to check if the spell is already in the inventory. If it 
        # isn't, we will add it to the dictionary.
        if spell_inst.id not in self.spell_list.keys():
            self.spell_list[spell_inst.id] = spell_inst # Insert the spell instance
            # Now we need to check if it is an attack spell or not
            if isinstance(spell_inst, Attack_Spell):
                self.atk_spell_list.append(spell_inst.id) # we add the id to the attack spell list.
            return True
        else:
            error_box("Spell already known/prepared!")
            return False
        
    def remove_spell(self, spell_id: int) -> bool:
        """
        A function to remove a spell from the character's inventory.
        Parameters:
            spell_id (int): The id of the spell we are removing.
        Returns:
            OUT (bool): True if the spell was removed, False if a KeyError occured.
        """
        removed_spell = self.spell_list.pop(spell_id, None)  # Returns None if key is missing
        if isinstance(removed_spell, Spell):
            # we now need to check if the spell was an attack spell or not
            if isinstance(removed_spell, Attack_Spell):
                self.atk_spell_list.remove(spell_id) # if it is a attack_spell, you remove it from the spell list
            return True
        else:
            error_box(f"Spell of id {spell_id} not found in known/prepared spells!")
            return False

    def adjust_spell_slots(self, spell_level: int, in_bool: bool):
        """
        A function to adjust the carachter's spell slot inventory.
        Paramaters:
            spell_level (int): The level of the spell we are casting.
            in_bool (bool): Are we using a spell slot (True) or gaining a spell slot (False).
        """
        # remember, we only want to adjust the first element in the pair, since that's the current spell
        # slots.
        if in_bool:
            self.spell_slots[spell_level][0] += -1
        else:
            self.spell_slots[spell_level][0] += 1
##########################################################################################



