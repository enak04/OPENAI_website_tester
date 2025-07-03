from app.client import client
import re



def extract_css_from_response(text):
    css = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    css = re.sub(r'```css|```', '', css).strip()
    return css.strip()

def analyze_prompt(prompt, css):
    system_msg = (
    "You are a CSS editing assistant for non-technical users.\n\n"
    "They will describe elements using terms like 'main button', 'header', 'top bar', etc.\n\n"
    "Only make changes if a matching selector or element is clearly present in the given CSS.\n\n"
    "If what the user is asking for is not present in the CSS, do NOT make up selectors.\n\n"
    "Instead, reply like this:\n\n"
    "{\n"
    "  \"suggestions\": [\"For such changes please contact us directly via mail or phone!\"]\n"
    "}\n\n"
    "If you feel what the user is asking may not be exactly possible but is closely related "
    "(for example, the user asks to make the icon bigger but you can only change the icon color), "
    "then reply like this:\n\n"
    "{\n"
    "  \"suggestions\": [\"Sorry, I cannot do that but I can edit the icon color for you!\"]\n"
    "}\n\n"
    "This is just an example. Read the CSS carefully and reply innovatively for other cases where "
    "the exact change is not possible.\n\n"
    "If the change is valid, return ONLY the updated CSS and the modified class names in the following format:\n\n"
    "{\n"
    "  \"css\": \".sh-body { background-color: #FF0000; color: white; }\\n.sh-header-main { background-color: red; padding: 10px; }\",\n"
    "  \"modifiedClasses\": [\"sh-body\", \"sh-header-main\"]\n"
    "}\n\n"
    "Do not add any additional explanations or comments outside this JSON.\n\n"
    "Always ensure returned CSS is minimal and only includes changed selectors with their updated properties."
    )
    print("\nreached here 2\n")
    response = client.chat.completions.create(
        model="gpt-4o-theme-customization",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Here is the current CSS:\n{css}"},
            {"role": "user", "content": f"User says:\n{prompt}"}
        ], 
        temperature=0.2
    )
    print("reached here 3 \n")
    reply = response.choices[0].message.content.strip()

    if reply.startswith("{") and '"suggestions"' in reply:
        return {"type": "suggestions", "content": eval(reply)["suggestions"]}

    clean_css = extract_css_from_response(reply)
    print("reached here 4\n")
    return {"type": "css", "content": clean_css}
