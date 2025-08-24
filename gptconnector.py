import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=openai_api_key)

def get_response(message: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Sends a message to OpenAI GPT and returns the response text.
    Args:
        message (str): The user's message to send to GPT.
        model (str): The model name to use (default: "gpt-3.5-turbo").
    Returns:
        str: The response from GPT.
    Raises:
        Exception: If the OpenAI API call fails.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a witty assistant. "
                        "Read the user's message, use it as context, and reply with a short joke in German. "
                        "Do not include any translation or explanation, only the joke itself as if you were a real person."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Log error or handle as needed
        return "Sorry, I couldn't process your request right now."