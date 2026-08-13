# Library that lets me communicate with SQLite databases
import sqlite3
from datetime import date

# Functions
def get_connection():
    return sqlite3.connect("nutrition.db")

def add_recipe_columns():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("ALTER TABLE meals ADD COLUMN ingredients TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE meals ADD COLUMN instructions TEXT")
    except sqlite3.OperationalError:
        pass

    connection.commit()
    connection.close()
    
# Making a table for the meals 
def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY,
        meal_name TEXT,
        region TEXT,
        meal_type TEXT,
        serving_size TEXT,
        calories INTEGER,
        protein REAL,
        carbs REAL,
        fat REAL,
        vegetarian INTEGER,
        vegan INTEGER,
        halal INTEGER,
        gluten_free INTEGER
        ingredients TEXT,
        instructions TEXT
    )
    """)

    connection.commit()
    connection.close()
    
# Adding meals to the database table 
def add_meal(
    name,
    region,
    meal_type,
    serving_size,
    calories,
    protein,
    carbs,
    fat,
    vegetarian,
    vegan,
    halal,
    gluten_free,
    ingredients,
    instructions
):
    connection = get_connection()
    cursor = connection.cursor()    

    cursor.execute("""
    INSERT INTO meals
    (
        meal_name,
        region,
        meal_type,
        serving_size,
        calories,
        protein,
        carbs,
        fat,
        vegetarian,
        vegan,
        halal,
        gluten_free,
        ingredients,
        instructions
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        name,
        region,
        meal_type,
        serving_size,
        calories,
        protein,
        carbs,
        fat,
        vegetarian,
        vegan,
        halal,
        gluten_free,
        ingredients,
        instructions
    ))

    connection.commit()
    connection.close()

# Function that Tkinter can call on to get recipes from the database
def get_all_recipes():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM meals
    """)

    recipes = cursor.fetchall()

    connection.close()

    return recipes

# Grouping recipes by dietary preference
def get_recipes_by_dietary_preference(dietary_preference):
    connection = get_connection()
    cursor = connection.cursor()

    if dietary_preference == "Vegetarian":
        cursor.execute("""
            SELECT *
            FROM meals
            WHERE vegetarian = 1
        """)

    elif dietary_preference == "Vegan":
        cursor.execute("""
            SELECT *
            FROM meals
            WHERE vegan = 1
        """)

    elif dietary_preference == "Halal":
        cursor.execute("""
            SELECT *
            FROM meals
            WHERE halal = 1
        """)

    elif dietary_preference == "Gluten-Free":
        cursor.execute("""
            SELECT *
            FROM meals
            WHERE gluten_free = 1
        """)

    else:
        cursor.execute("""
            SELECT *
            FROM meals
        """)

    recipes = cursor.fetchall()

    connection.close()

    return recipes

# Function that Tkinter can call on to receive meals from this database
def get_all_meals():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM meals")
    meals = cursor.fetchall()

    connection.close()

    return meals

# When user selects a meal name in Tkinter, return meal info
def get_meal_by_name(name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM meals WHERE meal_name = ?",
        (name,)
    )

    meal = cursor.fetchone()

    connection.close()

    return meal

# Storing logged meals in a table
def create_logged_meals_table():
    connection = sqlite3.connect("nutrition.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logged_meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER,
            log_date TEXT,
            user_name TEXT
        )
    """)

    connection.commit()
    connection.close()

# Getting logged meal into the table
def log_meal_to_database(meal_id, user_name):
    connection = sqlite3.connect("nutrition.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO logged_meals (meal_id, log_date, user_name) VALUES (?, ?, ?)",
        (meal_id, str(date.today()), user_name)
    )

    connection.commit()
    connection.close()

# Getting today's logged meals from database
def get_todays_logged_meals(user_name):
    connection = sqlite3.connect("nutrition.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT meal_id
        FROM logged_meals
        WHERE log_date = ? AND user_name = ?
    """, (str(date.today()), user_name))

    meals = cursor.fetchall()
    connection.close()
    return meals

def get_meal_by_id(meal_id):
    connection = sqlite3.connect("nutrition.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM meals WHERE id = ?",
        (meal_id,)
    )

    meal = cursor.fetchone()
    connection.close()
    return meal

# Getting full meal information for meals that this user logged today
def get_todays_meal_details(user_name):
    connection = sqlite3.connect("nutrition.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT meals.*
        FROM meals
        JOIN logged_meals
        ON meals.id = logged_meals.meal_id
        WHERE logged_meals.log_date = ?
        AND logged_meals.user_name = ?
    """, (str(date.today()), user_name))

    meals = cursor.fetchall()
    connection.close()
    return meals


#Calling function
create_table()
create_logged_meals_table()
add_recipe_columns()
