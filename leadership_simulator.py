import streamlit as st
from collections import defaultdict

st.set_page_config(page_title="Leadership Simulator", layout="wide")

# ---- Custom CSS ----
st.markdown("""
    <style>
        body {
            background-color: #f7f9fc;
        }
        .scenario-card {
            background-color: #e9eef6;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            font-size: 16px;
        }
        .feedback-box {
            background-color: #ffffff;
            border-left: 6px solid #4a90e2;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .feedback-title {
            font-weight: 600;
            font-size: 18px;
            margin-bottom: 10px;
        }
        .btn-style button {
            background-color: #4a90e2;
            color: white;
            border-radius: 8px;
            padding: 10px 18px;
            font-weight: 500;
            transition: all 0.2s ease-in-out;
        }
        .btn-style button:hover {
            background-color: #a0a0a0;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Leadership Styles ----
leadership_styles = ["Visionary", "Democratic", "Coaching", "Affiliative", "Commanding"]

# ---- Scenario Data ----
scenarios = [
    {
        "context": "You're leading a product team at a growing startup. It's Monday morning, and your senior engineer, Sarah, just informed you she’s burned out and considering stepping back. She’s crucial to next week’s product demo with investors.",
        "options": {
            "Visionary": "Inspire Sarah with the broader mission and how pivotal her role is in shaping the company's future.",
            "Coaching": "Set up a one-on-one to understand what's behind her burnout and how to support her growth.",
            "Affiliative": "Give Sarah some time off and reassign her tasks temporarily to show you care.",
            "Democratic": "Bring the issue to the team to brainstorm how to support Sarah and adjust workloads.",
            "Commanding": "Remind Sarah of her responsibilities and the importance of her delivering for the demo."
        }
    },
    {
        "context": "You’re managing a remote marketing team and notice that your weekly check-ins have become quiet and unproductive. Morale seems low.",
        "options": {
            "Visionary": "Reignite enthusiasm by reminding them of the team's larger goals.",
            "Coaching": "Schedule individual calls to understand what each person needs to re-engage.",
            "Affiliative": "Host a casual virtual coffee chat to rebuild emotional connections.",
            "Democratic": "Ask the team how they'd prefer check-ins to run and implement their ideas.",
            "Commanding": "Make participation mandatory and set expectations for each meeting."
        }
    },
    {
        "context": "You’re leading a finance team during budget cuts. One of your team members, Michael, is worried about job security.",
        "options": {
            "Visionary": "Reassure Michael by outlining how the team fits into the company’s strategic future.",
            "Coaching": "Work with Michael on upskilling so he feels more secure and prepared.",
            "Affiliative": "Acknowledge his concerns and create a supportive team environment.",
            "Democratic": "Open a discussion on how to collectively manage the cuts.",
            "Commanding": "Tell Michael to stay focused and not speculate."
        }
    },
    {
        "context": "At a fast-paced design agency, deadlines are tight and tensions high. You’ve overheard two team leads arguing in a shared channel.",
        "options": {
            "Visionary": "Remind both leads of the shared vision and refocus their energy.",
            "Coaching": "Privately coach each lead on better conflict resolution.",
            "Affiliative": "Organize a fun offsite activity to ease tension.",
            "Democratic": "Ask the team how conflicts should be resolved going forward.",
            "Commanding": "Call both leads into a meeting and establish ground rules."
        }
    },
    {
        "context": "You're overseeing an international project with cultural differences causing miscommunication. A European manager complains the American team is being too direct.",
        "options": {
            "Visionary": "Reiterate the unified purpose and need to work across cultures.",
            "Coaching": "Coach both parties on intercultural communication strategies.",
            "Affiliative": "Encourage a team-building call to foster empathy.",
            "Democratic": "Facilitate a group discussion on team norms and expectations.",
            "Commanding": "Set strict communication protocols to avoid misunderstandings."
        }
    }
]

# ---- Feedback Texts ----
feedback_texts = {
    "Visionary": "You tend to lead by inspiring others and rallying them around a shared purpose.",
    "Democratic": "You value team input and believe the best solutions come from collaboration.",
    "Coaching": "You support others by investing in their personal and professional growth.",
    "Affiliative": "You prioritize harmony and emotional connection in your leadership style.",
    "Commanding": "You take control and lead with clarity and decisiveness, especially in crisis."
}

# ---- Session State Setup ----
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = 0
    st.session_state.responses = []
    st.session_state.show_feedback = False
    st.session_state.last_choice = None

# ---- App Header ----
st.title("🧭 Leadership Simulator")
st.markdown("""
Welcome to the **Leadership Simulator** — a practical tool to explore how you lead in real-world workplace challenges.

You'll face **5 realistic scenarios** drawn from modern leadership challenges across industries. For each, you'll choose how to respond — and uncover which leadership style your decision reflects.

""")

# ---- Main Logic ----
if st.session_state.current_scenario < len(scenarios):
    scenario = scenarios[st.session_state.current_scenario]
    st.markdown(f"<div class='scenario-card'>{scenario['context']}</div>", unsafe_allow_html=True)

    st.write("**Choose your response:**")
    for style, response in scenario['options'].items():
        if st.button(response, key=style, use_container_width=True):
            st.session_state.last_choice = style
            st.session_state.responses.append(style)
            st.session_state.show_feedback = True

    if st.session_state.show_feedback and st.session_state.last_choice:
        chosen_style = st.session_state.last_choice
        feedback_msg = feedback_texts[chosen_style]

        st.markdown(f"""
        <div class='feedback-box'>
            <div class='feedback-title'>Your Response Reflects: {chosen_style} Leadership</div>
            <div>{feedback_msg}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Next Scenario", key="next"):
            st.session_state.current_scenario += 1
            st.session_state.show_feedback = False
            st.session_state.last_choice = None
            st.rerun()
else:
    # ---- Summary Results ----
    st.header("🔍 Your Leadership Style Summary")
    counts = {style: st.session_state.responses.count(style) for style in leadership_styles}
    total = len(st.session_state.responses)

    for style in leadership_styles:
        percent = int((counts[style] / total) * 100)
        st.write(f"**{style}**: {counts[style]} scenario(s) ({percent}%)")

    st.markdown("""
    ---
    ✅ **You’ve completed all scenarios!**  
    Use these results to reflect on your natural tendencies — and areas to grow as a leader.

    """)
