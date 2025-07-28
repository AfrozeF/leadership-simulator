import streamlit as st
from collections import defaultdict
import time

st.set_page_config(page_title="Leadership Journey AI", layout="wide", initial_sidebar_state="expanded")

# ---- Modern Black/White/Green Color Palette ----
# (Optional styling block can be added here)

# ---- Leadership Styles Data ----
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

# ---- Educational Scenarios ----
educational_content = {
    "intro": {
        "title": "🧭 Welcome to Leadership Journey AI",
        "content": "I'm your AI leadership coach, here to guide you through real workplace scenarios. Think of this as a conversation where we'll explore how different leadership energies work in practice. You'll earn points based on your choices, and I'll help you understand your natural leadership style. Ready to begin your leadership journey? 🚀"
    },
    "scenarios": [
        {
            "ai_intro": "🧠 **Transformational Leadership in Action**\n\nMicrosoft CEO Satya Nadella revitalized company culture by encouraging empathy and continuous learning—hallmarks of transformational leadership.",
            "context": "You're leading a product team at a growing startup. Your senior engineer, Sarah, just informed you she's burned out and considering stepping back. She's crucial to next week's investor demo.",
            "ai_question": "This is a critical moment that will test your leadership instincts. How do you respond to Sarah?",
            "learning_point": "**Crisis Leadership**: Different leadership energies respond uniquely to team struggles."
        },
        {
            "ai_intro": "🌐 **Servant Leadership & Remote Culture**\n\nBuffer, the fully remote company, thrives by prioritizing transparency and psychological safety.",
            "context": "You're managing a remote marketing team. Your weekly check-ins have become quiet and unproductive, with team morale noticeably declining.",
            "ai_question": "Virtual team dynamics require intentional leadership. What's your approach to re-energize your remote team?",
            "learning_point": "**Remote Team Dynamics**: Leading distributed teams requires intentional connection."
        },
        {
            "ai_intro": "🔁 **Adaptive Leadership in Uncertainty**\n\nCompanies like Airbnb lean into adaptive leadership during uncertainty—transparency and resilience are key.",
            "context": "You're leading a finance team during company-wide budget cuts. One of your top performers is worried about job security.",
            "ai_question": "During times of change, how do you help your team navigate uncertainty?",
            "learning_point": "**Change Management**: Support and direction are vital in uncertain times."
        },
        {
            "ai_intro": "🧩 **Conflict-Competent Leadership**\n\nNetflix leaders are trained to resolve tension through candid conversations and direct feedback.",
            "context": "Two team leads are arguing publicly in a shared Slack channel. Tensions are rising.",
            "ai_question": "Public conflicts can damage team dynamics. How do you handle it?",
            "learning_point": "**Conflict Resolution**: Leaders can choose direct or collaborative interventions."
        },
        {
            "ai_intro": "🌍 **Culturally Intelligent Leadership**\n\nGM CEO Mary Barra practices inclusive leadership by adapting communication across global teams.",
            "context": "You're overseeing an international project. A European manager complains that the American team is too direct.",
            "ai_question": "Cultural misunderstandings can derail projects. How do you navigate different styles?",
            "learning_point": "**Cross-Cultural Leadership**: Bridge communication gaps to maintain trust and clarity."
        }
    ]
}

# ---- Streamlit App Logic ----
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
    st.session_state.scores = defaultdict(int)
    st.session_state.finished = False

if st.session_state.current_index == 0:
    st.title(educational_content["intro"]["title"])
    st.markdown(educational_content["intro"]["content"])
    if st.button("Begin »"):
        st.session_state.current_index += 1
else:
    index = st.session_state.current_index - 1
    scenario = educational_content["scenarios"][index]

    st.subheader(f"Scenario {st.session_state.current_index}: {scenario['ai_intro']}")
    st.markdown(f"**Context:** {scenario['context']}")
    st.markdown(f"**Challenge:** {scenario['ai_question']}")

    options = list(leadership_styles.keys())
    choice = st.radio("Which energy best fits your response?", options)

    if st.button("Submit Choice"):
        points = leadership_styles[choice]["points"]
        st.session_state.scores[choice] += points

        st.success(f"✅ You chose **{choice}** energy.\n\n{leadership_styles[choice]['description']}")
        st.info(f"**Learning Point:** {scenario['learning_point']}")

        if st.session_state.current_index >= len(educational_content['scenarios']):
            st.session_state.finished = True
        else:
            time.sleep(1.5)
            st.session_state.current_index += 1

if st.session_state.finished:
    st.header("🎯 Your Leadership Style
