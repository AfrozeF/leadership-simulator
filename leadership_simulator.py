import streamlit as st
from collections import defaultdict
import time

st.set_page_config(page_title="Leadership Journey AI", layout="centered", initial_sidebar_state="collapsed")

# ---- Custom Colors ----
PRIMARY_GREEN = "#2ecc71"
GREY = "#bdc3c7"
BLACK = "#222222"
WHITE = "#fdfdfd"
CARROT = "#e67e22"

st.markdown(f"""
    <style>
        .reportview-container {{
            background-color: {WHITE};
            color: {BLACK};
        }}
        .stApp {{
            padding: 2rem;
        }}
        .stButton>button {{
            background-color: {PRIMARY_GREEN};
            color: white;
            border-radius: 8px;
            font-weight: bold;
            padding: 0.5rem 1.5rem;
        }}
        .stRadio > div {{
            background-color: {WHITE};
            padding: 10px;
            border-radius: 10px;
        }}
    </style>
""", unsafe_allow_html=True)

# ---- Leadership Styles ----
leadership_styles = {
    "Reassign workload and offer time to recharge (The Stabilizer)": {
        "style": "The Stabilizer",
        "description": "You lead with empathy, consistency, and a calm presence.",
        "traits": ["Patient", "Steady", "Systematic", "Good Listener", "Caring"],
        "strengths": "Creates psychological safety, ensures cohesion, builds long-term trust.",
        "development": "Speak up more assertively and embrace calculated risks.",
        "points": 20
    },
    "Push through and focus on demo outcomes (The Driver)": {
        "style": "The Driver",
        "description": "You lead with urgency, clarity, and a results-first mindset.",
        "traits": ["Competitive", "Results-Oriented", "Strong-Willed", "Risk-Taker", "Direct"],
        "strengths": "Pushes for results, tackles tough challenges, leads from the front.",
        "development": "Balance your directness with emotional awareness and collaborative input.",
        "points": 15
    },
    "Engage team to support and share load (The Motivator)": {
        "style": "The Motivator",
        "description": "You spark momentum and rally teams with passion and optimism.",
        "traits": ["Expressive", "Inspiring", "Trusting", "Talkative", "Sociable"],
        "strengths": "Energizes collaboration and drives shared vision.",
        "development": "Stay grounded in details and execution.",
        "points": 18
    },
    "Analyze priorities and rescope demo (The Strategist)": {
        "style": "The Strategist",
        "description": "You lead with logic, structure, and deliberate thinking.",
        "traits": ["Analytical", "Diplomatic", "Precise", "Questioning", "Conventional"],
        "strengths": "Excels at systems thinking and risk management.",
        "development": "Act with more agility when uncertainty is high.",
        "points": 12
    }
}

# ---- Educational Scenarios ----
educational_content = {
    "intro": {
        "title": "🧭 Welcome to Leadership Journey AI",
        "content": "I'm your AI leadership coach, here to guide you through real workplace scenarios. Think of this as a simulation to explore how your instincts play out. You'll earn points based on your choices, and we'll reveal your natural leadership profile. Ready to begin your journey? 🚀"
    },
    "scenarios": [
        {
            "ai_intro": "🧠 **Transformational Leadership in Action**\n\nSatya Nadella revitalized Microsoft’s culture through empathy and learning.",
            "context": "You're leading a startup team. Your senior engineer, Sarah, says she’s burned out a week before your investor demo.",
            "ai_question": "What do you do next?",
            "learning_point": "Crisis moments test your empathy, judgment, and ability to prioritize human needs alongside delivery."
        },
        {
            "ai_intro": "🔍 **Delegation and Trust**\n\nHoward Schultz at Starbucks empowered his team to own operations and decisions.",
            "context": "You're preparing for a product launch, but you're pulled into constant micro-decisions that others could own.",
            "ai_question": "How do you handle this?",
            "learning_point": "Great leaders know when to let go and enable autonomy without losing alignment."
        },
        {
            "ai_intro": "💬 **Feedback Culture**\n\nEd Catmull of Pixar fostered a safe space for creative criticism.",
            "context": "A team member shares an idea that misses the mark during a brainstorming session. Others stay silent.",
            "ai_question": "How do you respond?",
            "learning_point": "Your response to vulnerability can either build or break innovation culture."
        }
    ]
}

# ---- Streamlit App Logic ----
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
    st.session_state.scores = defaultdict(int)
    st.session_state.finished = False
    st.session_state.submitted = False
    st.session_state.selected_option = None

if st.session_state.current_index == 0:
    st.markdown(f"<h1 style='text-align: center;'>{educational_content['intro']['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{educational_content['intro']['content']}</p>", unsafe_allow_html=True)
    if st.button("Begin »"):
        st.session_state.current_index = 1
else:
    index = st.session_state.current_index - 1
    if index < len(educational_content["scenarios"]):
        scenario = educational_content["scenarios"][index]

        st.markdown(f"<h3 style='text-align: center;'>{scenario['ai_intro']}</h3>", unsafe_allow_html=True)
        st.markdown(f"**Context:** {scenario['context']}")
        st.markdown(f"**Challenge:** {scenario['ai_question']}")

        choice = st.radio("Choose your course of action:", list(leadership_styles.keys()), index=0)

        if not st.session_state.submitted:
            if st.button("Submit Choice"):
                selected = leadership_styles[choice]
                st.session_state.scores[selected["style"]] += selected["points"]
                st.session_state.selected_option = selected
                st.session_state.submitted = True

        if st.session_state.submitted and st.session_state.selected_option:
            style = st.session_state.selected_option
            st.markdown(f"<div style='background-color:{PRIMARY_GREEN}; padding:10px; border-radius:8px;'>✅ You chose: <strong>{style['style']}</strong><br/>{style['description']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='background-color:{GREY}; padding:10px; border-radius:8px;'>🧠 <em>Learning Point:</em> {scenario['learning_point']}</div>", unsafe_allow_html=True)

            if st.button("Next Scenario »"):
                st.session_state.current_index += 1
                st.session_state.submitted = False
                st.session_state.selected_option = None

    else:
        st.session_state.finished = True

if st.session_state.finished:
    st.header("🎯 Your Leadership Style Summary")
    totals = dict(st.session_state.scores)
    sorted_styles = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    top_style = sorted_styles[0][0] if sorted_styles else "Unknown"

    summary = leadership_styles[next(k for k, v in leadership_styles.items() if v["style"] == top_style)]

    st.subheader(f"🏆 Dominant Style: {summary['style']}")
    st.markdown(f"**Traits:** {', '.join(summary['traits'])}")
    st.markdown(f"**Strengths:** {summary['strengths']}")
    st.markdown(f"**Development Tip:** {summary['development']}")
    st.balloons()
    st.stop()
