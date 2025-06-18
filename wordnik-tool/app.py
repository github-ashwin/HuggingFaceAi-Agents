from smolagents import tool
import gradio as gr
import requests
from dotenv import load_dotenv
import os

load_dotenv() # Load .env file for API_KEY

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.wordnik.com/v4/word.json"

@tool
def get_word_info(word:str)->str:
    """
    Fetches the definition and example of a word using Wordnik API
    """

    if not API_KEY:
        return "API KEY not found"
    
    try:
        def_res = requests.get(
            f"{BASE_URL}/{word}/definitions",
            params={"limit":2,
                    "api_key":API_KEY}
        ).json()

        definitions = "\n".join([f"- {d['text']}" for d in def_res]) or "No definitions found."

        ex_res = requests.get(
            f"{BASE_URL}/{word}/examples",
            params={"limit": 2,
                     "api_key": API_KEY}
        ).json()

        examples = "\n".join([f"- {e['text']}" for e in ex_res.get("examples", [])]) or "No examples found."

        return f"**Definitions**:\n{definitions}\n\n**Examples**:\n{examples}"
    
    except Exception as e:
        return f"Error: {str(e)}"

iface = gr.Interface(
    fn=get_word_info,
    inputs=gr.Textbox(placeholder="Enter a word..."),
    outputs="text",
    title="Word Explorer",
    description="Type a word to get dynamic definitions and examples from the Wordnik API."
)

if __name__ == "__main__":
    iface.launch()