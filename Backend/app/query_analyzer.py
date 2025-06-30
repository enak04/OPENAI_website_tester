from app.client import client
import re



def extract_css_from_response(text):
    css = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    css = re.sub(r'```css|```', '', css).strip()
    return css.strip()

def analyze_prompt(prompt, css):
    system_msg = (
        "You are a CSS editing assistant for non-technical users. "
        "They will describe elements using terms like 'main button', 'header', 'top bar', etc. "
        "Only make changes if a matching selector or element is clearly present in the given CSS. "
        "If what the user is asking for is not present in the CSS, do NOT make up selectors. "
        "Instead, reply like this: {\"suggestions\": [\"For such changes please visit contact us directly via mail or phone!\"]}. "
        "But if you feel what the user is asking may not be exactly possible but closely related for example the user asks to make icon bigger but you can only change the icon color then reply like this : {\"suggestions\": [\"Sorry, I cannot do that but I can edit the icon color for you !\"]}. This is just an example read the CSS and reply innovatively for other cases where exact change is not possible"
        "If the change is valid, return ONLY the updated CSS, without comments or explanation."
    )
    response = client.chat.completions.create(
        model="gpt-4o-theme-customization",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Here is the current CSS:\n{css}"},
            {"role": "user", "content": f"User says:\n{prompt}"}
        ], 
        temperature=0.2
    )

    reply = response.choices[0].message.content.strip()

    if reply.startswith("{") and '"suggestions"' in reply:
        return {"type": "suggestions", "content": eval(reply)["suggestions"]}

    clean_css = extract_css_from_response(reply)
    return {"type": "css", "content": clean_css}
