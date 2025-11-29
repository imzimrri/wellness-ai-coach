import logging
import streamlit as st
from datetime import datetime

class AgentLogger:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("FitSync")
        
        # Initialize session state for logs if not exists
        if "agent_logs" not in st.session_state:
            st.session_state.agent_logs = []

    def log(self, agent_name: str, action: str, details: str):
        """
        Logs an action taken by an agent.
        
        Args:
            agent_name: Name of the agent (e.g., "Orchestrator").
            action: The action performed (e.g., "Routing", "Tool Call").
            details: Details about the action.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "agent": agent_name,
            "action": action,
            "details": details
        }
        
        # Add to Streamlit session state for UI display
        if "agent_logs" in st.session_state:
            st.session_state.agent_logs.append(log_entry)
            
        # Also log to console/file
        self.logger.info(f"[{agent_name}] {action}: {details}")

    def get_logs(self):
        """Returns the list of logs from session state."""
        if "agent_logs" in st.session_state:
            return st.session_state.agent_logs
        return []
