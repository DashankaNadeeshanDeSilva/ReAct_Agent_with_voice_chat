import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv


class LLM():
    def __init__(self):
        load_dotenv() # Load the .env file
        self.AGENT_LLM = os.getenv("AGENT_LLM")
        self.API_KEY = os.getenv("TOGETHER_API_KEY")
        os.environ["OPENAI_API_KEY"] = self.API_KEY
        self.MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")

    def init_llm(self):
        if not self.AGENT_LLM:
            raise ValueError("Agent llm model is not set in the environment variables.")
        if not self.API_KEY:
            raise ValueError("API_KEY is not set in the environment variables.")
        
        llm = init_chat_model(
            model=self.AGENT_LLM,
            model_provider=self.MODEL_PROVIDER,
            temperature=0.5
        )

        return llm


if __name__ == "__main__":
    print("Initializing LLM...")
    llm = LLM().init_llm()
    print(llm.invoke("Who went to the moon for the first time ?").content)