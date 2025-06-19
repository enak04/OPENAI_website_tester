from .client import client
import json
import os


# def get_valid_business_categories():
#     import os
#     themes_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'themes.json')
#     themes_path = os.path.abspath(themes_path)

#     try:
#         with open(themes_path, 'r') as file:
#             themes = json.load(file)
#             return list(set(theme.get("category") for theme in themes if "category" in theme))
#     except Exception as e:
#         return []

def submit_business_details( business_category):
    # Construct the relative path to themes.json (2 levels up from this file)
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construct full path to Data/themes.json
    themes_path = os.path.join(BASE_DIR, "themes.json")
    print("Looking for themes.json at:", themes_path)
    print("Getting theme from:", themes_path)
    print("Does file exist?", os.path.exists(themes_path))

    try:

        matching_themes = []
        print(business_category)

        with open(themes_path, 'r') as file:
            themes = json.load(file)
            for theme in themes:
                if theme.get('category', '').strip().lower() == business_category.strip().lower():
                    matching_themes.append(theme)

        print(matching_themes)
        
        return matching_themes

    except FileNotFoundError:
        return {"error": "themes.json file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in themes.json"}
    except Exception as e:
        return {"error": str(e)}


def customize_css(property_to_change, new_value):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(BASE_DIR, '..', 'data', 'base_theme_template.css')

    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()

        prompt = f"""
                Below is a CSS file.

                Change the CSS to reflect the following change:
                Property to change: {property_to_change}
                New value: {new_value}

                If there is a clash between multiple properties , clarify with the user which one they are talking about .
                STRICTLY ALWAYS CLARIFY . For an example , say if you are confused between primary and secondary button ask the user
                to give more clues about which button

                Return ONLY the **updated CSS rules**, without any explanations, comments, or additional formatting. Return valid CSS only, without backticks, without markdown, and without comments.
                {css_content}
                """
        
        response = client.chat.completions.create(
            model="gpt-4o-theme-customization",
            messages=[
                {"role": "system", "content": "You are a frontend assistant specializing in CSS customization."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error customizing CSS: {str(e)}"
