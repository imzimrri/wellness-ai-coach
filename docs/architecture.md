# Architecture Document: FitSync

## 1. High Level Architecture
[cite_start]FitSync uses a **Coordinator Multi-Agent Pattern** (Level 3: Collaborative Multi-Agent System)[cite: 889]. A central "Router" agent interprets user intent and delegates tasks to specialized sub-agents.

### System Diagram
```mermaid
graph TD
    User[User Interface (Streamlit)] <--> Router[Orchestrator Agent]
    Router <--> Memory[Session & Long-Term Memory]
    
    Router -->|Intent: Log Food| Nutrition[Nutritionist Agent]
    Router -->|Intent: Workout| Trainer[Trainer Agent]
    Router -->|Intent: Dining| Dining[Dining Agent]
    
    Nutrition -->|Tool Use| Calculator[Calculator Tool]
    Dining -->|Tool Use| GSearch[Google Search Tool]

#### Tech Stack
Frontend: Streamlit (Python) for rapid chat UI and image handling.

Backend/AI: Google Gen AI SDK (Python).

Model: Gemini 1.5 Pro (Orchestrator/Trainer), Gemini 1.5 Flash (Nutritionist/Dining).

State Management: Local JSON file (MVP) or SQLite for user_profile.

##### Agent Definitions
Orchestrator (Router):


Role: Manages conversation flow and state.

Responsibility: Detects intent, routes to sub-agents, manages session_history.

Nutritionist Agent:

Input: Image (Food) or Text.

Tools: calculate_macros.

Output: Structured JSON (Calories, Protein, Carbs, Fat).

Dining Agent:

Input: Restaurant Name.


Tools: Google Search_retrieval (Grounding).

Output: Top 3 menu recommendations fitting user goals.

4. Data Models
User Profile (Long-Term Memory)
JSON

{
  "user_id": "string",
  "name": "string",
  "goals": ["weight_loss", "muscle_gain"],
  "dietary_restrictions": ["vegan", "gluten_free"],
  "current_injuries": ["left_knee_pain"]
}

---