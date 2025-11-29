# Project Brief: FitSync (AI Wellness Concierge)

## 1. Executive Summary
FitSync is a multi-agent conversational concierge designed to reduce the friction of living a healthy lifestyle. Unlike passive tracking apps, FitSync actively "watches" what you eat via photos and adjusts your fitness plan in real-time based on user feedback. It combines a Nutritionist Agent, a Trainer Agent, and a Dining Assistant into a single chat interface.

## 2. Problem Statement
* **Friction of Tracking:** Manual data entry (weighing food, searching databases) causes high user churn.
* **Siloed Data:** Nutrition data rarely informs workout planning immediately (e.g., a heavy lunch doesn't trigger a lighter cardio suggestion).
* **Decision Fatigue:** Users struggle to make healthy choices at restaurants without pre-reading menus.

## 3. MVP Scope (The "Must Haves")
To meet the Nov 30 deadline, the MVP focuses strictly on Chat Interaction.

### Core Features
* **Visual Calorie Logging:** User uploads food photos; Agent estimates macros using multimodal capabilities.
* **Adaptive Workout Advice:** User reports physical state (e.g., "knee hurts"); Agent modifies the workout plan in real-time.
* **Restaurant Decider:** User names a restaurant; Agent retrieves the menu via Google Search and recommends dishes.
* **User Profile Memory:** Persists Name, Weight Goal, Allergies, and Injury Status across sessions.

### Out of Scope (Critical Exclusions)
* Real-time Apple Watch/HealthKit Integration.
* MyFitnessPal API Integration.
* Payment Processing.

## 4. Success Metrics
* **Accuracy:** Nutrition Agent correctly identifies food items in 8/10 test images.
* **Context Retention:** Trainer Agent recalls user injury status from previous turns in 100% of test cases.
* **Latency:** Restaurant Agent returns menu recommendations in <10 seconds.