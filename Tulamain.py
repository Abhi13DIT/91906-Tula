# -----------------------------------Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
from datetime import date

# Allows me to customise buttons because its limited on macOS
from tkmacosx import Button

# SQLite database
from database import (
    get_all_meals,
    get_meal_by_name,
    get_todays_logged_meals,
    get_meal_by_id,
    log_meal_to_database,
    get_todays_meal_details,
    get_recipes_by_dietary_preference
)
# ------------------------------------Variables

# Storing today's date
last_opened_date = date.today()

# Setting colours
theme = "#be3719"
button_colour = "#FFF380"
overbg_colour = "#FBB117"

# Dictionary for reading form input
user_profile = {}

# Daily totals for nutrition tracker
total_calories = 0
total_protein = 0
total_carbs = 0
total_fat = 0

# Macro goals for nutrition tracker
goal_kcal = 0
goal_protein = 0
goal_carbs = 0
goal_fat = 0

# Storing name variable
name_store = ""

# Varibale for choosing meal when logging
selected_meal = None

# List for "Todays logged meals"
logged_meals = []

# ------------------------------------Setup
window = tk.Tk()
window.title("Tula - South Asian Nutrition tracker")
window.geometry("470x850")
window.configure(bg=theme) 

# Creating style variable to customise Progress bars and Comboboxes
style = ttk.Style()
style.theme_use('clam')

style.configure(
    "TCombobox",
    fieldbackground="#212529",
    foreground="white",
    padding=5
)

style.map(
    "TCombobox",
    fieldbackground=[("readonly", "#212529")],
    foreground=[("readonly", "white")]
)

style.configure(
    "Tracker.Horizontal.TProgressbar",
    troughcolor="black",
    background="#FFF380",
    thickness= 40
)
# -----------------------------------Functions

# Storing form input

# Checking to see if goal values need to be reset for the day
def check_new_day():
    global last_opened_date
    global total_calories, total_protein, total_carbs, total_fat
    global logged_meals

    today = date.today()

    # If today isn't the same as the date when the user last opened the program, reset values
    if today != last_opened_date:
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0

        logged_meals.clear()

        last_opened_date = today

        update_nutrition_tracker()

"""This file reads the form input and calculates macronutrient goals for nutrition tracker"""       
def read_input():
    global name_store

    name_store = name_entry.get()
    age_string = age_entry.get()
    gender_store = gender_entry.get()
    weight_string = weight_entry.get()
    height_string = height_entry.get()
    activity_store = activity_entry.get()
    goal_store = goal_entry.get()
    dietary_store = dietary_entry.get()
 
    if (
        name_store == ""
        or age_string == ""
        or gender_store == ""
        or weight_string == ""
        or height_string == ""
        or activity_store == ""
        or goal_store == ""
        or dietary_store == ""
    ):
        show_error("Please fill in every box")
        return

    age_store=int(age_string)
    weight_store=int(weight_string)
    height_store=int(height_string)

    print(name_store, age_store, gender_store, weight_store, height_store, activity_store, goal_store, dietary_store) 

    # Dictionary values
    user_profile["name"] = name_store
    user_profile["age"] = age_store
    user_profile["gender"] = gender_store
    user_profile["weight"] = weight_store
    user_profile["height"] = height_store
    user_profile["activity"] = activity_store
    user_profile["goal"] = goal_store
    user_profile["dietary"] = dietary_store
    
    # Boundary values error messages
    if len(name_store) < 1 or len(name_store) > 30:
        show_error("Name must be between 1 and 30 characters")
        return

    if age_store < 13 or age_store > 120:
        show_error("Age must be between 13 and 120")
        return

    if weight_store < 30 or weight_store > 300:
        show_error("Weight must be between 30kg and 300kg")
        return

    if height_store < 100 or height_store > 270:
        show_error("Height must be between 100cm and 270cm")
        return

    # Calculating Basal Metabolic Rate
    if gender_store == "Male":
        BMR = 10*weight_store + 6.25*height_store -5*age_store + 5
        print("BMR =", BMR)
    else:
        BMR = 10*weight_store + 6.25*height_store -5*age_store - 161
        print("Basal Metabolic Rate =", BMR)

    # Calculating total daily energy expenditure
    if activity_store == "Sedentary (little to no exercise)": 
        TDEE = BMR*1.2
        TDEE = round(TDEE, 0)
        print("Total daily energy expenditure =", TDEE)
    elif activity_store == "Light (1-3 days/week)": 
        TDEE = BMR*1.375
        TDEE = round(TDEE, 0)
        print("Total daily energy expenditure =", TDEE)
    elif activity_store == "Moderate (3-5 days/week)": 
        TDEE = BMR*1.55
        TDEE = round(TDEE, 0)
        print("Total daily energy expenditure =", TDEE)
    elif activity_store == "Intense (6-7 days/week)": 
        TDEE = BMR*1.725
        TDEE = round(TDEE, 0)
        print("Total daily energy expenditure =", TDEE)
    elif activity_store == "Athlete (2x per day)":
        TDEE = BMR*1.9
        TDEE = round(TDEE, 0)
        print("Total daily energy expenditure =", TDEE)

    # Creating nutrition goals based on user goal
    if goal_store == "Improving general health":
        kcal_multiplier = 1.0
        protein_multiplier = 0.8

    if goal_store == "Losing weight":
        kcal_multiplier = 0.85
        protein_multiplier = 1.8

    elif goal_store == "Gaining weight":
        kcal_multiplier = 1.15
        protein_multiplier = 1.6

    elif goal_store == "Maintaining weight":
        kcal_multiplier = 1.0
        protein_multiplier = 1.0

    elif goal_store == "Build muscle":
        kcal_multiplier = 1.08
        protein_multiplier = 2.0

    global goal_kcal
    global goal_protein
    global goal_fat
    global goal_carbs
    
    goal_kcal = round(TDEE * kcal_multiplier, 0)
    goal_protein = round(weight_store * protein_multiplier, 0)
    goal_fat = round((goal_kcal * 0.25) / 9, 0)
    goal_carbs = round((goal_kcal - goal_protein * 4 - goal_fat * 9) / 4,0)

    print("Daily calorie goal (kcal):", goal_kcal)
    print("Daily protein goal (g):", goal_protein)
    print("Daily carbohydrate goal (g):", goal_carbs)
    print("Daily fat goal (g):", goal_fat)

    go_to_home()

# Adding the dietary preferences to the meals
def get_dietary_labels(recipe):
    labels = []

    if recipe[9] == 1:
        labels.append("Vegetarian")

    if recipe[10] == 1:
        labels.append("Vegan")

    if recipe[11] == 1:
        labels.append("Halal")

    if recipe[12] == 1:
        labels.append("Gluten-Free")

    return " • ".join(labels)

def load_recipes():
    # Remove old widget buttons
    for widget in recipe_list_frame.winfo_children():
        widget.destroy()

    # Get user's dietary preference
    dietary_preference = user_profile.get("dietary", "No preference")

    recipe_subtext.config(
        text=f"Recipes suitable for: {dietary_preference}"
    )

    # Get recipes from database
    recipes = get_recipes_by_dietary_preference(
        dietary_preference
    )

    # Create a button for each recipe
    for row, recipe in enumerate(recipes):

        recipe_button = Button(
            recipe_list_frame,
            text=recipe[1],
            font=("Kefa", 18, "bold"),
            bg=button_colour,
            fg="black",
            width=250,
            height=50,
            relief="flat",
            command=lambda r=recipe: show_recipe_popup(r)
        )
        recipe_button.grid(
            row=row,
            column=0,
            padx=20,
            pady=15
        )
        
# Creating a popup window for the recipes     
def show_recipe_popup(recipe):

    popup = tk.Toplevel(window)
    popup.title(recipe[1])
    popup.geometry("600x700")
    popup.configure(bg=theme)

    # Recipe name
    title = tk.Label(
        popup,
        text=recipe[1],
        font=("Chalkduster", 40, "bold"),
        bg=theme
    )
    title.pack(pady=(20, 5))

    # Dietary information
    dietary_label = tk.Label(
        popup,
        text=get_dietary_labels(recipe),
        font=("Kefa", 16),
        bg=theme,
        fg="white"
    )
    dietary_label.pack(pady=(0, 20))

    # Nutrition heading
    nutrition_heading = tk.Label(
        popup,
        text="Nutrition per serving",
        font=("Kefa", 25, "bold"),
        bg=theme
    )
    nutrition_heading.pack()

    # Nutrition information
    nutrition_text = (
        f"Calories: {recipe[5]} kcal\n"
        f"Protein: {recipe[6]} g\n"
        f"Carbohydrates: {recipe[7]} g\n"
        f"Fat: {recipe[8]} g"
    )

    nutrition_label = tk.Label(
        popup,
        text=nutrition_text,
        font=("Kefa", 17),
        bg=theme,
        justify="left"
    )
    nutrition_label.pack(pady=10)

    # Ingredients heading
    ingredients_heading = tk.Label(
        popup,
        text="Ingredients",
        font=("Kefa", 25, "bold"),
        bg=theme
    )
    ingredients_heading.pack(pady=(20, 5))

    # Ingredients
    ingredients_label = tk.Label(
        popup,
        text=recipe[13],
        font=("Kefa", 17),
        bg=theme,
        wraplength=500,
        justify="left"
    )
    ingredients_label.pack(padx=30)

    # Instructions heading
    instructions_heading = tk.Label(
        popup,
        text="Instructions",
        font=("Kefa", 25, "bold"),
        bg=theme
    )
    instructions_heading.pack(pady=(20, 5))

    # Instructions
    instructions_label = tk.Label(
        popup,
        text=recipe[14],
        font=("Kefa", 17),
        bg=theme,
        wraplength=500,
        justify="left"
    )
    instructions_label.pack(padx=30)

    # Close button
    close_button = Button(
        popup,
        text="Close",
        width=100,
        height=50,
        bg=button_colour,
        font=("Kefa", 18, "bold"),
        command=popup.destroy
    )
    close_button.pack(pady=20)
    
# Moving between frames
def back_button(frame, destination):
    return Button(
    frame,
    text="Back",
    font=("Kefa", 15, "bold"),
    width=60,
    height=30,
    bg=button_colour,
    overbackground="#FBB117",
    command=destination
    )

def go_to_intro():
    preform_frame.pack_forget()
    about_frame.pack_forget()
    intro_frame.pack(fill="both", expand=True)

def go_to_about():
    intro_frame.pack_forget()
    about_frame.pack(fill="both", expand=True)

def go_to_preform():
    intro_frame.pack_forget()
    form_frame.pack_forget()
    preform_frame.pack(fill="both", expand=True)

def go_to_form():
    preform_frame.pack_forget()
    form_frame.pack(fill="both", expand=True)

def go_to_home():
    # Update home screen with dictionary data
    home_label.config(text=f"Hi {user_profile.get('name')},")

    # Frame switching
    form_frame.pack_forget()
    nutrition_frame.pack_forget()
    recipe_frame.pack_forget()
    help_frame.pack_forget()
    home_frame.pack(fill="both", expand=True)

def go_to_nutrition():
    home_frame.pack_forget()
    log_frame.pack_forget()
    
    load_today_nutrition()
    update_nutrition_tracker()
    
    nutrition_frame.pack(fill="both", expand=True)

def go_to_log():
    nutrition_frame.pack_forget()
    log_frame.pack(fill="both", expand=True)
    
    # Getting all meals from database.py
    meals = get_all_meals()
    
    # Takes meal names and puts it into a dropdown 
    meal_names = []

    for meal in meals:
        meal_names.append(meal[1])

    meal_dropdown["values"] = meal_names
    

def go_to_recipes():
    home_frame.pack_forget()

    load_recipes()
    
    recipe_frame.pack(fill="both", expand=True)

def go_to_help():
    home_frame.pack_forget()
    help_frame.pack(fill="both", expand=True)

# When meal is selected meal nutrition is displayed
def display_nutrition(event):
    global selected_meal

    meal_name = meal_dropdown.get()
    selected_meal = get_meal_by_name(meal_name)

    meal_info.config(
        text=f"Calories: {selected_meal[5]} kcal\n"
             f"Protein: {selected_meal[6]} g\n"
             f"Carbs: {selected_meal[7]} g\n"
             f"Fat: {selected_meal[8]} g"
    )

# Updating totals when meal is logged
def log_selected_meal():
    global selected_meal
    
    if selected_meal is None:
        messagebox.showwarning(
            "No meal selected",
            "Please choose a meal before clicking 'Log Meal'.")
        return
    
    # Adding meal to "Today's Logged Meals"
    logged_meals.append(selected_meal[1])
    
    global total_calories
    global total_protein
    global total_carbs
    global total_fat

    # Updating macros based on meal logged
    total_calories += selected_meal[5]
    total_protein += selected_meal[6]
    total_carbs += selected_meal[7]
    total_fat += selected_meal[8]

    print(total_calories, total_protein, total_carbs, total_fat)
    log_meal_to_database(selected_meal[0], name_store)
    
    update_nutrition_tracker()
    go_to_nutrition()


def load_today_nutrition():
    global total_calories
    global total_protein
    global total_carbs
    global total_fat

    # Reset totals
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    logged_meals = get_todays_logged_meals(name_store)

    for meal in logged_meals:
        meal_data = get_meal_by_id(meal[0])

        if meal_data:
            total_calories += meal_data[5]
            total_protein += meal_data[6]
            total_carbs += meal_data[7]
            total_fat += meal_data[8]

    update_nutrition_tracker()

# Updating nutrition tracker
def update_nutrition_tracker():
    calories_tracker.config(text=f"Calories: {total_calories} / {goal_kcal} kcal")
    protein_tracker.config(text=f"Protein: {total_protein}/ {goal_protein} g")
    carbs_tracker.config(text=f"Carbs: {total_carbs}/ {goal_carbs} g")
    fat_tracker.config(text=f"Fat: {total_fat}/ {goal_fat} g")

    if goal_kcal > 0:
        calories_bar["value"] = min((total_calories / goal_kcal) * 100, 100)

    if goal_protein > 0:
        protein_bar["value"] = min((total_protein / goal_protein) * 100, 100)

    if goal_carbs > 0:
        carbs_bar["value"] = min((total_carbs / goal_carbs) * 100, 100)

    if goal_fat > 0:
        fat_bar["value"] = min((total_fat / goal_fat) * 100, 100)

def show_logged_meals():
    
    # Creating a popup to show Today's Logged meals
    popup = tk.Toplevel()
    popup.title("Today's Logged Meals")
    popup.geometry("300x300")

    title = tk.Label(
        popup,
        text="Today's Logged Meals",
        font=("Kefa", 18, "bold")
    )
    title.pack(pady=10)

    meals = get_todays_meal_details(name_store)
    
    if len(meals) == 0:
        meals_text = "No meals logged yet."
    else:
        meals_text = ""
        for i, meal in enumerate(meals, start=1):
            meals_text += f"{i}. {meal[1]}\n"

    meals_label = tk.Label(
        popup,
        text=meals_text,
        font=("Kefa", 14),
        justify="left"
    )
    meals_label.pack(padx=10, pady=10)
    
# Validation checks
def is_alpha(proposed_value):
    if proposed_value=="": return True
    for char in proposed_value:
        if not (char.isalpha() or char == " " or char == "-" or char == "'"): return False
    return True

def is_int(proposed_value):
    if proposed_value=="": return True
    try:
        int(proposed_value); return True
    except ValueError:
        return False
    
# Invalid input callbacks
def show_error(message):
    lbl_error.config(text=message)
    window.after(2000, lambda: lbl_error.config(text=''))

def on_invalid_alpha():
    show_error("Please use letters, spaces, hyphens, and apostrophes")

def on_invalid_int():
    show_error("Please only use whole numbers (e.g 38)")    

# ----------------Variables for alphabet and integer checks
vcmd_alpha = window.register(is_alpha)
ivcmd_alpha = window.register(on_invalid_alpha)
vcmd_int = window.register(is_int)
ivcmd_int = window.register(on_invalid_int)  

# ----------------------------Intro Screen
intro_frame = tk.Frame(window, bg=theme)

title = tk.Label(intro_frame, text=("Tula"), font=("Chalkduster", 120, "bold"), bg=theme).pack(pady=40)

get_started = Button(
    intro_frame,
    text="Get started",
    font=("Kefa", 20, "bold"),
    width=250,
    height=55,
    bg=button_colour,
    overbackground=overbg_colour,
    command=go_to_preform
    ).pack(pady=60)

about_us = Button(
    intro_frame,
    text="About Us",
    font=("Kefa", 20, "bold"),
    width=250,
    height=55,
    bg=button_colour,
    overbackground=overbg_colour,
    command=go_to_about
    ).pack()

intro_frame.pack(fill="both", expand=True)
# ----------------------------------------------------------------About Me screen
about_frame = tk.Frame(window, bg=theme)

# Setting the grid to only one column so everything can be centered 
about_frame.grid_columnconfigure(0, weight=1)

tk.Label(about_frame, text="About Us", font=("Chalkduster", 50, "bold"), bg=theme).grid(row=1, column=0, sticky="ew", pady=20)
tk.Label(about_frame, text="Hi, I'm Abhi!", font=("Chalkduster", 20), bg=theme).grid(row=2, column=0, sticky="ew", pady=20)
tk.Message(about_frame,text= "As a South Asian student in New Zealand, I have noticed that while there are many nutrition tracking tools out there, most of them are only focused on Western diets. "
    "With recipe recommendations like popcorn and pot-pies, South Asians are left making food they don’t enjoy, or resorting back to old, unhealthy eating habits. "
    "For my digital technologies project, I have used this opportunity to come up with a solution; a nutrition tracking program that caters directly to South Asian diets.", font=("Kefa", 15), bg=theme, width=300).grid(row=3, column=0, sticky="ew", pady=10)
tk.Message(about_frame, text="The name, Tula, means balance in Sanskrit, representing the nutritional balance that can be found for South Asians through using this program. "
    "From the design, to the recipe recommendations, to the dietary preference considerations, South Asians can find a space where they can comfortably change diet habits and experience real progress!", font=("Kefa", 15), bg=theme, width=300).grid(row=4, column=0, sticky="ew", pady=10)

# Back button
about_back = back_button(about_frame, go_to_intro)
about_back.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

# ----------------------------------------------------------------Pre-form screen
preform_frame = tk.Frame(window, bg=theme)

# Setting the grid to only one column so everything can be centered 
preform_frame.grid_columnconfigure(0, weight=1)

preform = tk.Label(preform_frame, text="Your privacy", font=("Chalkduster", 55, "bold"), bg=theme).grid(row=1, column=0, sticky="ew",  pady=20)

tk.Message(preform_frame, text=" The next step to using Tula is to fill out a short form so that we can set specific nutrition goals for your tracker and know what South Asian recipe recommendations are relevant to you."
    "We understand that this requires sharing some private information, so we ensure that information you give us will be used only for these two purposes and will not be shared externally. "
    "We also understand that you may not want to share personal details and there is the option to continue without filling the form. "
    "This pathway will mean that you will not have set specific nutrition goals, however you will still be able to view South Asian recipe recommendations. ", font=("Kefa", 15), bg=theme, width=350).grid(row=3, column=0, sticky="ew", pady=(10, 50))
            
to_form = Button(
    preform_frame,
    text="Proceed to form",
    font=("Kefa", 20, "bold"),
    width=250,
    height=55,
    bg=button_colour,
    overbackground="#FBB117",
    command=go_to_form
    )
to_form.grid(row=7, column=0, pady=15)

# Back button
preform_back = back_button(preform_frame, go_to_intro)
preform_back.grid(row=0, column=0, columnspan=2, sticky="nw", padx=10, pady=10)

# ----------------------------------------------------------------Form screen

form_frame = tk.Frame(window, bg=theme)

# Setting the grid to only one column so everything can be centered
form_frame.grid_columnconfigure(0, weight=1)

# Form page title
form_label = tk.Label(
    form_frame,
    text="Form",
    font=("Chalkduster", 55, "bold"),
    bg=theme
)
form_label.grid(row=0, column=0, padx=10, pady=(20, 25))

input_frame = tk.Frame(form_frame, bg=theme)
input_frame.grid(row=1, column=0, pady=8)

# Asking for name
tk.Label(input_frame, text="Name:", bg=theme).grid(row=0, column=0, padx=(0, 15), pady=15)
name_entry = tk.Entry(input_frame, validate="key", validatecommand=(vcmd_alpha, "%P"), invalidcommand=ivcmd_alpha, width=25)
name_entry.grid(row=0, column=1)

# Asking for age
tk.Label(input_frame, text="Age:", bg=theme).grid(row=1, column=0, padx=(0, 15), pady=15)
age_entry = tk.Entry(input_frame, validate="key", validatecommand=(vcmd_int, "%P"), invalidcommand=ivcmd_int, width=25)
age_entry.grid(row=1, column=1)

# Asking for gender
tk.Label(input_frame, text="Biological sex:", bg=theme).grid(row=2, column=0, padx=(0, 15), pady=15)
gender = tk.StringVar()
gender_entry = ttk.Combobox(input_frame, width=23, textvariable=gender, state="readonly", style="TCombobox")

gender_entry["values"] = ("Male", "Female")
gender_entry.grid(row=2, column=1)
gender_entry.current()

# Asking for weight
tk.Label(input_frame, text="Weight (in kg):", bg=theme).grid(row=3, column=0, padx=(0, 15), pady=15)
weight_entry = tk.Entry(input_frame, validate="key", validatecommand=(vcmd_int, "%P"), invalidcommand=ivcmd_int, width=25)
weight_entry.grid(row=3, column=1)

# Asking for height
tk.Label(input_frame, text="Height (in cm):", bg=theme).grid(row=4, column=0, padx=(0, 15), pady=15)
height_entry = tk.Entry(input_frame, validate="key", validatecommand=(vcmd_int, "%P"), invalidcommand=ivcmd_int, width=25)
height_entry.grid(row=4, column=1)

# Asking for activity level
tk.Label(input_frame, text="Activity level:", bg=theme).grid(row=5, column=0, padx=(0, 15), pady=15)
activity = tk.StringVar()
activity_entry = ttk.Combobox(input_frame, width=23, textvariable=activity, state="readonly", style="TCombobox")

activity_entry["values"] = ('Sedentary (little to no exercise)', 'Light (1-3 days/week)', 'Moderate (3-5 days/week)', 'Intense (6-7 days/week)', 'Athlete (2x per day)')
activity_entry.grid(row=5, column=1)
activity_entry.current()

# Asking for goal
tk.Label(input_frame, text="Health goal:", bg=theme).grid(row=6, column=0, padx=(0, 15), pady=15)
goal = tk.StringVar()
goal_entry = ttk.Combobox(input_frame, width=23, textvariable=goal, state="readonly", style="TCombobox")

goal_entry["values"] = ('Improving general health', 'Losing weight', 'Gaining weight', 'Maintaining weight', 'Build muscle')
goal_entry.grid(row=6, column=1)
goal_entry.current()

# Asking for dietary preference
tk.Label(input_frame, text="Dietary preference:", bg=theme).grid(row=7, column=0, padx=(0, 15), pady=15)
dietary = tk.StringVar()
dietary_entry = ttk.Combobox(input_frame, width=23, textvariable=dietary, state="readonly", style="TCombobox")

dietary_entry["values"] = ('Vegetarian', 'Vegan', 'Halal', 'Gluten-Free', 'No preference')
dietary_entry.grid(row=7, column=1)
dietary_entry.current()

# Label error initial
lbl_error = tk.Message(form_frame, text='', font=("Helvetica", 14, "bold"), fg="white", bg=theme, width=450)
lbl_error.grid(row=9, column=0)
                     
submit_button = Button(
    form_frame,
    text="Submit form",
    font=("Kefa", 18, "bold"),
    width=250,
    height=50,
    bg="#FFF380",
    overbackground="#FBB117",
    command=lambda: read_input()
)
submit_button.grid(row=10, column=0, pady=15)

# Back button
form_back = back_button(form_frame, go_to_preform)
form_back.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

# --------------------------------------------Home Screen
home_frame = tk.Frame(window, bg=theme)

# Setting the grid to only one column so everything can be centered 
home_frame.grid_columnconfigure(0, weight=1)

# Home page title
home_label = tk.Label(home_frame, text="", font=("Chalkduster", 50, "bold"), bg=theme)
home_label.grid(row=0, column=0, padx=10, pady=(50, 35))

home_subtext = tk.Label(home_frame, text="What would you like to view?", font=("Kefa", 25, "bold"), bg=theme)
home_subtext.grid(row=1, column=0, padx=10, pady=(20, 40))

nutrition_tracker = Button(
    home_frame,
    text="Nutrition tracker",
    font=("Kefa", 20, "bold"),
    width=250,
    height=55,
    bg=button_colour,
    overbackground="#FBB117",
    command=go_to_nutrition
    )
nutrition_tracker.grid(row=2, column=0, pady=20)

recipes = Button(
    home_frame,
    text="Recipes",
    font=("Kefa", 20, "bold"),
    width=250,
    height=55,
    bg=button_colour,
    overbackground="#FBB117",
    command=go_to_recipes
    )
recipes.grid(row=3, column=0, pady=20)

help = Button(
    home_frame,
    text="Help",
    font=("Kefa", 20, "bold"),
    width=250,
    height=55,
    bg=button_colour,
    overbackground="#FBB117",
    command=go_to_help
    )
help.grid(row=4, column=0, pady=20)

# ----------------------------Nutrition tracker Screen
nutrition_frame = tk.Frame(window, bg=theme)

# Setting the grid to only one column so everything can be centered 
nutrition_frame.grid_columnconfigure(0, weight=1)

# Nutrition page title
nutrition_label = tk.Label(nutrition_frame, text="Nutrition tracker", font=("Chalkduster", 45, "bold"), bg=theme)
nutrition_label.grid(row=1, column=0, padx=10, pady=20)

# Text for macro tracker
calories_tracker = tk.Label(nutrition_frame, text=f"Calories: {total_calories}/{goal_kcal} kcal", font=("Kefa", 18, "bold"), bg=theme)
calories_tracker.grid(row=2, column=0, padx=10, pady=20)
protein_tracker = tk.Label(nutrition_frame, text=f"Protein: {total_protein}/{goal_protein} g", font=("Kefa", 18, "bold"), bg=theme)
protein_tracker.grid(row=4, column=0, padx=10, pady=20)
carbs_tracker = tk.Label(nutrition_frame, text=f"Carbohydrates: {total_carbs}/{goal_carbs} g", font=("Kefa", 18, "bold"), bg=theme)
carbs_tracker.grid(row=6, column=0, padx=10, pady=20)
fat_tracker = tk.Label(nutrition_frame, text=f"Fat: {total_fat}/{goal_fat} g", font=("Kefa", 18, "bold"), bg=theme)
fat_tracker.grid(row=8, column=0, padx=10, pady=20)

calories_bar = ttk.Progressbar(nutrition_frame, length=300, maximum=100, style="Tracker.Horizontal.TProgressbar")
calories_bar.grid(row=3, column=0, padx=10)
protein_bar = ttk.Progressbar(nutrition_frame, length=300, maximum=100, style="Tracker.Horizontal.TProgressbar")
protein_bar.grid(row=5, column=0, padx=10)
carbs_bar = ttk.Progressbar(nutrition_frame, length=300, maximum=100, style="Tracker.Horizontal.TProgressbar")
carbs_bar.grid(row=7, column=0, padx=10)
fat_bar = ttk.Progressbar(nutrition_frame, length=300, maximum=100, style="Tracker.Horizontal.TProgressbar")
fat_bar.grid(row=9, column=0, padx=10)

log_a_meal = Button(
    nutrition_frame,
    text="Log a meal",
    font=("Kefa", 20, "bold"),
    width=250,
    height=55,
    bg=button_colour,
    overbackground="#FBB117",
    command=go_to_log
    )
log_a_meal.grid(row=10, column=0, pady=30)

nutrition_message = tk.Message(nutrition_frame, text="If you are over or under any of the goals by the end of the day, don't worry. "
         "This tracker is only a recommendation of the amount of macronutrients you should be consuming "
         "to achieve your health goal at a good pace, not a definite limit." , font=("Kefa", 13), bg=theme, width=390).grid(row=11, column=0, sticky="ew", padx=45)


nutrition_back = back_button(nutrition_frame, go_to_home)
nutrition_back.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

# ----------------------------Log meal Screen
log_frame = tk.Frame(window, bg=theme)

# Setting the grid to only one column so everything can be centered 
log_frame.grid_columnconfigure(0, weight=1)

# Log page title
log_label = tk.Label(log_frame, text="Log meal", font=("Chalkduster", 60, "bold"), bg=theme)
log_label.grid(row=1, column=0, padx=10, pady=20)

log_subtext = tk.Label(log_frame, text="What food would you like to log?", font=("Kefa", 20, "bold"), bg=theme)
log_subtext.grid(row=2, column=0, padx=10, pady=(20, 40))

# Dropdown to select meals to log
meal_dropdown = ttk.Combobox(
    log_frame,
    state="readonly",
    width=30,
    style="TCombobox"
)
meal_dropdown.grid(row=3, column=0)

meal_info = tk.Label(log_frame, text="", font=("Kefa", 20, "bold"), bg=theme)
meal_info.grid(row=4, column=0, padx=10, pady=(20, 40))

# When dropdown item selected, run display_nutrition function
meal_dropdown.bind(
    "<<ComboboxSelected>>",
    display_nutrition
)

log_selected_meal = Button(
    log_frame,
    text="Log selected meal",
    font=("Kefa", 20, "bold"),
    width=300,
    height=55,
    bg=button_colour,
    overbackground="#FBB117",
    command=log_selected_meal
    )
log_selected_meal.grid(row=9, column=0, pady=20)

see_meals = Button(
    log_frame,
    text="Today's logged meals",
    font=("Kefa", 20, "bold"),
    width=300,
    height=55,
    bg=button_colour,
    overbackground="#FBB117",
    command=show_logged_meals
    )
see_meals.grid(row=10, column=0, pady=20)

# Back button to nutrition page
log_back = back_button(log_frame, go_to_nutrition)
log_back.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

# ----------------------------Recipe Screen
recipe_frame = tk.Frame(window, bg=theme)

# Setting the grid so everything can be centered and ordered
recipe_frame.grid_rowconfigure(3, weight=1)
recipe_frame.grid_columnconfigure(0, weight=1)

# Recipe page title and subtext
recipe_title = tk.Label(recipe_frame, text="Recipes", font=("Chalkduster", 60, "bold"), bg=theme)
recipe_title.grid(row=1, column=0, padx=10, pady=20)

recipe_subtext  = tk.Label(recipe_frame, text="Recipes suitable for your dietary preference", font=("Kefa", 20, "bold"), bg=theme)
recipe_subtext.grid(row=2, column=0, padx=10, pady=(20, 40))

recipe_back = back_button(recipe_frame, go_to_home)
recipe_back.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

# Contains recipe buttons
recipe_list_frame = tk.Frame(recipe_frame, bg=theme) 
recipe_list_frame.grid(
    row=3,
    column=0,
    padx=20,
    pady=20,
    sticky="nsew"
)

# Centering buttons for the recipe options by making it all fit in column 0
recipe_list_frame.grid_columnconfigure(0, weight=1)

# ----------------------------Help Screen
help_frame = tk.Frame(window, bg=theme)

# Setting the grid to only one column so everything can be centered 
help_frame.grid_columnconfigure(0, weight=1)

# Help page title
help_label = tk.Label(help_frame, text="Help", font=("Chalkduster", 50, "bold"), bg=theme)
help_label.grid(row=1, column=0, padx=10, pady=20)

tk.Label(help_frame,text= "How to use the Nutrition tracker and Recipe features:", font=("Chalkduster", 15), bg=theme).grid(row=2, column=0, sticky="ew", pady=15)
tk.Message(help_frame,text= "Click on 'Nutrition tracker' where you will find progress bars that track your macronutrient intake."
           "Everytime you eat a meal, you can log it into the nutrition tracker by clicking on the dropdown list and selecting your meal. Then click 'Log meal'."
           "The progress bars will update. The Recipe page is where you will be able to try new healthy recipes. All visible recipes are catered "
           "to your dietary preferences! Click on a recipe and you will see all the nutrional information, ingredients and instructions!",
           font=("Kefa", 13), bg=theme, width=420).grid(row=3, column=0, sticky="ew")

tk.Label(help_frame, text="Commonly asked questions", font=("Chalkduster", 15), bg=theme).grid(row=4, column=0, sticky="ew", pady=15)
tk.Message(help_frame,text= "How do I view the meals I've eaten today? "
           "Once you are on the nutrition tracker page, clicked “log a meal”. From here, click a button called 'Today’s logged meals'. "
           "A popup should appear that lists everything you have eaten today. ",
           font=("Kefa", 13), bg=theme, width=420).grid(row=5, column=0, sticky="ew")

tk.Message(help_frame,text= "How is the nutrition tracker goals set up? "
           "Based on the information you gave us on the form, we were able to calculate what your calorie,"
           "protein, carbohydrate and fat goals should be to help you reach your health/body goal. "
           "The information you gave us was used solely to help us accurately calculate these goals. ",
           font=("Kefa", 13), bg=theme, width=422).grid(row=6, column=0, sticky="ew")

tk.Message(help_frame,text= "What does the nutrition tracker actually do? "
           "The nutrition tracker is a daily macronutrient goal progress checker for you to visualise how the food you eat is helping "
           "you progress towards your health goal. Every time you log a meal that you eat, Tula calculates the calories, protein, carbs "
           "and fat you gained from that meal and adds it to your daily tracker. The tracker’s progress bars are there to help you visualise the changes.",
           font=("Kefa", 13), bg=theme, width=422).grid(row=7, column=0, sticky="ew")

help_back = back_button(help_frame, go_to_home)
help_back.grid(row=0, column=0, sticky="nw", padx=10, pady=(10,0))
window.mainloop()
