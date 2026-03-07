FRENCH_WORDS = [
    {"en": "One", "fr": "Un", "emoji": "1️⃣", "category": "Numbers"},
    {"en": "Two", "fr": "Deux", "emoji": "2️⃣", "category": "Numbers"},
    {"en": "Three", "fr": "Trois", "emoji": "3️⃣", "category": "Numbers"},
    {"en": "Four", "fr": "Quatre", "emoji": "4️⃣", "category": "Numbers"},
    {"en": "Five", "fr": "Cinq", "emoji": "5️⃣", "category": "Numbers"},
    {"en": "Red", "fr": "Rouge", "emoji": "🔴", "category": "Colors"},
    {"en": "Blue", "fr": "Bleu", "emoji": "🔵", "category": "Colors"},
    {"en": "Green", "fr": "Vert", "emoji": "🟢", "category": "Colors"},
    {"en": "Yellow", "fr": "Jaune", "emoji": "🟡", "category": "Colors"},
    {"en": "Black", "fr": "Noir", "emoji": "⚫", "category": "Colors"},
    {"en": "White", "fr": "Blanc", "emoji": "⚪", "category": "Colors"},
    {"en": "Dog", "fr": "Chien", "emoji": "🐶", "category": "Animals"},
    {"en": "Cat", "fr": "Chat", "emoji": "🐱", "category": "Animals"},
    {"en": "Bird", "fr": "Oiseau", "emoji": "🐦", "category": "Animals"},
    {"en": "Fish", "fr": "Poisson", "emoji": "🐟", "category": "Animals"},
    {"en": "Horse", "fr": "Cheval", "emoji": "🐴", "category": "Animals"},
    {"en": "Apple", "fr": "Pomme", "emoji": "🍎", "category": "Food"},
    {"en": "Bread", "fr": "Pain", "emoji": "🥖", "category": "Food"},
    {"en": "Water", "fr": "Eau", "emoji": "💧", "category": "Food"},
    {"en": "Milk", "fr": "Lait", "emoji": "🥛", "category": "Food"},
    {"en": "Cheese", "fr": "Fromage", "emoji": "🧀", "category": "Food"},
    {"en": "Hello", "fr": "Bonjour", "emoji": "👋", "category": "Greetings"},
    {"en": "Goodbye", "fr": "Au revoir", "emoji": "🚶", "category": "Greetings"},
    {"en": "Please", "fr": "S'il vous plaît", "emoji": "🙏", "category": "Greetings"},
    {"en": "Thank you", "fr": "Merci", "emoji": "🎉", "category": "Greetings"},
    {"en": "Yes", "fr": "Oui", "emoji": "👍", "category": "Greetings"},
    {"en": "No", "fr": "Non", "emoji": "👎", "category": "Greetings"},
    {"en": "Boy", "fr": "Garçon", "emoji": "👦", "category": "People"},
    {"en": "Girl", "fr": "Fille", "emoji": "👧", "category": "People"},
    {"en": "House", "fr": "Maison", "emoji": "🏠", "category": "Places"},
    {"en": "School", "fr": "École", "emoji": "🏫", "category": "Places"}
]

def get_french_categories():
    categories = set()
    for w in FRENCH_WORDS:
        categories.add(w["category"])
    return sorted(list(categories))

def get_french_words_by_category(category):
    if category == "All":
        return FRENCH_WORDS
    return [w for w in FRENCH_WORDS if w["category"] == category]
