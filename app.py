import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
from agents.orchestrator import Orchestrator

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(page_title="FitSync", page_icon="💪", layout="wide")

# Initialize Orchestrator
if "orchestrator" not in st.session_state:
    try:
        st.session_state.orchestrator = Orchestrator()
    except Exception as e:
        st.error(f"Failed to initialize Orchestrator: {e}")
        st.stop()

# Load Memory
memory = {}
if "orchestrator" in st.session_state:
    memory = st.session_state.orchestrator.memory_bank.load_memory()

# Onboarding Flow
if not memory.get("name"):
    st.title("Welcome to FitSync! 👋")
    st.markdown("Let's get to know you better to personalize your wellness journey.")
    
    with st.form("onboarding_form"):
        st.subheader("Tell us about yourself")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("What should we call you?")
            age = st.number_input("Age", min_value=1, max_value=120, step=1, value=30)
            height = st.text_input("Height (e.g., 5'10\" or 178cm)")
        with col2:
            weight = st.text_input("Weight (e.g., 160lbs or 75kg)")
            gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Non-binary", "Other"])
        
        st.subheader("Your Wellness Profile")
        goals = st.multiselect("What are your main goals?", 
                               ["Weight Loss", "Muscle Gain", "Endurance", "Flexibility", "Stress Management", "Better Sleep", "General Health"],
                               ["General Health"])
        
        dietary_restrictions = st.multiselect("Any dietary restrictions?", 
                                              ["None", "Vegan", "Vegetarian", "Gluten-Free", "Keto", "Dairy-Free", "Nut Allergy", "Shellfish Allergy"],
                                              ["None"])
        
        injuries = st.text_area("Do you have any current injuries or physical limitations?", "None")
        
        submitted = st.form_submit_button("Start My Journey 🚀")
        
        if submitted:
            if name:
                user_profile = {
                    "name": name,
                    "age": age,
                    "height": height,
                    "weight": weight,
                    "gender": gender,
                    "goals": goals,
                    "dietary_restrictions": dietary_restrictions,
                    "current_injuries": injuries
                }
                # Save to memory
                st.session_state.orchestrator.memory_bank.save_memory(user_profile)
                st.success("Profile saved! specificy reloading...")
                st.rerun()
            else:
                st.error("Please enter your name.")
    
    # Stop execution here so the main app doesn't load until onboarding is done
    st.stop()

# Sidebar: User Profile (Long-term Memory)
with st.sidebar:
    st.title(f"Hi, {memory.get('name')}!")
    
    with st.expander("Edit Profile"):
        # Editable Fields with defaults from Memory
        name = st.text_input("Name", memory.get("name", ""))
        goals = st.multiselect("Goals", 
                               ["Weight Loss", "Muscle Gain", "Endurance", "Flexibility", "Stress Management", "Better Sleep", "General Health"],
                               memory.get("goals", []))
        dietary_restrictions = st.multiselect("Dietary Restrictions", 
                                              ["None", "Vegan", "Vegetarian", "Gluten-Free", "Keto", "Dairy-Free", "Nut Allergy", "Shellfish Allergy"],
                                              memory.get("dietary_restrictions", []))
        injuries = st.text_area("Current Injuries", memory.get("current_injuries", "None"))
        
        if st.button("Update Profile"):
            updated_profile = memory.copy()
            updated_profile.update({
                "name": name,
                "goals": goals,
                "dietary_restrictions": dietary_restrictions,
                "current_injuries": injuries
            })
            st.session_state.orchestrator.memory_bank.save_memory(updated_profile)
            st.success("Updated!")
            st.rerun()
    
    # Construct user_profile for Agents
    user_profile = memory
    
    st.divider()
    st.subheader("🧠 Memory Bank")
    st.json(memory)

    st.divider()
    if st.button("Reset Onboarding", type="primary"):
        st.session_state.orchestrator.memory_bank.clear_memory()
        # Clear session state to ensure clean slate
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Main Chat Interface
st.title("FitSync: Your AI Wellness Concierge")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], width=200)

# User Input
user_input = st.chat_input("How can I help you today?")

# File Uploader in Expander (Bottom of chat)
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

with st.expander("📸 Upload Food Photo", expanded=False):
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"], key=f"uploader_{st.session_state.uploader_key}")

if user_input or uploaded_file:
    # Handle Image Upload
    image_part = None
    if uploaded_file:
        image = Image.open(uploaded_file)
        # Display user image in chat
        with st.chat_message("user"):
            if user_input:
                st.markdown(user_input)
            st.image(image, width=200)
        
        # Add to history
        st.session_state.messages.append({"role": "user", "content": user_input or "Uploaded an image", "image": image})
        
        # Prepare image for Gemini
        image_part = image
        
        # Increment key to clear uploader on next run
        st.session_state.uploader_key += 1
        # We don't rerun immediately here because we want to show the response first? 
        # Actually, if we rerun, we lose the execution flow for the response generation?
        # No, we need to generate response FIRST, then maybe rerun or just let the key update for NEXT interaction.
        # But if we don't rerun, the file stays in the widget UI until the user interacts again.
        # Let's process, then set a flag to rerun? 
        # Or just let it be. The key update will take effect on the NEXT script run. 
        # But the user sees the "x" until then.
        # To clear it immediately visually, we need a rerun.
        # But if we rerun, we lose the `uploaded_file` variable for *this* run? 
        # No, we have `image` object now.
        
    elif user_input:
        # Display user text in chat
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

    # Get Agent Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = st.session_state.orchestrator.route_request(
                user_input=user_input or "Analyze this image",
                user_profile=user_profile,
                image_part=image_part
            )
            st.markdown(response_text)
            
    # Add to history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    # If we processed an image, force a rerun to clear the uploader visually
    if image_part:
        st.rerun()

# Developer Mode: Observability
with st.expander("🛠️ Developer Mode: Agent Logs"):
    if "agent_logs" in st.session_state:
        for log in st.session_state.agent_logs:
            st.text(f"[{log['timestamp']}] {log['agent']} - {log['action']}: {log['details']}")
