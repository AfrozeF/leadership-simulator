import streamlit as st
import random

st.set_page_config(page_title="Leadership Simulator", layout="centered")

# ---------- Styling ----------
custom_css = """
<style>
    body {
        background-color: #f4f6f8;
    }

    .main {
        font-family: 'Segoe UI', sans-serif;
        color: #1c1e21;
    }

    .stButton>button {
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        transition: 0.3s ease-in-out;
    }

    .stButton>button:hover {
        background-color: #145a86;
        color: white;
    }

    .scenario-box {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .feedback-box {
        background-color: #e8f0fe;
        border-left: 6px solid #1f77b4;
        padding: 16px;
        margin-top: 20px;
        border-radius: 8px;
    }

    .quadrant-box {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 24px;
    }

    .quad {
        padding: 16px;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        min-height: 100px;
    }

    .red { background-color: #d62728; }
    .blue { background-color: #1f77b4; }
    .green { background-color: #2ca02c; }
    .yellow { background-color: #ff7f0e; }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ---------- Leadership Color Insights ----------
st.markdown("## 🧭 Discover Your Leadership Style")
st.markdown("Understanding your leadership style can help you adapt your approach to lead more effectively in different situations.")

st.markdown("### The 4 Colors of Leadership Energy")

with st.container():
    st.markdown("""
<div class="quadrant-box">
    <div class="quad red">
        <strong>Red Energy</strong><br>
        Competitive<br>
        Results-Oriented<br>
        Direct
    </div>
    <div class="quad yellow">
        <strong>Yellow Energy</strong><br>
        Expressive<br>
        Trusting<br>
        Sociable
    </div>
    <div class="quad green">
        <strong>Green Energy</strong><br>
        Patient<br>
        Systematic<br>
        Caring
    </div>
    <div class="quad blue">
        <strong>Blue Energy</strong><br>
        Analytical<br>
        Diplomatic<br>
        Precise
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- Scenario Data ----------
scenarios = [
    {
        "situation": "Your team missed a key deadline due to miscommunication.",
        "options": {
            "Take immediate responsibility and clarify next steps": {"Empathy": 2, "Communication": 1},
            "Hold a team meeting to investigate what went wrong": {"Analytical Thinking": 2, "Team Awareness": 1},
            "Privately speak with the person responsible": {"Decisiveness": 1, "Empathy": 1},
        }
    },
    {
        "situation": "A team member is consistently quiet in meetings.",
        "options": {
            "Assign them a visible role to encourage contribution": {"Empowerment": 2, "Trust": 1},
            "Have a private check-in to understand their hesitation": {"Empathy": 2, "Listening": 1},
            "Continue with the current format, assuming they'll speak up when ready": {"Patience": 2},
        }
    },
]

# ---------- App State ----------
if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = 0
if "score" not in st.session_state:
    st.session_state.score = {}

# ---------- Scenario Display ----------
scenario = scenarios[st.session_state.current_scenario]
st.markdown("## 💼 Scenario")
st.markdown(f"<div class='scenario-box'><strong>{scenario['situation']}</strong></div>", unsafe_allow_html=True)

user_choice = st.radio("What would you do?", list(scenario["options"].keys()))

if st.button("Submit Response"):
    boosts = scenario["options"][user_choice]
    for skill, value in boosts.items():
        st.session_state.score[skill] = st.session_state.score.get(skill, 0) + value

    st.markdown("### ✅ Why this matters:")
    st.markdown("Good leadership isn’t about always being right — it’s about understanding how your actions ripple through your team.")

    st.markdown("#### Leadership Competency Boosts from your choice:")
    st.markdown(f"<div class='feedback-box'>", unsafe_allow_html=True)
    for k, v in boosts.items():
        st.markdown(f"**{k}**: +{v}")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Next Scenario"):
        st.session_state.current_scenario = (st.session_state.current_scenario + 1) % len(scenarios)
        st.experimental_rerun()
