from .client import client
import json
import os
import re

# ----------------------------
# SYSTEM PROMPT SETUP
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, '..', 'static' , 'prompts', 'themeselection_prompt.txt')

with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read()

# ----------------------------
# FUNCTION TO GET BEST THEMES
# ----------------------------
def get_best_theme(user_request: str, theme_list: list[dict]) -> list[dict]:
    print("Theme_list is :" , theme_list , "\n") 
    response = client.chat.completions.create(
        model="gpt-4o-theme-customization",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""Theme List:\n```json\n{json.dumps(theme_list, indent=2)}\n```\n\nUser Request:\n\"{user_request}\""""}
        ],
        temperature=0.2,
    )

    # Extract the response content
    
    content = response.choices[0].message.content.strip()
    

    try:
        # Remove triple backticks if present
        if content.startswith("```"):
            content = content.strip("`")  # remove backticks
            content = content.strip("json")  # remove json hint
            content = content.strip()  # trim whitespace

        # Now parse JSON
        return json.loads(content)
    except json.JSONDecodeError:
        # Fallback: Extract JSON list using regex
        match = re.search(r'\[\s*\{.*?\}\s*\]', content, re.DOTALL)
        if match:
            json_str = match.group()
            return json.loads(json_str)
        else:
            raise ValueError("Failed to extract valid JSON list from ChatGPT response.")
