import json
import os


def get_valid_business_categories():
    import os
    themes_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'themes.json')
    themes_path = os.path.abspath(themes_path)

    try:
        with open(themes_path, 'r') as file:
            themes = json.load(file)
            return list(set(theme.get("category") for theme in themes if "category" in theme))
    except Exception as e:
        return []

def submit_business_details( business_category):
    # Construct the relative path to themes.json (2 levels up from this file)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Construct full path to Data/themes.json
    themes_path = os.path.join(BASE_DIR, 'Data', 'themes.json')

    try:

        matching_themes = []

        with open(themes_path, 'r') as file:
            themes = json.load(file)
            for theme in themes:
                if theme.get('category', '').strip().lower() == business_category.strip().lower():
                    matching_themes.append(theme)
        
        return matching_themes

    except FileNotFoundError:
        return {"error": "themes.json file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in themes.json"}
    except Exception as e:
        return {"error": str(e)}


def change_theme_color(color):
    # Apply theme logic
    return f"Theme color has been changed to {color}."
