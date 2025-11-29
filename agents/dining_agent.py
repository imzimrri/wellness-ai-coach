from google.genai import types
from google.genai import Client
import os
from tools.search_tool import get_search_tool
from utils.logger import AgentLogger

class DiningAgent:
    def __init__(self, client: Client):
        self.client = client
        self.model = "gemini-2.5-flash"
        self.logger = AgentLogger()
        self.system_instruction = """
        Role: You are a savvy dining concierge who finds healthy gems on any menu.
        Tools: You have access to Google Search to find real menus.
        Instructions:
        1.  Use Google Search to find the menu of the requested restaurant.
        2.  Filter items based on the user's `dietary_restrictions` (e.g., Vegan).
        3.  Recommend the 3 best options that align with their `goals` (e.g., High Protein).
        """
        self.tools = [get_search_tool()]

    def recommend_items(self, restaurant_name: str, user_profile: dict):
        """
        Finds healthy menu items for a given restaurant.
        
        Args:
            restaurant_name: The name of the restaurant.
            user_profile: The user's profile containing dietary restrictions and goals.
            
        Returns:
            The model's recommendation.
        """
        self.logger.log("DiningAgent", "Action", f"Searching menu for: {restaurant_name}")
        
        prompt = f"""
        Restaurant: {restaurant_name}
        User Profile: {user_profile}
        
        Find the menu and recommend the best options.
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                tools=self.tools,
                temperature=0.2
            )
        )
        
        # Log tool usage if present
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                     self.logger.log("DiningAgent", "Tool Call", f"Using {part.function_call.name}")
                     
        return response.text
