import streamlit as st
from collections import defaultdict
import time

st.set_page_config(page_title="Leadership Journey AI", layout="wide", initial_sidebar_state="expanded")

# ---- Modern Black/White/Green Color Palette ----
# [CSS block remains unchanged — omitted here for brevity]

# ---- Enhanced Leadership Data with Points System ----
leadership_styles = {
    "Red Energy": {
        "traits": ["Competitive", "Results-Oriented", "Strong-Willed", "Risk-Taker", "Direct"],
        "description": "You lead with intensity and drive, focusing on results and pushing boundaries",
        "strengths": "Drives performance, makes tough decisions, creates urgency, delivers results",
        "development": "Balance directness with empathy, involve others in decision-making",
        "points": 15
    },
    "Blue Energy": {
        "traits": ["Analytical", "Diplomatic", "Precise", "Questioning", "Conventional"],
        "description": "You lead through careful analysis and systematic approaches",
        "strengths": "Makes data-driven decisions, ensures quality, manages risk effectively",
        "development": "Speed up decision-making, embrace creative solutions, trust intuition",
        "points": 12
    },
    "Yellow Energy": {
        "traits": ["Expressive", "Inspiring", "Trusting", "Talkative", "Sociable"],
        "description": "You lead by energizing others and building enthusiasm around shared goals",
        "strengths": "Motivates teams, builds relationships, drives innovation, creates positive culture",
        "development": "Focus on follow-through, pay attention to details, balance optimism with realism",
        "points": 18
    },
    "Green Energy": {
        "traits": ["Patient", "Steady", "Systematic", "Good Listener", "Caring"],
        "description": "You lead through stability and genuine care for your team members",
        "strengths": "Builds trust, ensures team cohesion, provides consistent support, maintains stability",
        "development": "Embrace change more readily, make decisions faster, assert when necessary",
        "points": 20
    }
}

educational_content = {
    "intro": {
        "title": "🧭 Welcome to Leadership Journey AI",
        "content": "I'm your AI leadership coach, here to guide you through real workplace scenarios. Think of this as a conversation where we'll explore how different leadership energies work in practice. You'll earn points based on your choices, and I'll help you understand your natural leadership style. Ready to begin your leadership journey? 🚀"
    },
    "scenarios": [
        {
            "ai_intro": "🧠 **Transformational Leadership in Action**\n\nMicrosoft CEO Satya Nadella revitalized company culture by encouraging empathy and continuous learning—hallmarks of transformational leadership. This style empowers individuals to rise to challenges through inspiration and trust.",
            "context": "You're leading a product team at a growing startup. Your senior engineer, Sarah, just informed you she's burned out and considering stepping back. She's crucial to next week's investor demo.",
            "ai_question": "This is a critical moment that will test your leadership instincts. How do you respond to Sarah?",
            "learning_point": "**Crisis Leadership**: When team members are struggling, different leadership energies respond differently. Red energy takes charge, Blue analyzes the situation, Yellow focuses on morale, and Green provides support."
        },
        {
            "ai_intro": "🌐 **Servant Leadership & Remote C
