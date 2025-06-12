from openai import AzureOpenAI
from .config import Config
from .functions import submit_business_details, change_theme_color , get_valid_business_categories
import json

client = AzureOpenAI(
    api_key=Config.OPENAI_API_KEY,
    api_version="2025-01-01-preview",
    azure_endpoint="https://shoop-ma9lhvun-eastus2.openai.azure.com"
)

# ----------------------------
# SYSTEM PROMPT
# ----------------------------
SYSTEM_PROMPT = """
You are a friendly and respectful chatbot helping users set up their business profile.

Your **primary goal** is to extract following pieces of information from the user:
2. Their **business category** 

Once you have it, call the function `submitBusinessDetails(business_category)`.

If the user **asks to change the theme color**, you may optionally call `changeThemeColor(color)` with their preferred color. Do not prompt for it unless they bring it up.

Stay conversational and helpful. Avoid asking for everything at once. Gently guide the user to give the required info. If they go off-topic, kindly steer them back to completing the business setup.
"""

# ----------------------------
# FUNCTION DEFINITIONS (TOOLS)
# ----------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "submitBusinessDetails",
            "description": "Submit the user's business category once available. Business category must exactly match one of the known categories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "business_category": {
                        "type": "string",
                        "description": "Type of business.Strictly return a category from any of the following : Grocery , Shopping"
                    }
                },
                "required": ["business_category"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "changeThemeColor",
            "description": "Change the website/app theme color based on user request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "color": {
                        "type": "string",
                        "description": "The preferred color theme (e.g., red, blue, dark mode)"
                    }
                },
                "required": ["color"]
            }
        }
    }
]

# ----------------------------
# OPENAI CHAT FUNCTION
# ----------------------------
def get_openai_response(user_input, chat_history):
    try:
        # Add system prompt if not yet present
        if not any(msg['role'] == 'system' for msg in chat_history):
            chat_history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})

        # Add user input to history
        chat_history.append({"role": "user", "content": user_input})

        # Send to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-theme-customization",
            messages=chat_history,
            tools=tools,
            tool_choice="auto"
        )

        choice = response.choices[0]
        message = choice.message

        if message.tool_calls:
            chat_history.append({
                "role": "assistant",
                "content": None,
                "tool_calls": message.tool_calls
            })

            tool_call = message.tool_calls[0].model_dump()
            function_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"])


            # Call the appropriate function
            if function_name == "submitBusinessDetails":
                valid_categories = ["grocery"]
                category = arguments.get("business_category", "").strip().lower()

                if category in [vc.lower() for vc in valid_categories]:
                    themes  = submit_business_details(**arguments)
                    result = {
                        "reply" : "Please select a theme!", 
                        "themes" : themes
                    }
                else:
                    result = {
                        "error": f"'{category}' is not a valid business category. Please choose from: {', '.join(valid_categories)}"
                    }
            elif function_name == "changeThemeColor":
                result = change_theme_color(**arguments)
            else:
                result = f"Unknown function: {function_name}"

            chat_history.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": function_name,
                "content": result
            })


            return result

        else:
            chat_history.append({"role": "assistant", "content": message.content})
            return {"reply" : message.content }

    except Exception as e:
        return f"Error: {str(e)}"