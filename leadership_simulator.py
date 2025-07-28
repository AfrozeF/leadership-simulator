import streamlit as st
import random

st.set_page_config(page_title="Leadership Simulator", layout="centered")

# --- Color and Style Settings ---
PRIMARY_COLOR = "#1B263B"   # Navy
SECONDARY_COLOR = "#415A77" # Slate Blue
ACCENT_COLOR = "#E0E1DD"    # Light Gray
HOVER_COLOR = "#D6D6D6"     # Softer hover color
FEEDBACK_BG = "#F1F1F1"     # Feedback box background

st.markdown("""
    <style>
        .stButton>button {
            background-color: """ + SECONDARY_COLOR + """;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1.5em;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: """ + HOVER_COLOR + """;
            color: black;
        }
        .scenario-box {
            background-color: #EDF2F7;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            border: 1px solid #ccc;
        }
        .feedback-box {
            background-color: """ + FEEDBACK_BG + """;
            padding: 18px;
            border-radius: 10px;
            border: 1px solid #ccc;
            margin-top: 15px;
            margin-bottom: 25px;
        }
        .feedback-title {
            font-weight: 700;
            font-size: 1.1em;
            margin-bottom: 8px;
            color: #1B263B;
        }
        .leadership-style {
            display: flex;
            align-items: center;
            margin: 5px 0;
        }
        .circle {
            height: 12px;
            width: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Intro Header ---
st.title("🧭 Leadership Simulator")

st.markdown("""
Welcome to the **Leadership Simulator** – an interactive learning tool to help you strengthen your decision-making, empathy, and leadership judgment in real-world scenarios.

You’ll face **5 realistic leadership challenges**. After each decision, you'll receive **insightful feedback** tied to a leadership style — and track how your choices align across different styles. Let’s get started!
""")

# --- Leadership Styles ---
leadership_styles = {
    "Visionary": "#0D47A1",
    "Democratic": "#00796B",
    "Coaching": "#F57C00",
    "Affiliative": "#6A1B9A",
    "Commanding": "#C62828"
}

# --- Scenarios (add more later) ---
scenarios = [
    {
        "context": "You're leading a product team at a growing startup. It's Monday morning, and your senior engineer, Sarah, just informed you she’s burned out and considering stepping back. She’s crucial to next week’s product demo with investors.",
        "options": {
            "Offer Sarah time off immediately and reorganize project priorities.": "Affiliative",
            "Have a one-on-one to coach her through stress and find longer-term solutions.": "Coaching",
            "Remind her of her responsibilities and the importance of next week’s demo.": "Commanding",
            "Ask the team for ideas on how to redistribute work and support Sarah.": "Democratic",
            "Motivate the team with a bold vision of how this demo could unlock funding.": "Visionary"
        }
    },
    {
        "context": "At a well-established marketing agency, you're promoted to lead a team that just lost two senior creatives. The team feels unstable, and project deadlines are fast approaching.",
        "options": {
            "Meet with everyone to brainstorm solutions and co-create next steps.": "Democratic",
            "Set clear roles and responsibilities and make decisions swiftly.": "Commanding",
            "Inspire the team with your long-term vision for revitalizing the department.": "Visionary",
            "Pull aside your team leads to mentor and build them up for leadership.": "Coaching",
            "Host a team retreat to rebuild morale and address burnout.": "Affiliative"
        }
    },
    # Add more scenarios here
]

# --- Session State ---
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = 0
    st.session_state.responses = []
    st.session_state.show_feedback = False

# --- Show Scenario ---
current = st.session_state.current_scenario

if current < len(scenarios):
    scenario = scenarios[current]

    st.markdown(f"<div class='scenario-box'><strong>Scenario {current + 1}:</strong> {scenario['context']}</div>", unsafe_allow_html=True)
    options = list(scenario["options"].keys())

    selected = st.radio("What would you do?", options)

    if st.button("Submit Response"):
        st.session_state.responses.append(scenario["options"][selected])
        st.session_state.show_feedback = True

    if st.session_state.show_feedback:
        chosen_style = scenario["options"][selected]
feedback_texts = {
    'Visionary': 'You motivate your team with purpose and long-term thinking.',
    'Democratic': 'You encourage participation and team-based decision-making.',
    'Coaching': 'You prioritize development and long-term growth.',
    'Affiliative': 'You care about emotional bonds and team morale.',
    'Commanding': 'You take direct control and demand immediate results.'
}

feedback_msg = feedback_texts[chosen_style]

st.markdown(f"""
<div class='feedback-box'>
    <div class='feedback-title'>Your Response Reflects: {chosen_style} Leadership</div>
    <div>{feedback_msg}</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.show_feedback and st.button("Next Scenario"):
        st.session_state.current_scenario += 1
        st.session_state.show_feedback = False
        st.rerun()

else:
    # --- Results Summary ---
    st.header("🔍 Your Leadership Style Summary")
    counts = {style: st.session_state.responses.count(style) for style in leadership_styles}

    for style, count in counts.items():
        st.markdown(f"""
            <div class='leadership-style'>
                <span class='circle' style='background-color:{leadership_styles[style]}'></span>
                <strong>{style}</strong>: {count} scenario(s)
            </div>
        """, unsafe_allow_html=True)

    st.success("You’ve completed all scenarios! Use these results to reflect on your natural tendencies — and areas to grow as a leader.")
