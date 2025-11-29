from google.genai import types
from google.genai import Client
import os

# Initialize the client (assuming GOOGLE_API_KEY is set in env)
# In a real tool context, the client might be passed in or initialized globally
# For this simple tool wrapper, we'll just define the tool configuration

search_tool = types.Tool(
    google_search=types.GoogleSearch()
)

def get_search_tool():
    """Returns the Google Search tool configuration for the Gen AI SDK."""
    return search_tool
