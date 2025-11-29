from google.genai import types
from google.genai import Client
import os
from agents.nutrition_agent import NutritionAgent
from agents.dining_agent import DiningAgent
from agents.trainer_agent import TrainerAgent
from utils.logger import AgentLogger
from utils.memory import MemoryBank

class Orchestrator:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        self.client = Client(api_key=api_key)
        self.nutrition_agent = NutritionAgent(self.client)
        self.dining_agent = DiningAgent(self.client)
        self.trainer_agent = TrainerAgent(self.client)
        self.logger = AgentLogger()
        
        self.model = "gemini-2.5-pro"

        # Initialize Memory
        self.memory_bank = MemoryBank()

        # Load System Instructions
        # We hardcode this to prevent the Orchestrator from seeing other agents' tools (like Search)
        # and trying to use them, which causes a crash.
        self.system_instruction = """
        **Role:** You are the Head Coach of FitSync. Your job is to manage the user's wellness journey by routing them to your team of specialists.
        **Context:** You have access to the `User Profile` including name, goals, and injuries.
        **Instructions:**
        1.  Analyze the user's input.
        2.  If the user explicitly asks you to remember something (e.g., "I am vegan", "My name is Alex"), call the `remember_fact` tool.
        3.  Otherwise, determine the best specialist to handle the request.
        4.  Output ONLY the name of the specialist: "Nutritionist", "Trainer", "Dining", or "Chat" (for general conversation).
        5.  Do NOT call the specialist as a tool. Just output their name.
        """

        # Define Tools
        self.tools = [self.remember_fact]

    def remember_fact(self, key: str, value: str):
        """
        Saves a fact about the user to long-term memory.
        Use this when the user explicitly tells you something important to remember, 
        or when you learn a new preference (e.g., "I am vegan", "My name is Alex").
        
        Args:
            key: A short key for the fact (e.g., "name", "diet", "allergies").
            value: The value of the fact.
        """
        self.logger.log("Orchestrator", "Memory", f"Remembering: {key} = {value}")
        self.memory_bank.set_fact(key, value)
        return f"I have remembered that your {key} is {value}."

    def route_request(self, user_input: str, user_profile: dict, image_part=None):
        """
        Determines the users intent and routes to the appropriate agent.
        """
        try:
            # If there's an image, default to Nutritionist
            if image_part:
                self.logger.log("Orchestrator", "Routing", "Image detected -> NutritionAgent")
                return self.nutrition_agent.analyze_food([user_input, image_part])

            # Inject Long-term Memory into Context
            memory_context = self.memory_bank.get_all_memories_as_text()
            full_context = f"User Profile: {user_profile}\n{memory_context}"
            
            self.logger.log("Orchestrator", "Analysis", f"Input: {user_input}")

            # 1. Ask the model to determine intent OR use memory tools
            response = self.client.models.generate_content(
                model=self.model,
                contents=f"User Input: {user_input}\nContext: {full_context}\n\nDetermine the best agent (Nutritionist, Dining, Trainer) or handle as Chat. Output ONLY the agent name or use the remember_fact tool.",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    tools=self.tools,
                    temperature=0.1
                )
            )

            # Check for tool calls (Memory storage)
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.function_call:
                        if part.function_call.name == "remember_fact":
                            # Execute the tool
                            args = part.function_call.args
                            result = self.remember_fact(args["key"], args["value"])
                            return result

            # Parse the text response for routing
            agent_name = response.text.strip().lower() if response.text else "chat"
            
            # Clean up potential extra text if the model is chatty
            if "nutritionist" in agent_name: agent_name = "nutritionist"
            elif "dining" in agent_name: agent_name = "dining"
            elif "trainer" in agent_name: agent_name = "trainer"
            
            self.logger.log("Orchestrator", "Routing", f"Intent detected: {agent_name}")
            
            if agent_name == "nutritionist":
                return self.nutrition_agent.analyze_food([user_input], context=full_context)
            elif agent_name == "dining":
                enriched_profile = user_profile.copy()
                enriched_profile["memory_bank"] = memory_context
                return self.dining_agent.recommend_items(user_input, enriched_profile)
            elif agent_name == "trainer":
                enriched_profile = user_profile.copy()
                enriched_profile["memory_bank"] = memory_context
                return self.trainer_agent.get_workout_advice(user_input, enriched_profile)
            else:
                # Fallback to Orchestrator handling general chat with memory context
                self.logger.log("Orchestrator", "Action", "Handling general chat")
                # We can just return the text if the model already answered, but often 
                # the routing prompt is just "Trainer", so we might need a second call for chat 
                # IF the first call was just a classification.
                # However, for "Chat", we usually want a real response.
                # Let's do a specific chat call if it falls back to chat, to ensure a good response.
                
                chat_response = self.client.models.generate_content(
                    model=self.model,
                    contents=f"User Input: {user_input}\n{full_context}",
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        tools=self.tools # Allow memory tools here too
                    )
                )
                
                # Check for tool calls again in chat response
                if chat_response.candidates and chat_response.candidates[0].content.parts:
                    for part in chat_response.candidates[0].content.parts:
                        if part.function_call:
                            if part.function_call.name == "remember_fact":
                                args = part.function_call.args
                                return self.remember_fact(args["key"], args["value"])

                return chat_response.text

        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            self.logger.log("Orchestrator", "Error", f"{str(e)}\n{error_trace}")
            return f"Error in orchestration: {str(e)}"
