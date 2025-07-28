import streamlit as st
from collections import defaultdict
import time

st.set_page_config(page_title="Leadership Journey AI", layout="wide", initial_sidebar_state="expanded")

# ---- Leadership Styles Data (Renamed & Refined) ----
leadership_styles = {
    "The Driver (decisive, action-oriented, direct)": {
        "traits": ["Competitive", "Results-Oriented", "Strong-Willed", "Risk-Taker", "Direct"],
        "description": "You lead with urgency, clarity, and focus on outcomes.",
        "strengths": "Pushes for results, tackles tough challenges, leads from the front.",
        "development": "Balance your directness with emotional awareness and collaborative input.",
        "points": 15
    },
    "The Strategist (analytical, thoughtful, deliberate)": {
        "traits": ["Analytical", "Diplomatic", "Precise", "Questioning", "Conventional"],
        "description": "You approach leadership with logic, structure, and methodical decision-making.",
        "strengths": "Excels at risk management, systems thinking, and informed decisions.",
        "development": "Lean into intuition and act decisively when data is incomplete.",
        "points": 12
    },
    "The Motivator (inspiring, energetic, persuasive)": {
        "traits": ["Expressive", "Inspiring", "Trusting", "Talkative", "Sociable"],
        "description": "You spark momentum and rally teams with passion and optimism.",
        "strengths": "Inspires belief, energizes collaboration, drives vision.",
        "development": "Ensure consistency and manage details with discipline.",
        "points": 18
    },
    "The Stabilizer (calm, dependable, supportive)": {
        "traits": ["Patient", "Steady", "Systematic", "Good Listener", "Caring"],
        "description": "You lead with empathy, consistency, and a calm presence.",
        "strengths": "Creates psychological safety, ensures cohesion, builds long-term trust.",
        "development": "Step into discomfort, speak up more assertively, and embrace calculated risks.",
        "points": 20
    }
}

# ---- Educational Scenarios ----
educational_content = {
    "intro": {
        "title": "🧭 Welcome to Leadership Journey AI",
        "content": "I'm your AI leadership coach, here to guide you through real workplace scenarios. Think of this as a conversation where we'll explore how different leadership tendencies show up in practice. You'll earn points based on your choices, and I'll help you understand your natural leadership approach. Ready to begin your leadership journey? 🚀"
    },
    "scenarios": [
        {
            "ai_intro": "🧠 **Transformational Leadership in Action**\n\nMicrosoft CEO Satya Nadella revitalized company culture by encouraging empathy and continuous learning—hallmarks of transformational leadership.",
            "context": "You're leading a product team at a growing startup. Your senior engineer, Sarah, just informed you she's burned out and considering stepping back. She's crucial to next week's investor demo.",
            "ai_question": "This is a critical moment that will test your leadership instincts. How do you respond to Sarah?",
            "learning_point": "**Crisis Leadership**: Different leadership instincts shape how we handle burnout and performance stress."
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
    st.session_state.submitted = False

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
    choice = st.radio("Which leadership mindset best matches your instinct?", options)

    if not st.session_state.submitted:
        if st.button("Submit Choice"):
            points = leadership_styles[choice]["points"]
            st.session_state.scores[choice] += points

            st.success(f"✅ You chose **{choice}**.\n\n{leadership_styles[choice]['description']}")
            st.info(f"**Learning Point:** {scenario['learning_point']}")
            st.session_state.submitted = True

    if st.session_state.submitted:
        if st.session_state.current_index >= len(educational_content['scenarios']):
            st.session_state.finished = True
        else:
            if st.button("Next Scenario »"):
                st.session_state.current_index += 1
                st.session_state.submitted = False

if st.session_state.finished:
    st.header("🎯 Your Leadership Style Summary")
    totals = dict(st.session_state.scores)
    sorted_styles = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    top_style = sorted_styles[0][0] if sorted_styles else "Unknown"

    st.subheader(f"🏆 Dominant Style: {top_style}")
    st.markdown(f"**Traits:** {', '.join(leadership_styles[top_style]['traits'])}")
    st.markdown(f"**Strengths:** {leadership_styles[top_style]['strengths']}")
    st.markdown(f"**Development Tip:** {leadership_styles[top_style]['development']}")
    st.balloons()
    st.stop()
