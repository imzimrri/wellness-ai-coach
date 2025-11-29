# Project Description: FitSync

### Problem Statement
Living a healthy lifestyle is often harder than it should be due to three main friction points:
1.  **The Burden of Tracking:** Manual data entry (weighing food, searching databases) is tedious and leads to high user churn. Most people stop tracking because it feels like a second job.
2.  **Siloed Data:** Nutrition data rarely informs workout planning immediately. For example, eating a heavy lunch doesn't automatically trigger a suggestion for a lighter cardio session later that day.
3.  **Decision Fatigue:** Making healthy choices at restaurants is difficult. Users often have to pre-read menus or guess which items fit their goals, leading to "cheat meals" out of convenience rather than choice.

I built FitSync to solve these problems by creating an active, intelligent concierge that removes the manual work from wellness.

### Why agents?
Agents are the right solution because wellness is multifaceted and requires specialized reasoning that a single chat bot cannot provide effectively.
*   **Specialization:** A Nutritionist needs vision capabilities to analyze food photos, while a Dining Assistant needs search capabilities to find menus. Separating these into agents allows for optimized prompting and tool use.
*   **Context Sharing:** Agents can share a "Memory Bank." When the Nutritionist logs a high-calorie meal, the Trainer agent needs to know about it to adjust the workout. A multi-agent system allows this dynamic interplay of state.
*   **Active vs. Passive:** Standard apps wait for input. Agents can proactively "think" about how one action (eating) affects another (training), mimicking a real human coaching team.

### What you created
I built **FitSync**, a multi-agent conversational concierge. The architecture consists of:
1.  **Orchestrator Agent:** The central brain that analyzes user input and routes requests. It decides whether you need a nutritionist, a trainer, or help with a restaurant menu.
2.  **Nutritionist Agent:** Powered by Gemini's multimodal capabilities, it analyzes food photos to estimate calories and macros without manual entry.
3.  **Trainer Agent:** Provides adaptive workout advice. It checks your profile and current state (e.g., "my knee hurts") to modify training plans in real-time.
4.  **Dining Agent:** Uses Google Search to retrieve real restaurant menus and recommends specific dishes that align with your dietary goals.
5.  **Memory Bank:** A persistent storage layer that holds the user's profile (goals, injuries, allergies) and conversation history, ensuring every agent knows who you are.

### Demo
*   **Onboarding:** The user starts by chatting with the system, which learns their name, goals (e.g., "Muscle Gain"), and limitations (e.g., "Knee injury").
*   **Visual Logging:** The user uploads a photo of a burger. The Nutritionist Agent instantly identifies it, estimates the macros, and logs it to memory.
*   **Adaptive Training:** The user asks, "I'm feeling sluggish after that burger, what should I do at the gym?" The Trainer Agent suggests a modified, lower-intensity workout.
*   **Dining Out:** The user asks, "What should I eat at The Cheesecake Factory?" The Dining Agent searches the menu and suggests the "SkinnyLicious Grilled Salmon" to stay on track.

### The Build
FitSync was built using:
*   **Google Gemini 2.0 Flash:** The core intelligence powering all agents for its speed and multimodal capabilities.
*   **Python & Streamlit:** For the application logic and interactive web interface.
*   **Google GenAI SDK:** To interface with the Gemini models.
*   **Custom Tooling:** I implemented a custom `MemoryBank` class to handle state persistence and a `Search` tool for the Dining Agent.

### If I had more time, this is what I'd do
*   **Wearable Integration:** I would integrate with Apple HealthKit or Google Fit to pull real-time activity data (steps, heart rate) directly into the Memory Bank.
*   **MyFitnessPal Sync:** Instead of just estimating calories, I would sync with established databases for higher precision.
*   **Proactive Notifications:** I would add a background agent that sends push notifications (e.g., "You haven't logged lunch yet, here's a quick recipe").
*   **Payment Processing:** I would add a subscription model for premium features like detailed meal plans and 1-on-1 coaching mode.
