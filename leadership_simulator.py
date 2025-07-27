import streamlit as st

# --- Page configuration ---
st.set_page_config(
    page_title="Leadership Skills Simulator",
    page_icon="🤖",
    layout="wide"
)

# --- Initialize session state ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'completed_scenarios' not in st.session_state:
    st.session_state.completed_scenarios = set()
if 'user_choices' not in st.session_state:
    st.session_state.user_choices = {}
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# --- Scenario data ---
scenarios = {
    "1": {
        "title": "Meeting Deadlines Challenge",
        "description": "Your team hasn't been meeting deadlines lately.",
        "question": "What do you do?",
        "options": {
            "A": "Set strict rules and deadlines going forward.",
            "B": "Meet with the team to explore what's causing the delays.",
            "C": "Let it go — they'll probably fix it themselves."
        },
        "feedback": {
            "a": ("🔎 You're taking control, but beware: strictness without dialogue may cause pushback.", 1),
            "b": ("✅ Great leadership! You're listening, diagnosing the issue, and building trust.", 3),
            "c": ("⚠️ Ignoring problems can harm trust and accountability over time.", 0)
        },
        "tag": "Accountability"
    },
    "2": {
        "title": "Team Conflict Resolution",
        "description": "Two team members are constantly disagreeing during meetings.",
        "question": "What do you do?",
        "options": {
            "A": "Ask them to settle it privately.",
            "B": "Facilitate a group discussion to resolve the conflict openly.",
            "C": "Ignore it — it's probably just personality clashes."
        },
        "feedback": {
            "a": ("⚠️ Conflict might continue if it's left to them without guidance.", 1),
            "b": ("✅ Great choice! You're creating space for dialogue and resolution.", 3),
            "c": ("🔎 Avoiding conflict can hurt team trust and collaboration.", 0)
        },
        "tag": "Trust Building"
    },
    "3": {
        "title": "Late Arrival Management",
        "description": "A team member keeps arriving late to meetings.",
        "question": "What do you do?",
        "options": {
            "A": "Call them out in front of the group.",
            "B": "Speak to them privately to understand what's going on.",
            "C": "Say nothing and hope it stops."
        },
        "feedback": {
            "a": ("⚠️ Public shaming can damage trust — best avoided.", 1),
            "b": ("✅ Well done! One-on-one check-ins build trust and accountability.", 3),
            "c": ("🔎 Inaction may lead to worse behavior or resentment.", 0)
        },
        "tag": "Delegation"
    },
    "4": {
        "title": "Leading Former Peers",
        "description": "You've been promoted to lead your former peers.",
        "question": "What do you do?",
        "options": {
            "A": "Distance yourself from them immediately.",
            "B": "Acknowledge the change and invite open conversation.",
            "C": "Act like nothing has changed."
        },
        "feedback": {
            "a": ("⚠️ Cutting ties quickly can alienate your team.", 1),
            "b": ("✅ Excellent! Transparency and openness builds trust in new roles.", 3),
            "c": ("🔎 Denial of change can lead to confusion or blurred authority.", 0)
        },
        "tag": "Conflict Resolution"
    },
    "5": {
        "title": "Managing Discussion Dominance",
        "description": "You notice one person dominating all team discussions.",
        "question": "What do you do?",
        "options": {
            "A": "Let them speak — they're confident and smart.",
            "B": "Set guidelines to ensure equal participation.",
            "C": "Talk to quieter members privately."
        },
        "feedback": {
            "a": ("⚠️ Dominance can silence diverse perspectives.", 1),
            "b": ("✅ Great job! Structure encourages inclusion and fairness.", 3),
            "c": ("🔎 Good move — follow it up with visible changes in meetings.", 2)
        },
        "tag": "Communication"
    }
}

# --- Utility functions ---
def reset_simulation():
    st.session_state.score = 0
    st.session_state.completed_scenarios = set()
    st.session_state.user_choices = {}
    st.session_state.current_scenario = None
    st.session_state.show_results = False

def analyze_leadership_style():
    b_count = sum(1 for c in st.session_state.user_choices.values() if c == "b")
    a_count = sum(1 for c in st.session_state.user_choices.values() if c == "a")
    c_count = sum(1 for c in st.session_state.user_choices.values() if c == "c")
    if b_count >= 4:
        return "💡 You're a **Coaching-style leader** — reflective, empathetic, and collaborative."
    elif a_count >= 3:
        return "🚀 You're an **Action-oriented leader** — decisive and direct."
    elif c_count >= 3:
        return "🧩 You lean toward **Avoidant leadership** — consider engaging more directly."
    else:
        return "📊 You have a **flexible style**. You adapt your approach based on the situation."

# --- Header banner ---
st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 style='color: #3E8EDE;'>🤖 Leadership Skills Simulator</h1>
        <p style='color: #555;'>An interactive learning experience to explore your leadership strengths.</p>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("📊 Progress Tracker")
    if st.session_state.user_name:
        st.write(f"👋 Welcome, **{st.session_state.user_name}**!")
    progress = len(st.session_state.completed_scenarios) / len(scenarios)
    st.progress(progress)
    st.write(f"Completed: {len(st.session_state.completed_scenarios)}/{len(scenarios)} scenarios")
    st.write(f"Current Score: {st.session_state.score}/15")
    st.divider()
    if st.button("🔄 Reset Simulation", type="secondary"):
        reset_simulation()
        st.rerun()

# --- Main Interface ---
if not st.session_state.user_name:
    st.header("Welcome! Let's Get Started")
    name = st.text_input("What's your name?", placeholder="Enter your name here...")
    if st.button("Start Simulation", disabled=not name):
        st.session_state.user_name = name
        st.rerun()
elif not st.session_state.show_results:
    remaining_scenarios = [num for num in scenarios if num not in st.session_state.completed_scenarios]
    if remaining_scenarios:
        st.subheader("📋 Available Scenarios")
        scenario_label = st.selectbox(
            "Choose a scenario to begin:",
            options=[f"{num} - {scenarios[num]['title']} ({scenarios[num]['tag']})" for num in remaining_scenarios]
        )
        selected_num = scenario_label.split(" - ")[0]
        if st.button("▶️ Start Scenario"):
            st.session_state.current_scenario = selected_num
            st.rerun()

    if st.session_state.current_scenario:
        num = st.session_state.current_scenario
        scenario = scenarios[num]
        st.divider()
        st.subheader(f"🎯 Scenario {num}: {scenario['title']}")
        st.write(f"**Situation:** {scenario['description']}")
        st.write(f"**{scenario['question']}**")
        choice = st.radio(
            "Select your response:",
            options=list(scenario['options'].keys()),
            format_func=lambda x: f"{x}) {scenario['options'][x]}",
            key=f"choice_{num}"
        )
        if st.button("Submit Response", type="primary"):
            feedback_text, points = scenario['feedback'][choice.lower()]
            st.session_state.user_choices[num] = choice.lower()
            st.session_state.score += points
            st.session_state.completed_scenarios.add(num)
            st.session_state.current_scenario = None
            st.success(feedback_text)
            st.info(f"Points earned: {points}")
            if len(st.session_state.completed_scenarios) == len(scenarios):
                st.session_state.show_results = True
            st.rerun()
else:
    st.header(f"🎉 Congratulations, {st.session_state.user_name}!")
    st.subheader("You've completed all scenarios!")
    st.metric("Final Score", f"{st.session_state.score}/15")
    st.metric("Success Rate", f"{round((st.session_state.score / 15) * 100)}%")
    st.metric("Scenarios Completed", f"{len(st.session_state.completed_scenarios)}/5")
    st.subheader("📈 Leadership Assessment")
    score = st.session_state.score
    if score >= 13:
        st.success("🏆 You're a collaborative and emotionally intelligent leader!")
    elif score >= 9:
        st.info("👏 Solid leadership! You balance authority with empathy.")
    elif score >= 5:
        st.warning("⚠️ You're on the right track, but consider listening more.")
    else:
        st.error("🚧 Consider practicing active communication and reflection.")

    st.subheader("🧠 Your Leadership Style")
    st.write(analyze_leadership_style())

    st.subheader("📊 Scenario Breakdown")
    for num in sorted(st.session_state.user_choices.keys()):
        s = scenarios[num]
        choice = st.session_state.user_choices[num].upper()
        feedback_text, points = s['feedback'][choice.lower()]
        with st.expander(f"Scenario {num}: {s['title']} - {points}/3 points"):
            st.write(f"**Your choice:** {choice}) {s['options'][choice]}")
            st.write(f"**Feedback:** {feedback_text}")

    report = f"Leadership Skills Summary for {st.session_state.user_name}\n\nFinal Score: {st.session_state.score}/15\nLeadership Style: {analyze_leadership_style()}\n\n"
    for num in sorted(st.session_state.user_choices.keys()):
        s = scenarios[num]
        choice = st.session_state.user_choices[num].upper()
        feedback_text, points = s['feedback'][choice.lower()]
        report += f"Scenario {num}: {s['title']} ({points}/3)\nChoice: {choice}) {s['options'][choice]}\nFeedback: {feedback_text}\n\n"
    st.download_button("📄 Download Summary", report, file_name="leadership_summary.txt")

    if st.button("🔄 Try Again with Different Choices", type="primary"):
        reset_simulation()
        st.rerun()

# --- Footer ---
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    <p>Leadership Skills Simulator | Designed for Leadership & Development Portfolio</p>
</div>
""", unsafe_allow_html=True)
