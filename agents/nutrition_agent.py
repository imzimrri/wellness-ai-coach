from google.genai import types
from google.genai import Client
import os
from tools.calculator import calculate_macros
from utils.logger import AgentLogger

class NutritionAgent:
    def __init__(self, client: Client):
        self.client = client
        self.model = "gemini-2.5-flash"
        self.logger = AgentLogger()
        self.system_instruction = """
        Role: You are a clinical nutritionist. You are analytical, precise, and non-judgmental.
        Capabilities: You can "see" food via the user's uploaded images.
        Instructions:
        1.  Identify every food item in the image.
        2.  Estimate portion size and macros (Protein, Carbs, Fat, Calories).
        3.  Use the `calculate_macros` tool to sum the totals; do not do math in your head.
        4.  Output a neat summary table.
        """
        self.tools = [calculate_macros]

    def analyze_food(self, content_parts, context: str = ""):
        """
        Analyzes food content (text and/or image) to estimate macros.
        
        Args:
            content_parts: A list of content parts (text or image) for the model.
            context: Additional context (User Profile + Memory).
            
        Returns:
            The model's response text.
        """
        self.logger.log("NutritionAgent", "Action", "Analyzing food content")
        
        # If context is provided, append it to the content parts (as text)
        final_contents = content_parts
        if context:
            # If content_parts is a list, append the context string
            if isinstance(final_contents, list):
                final_contents.append(f"\n\nContext:\n{context}")
            else:
                # If it's just a string (unlikely given type hint but possible), append
                final_contents = [final_contents, f"\n\nContext:\n{context}"]

        response = self.client.models.generate_content(
            model=self.model,
            contents=final_contents,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                tools=self.tools,
                temperature=0.1 # Low temperature for precision
            )
        )
        
        # Log tool usage if present
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                     self.logger.log("NutritionAgent", "Tool Call", f"Using {part.function_call.name}")

        return response.text
