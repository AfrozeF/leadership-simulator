import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Leadership Simulator", layout="wide")

# ---- COLORS AND STYLES ----
primary_color = "#2C3E50"  # dark navy
accent_color = "#3498DB"   # cobalt blue
text_color = "#ECECEC"     # light grey
bg_color = "#1C1C1C"

st.markdown(f"""
    <style>
        .reportview-container {{ background-color: {bg_color}; color: {text_color}; }}
        .sidebar .sidebar-content {{ background-color: {bg_color}; }}
        .css-1d391kg {{ color: {text_color}; }}
        .css-1v0mbdj p, .css-1v0mbdj h1, .css-1v0mbdj h2 {{ color: {text_color}; }}
        .stButton > button {{ background-color: {accent_color}; color: white; border: none; padding: 0.6em 1.2em; }}
    </style>
""", unsafe_allow_html=True)

# ---- APP STATE ----
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'score' not in st.session_state:
    st.session_state.score = {"Empathy": 0, "Decisiveness": 0, "Communication": 0}
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = 0

# ---- DATA ----
scenarios = [
    {
        "title": "Handling a Difficult Team Member",
        "background": "You’re leading a project in a remote-first company. One team member, Sam, frequently misses deadlines but contributes creative ideas.",
        "question": "What would you do?",
        "options": {
            "Have a private conversation to explore the root cause and offer support.": {"Empathy": 2, "Communication": 1},
            "Reassign tasks quietly to avoid delays and minimize conflict.": {"Decisiveness": 1},
            "Call it out in a team meeting to set a clear standard.": {"Communication": 2, "Decisiveness": 1}
        }
    },
    {
        "title": "Responding to Last-Minute Changes",
        "background": "You’re 15 minutes away from presenting to stakeholders. A new report shows your team’s data may be inaccurate.",
        "question": "What’s your move?",
        "options": {
            "Proceed with the presentation but disclose limitations transparently.": {"Communication": 2},
            "Delay the meeting briefly to re-verify the numbers.": {"Decisiveness": 1, "Empathy": 1},
            "Ignore the report for now — it’s too late to change anything.": {"Decisiveness": 2}
        }
    },
    {
        "title": "Dealing with Burnout",
        "background": "Two team members confide in you that they’re overwhelmed and considering leaving.",
        "question": "How do you respond?",
        "options": {
            "Create a safe space to listen, then revisit workloads collaboratively.": {"Empathy": 2, "Communication": 1},
            "Encourage them to use vacation days and talk to HR.": {"Empathy": 1},
            "Remind them of project timelines and your team’s commitment.": {"Decisiveness": 1}
        }
    }
]

# ---- FUNCTIONS ----
def show_welcome():
    st.title("Leadership Simulator")
    st.subheader("Sharpen your decision-making, empathy, and communication skills")
    st.markdown("Leadership today demands more than authority. This simulator puts you in the hot seat with real-world scenarios.")
    if st.button("Start Assessment"):
        st.session_state.page = 'instructions'


def show_instructions():
    st.header("🧭 How It Works")
    st.markdown("You'll navigate a series of leadership dilemmas, each based on real team challenges. Your choices will shape your leadership profile across key competencies:")
    st.markdown("- **Empathy** – How well do you understand and support others?")
    st.markdown("- **Communication** – Are you transparent, timely, and thoughtful?")
    st.markdown("- **Decisiveness** – Can you act quickly with clarity?")
    if st.button("Begin Scenario 1"):
        st.session_state.page = 'scenario'


def show_scenario():
    index = st.session_state.current_scenario
    scenario = scenarios[index]

    st.subheader(f"Scenario {index + 1}: {scenario['title']}")
    st.markdown(f"**Context**: {scenario['background']}")
    st.markdown(f"**Challenge**: {scenario['question']}")

    for option_text, trait_scores in scenario['options'].items():
        if st.button(option_text):
            for trait, value in trait_scores.items():
                st.session_state.score[trait] += value
            st.session_state.page = 'feedback'
            break


def show_feedback():
    index = st.session_state.current_scenario
    scenario = scenarios[index]
    st.success("Response submitted!")

    st.markdown("### Why this matters:")
    st.markdown("Good leadership isn’t about always being right — it’s about understanding how your actions ripple through your team.")

    st.markdown("**Leadership Competency Boosts** from your choice:")
    chart_data = st.session_state.score
    st.write(chart_data)

    if index + 1 < len(scenarios):
        if st.button("Next Scenario"):
            st.session_state.current_scenario += 1
            st.session_state.page = 'scenario'
    else:
        if st.button("View My Leadership Profile"):
            st.session_state.page = 'results'


def show_results():
    st.header("🧠 Your Leadership Profile")
    labels = list(st.session_state.score.keys())
    values = list(st.session_state.score.values())

    fig, ax = plt.subplots()
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles), labels)
    ax.set_title("Leadership Competency Radar", size=16)
    ax.grid(True)

    st.pyplot(fig)

    st.markdown("### Next Steps")
    st.markdown("Continue building these skills with reflection, coaching, and real-world practice.")
    if st.button("Restart Assessment"):
        st.session_state.page = 'welcome'
        st.session_state.current_scenario = 0
        st.session_state.score = {"Empathy": 0, "Decisiveness": 0, "Communication": 0}


# ---- MAIN APP ----
if st.session_state.page == 'welcome':
    show_welcome()
elif st.session_state.page == 'instructions':
    show_instructions()
elif st.session_state.page == 'scenario':
    show_scenario()
elif st.session_state.page == 'feedback':
    show_feedback()
elif st.session_state.page == 'results':
    show_results()
