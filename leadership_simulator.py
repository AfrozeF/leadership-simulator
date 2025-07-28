import streamlit as st
import random

st.set_page_config(page_title="Leadership Simulator", layout="centered")

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f8f9fa;
    }

    .stButton>button {
        background-color: #1e3a5f;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6em 1.4em;
        border: none;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #162c47;
    }

    .scenario-box {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }

    .feedback-box {
        background-color: #edf2f7;
        border-left: 4px solid #1e3a5f;
        padding: 16px;
        border-radius: 8px;
        margin-top: 20px;
    }

    .style-card {
        border: 1px solid #d3d3d3;
        padding: 12px;
        border-radius: 10px;
        background-color: #ffffff;
        margin-bottom: 10px;
    }

    .intro-box {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- App Intro ----------
st.markdown("## Leadership Simulation Experience")
st.markdown("""
<div class="intro-box">
    <p>Welcome to the <strong>Leadership Simulator</strong> – an immersive experience designed to help you test, explore, and improve your leadership decision-making in real-world situations.</p>
    <p>You’ll be presented with <strong>5 realistic leadership scenarios</strong> drawn from corporate, startup, and team-based settings. Each choice you make will develop certain leadership competencies.</p>
    <p>There are no right or wrong answers — only insights to grow from. You’ll receive meaningful feedback after every decision.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Leadership Styles (Collapsible) ----------
with st.expander("See the Four Leadership Energy Styles"):
    st.markdown("""
    <div class="style-card"><strong>🔹 Blue Energy</strong> – Analytical, structured, data-driven</div>
    <div class="style-card"><strong>🟢 Green Energy</strong> – Caring, empathetic, harmony-seeking</div>
    <div class="style-card"><strong>🟠 Yellow Energy</strong> – Expressive, creative, sociable</div>
    <div class="style-card"><strong>🔴 Red Energy</strong> – Bold, competitive, outcome-focused</div>
    """, unsafe_allow_html=True)

# ---------- Scenario Definitions ----------
scenarios = [
    {
        "situation": "You're leading a product team at a growing fintech startup. It's Monday morning, and your senior engineer, Priya, just informed you she’s burned out and considering stepping back. She’s crucial to next week’s product demo with investors.",
        "options": {
            "Reassign her responsibilities temporarily and schedule a 1:1 to discuss her well-being": {"Empathy": 2, "Trust Building": 1},
            "Encourage her to push through the demo and take leave after": {"Execution Focus": 2, "Short-term Gains": 1},
            "Immediately call a team huddle and redistribute her tasks": {"Agility": 2, "Team Awareness": 1},
        }
    },
    {
        "situation": "At Orion Consulting, you’ve just taken over as team lead. One team member, Marcus, regularly challenges your direction in meetings, which is disrupting group momentum.",
        "options": {
            "Privately meet Marcus to understand his point of view": {"Listening": 2, "Conflict Navigation": 1},
            "Establish stronger meeting protocols and assert control": {"Authority": 2, "Decisiveness": 1},
            "Invite Marcus to co-lead the next project phase": {"Empowerment": 2, "Influence": 1},
        }
    },
    {
        "situation": "Your marketing team is planning a campaign for a major retail client. You’re behind schedule, and two departments are blaming each other.",
        "options": {
            "Call a joint workshop to collaboratively address bottlenecks": {"Collaboration": 2, "Facilitation": 1},
            "Assign clear deadlines and hold each lead accountable": {"Ownership": 2, "Structure": 1},
            "Delay the campaign and reallocate resources next sprint": {"Risk Mitigation": 2, "Prioritization": 1},
        }
    },
    {
        "situation": "In a hybrid work setup, your team in Singapore feels disconnected from HQ in New York. Engagement is dropping.",
        "options": {
            "Create cross-office buddy systems and monthly check-ins": {"Culture Building": 2, "Inclusion": 1},
            "Survey them anonymously before making any changes": {"Listening": 2, "Diagnosis": 1},
            "Request managers to report on team morale weekly": {"Accountability": 2, "Monitoring": 1},
        }
    },
    {
        "situation": "During a client pitch, your colleague contradicts you publicly. The client looks visibly confused.",
        "options": {
            "Smooth over the contradiction and clarify the direction calmly": {"Composure": 2, "Client Handling": 1},
            "Confront your colleague afterward and establish boundaries": {"Assertiveness": 2, "Team Alignment": 1},
            "Ignore it for now and follow up later with the client privately": {"Diplomacy": 2, "Damage Control": 1},
        }
    },
]

# ---------- State Management ----------
if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = 0
if "score" not in st.session_state:
    st.session_state.score = {}

# ---------- Display Current Scenario ----------
current = st.session_state.current_scenario
scenario = scenarios[current]

st.markdown(f"### Scenario {current + 1} of {len(scenarios)}")
st.markdown(f"<div class='scenario-box'><strong>{scenario['situation']}</strong></div>", unsafe_allow_html=True)

user_choice = st.radio("What would you do?", list(scenario["options"].keys()))

if st.button("Submit Response"):
    boosts = scenario["options"][user_choice]
    for skill, value in boosts.items():
        st.session_state.score[skill] = st.session_state.score.get(skill, 0) + value

    st.markdown("#### Feedback from your choice:")
    st.markdown("<div class='feedback-box'>", unsafe_allow_html=True)
    for skill, pts in boosts.items():
        st.markdown(f"- **{skill}**: +{pts}")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.current_scenario < len(scenarios) - 1:
        if st.button("Next Scenario"):
            st.session_state.current_scenario += 1
            st.experimental_rerun()
    else:
        st.markdown("### ✅ You’ve completed all scenarios!")
        st.markdown("Thanks for participating in the Leadership Simulator.")
