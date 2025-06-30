from app.client import client
from .openai_themeselector import get_best_theme
from mongodb.modifying_databases import retrieve_css_for_user , retrieve_theme_data
from .query_analyzer import analyze_prompt
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


def submit_business_theme_details(business_category, primary_color, secondary_color, chat_history):
    """
    Given a business category (or list), color preferences, and chat history,
    returns one or more themes with colors and context applied.
    """
    results = []

    # Handle both string and list input
    if isinstance(business_category, str):
        business_categories = [business_category]
    elif isinstance(business_category, list):
        business_categories = business_category
    else:
        raise ValueError("Invalid business_category format")

    # Optional: Get recent user context
    user_context = "\n".join(
        msg["content"]
        for msg in reversed(chat_history)
        if msg["role"] == "user"
    )[-500:]  # limit to last 500 chars

    themes = submit_business_details(business_categories)

    
    for category in business_categories:
        # 1. Get matching themes
        themes = submit_business_details(category)

        print("Themes received from submit_business_details are " , themes)

        # 2. Build input prompt
        user_request = (
            f"Choose a theme for a '{category}' website with:\n"
            f"- Primary color: {primary_color}\n"
            f"- Secondary color: {secondary_color}\n"
        )
        print("user request is : " , user_request , "\n")
        # if user_context:
        #     user_request += f"\nUser context:\n{user_context}"

        print("User request is : \n" , user_request , "\n")

        # 3. Select best theme
        best_theme = get_best_theme(user_request, themes)

        # 4. Append additional data
        for theme in best_theme:
            theme["primary_color"] = primary_color
            theme["secondary_color"] = secondary_color

        results.append(best_theme)

    return results if len(results) > 1 else results[0]

def submit_business_details( extracted_categories):
    # Construct the relative path to themes.json (2 levels up from this file)
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # /Backend/app
    themes_path = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "themes.json")) 
    # print("Base directory is :" , BASE_DIR)
    # print("Looking for themes.json at:", themes_path)
    # print("Getting theme from:", themes_path)
    # print("Does file exist?", os.path.exists(themes_path))

    try:
        if isinstance(extracted_categories, str):
            extracted_categories = [extracted_categories]
        matching_themes = []
        print(extracted_categories)

        with open(themes_path, 'r') as file:
            themes = json.load(file)
            for theme in themes:
                theme_category = theme.get('category', '').strip().lower()
                if theme_category in [cat.strip().lower() for cat in extracted_categories]:
                    matching_themes.append(theme)

        
        return {
            "theme": matching_themes,
            "content": "select a theme"
        }

    except FileNotFoundError:
        return {"error": "themes.json file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in themes.json"}
    except Exception as e:
        return {"error": str(e)}
    
def get_theme(theme_name):
    theme_name = ""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(BASE_DIR, '..', 'data', 'base_theme_template.css')

    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
            return css_content

    except Exception as e:
        return f"Error customizing CSS: {str(e)}"


def customize_css(property_to_change, new_value , user_id , session_id):

    try:
        css_content = retrieve_theme_data(user_id , session_id)

        prompt = f"""
                Below is a CSS file.

                Change the CSS to reflect the following change:
                Property to change: {property_to_change}
                New value: {new_value}

                If there is a clash between multiple properties , clarify with the user which one they are talking about .
                STRICTLY ALWAYS CLARIFY . For an example , say if you are confused between primary and secondary button ask the user
                to give more clues about which button

                Return the full updated CSS, without any explanations, comments, or additional formatting. Return valid CSS only, without backticks, without markdown, and without comments.
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
    

def submit_color_preferences(primary_color: str, secondary_color: str):
    return {
        "primary_color": primary_color,
        "secondary_color": secondary_color
    }

def edit_css(user_id: str, prompt: str):

    # theme_data = get_theme_by_userid(user_id)
    # if not theme_data or "css" not in theme_data:
    #     return jsonify({"error": "No theme found for user"}), 404

    # original_css = theme_data["css"]
    original_css = retrieve_css_for_user(user_id)
    print(original_css)
    print("\n\n\nPrompt is : " , prompt , "\n")

    result = analyze_prompt(prompt, original_css)
    print("\n\n\nCss changes are : " , result["content"] , "\n")

    if isinstance(result["content"], list):
        return {"user": user_id, "content": result["content"][0]}
    else:
        return {"user": user_id, "css": result["content"]}

