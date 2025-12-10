import smolagents

#################################pip#######################################
import dotenv
import os
# Environment loading
g_dotenv_loaded = False
def getenv(variable: str) -> str:
    global g_dotenv_loaded
    if not g_dotenv_loaded:
        g_dotenv_loaded = True
        dotenv.load_dotenv()
    value = os.getenv(variable)
    return value

def get_api_key(key_name):
    api_key = getenv(key_name)
    if not api_key:
        msg = (f"{key_name} not set. "
               f"Be sure .env has {key_name}. "
               f"Be sure dotenv.load_dotenv() is called at initialization.")
        raise ValueError(msg)
    return api_key

########################################################################
from smolagents import OpenAIServerModel
def groq_build_reasoning_model(model_id="llama-3.3-70b-versatile"):
    key_name = "GROQ_KEY"
    api_base = "https://api.groq.com/openai/v1"
    api_key = get_api_key(key_name)
    
    model = OpenAIServerModel(model_id=model_id,
                              api_base=api_base,
                              api_key=api_key,
                              client_kwargs={"max_retries": 8} 
                              )
    return model
