import streamlit as st
from collections import defaultdict

st.set_page_config(page_title="Leadership Simulator", layout="wide")

# ---- Enhanced Custom CSS ----
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .main > div {
            padding-top: 2rem;
        }
        
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Inter', sans-serif;
        }
        
        .main-container {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            min-height: 600px;
            position: relative;
        }
        
        .welcome-card {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
        }
        
        .progress-container {
            background: #f8fafc;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 2rem;
            border: 1px solid #e2e8f0;
        }
        
        .progress-bar {
            background: #e2e8f0;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            height: 100%;
            transition: width 0.3s ease;
        }
        
        .scenario-card {
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            border-left: 4px solid #6366f1;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        
        .scenario-title {
            color: #1e293b;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .scenario-text {
            color: #475569;
            font-size: 1rem;
            line-height: 1.6;
        }
        
        .option-button {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin: 0.5rem 0;
            width: 100%;
            text-align: left;
            transition: all 0.2s ease;
            cursor: pointer;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        .option-button:hover {
            border-color: #6366f1;
            background: #f8fafc;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
        }
        
        .feedback-card {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            margin: 2rem 0;
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
        }
        
        .feedback-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .feedback-description {
            font-size: 1rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        
        .insight-box {
            background: rgba(255,255,255,0.1);
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
        }
        
        .results-container {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 16px;
            margin: 2rem 0;
        }
        
        .style-bar {
            background: rgba(255,255,255,0.1);
            height: 30px;
            border-radius: 15px;
            margin: 0.5rem 0;
            position: relative;
            overflow: hidden;
        }
        
        .style-fill {
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            height: 100%;
            border-radius: 15px;
            display: flex;
            align-items: center;
            padding: 0 1rem;
            font-size: 0.85rem;
            font-weight: 500;
            transition: width 0.5s ease;
        }
        
        .nav-buttons {
            position: fixed;
            top: 50%;
            transform: translateY(-50%);
            z-index: 1000;
        }
        
        .nav-left {
            left: 1rem;
        }
        
        .nav-right {
            right: 1rem;
        }
        
        .nav-btn {
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 1.2rem;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            transition: all 0.2s ease;
        }
        
        .nav-btn:hover {
            background: #4f46e5;
            transform: scale(1.1);
        }
        
        .name-input {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem;
            font-size: 1.1rem;
            width: 100%;
            margin: 1rem 0;
            transition: border-color 0.2s ease;
        }
        
        .name-input:focus {
            border-color: #6366f1;
            outline: none;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        .start-btn {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 1rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }
        
        .start-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
        }
    </style>
""", unsafe_allow_html=True)

# ---- Enhanced Data ----
leadership_styles = {
    "Visionary": {
        "description": "You lead by inspiring others with a compelling vision of the future",
        "strengths": "Motivates teams, drives innovation, creates alignment around goals",
        "development": "Focus on tactical execution and supporting team members' individual needs"
    },
    "Democratic": {
        "description": "You value team input and believe the best solutions come from collaboration",
        "strengths": "Builds buy-in, leverages diverse perspectives, creates inclusive environment",
        "development": "Work on making faster decisions when time is critical"
    },
    "Coaching": {
        "description": "You support others by investing in their personal and professional growth",
        "strengths": "Develops talent, improves performance, builds long-term capabilities",
        "development": "Balance individual development with immediate business needs"
    },
    "Affiliative": {
        "description": "You prioritize harmony and emotional connection in your leadership approach",
        "strengths": "Builds trust, improves morale, creates psychological safety",
        "development": "Practice giving constructive feedback and addressing performance issues"
    },
    "Commanding": {
        "description": "You take control and lead with clarity and decisiveness",
        "strengths": "Provides clear direction, makes tough decisions, effective in crisis",
        "development": "Focus on building consensus and developing others' leadership skills"
    }
}

scenarios = [
    {
        "title": "The Burnout Crisis",
        "context": "You're leading a product team at a growing startup. It's Monday morning, and your senior engineer, Sarah, just informed you she's burned out and considering stepping back. She's crucial to next week's product demo with investors.",
        "options": {
            "Visionary": "Inspire Sarah with the broader mission and how pivotal her role is in shaping the company's future.",
            "Coaching": "Set up a one-on-one to understand what's behind her burnout and create a development plan.",
            "Affiliative": "Give Sarah some time off and reassign her tasks temporarily to show you care about her wellbeing.",
            "Democratic": "Bring the issue to the team to brainstorm how to support Sarah and adjust workloads collectively.",
            "Commanding": "Remind Sarah of her responsibilities and the critical importance of delivering for the demo."
        }
    },
    {
        "title": "Remote Team Disconnect",
        "context": "You're managing a remote marketing team and notice that your weekly check-ins have become quiet and unproductive. Team morale seems low and engagement is dropping.",
        "options": {
            "Visionary": "Reignite enthusiasm by reconnecting them with the team's larger goals and impact.",
            "Coaching": "Schedule individual calls to understand what each person needs to re-engage and grow.",
            "Affiliative": "Host a casual virtual coffee chat to rebuild emotional connections and team bonds.",
            "Democratic": "Ask the team how they'd prefer check-ins to run and implement their suggestions.",
            "Commanding": "Make participation mandatory and set clear expectations for each meeting."
        }
    },
    {
        "title": "Budget Cut Anxiety",
        "context": "You're leading a finance team during company-wide budget cuts. One of your top performers, Michael, is worried about job security and his productivity is suffering.",
        "options": {
            "Visionary": "Reassure Michael by outlining how the team fits into the company's strategic future.",
            "Coaching": "Work with Michael on upskilling so he feels more secure and prepared for challenges.",
            "Affiliative": "Acknowledge his concerns and create a more supportive, reassuring team environment.",
            "Democratic": "Open a team discussion on how to collectively manage the uncertainty of cuts.",
            "Commanding": "Tell Michael to stay focused on his work and not speculate about job security."
        }
    },
    {
        "title": "Creative Conflict",
        "context": "At your fast-paced design agency, deadlines are tight and tensions are running high. You've overheard two team leads arguing publicly in a shared Slack channel.",
        "options": {
            "Visionary": "Remind both leads of the shared vision and refocus their energy on common goals.",
            "Coaching": "Privately coach each lead on better conflict resolution and communication skills.",
            "Affiliative": "Organize a fun team activity to ease tension and rebuild positive relationships.",
            "Democratic": "Facilitate a team discussion on how conflicts should be resolved going forward.",
            "Commanding": "Call both leads into a meeting immediately and establish clear ground rules."
        }
    },
    {
        "title": "Cultural Miscommunication",
        "context": "You're overseeing an international project with team members from different cultures. A European manager complains that the American team is being too direct and aggressive in their communication style.",
        "options": {
            "Visionary": "Reiterate the unified purpose and emphasize the need to work across cultural differences.",
            "Coaching": "Coach both parties on intercultural communication strategies and awareness.",
            "Affiliative": "Encourage team-building activities to foster empathy and cultural understanding.",
            "Democratic": "Facilitate a group discussion on team communication norms and cultural expectations.",
            "Commanding": "Set strict communication protocols to avoid future cultural misunderstandings."
        }
    }
]

# ---- Session State Setup ----
if 'app_started' not in st.session_state:
    st.session_state.app_started = False
    st.session_state.user_name = ""
    st.session_state.current_scenario = 0
    st.session_state.responses = []
    st.session_state.show_feedback = False
    st.session_state.last_choice = None
    st.session_state.completed = False

# ---- Navigation Functions ----
def restart_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def exit_app():
    st.session_state.completed = True
    st.session_state.current_scenario = len(scenarios)

# ---- Welcome Screen ----
if not st.session_state.app_started:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="welcome-card">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">Leadership Simulator</h1>
        <p style="font-size: 1.2rem; margin: 1rem 0; opacity: 0.9;">
            Discover your leadership style through real-world scenarios
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h2 style="color: #1e293b; margin-bottom: 1rem;">Welcome to Your Leadership Journey</h2>
        <p style="color: #64748b; font-size: 1.1rem; line-height: 1.6; max-width: 600px; margin: 0 auto;">
            You'll navigate through 5 realistic workplace scenarios, each presenting different leadership challenges. 
            Your choices will reveal your natural leadership tendencies and provide insights for professional growth.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    name = st.text_input("", placeholder="Enter your name to begin", key="name_input", 
                        help="We'll personalize your experience")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Your Leadership Assessment", key="start_btn", use_container_width=True):
            if name.strip():
                st.session_state.user_name = name.strip()
                st.session_state.app_started = True
                st.rerun()
            else:
                st.error("Please enter your name to continue")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Main Application ----
elif st.session_state.current_scenario < len(scenarios):
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("← Start Over", key="restart", help="Restart the assessment"):
            restart_app()
    with col3:
        if st.button("Exit →", key="exit", help="Exit the assessment"):
            exit_app()
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Progress indicator
    progress = (st.session_state.current_scenario + 1) / len(scenarios)
    st.markdown(f"""
    <div class="progress-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-weight: 600; color: #475569;">Progress</span>
            <span style="color: #6b7280;">Scenario {st.session_state.current_scenario + 1} of {len(scenarios)}</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress * 100}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    scenario = scenarios[st.session_state.current_scenario]
    
    # Personalized greeting
    greeting = f"Hi {st.session_state.user_name}!" if st.session_state.current_scenario == 0 else ""
    
    st.markdown(f"""
    <div class="scenario-card">
        <div class="scenario-title">
            {greeting} {scenario['title']}
        </div>
        <div class="scenario-text">
            {scenario['context']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**{st.session_state.user_name}, how would you respond?**")
    
    # Option buttons
    for style, response in scenario['options'].items():
        if st.button(response, key=style, use_container_width=True):
            st.session_state.last_choice = style
            st.session_state.responses.append(style)
            st.session_state.show_feedback = True

    # Enhanced feedback
    if st.session_state.show_feedback and st.session_state.last_choice:
        chosen_style = st.session_state.last_choice
        style_info = leadership_styles[chosen_style]
        
        st.markdown(f"""
        <div class="feedback-card">
            <div class="feedback-title">Your Response: {chosen_style} Leadership</div>
            <div class="feedback-description">{style_info['description']}.</div>
            <div class="insight-box">
                <strong>Key Strengths:</strong> {style_info['strengths']}<br>
                <strong>Growth Area:</strong> {style_info['development']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            if st.button("Continue to Next Scenario", key="next", use_container_width=True):
                st.session_state.current_scenario += 1
                st.session_state.show_feedback = False
                st.session_state.last_choice = None
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Results Screen ----
else:
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("← Start Over", key="restart_final"):
            restart_app()
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Calculate results
    counts = {style: st.session_state.responses.count(style) for style in leadership_styles.keys()}
    total = len(st.session_state.responses)
    dominant_style = max(counts, key=counts.get)
    
    st.markdown(f"""
    <div class="results-container">
        <h1 style="text-align: center; margin-bottom: 2rem; font-size: 2.2rem;">
            {st.session_state.user_name}'s Leadership Profile
        </h1>
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #a78bfa; margin-bottom: 0.5rem;">Primary Style: {dominant_style}</h2>
            <p style="font-size: 1.1rem; opacity: 0.9;">
                {leadership_styles[dominant_style]['description']}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Your Complete Leadership Style Breakdown")
    
    for style in leadership_styles.keys():
        percentage = int((counts[style] / total) * 100)
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <strong>{style}</strong>
                <span>{percentage}% ({counts[style]} scenarios)</span>
            </div>
            <div class="style-bar">
                <div class="style-fill" style="width: {percentage}%;">
                    {percentage}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed insights
    st.markdown("### Personalized Development Insights")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **Your Strengths ({dominant_style} Leadership):**
        - {leadership_styles[dominant_style]['strengths']}
        """)
    
    with col2:
        st.markdown(f"""
        **Development Opportunity:**
        - {leadership_styles[dominant_style]['development']}
        """)
    
    # Least used style insight
    least_used = min(counts, key=counts.get)
    if counts[least_used] == 0:
        st.info(f"**Expansion Opportunity:** You didn't select any {least_used} responses. Consider exploring when this style might be most effective: {leadership_styles[least_used]['description'].lower()}.")
    
    st.markdown(f"""
    ---
    **Congratulations, {st.session_state.user_name}!** You've completed the Leadership Simulator. 
    Use these insights to reflect on your natural leadership tendencies and identify areas for continued growth.
    
    *Remember: The most effective leaders adapt their style to the situation and the people they're leading.*
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
