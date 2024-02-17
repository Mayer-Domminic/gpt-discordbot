
import json
from openai import OpenAI

with open('config.json') as config_file:
    config = json.load(config_file)

# openai.api_key = config.get('apikey')
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)
def call_openai_api(prompt, message_type, messages=None, engine='davinci', temperature=0.7, max_tokens=150):
    """
    Call OpenAI API with the given prompt and context.

    Args:
        prompt (str): The prompt to send to the API.
        message_type (str): The type of message (e.g., 'text', 'code', etc.).
        messages (list, optional): List of previous messages to keep the context.
        engine (str): The engine to use for the completion.
        temperature (float): The randomness of the response (between 0 and 1).
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        str: The text of the response from the API.
    """
    
    # If there are previous messages, prepend them to the prompt
    if messages:
        context = '\n'.join(messages) + '\n'
        prompt = context + prompt

    
    try:
        # Call the OpenAI API
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or another model name you're subscribed to
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # Return the response text
        return response.choices[0].text.strip()
    except Exception as e:  # Catching all exceptions since openai.error is not available
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    type = "text"
    prompt = "What's the weather like today?"
    messages = ["Hi, how are you?", "I'm fine, thanks for asking."]
    
    response = call_openai_api(prompt, type, messages)
    print(response)
