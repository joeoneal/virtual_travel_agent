import os
import dotenv
from serpapi import GoogleSearch

dotenv.load_dotenv()

class SerpApiClient:
    def __init__(self):
        self.key = os.getenv("SERP_KEY")

        if not self.key:
            raise ValueError("SERP_KEY not found. Please check your .env file.")
    
    def search(self, params: dict) -> dict:
        params["api_key"] = self.key
        search = GoogleSearch(params)
        return search.get_dict()