from openai import AzureOpenAI
from .config import Config
from .functions import extract_physics_concept
import json

client = AzureOpenAI(
    api_key=Config.OPENAI_API_KEY,
    api_version="2025-01-01-preview",
    azure_endpoint="https://shoop-ma9lhvun-eastus2.openai.azure.com"
)

def get_openai_response(user_input, chat_history):
    try:
        # Add user input to history
        chat_history.append({"role": "user", "content": user_input})

        # Send chat history to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-theme-customization",
            messages=chat_history,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "extract_physics_concept",
                        "description": "Extract the main physics concept from a sentence",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "concept": {
                                    "type": "string",
                                    "description": "The key physics concept involved, e.g., Newton's Second Law"
                                }
                            },
                            "required": ["concept"]
                        }
                    }
                }
            ],
            tool_choice="auto"
        )

        choice = response.choices[0]
        message = choice.message

        if message.tool_calls:
            # Save the tool call to chat history
            chat_history.append({
                "role": "assistant",
                "content": None,
                "tool_calls": message.tool_calls
            })

            # Execute the first function
            tool_call = message.tool_calls[0]
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if name == "extract_physics_concept":
                result = extract_physics_concept(**args)
            else:
                result = f"Unknown function: {name}"

            # Save the tool response to chat history
            chat_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": name,
                "content": result
            })

            return result

        else:
            # Normal assistant reply
            chat_history.append({"role": "assistant", "content": message.content})
            return message.content

    except Exception as e:
        return f"Error: {str(e)}"
