from app.client import client
import re
import os



def extract_css_from_response(text):
    css = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    css = re.sub(r'```css|```', '', css).strip()
    return css.strip()

def analyze_prompt(prompt, cssdata , jsondata , htmldata):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROMPT_PATH = os.path.join(BASE_DIR, '..', 'static' , 'prompts', 'queryanalyzer_prompt.txt')

    with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
        SYSTEM_PROMPT = f.read()
    
    system_msg = SYSTEM_PROMPT

    print("\nPrompt is" , prompt)

    print("\nreached here 2\n")
    response = client.chat.completions.create(
        model="gpt-4o-theme-customization",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Here is the current CSS:\n{cssdata}"},
            {"role": "user", "content": f"Here is the html of the site:\n{htmldata}"},
            {"role": "user", "content": f"Here is the current JSON:\n{jsondata}"},
            {"role": "user", "content": f"User says:\n{prompt}"}
        ], 
        temperature=0.2
    )
    print("reached here 3 \n")
    reply = response.choices[0].message.content.strip()

    json_match = re.search(r"\{[\s\S]*\}", reply)

    if json_match:
        clean_json = json_match.group(0)
    else:
        clean_json = reply

    # if reply.startswith("{") and '"suggestions"' in reply:
    #     return {"type": "suggestions", "content": eval(reply)["suggestions"]}

    # clean_css = extract_css_from_response(reply)
    print("reached here 4\n")
    print(clean_json)
    # return {"type": "css", "content": clean_css}
    return {"content" : clean_json}
