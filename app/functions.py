from app.client import client
from .openai_themeselector import get_best_theme
from database.modifying_databases import retrieve_css_and_json_for_user , retrieve_theme_data , store_css_and_json_for_user
from .query_analyzer import analyze_prompt
import json
import os
import re
# def modify_css(css_string, modification):
    
#     """
#     Modifies css_string based on selectors and properties in modification["css"].

#     Args:
#         css_string (str): Original CSS string.
#         modification (dict): JSON with keys:
#             - "css": str containing CSS to modify selectors.
#             - "modifiedClasses": list of selectors.

#     Returns:
#         dict: {
#             "css": updated CSS string,
#             "modifiedClasses": [...]
#         }
#     """
#     # Parse modification["css"] into selector -> properties mapping    
#     if isinstance(modification, str):
#         modification = json.loads(modification)
#     mod_css_lines = modification["css"].split("\n")
    
#     changes = {}
#     for line in mod_css_lines:
#         if not line.strip():
#             continue
#         selector, properties = line.split("{")
#         selector = selector.strip()
#         properties = properties.strip("} ").strip()
#         changes[selector] = properties

#     updated_css = css_string

#     # Apply each modification using regex replacement
#     for selector, new_props in changes.items():
#         # Regex pattern to find the exact selector block
#         pattern = re.compile(r'(' + re.escape(selector) + r')\s*\{[^}]*\}')
#         replacement = f"{selector} {{ {new_props} }}"
#         updated_css, count = pattern.subn(replacement, updated_css)
#         if count == 0:
#             print(f"Selector '{selector}' not found, skipping modification.")

#     return updated_css


import json
import re

def modify_css(css_string, modification):
    """
    Modifies css_string based on selectors and properties in modification["css"].

    Args:
        css_string (str): Original CSS string.
        modification (dict): JSON with keys:
            - "css": str containing CSS to modify selectors.
            - "modifiedClasses": list of selectors.

    Returns:
        str: Updated CSS string.
    """
    if isinstance(modification, str):
        modification = json.loads(modification)

    changes = {}

    # Use regex to find all selector blocks in the input CSS
    for match in re.finditer(r'([^{]+)\{([^}]+)\}', modification["css"]):
        selector = match.group(1).strip()
        properties = match.group(2).strip()
        changes[selector] = properties

    updated_css = css_string

    # Apply modifications
    for selector, new_props in changes.items():
        pattern = re.compile(r'(' + re.escape(selector) + r')\s*\{[^}]*\}')
        replacement = f"{selector} {{ {new_props} }}"
        updated_css, count = pattern.subn(replacement, updated_css)
        if count == 0:
            print(f"Selector '{selector}' not found, skipping modification.")

    return updated_css

import json

# def modify_json(original_json_str: str, modification_dict: dict) -> str:
#     """
#     Modifies original JSON string by applying the provided modification_dict["updates"]["json"].

#     Args:
#         original_json_str (str): The original JSON string stored for the user.
#         modification_dict (dict): The parsed modification JSON containing the updates under modification_dict["updates"]["json"].

#     Returns:
#         str: Updated JSON string ready for storage.
#     """
#     try:
#         # Parse the original JSON string into a dict
#         original_json = json.loads(original_json_str)
#     except json.JSONDecodeError:
#         print("Error decoding original JSON, using empty JSON object.")
#         original_json = {}

#     # Extract the modifications
#     json_updates = modification_dict.get("updates", {}).get("json", {})

#     # Recursively update the original JSON with the modifications
#     def recursive_update(orig, updates):
#         for key, value in updates.items():
#             if isinstance(value, dict) and isinstance(orig.get(key), dict):
#                 recursive_update(orig[key], value)
#             else:
#                 orig[key] = value

#     recursive_update(original_json, json_updates)

#     # Return the updated JSON string
#     return json.dumps(original_json, indent=2)

def modify_json(original_json_str: str, modification_dict: dict) -> str:
    """
    Modifies original JSON string by applying the provided modification_dict["updates"]["json"].
    Handles direct key replacements including nested 'payload.rows' replacement when 'rows' is provided.
    """
    try:
        original_json = json.loads(original_json_str)
    except json.JSONDecodeError:
        print("Error decoding original JSON, using empty JSON object.")
        original_json = {}

    json_updates = modification_dict.get("updates", {}).get("json", {})

    def recursive_update(orig, updates):
        for key, value in updates.items():
            if isinstance(value, dict) and isinstance(orig.get(key), dict):
                recursive_update(orig[key], value)
            else:
                orig[key] = value

    recursive_update(original_json, json_updates)

    # Handle special case: replace payload["rows"] if "rows" is provided at top level
    if "rows" in json_updates:
        if "payload" in original_json and isinstance(original_json["payload"], dict):
            original_json["payload"]["rows"] = json_updates["rows"]

    return json.dumps(original_json, indent=2)





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

        

        # 2. Build input prompt
        user_request = (
            f"Choose a theme for a '{category}' website with:\n"
            f"- Primary color: {primary_color}\n"
            f"- Secondary color: {secondary_color}\n"
        )
        
        # if user_context:
        #     user_request += f"\nUser context:\n{user_context}"

        

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
    themes_path = os.path.abspath(os.path.join(BASE_DIR, "..", "static" , "themes", "themes.json")) 

    try:
        if isinstance(extracted_categories, str):
            extracted_categories = [extracted_categories]
        matching_themes = []
        

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
    css_path = os.path.join(BASE_DIR, '..', 'static' , 'themes', 'base_theme_template.css')

    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
            return css_content

    except Exception as e:
        return f"Error customizing CSS: {str(e)}"


# def customize_css(property_to_change, new_value , user_id , session_id):

#     try:
#         css_content = retrieve_theme_data(user_id , session_id)

#         prompt = f"""
#                 Below is a CSS file.

#                 Change the CSS to reflect the following change:
#                 Property to change: {property_to_change}
#                 New value: {new_value}

#                 If there is a clash between multiple properties , clarify with the user which one they are talking about .
#                 STRICTLY ALWAYS CLARIFY . For an example , say if you are confused between primary and secondary button ask the user
#                 to give more clues about which button

#                 Return the full updated CSS, without any explanations, comments, or additional formatting. Return valid CSS only, without backticks, without markdown, and without comments.
#                 {css_content}
#                 """
        
#         response = client.chat.completions.create(
#             model="gpt-4o-theme-customization",
#             messages=[
#                 {"role": "system", "content": "You are a frontend assistant specializing in CSS customization."},
#                 {"role": "user", "content": prompt}
#             ]
#         )

#         return response.choices[0].message.content.strip()

#     except Exception as e:
#         return f"Error customizing CSS: {str(e)}"
    

def submit_color_preferences(primary_color: str, secondary_color: str):
    return {
        "primary_color": primary_color,
        "secondary_color": secondary_color
    }

def edit_css(user_id: str, prompt: str , json_id : str):

    # theme_data = get_theme_by_userid(user_id)
    # if not theme_data or "css" not in theme_data:
    #     return jsonify({"error": "No theme found for user"}), 404

    # original_css = theme_data["css"]
    retrieved_data = retrieve_css_and_json_for_user(user_id)
    prompt = prompt + "Strictly follow the output format.Don't give any extra explanation fields or text."
    # print("\n" , retrieved_data)
    original_css = retrieved_data["css"]
    original_json = retrieved_data["json"]
    original_html = retrieved_data["html"]
    
    result = analyze_prompt(prompt, original_css , original_json ,original_html)
    result2 = json.loads(result["content"]) #converting string to json format
    # print(result2)
    # print("Error here")

    if "suggestions" in result2:
        return {
            "user" : user_id,
            "content" : result2["suggestions"][0]
        }

    
    if isinstance(result["content"], list):
        return {"user": user_id, "content": result["content"][0]}
    else:
        
        # print("Error here 2")
        # modified_css = modify_css(original_css , result2["updates"])
        # print(modified_css)
        if result2["updates"].get("css_update", False):
            modified_css = modify_css(original_css, result2["updates"])
        else:
            modified_css = original_css

        if result2["updates"].get("json_update", False):
            json_changed = result2.get("updates", {}).get("complete_json", {})
            json_new = json.dumps(json_changed)
        else:
            json_new = original_json

        # print(modified_json)
        
        # store_css_and_json_for_user(user_id , modified_css , original_json)
        store_css_and_json_for_user(user_id , modified_css , json_new , json_id , original_html)
        return {
            "user": user_id,
            "json_id" : json_id,
            **result2 
        }

