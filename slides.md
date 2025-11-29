# FitSync: Your AI Wellness Concierge

---

## Problem Statement
**The Friction of Healthy Living**

*   **Tracking is tedious:** Manual entry leads to high churn.
*   **Data is siloed:** Nutrition doesn't inform fitness in real-time.
*   **Decision Fatigue:** Eating out requires too much research.

**Goal:** Remove the manual work from wellness with an active, intelligent concierge.

---

## Why Agents?
**Specialization & Collaboration**

*   **Specialized Roles:** A Nutritionist needs vision; a Dining Assistant needs search. Agents allow for optimized tools and prompts.
*   **Shared Context:** Agents share a "Memory Bank." If you eat a heavy meal, the Trainer knows to adjust your workout.
*   **Active Reasoning:** Agents don't just log data; they "think" about how one action affects another.

---

## Architecture
**Multi-Agent System**

*   **Orchestrator:** The central brain that routes requests.
*   **Nutritionist Agent:** Uses **Gemini Multimodal** to analyze food photos.
*   **Trainer Agent:** Adapts workouts based on profile and injury status.
*   **Dining Agent:** Uses **Google Search** to find healthy menu items.
*   **Memory Bank:** Persists user context across all interactions.

*(Insert Architecture Diagram Here)*

---

## Demo
**FitSync in Action**

1.  **Onboarding:** System learns your goals and injuries.
2.  **Visual Logging:** Upload a photo -> Instant calorie/macro logging.
3.  **Adaptive Training:** "My knee hurts" -> Trainer modifies leg day.
4.  **Dining Out:** "Cheesecake Factory" -> Dining Agent recommends the "SkinnyLicious Salmon."

---

## The Build
**Tech Stack**

*   **Core Intelligence:** Google Gemini 2.0 Flash
*   **Framework:** Python & Streamlit
*   **Tools:** Google GenAI SDK, Custom Memory Bank, Google Search Tool
*   **Key Concept:** Context Injection for personalized, long-term memory.
