#Libraries
from database import add_meal
from database import get_all_meals

meals = get_all_meals()

# Butter Chicken
add_meal(
    "Butter Chicken",
    "North Indian",
    "Dinner",
    "1 bowl (250g)",
    490,
    34,
    12,
    31,
    0,
    0,
    1,
    1,
    """Chicken, butter, tomato, cream, onion, garlic, ginger,
    garam masala, turmeric, cumin and salt.""",
    """ 1. Marinate the chicken with the spices.
2. Cook the chicken in a pan until browned.
3. Prepare the tomato, onion, and spice sauce.
4. Add the cooked chicken to the sauce and stir.
5. Add butter and cream and simmer until fully cooked."""  
)

# Massor Dal Tadka
add_meal(
    "Masoor Dal Tadka",
    "North Indian",
    "Dinner",
    "1 bowl (250g)",
    300,
    18,
    45,
    7,
    1,
    1,
    1,
    1,
    """Red lentils, onion, tomato, garlic, ginger, cumin,
turmeric, chilli, coriander and oil.""",
    """1. Rinse the lentils.
2. Cook the lentils with water and turmeric.
3. Fry the onion, garlic, ginger and spices in hot oil.
4. Add the cooked lentils.
5. Simmer for several minutes or until consistency is soft and serve!"""
)

#Chicken Biryani
add_meal(
    "Chicken Biryani",
    "Pakistani",
    "Dinner",
    "1 plate (300g)",
    600,
    30,
    70,
    20,
    0,
    0,
    1,
    1,
    """Basmati rice, chicken, onion, garlic, ginger, yoghurt,
biryani spices, saffron and coriander.""",
    """1. Marinate the chicken with yoghurt and spices.
2. Cook the chicken with the onion and spices.
3. Partially cook the basmati rice.
4. Layer the rice over the chicken.
5. Cover and cook until the rice is fully cooked."""
)

# Masala Dosa
add_meal(
    "Masala Dosa",
    "South Indian",
    "Breakfast",
    "1 dosa",
    350,
    8,
    55,
    10,
    1,
    0,
    1,
    1,
    """Dosa batter, potatoes, onion, mustard seeds, curry leaves,
turmeric, green chilli and oil.""",
    """
1. Prepare the potato filling by mixing boiled potatoes with with onion and spices.
2. Heat a dosa pan.
3. Spread the dosa batter into a thin circle.
4. Cook until golden.
5. Add the potato filling and fold the dosa when browned/crispy."""
)

# Chana Masala
add_meal(
    "Chana Masala",
    "North Indian",
    "Dinner",
    "1 bowl (250g)",
    320,
    15,
    50,
    8,
    1,
    1,
    1,
    1,
    """Chickpeas, onion, tomato, garlic, ginger, cumin,
coriander, turmeric, chilli and oil.""",
    """1. Heat oil in a pan.
2. Cook the onion until softened.
3. Add garlic, ginger and spices.
4. Add tomatoes and cook until softened.
5. Add chickpeas and simmer for approximately 10 minutes."""
)
