import streamlit as st

# --- App Config ---
st.set_page_config(page_title="Leadership Simulator", layout="centered")

# --- App Style ---
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
        }
        .title {
            font-size: 2.2em;
            font-weight: bold;
            color: #1F4E79;
            margin-bottom: 0.2em;
        }
        .subtitle {
            font-size: 1.2em;
            color: #555;
        }
        .scenario-card {
            background-color: #F3F6FA;
            padding: 20px;
            border-left: 6px solid #1F4E79;
            border-radius: 10px;
            margin-top: 25px;
        }
        .feedback-box {
            background-color: #E8F0FE;
            padding: 16px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 4px solid #1F4E79;
        }
        .feedback-title {
            font-weight: bold;
            color: #1F4E79;
            margin-bottom: 10px;
        }
        button[kind="primary"] {
            background-color: #1F4E79 !important;
        }
        button[kind="primary"]:hover {
            background-color: #3A6EA5 !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Leadership Styles & Feedback ---
leadership_styles = ["Visionary", "Coaching", "Affiliative", "Democratic", "Commanding"]
feedback_texts = {
    "Visionary": "You’re motivated by a bigger picture and inspire others toward a common goal. This is great for innovation and growth.",
    "Coaching": "You prioritize individual growth, helping team members develop their strengths — ideal for building long-term capability.",
    "Affiliative": "You foster harmony and emotional bonds, which is great for morale but needs balancing with structure.",
    "Democratic": "You value collaboration and group input, often leading to shared commitment and higher satisfaction.",
    "Commanding": "You take quick control in crises and urgent situations. Be mindful of overuse — it can reduce morale."
}

# --- Scenarios ---
scenarios = [
    {
        "id": 1,
        "text": "You're leading a product team at a growing startup. It's Monday morning, and your senior engineer, Sarah, just informed you she’s burned out and considering stepping back. She’s crucial to next week’s product demo with investors.",
        "options": {
            "Visionary": "Inspire Sarah by reminding her of the bigger mission and her impact.",
            "Coaching": "Offer Sarah a one-on-one session to understand her burnout and support her growth.",
            "Affiliative": "Encourage Sarah to take a break and assure her the team will support her.",
            "Democratic": "Call a team meeting to discuss redistributing her tasks collaboratively.",
            "Commanding": "Assign her tasks regardless, emphasizing the importance of delivery."
        }
    },
    {
        "id": 2,
        "text": "Your client presentation is tomorrow. The team is divided on the final strategy. Some are pushing for a bold move, while others prefer a conservative plan.",
        "options": {
            "Visionary": "Articulate a long-term vision and persuade the team to align with it.",
            "Coaching": "Talk individually with team members to understand their reasoning and guide growth.",
            "Affiliative": "Ease tensions and remind the team that harmony is key.",
            "Democratic": "Facilitate a vote or group discussion to finalize the plan.",
            "Commanding": "Make the final decision yourself and direct the team accordingly."
        }
    },
    {
        "id": 3,
        "text": "You're the new team lead in a remote-first company. Productivity is down, and the team feels disconnected.",
        "options": {
            "Visionary": "Paint a compelling picture of how improved communication boosts the team’s goals.",
            "Coaching": "Pair teammates for weekly mentorship sessions to rebuild morale.",
            "Affiliative": "Organize virtual social events to strengthen bonds.",
            "Democratic": "Ask the team what’s missing and how they'd like to improve.",
            "Commanding": "Set mandatory check-ins and tighten deadlines to enforce structure."
        }
    },
    {
        "id": 4,
        "text": "Your junior designer, Alex, keeps missing deadlines. Their work is good, but you’re under pressure to deliver.",
        "options": {
            "Visionary": "Share how their work connects to the company’s success to motivate them.",
            "Coaching": "Help Alex identify what’s blocking their efficiency and offer guidance.",
            "Affiliative": "Reassure Alex you value their contribution and ask how to help.",
            "Democratic": "Ask the team if they’ve faced similar issues and discuss possible solutions.",
            "Commanding": "Issue a clear deadline and consequences if it’s missed again."
        }
    },
    {
        "id": 5,
        "text": "You’ve just joined a large corporation known for its rigid hierarchy. Your manager expects compliance, but you see opportunities for innovation.",
        "options": {
            "Visionary": "Propose a long-term transformation plan to modernize workflows.",
            "Coaching": "Quietly mentor colleagues who are open to new ways of working.",
            "Affiliative": "Build internal relationships and earn trust before initiating change.",
            "Democratic": "Survey the team to gauge appetite for change and build consensus.",
            "Commanding": "Challenge the status quo directly and push for immediate changes."
        }
    }
]

# --- Session State Setup ---
if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = 0
    st.session_state.responses = []
    st.session_state.show_feedback = False
    st.session_state.chosen_style = ""

# --- Intro Section ---
if st.session_state.current_scenario == 0 and not st.session_state.show_feedback and not st.session_state.responses:
    st.markdown("<div class='title'>Leadership Scenario Simulator</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Sharpen your leadership style through real-world challenges. Make decisions, get feedback, and understand your leadership approach.</div>", unsafe_allow_html=True)
    st.write("You'll go through 5 realistic scenarios. For each one, pick the response that best matches what you'd do. At the end, you'll see your leadership profile.")

# --- Scenario Display ---
if st.session_state.current_scenario < len(scenarios):
    scenario = scenarios[st.session_state.current_scenario]

    st.markdown(f"<div class='scenario-card'><strong>Scenario {scenario['id']}:</strong> {scenario['text']}</div>", unsafe_allow_html=True)

    if not st.session_state.show_feedback:
        st.write("**Choose your response:**")
        for style, response in scenario["options"].items():
            if st.button(response):
                st.session_state.responses.append(style)
                st.session_state.chosen_style = style
                st.session_state.show_feedback = True
                st.rerun()

    else:
        chosen_style = st.session_state.chosen_style
        feedback_msg = feedback_texts[chosen_style]

        st.markdown(f"""
            <div class='feedback-box'>
                <div class='feedback-title'>Your Response Reflects: {chosen_style} Leadership</div>
                <div>{feedback_msg}</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Next Scenario"):
            st.session_state.current_scenario += 1
            st.session_state.show_feedback = False
            st.rerun()

# --- Results Summary ---
if st.session_state.current_scenario >= len(scenarios):
    st.header("🔍 Your Leadership Style Summary")
    counts = {style: st.session_state.responses.count(style) for style in leadership_styles}

    for style, count in counts.items():
        st.markdown(f"**{style}**: {count} scenario(s)")

    st.success("You’ve completed all scenarios! Use these results to reflect on your natural tendencies — and areas to grow as a leader.")
