#-----------------------------------Libraries
import tkinter as tk
from tkinter import ttk

#------------------------------------Variables
        
#------------------------------------Setup
window = tk.Tk()
window.title("Tula - South Asian Nutrition tracker")
window.geometry("470x700")
window.configure(bg="white")

#-----------------------------------Functions

#Storing form input
def read_input():
    name_store = name_entry.get()
    age_string = age_entry.get()
    gender_store = gender_entry.get()
    weight_string = weight_entry.get()
    height_string = height_entry.get()
    activity_store = activity_entry.get()
    goal_store = goal_entry.get()
    dietary_store = dietary_entry.get()

    if name_store=="" or age_string=="" or gender_store=="" or weight_string=="" or height_string=="" or activity_store=="" or goal_store=="" or dietary_store=="":
        show_error("Please fill in every box")
        return

    age_store=int(age_string)
    weight_store=int(weight_string)
    height_store=int(height_string)

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
    
    print(name_store, age_store, gender_store, weight_store, height_store, activity_store, goal_store, dietary_store)
    
#Moving between pages
def back_button(frame, destination):
    return tk.Button(
    frame,
    text="Back",
    font=("Chalkduster", 15, "bold"),
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

#Validation checks
def is_alpha(proposed_value):
    if proposed_value=="": return True
    for char in proposed_value:
        if not (char.isalpha() or char ==" " or char=="-" or char=="'"): return False
    return True

def is_int(proposed_value):
    if proposed_value=="": return True
    try:
        int(proposed_value); return True
    except ValueError:
        return False

#Invalid input Callbacks
def show_error(message):
    lbl_error.config(text=message)
    window.after(2000, lambda: lbl_error.config(text=''))

def on_invalid_alpha():
    show_error("Please use letters, spaces, hyphens and apostrophes")

def on_invalid_int():
    show_error("Please only use whole numbers (e.g 38)")    

#----------------Variables for alphabet and integer checks
vcmd_alpha = window.register(is_alpha)
ivcmd_alpha = window.register(on_invalid_alpha)
vcmd_int = window.register(is_int)
ivcmd_int = window.register(on_invalid_int)  

#----------------------------Intro Screen
intro_frame = tk.Frame(window, bg="white")

title = tk.Label(intro_frame, text=("Tula"), font=("Arial", 120, "bold"), bg="black").pack(pady=40)

get_started = tk.Button(
    intro_frame,
    text="Get started",
    font=("Kefa", 20, "bold"),
    width=10,
    height=2,
    command=go_to_preform
    ).pack(pady=60)

about_us = tk.Button(
    intro_frame,
    text="About Us",
    font=("Kefa", 20, "bold"),
    width=10,
    height=2,
    command=go_to_about
    ).pack()

intro_frame.pack(fill="both", expand=True)
#----------------------------------------------------------------About Me screen
about_frame = tk.Frame(window, bg="white")

tk.Label(about_frame, text="About Us", font=("Arial", 50, "bold"), bg="black").grid(row=1, column=2, columnspan=1, sticky="ew", pady=20)
tk.Label(about_frame, text="Hi, I'm Abhi!", font=("Chalkduster", 20), bg="black").grid(row=2, column=2, columnspan=1, sticky="ew", pady=20)
tk.Message(about_frame,text= "As a South Asian student in New Zealand, I have noticed that while there are many nutrition tracking tools out there, most of them are only focused on Western diets. "
    "With recipe recommendations like popcorn and pot-pies, South Asians are left making food they don’t enjoy, or resorting back to old, unhealthy eating habits. "
    "For my digital technologies project, I have used this opportunity to come up with a solution; a nutrition tracking program that caters directly to South Asian diets.", font=("Kefa", 15), bg="black", width=300).grid(row=3, column=1, columnspan=3, sticky="ew", pady=10)
tk.Message(about_frame, text="The name, Tula, means balance in Sanskrit, representing the nutritional balance that can be found for South Asians through using this program. "
    "From the design, to the recipe recommendations, to the dietary preference considerations, South Asians can find a space where they can comfortably change diet habits and experience real progress!", font=("Kefa", 15), bg="black", width=300).grid(row=4, column=2, columnspan=3, sticky="ew", pady=10)

#back button
about_back = back_button(about_frame, go_to_intro)
about_back.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

#----------------------------------------------------------------Pre-form screen
preform_frame = tk.Frame(window, bg="white")

preform = tk.Label(preform_frame, text="Your privacy", font=("Arial", 45, "bold"), bg="black").grid(row=1, column=2, columnspan=3, pady=20)

tk.Message(preform_frame, text=" The next step to using Tula is to fill out a short form so that we can set specific nutrition goals for your tracker and know what South Asian recipe recommendations are relevant to you."
    "We understand that this requires sharing some private information, so we ensure that information you give us will be used only for these two purposes and will not be shared externally. "
    "We also understand that you may not want to share personal details and there is the option to continue without filling the form. "
    "This pathway will mean that you will not have set specific nutrition goals, however you will still be able to view South Asian recipe recommendations. ", font=("Kefa", 15), bg="black", width=300).grid(row=3, column=2, columnspan=3, sticky="ew", pady=10)
            
to_form = tk.Button(
    preform_frame,
    text="Proceed to form",
    font=("Kefa", 20, "bold"),
    width=10,
    height=2,
    activeforeground="green",
    command=go_to_form
    )
to_form.grid(row=7, column=2, pady=15)

skip_form = tk.Button(
    preform_frame,
    text="Skip form",
    font=("Kefa", 20, "bold"),
    width=10,
    height=2,
    activeforeground="green"
    )
skip_form.grid(row=8, column=2, pady=15)

#back button
preform_back = back_button(preform_frame, go_to_intro)
preform_back.grid(row=0, column=0, columnspan=2, sticky="nw", padx=10, pady=10)

#----------------------------------------------------------------Form screen
form_frame = tk.Frame(window, bg="white")

form = tk.Label(form_frame, text="Form", font=("Arial", 50, "bold"), bg="black").grid(row=0, column=1, sticky="w", padx=10, pady=20)
    
#asking for name
tk.Label(form_frame, text="Name:", bg="black").grid(row=1, column=0, sticky="e", padx=10, pady=15)
name_entry = tk.Entry(form_frame, validate="key", validatecommand=(vcmd_alpha, "%P"), invalidcommand=ivcmd_alpha)
name_entry.grid(row=1, column=1, sticky="w")

#asking for age
tk.Label(form_frame, text="Age:", bg="black").grid(row=2, column=0, sticky="e", padx=10, pady=15)
age_entry = tk.Entry(form_frame, validate="key", validatecommand=(vcmd_int, "%P"), invalidcommand=ivcmd_int)
age_entry.grid(row=2, column=1, sticky="w")

#asking for gender
tk.Label(form_frame, text="Biological sex:", bg="black").grid(row=3, column=0, sticky="e", padx=10, pady=15)
#combobox for gender
gender = tk.StringVar()
gender_entry = ttk.Combobox(form_frame, width = 18, textvariable=gender)
#adding combobox drop down list
gender_entry['values'] = ('Male', 'Female')
gender_entry.grid(row=3,column=1, sticky="w")
gender_entry.current()

#asking for weight
tk.Label(form_frame, text="Weight (in kg):", bg="black").grid(row=4, column=0, sticky="e", padx=10, pady=15)
weight_entry = tk.Entry(form_frame, validate="key", validatecommand=(vcmd_int, "%P"), invalidcommand=ivcmd_int)
weight_entry.grid(row=4, column=1, sticky="w")

#asking for height
tk.Label(form_frame, text="Height (in cm):", bg="black").grid(row=5, column=0, sticky="e", padx=10, pady=15)
height_entry = tk.Entry(form_frame, validate="key", validatecommand=(vcmd_int, "%P"), invalidcommand=ivcmd_int)
height_entry.grid(row=5, column=1, sticky="w")

#asking for activity level
tk.Label(form_frame, text="Activity level:", bg="black").grid(row=6, column=0, sticky="e", padx=10, pady=15)
#combobox for health goal
activity = tk.StringVar()
activity_entry = ttk.Combobox(form_frame, width = 18, textvariable=activity)
#adding combobox drop down list
activity_entry['values'] = ('Sedentary (little to no exercise)', 'Light (1-3 days/week)', 'Moderate (3-5 days/week)', 'Intense (6-7 days/week)')
activity_entry.grid(column=1, row=6, sticky="w")
activity_entry.current()

#asking for goal
tk.Label(form_frame, text="Health Goal:", bg="black").grid(row=7, column=0, sticky="e", padx=10, pady=15)
#combobox for health goal
goal = tk.StringVar()
goal_entry = ttk.Combobox(form_frame, width = 18, textvariable=goal)
#adding combobox drop down list
goal_entry['values'] = ('Improving general health', 'Losing weight', 'Gaining weight', 'Maintaining weight', 'Build muscle')
goal_entry.grid(column = 1, row = 7, sticky="w")
goal_entry.current()

#asking for dietary preference
tk.Label(form_frame, text="Dietary preference:", bg="black").grid(row=8, column=0, sticky="e", padx=10, pady=15)
#combobox for dietary preferences
dietary = tk.StringVar()
dietary_entry = ttk.Combobox(form_frame, width = 18, textvariable=dietary)
#adding combobox drop down list
dietary_entry['values'] = ('Vegetarian', 'Vegan', 'Halal', 'Gluten-Free', 'No preference')
dietary_entry.grid(column = 1, row = 8, sticky="w")
dietary_entry.current()

#Label error initial
lbl_error = tk.Label(form_frame, text='', font=("Helvetica", 14, "bold"), fg='yellow', bg="black")
lbl_error.grid(row=9, column=1)

#submit form button
submit_button = tk.Button(
    form_frame,
    text="Submit form",
    font=("Chalkduster", 18, "bold"),
    width=12,
    height=2,
    activeforeground="green",
    command=read_input,
)
submit_button.grid(row=10, column=1, sticky="w", pady=15)

#back button
form_back = back_button(form_frame, go_to_preform)
form_back.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

window.mainloop()
