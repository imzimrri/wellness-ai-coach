from google.genai import types
from google.genai import Client
import os

class TrainerAgent:
    def __init__(self, client: Client):
        self.client = client
        self.model = "gemini-2.5-pro" # Using Pro for better reasoning on complex plans
        self.system_instruction = """
        Role: You are a supportive but firm fitness instructor.
        Context: You must respect the user's `current_injuries` in the User Profile.
        Instructions:
        1.  If the user reports pain (e.g., "knee hurts"), IMMEDIATELY modify the plan to be low-impact (e.g., switch squats to swimming).
        2.  If the user reports high calorie intake from the Nutritionist, suggest a slightly more intense cardio session to balance it.
        3.  Keep responses short and action-oriented (bullet points).
        """

    def get_workout_advice(self, user_input: str, user_profile: dict):
        """
        Provides workout advice based on user input and profile.
        
        Args:
            user_input: The user's query or status report.
            user_profile: The user's profile.
            
        Returns:
            The model's advice.
        """
        prompt = f"""
        User Input: {user_input}
        User Profile: {user_profile}
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.5
            )
        )
        return response.text
