import streamlit as st
from collections import defaultdict

st.set_page_config(page_title="Leadership Insights Simulator", layout="wide")

# ---- Enhanced Custom CSS with proper color palette ----
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            font-family: 'Inter', sans-serif;
        }
        
        .hero-section {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(37, 99, 235, 0.2);
        }
        
        .hero-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        
        .info-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 4px solid #2563eb;
        }
        
        .red-energy { border-left-color: #dc2626; }
        .yellow-energy { border-left-color: #f59e0b; }
        .green-energy { border-left-color: #059669; }
        .blue-energy { border-left-color: #2563eb; }
        
        .progress-container {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .progress-bar {
            background: #e5e7eb;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            background: linear-gradient(90deg, #2563eb, #1d4ed8);
            height: 100%;
            transition: width 0.3s ease;
        }
        
        .scenario-container {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        }
        
        .scenario-info {
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border-left: 4px solid #f59e0b;
        }
        
        .scenario-context {
            background: #fafafa;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            border: 1px solid #e5e7eb;
            font-style: italic;
        }
        
        .option-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin: 2rem 0;
        }
        
        .option-card {
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s ease;
            cursor: pointer;
            text-align: left;
            min-height: 120px;
            display: flex;
            align-items: center;
        }
        
        .option-card:hover {
            border-color: #2563eb;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.15);
        }
        
        .red-option { border-left: 4px solid #dc2626; }
        .yellow-option { border-left: 4px solid #f59e0b; }
        .green-option { border-left: 4px solid #059669; }
        .blue-option { border-left: 4px solid #2563eb; }
        
        .feedback-card {
            background: linear-gradient(135deg, #059669 0%, #047857 100%);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            margin: 2rem 0;
            box-shadow: 0 10px 25px rgba(5, 150, 105, 0.3);
        }
        
        .insight-box {
            background: rgba(255,255,255,0.1);
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 1rem;
        }
        
        .results-container {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 16px;
            margin: 2rem 0;
        }
        
        .color-bar {
            height: 40px;
            border-radius: 20px;
            margin: 1rem 0;
            display: flex;
            align-items: center;
            padding: 0 1.5rem;
            font-weight: 600;
            transition: all 0.5s ease;
        }
        
        .red-bar { background: linear-gradient(90deg, #dc2626, #b91c1c); }
        .yellow-bar { background: linear-gradient(90deg, #f59e0b, #d97706); }
        .green-bar { background: linear-gradient(90deg, #059669, #047857); }
        .blue-bar { background: linear-gradient(90deg, #2563eb, #1d4ed8); }
        
        .nav-button {
            background: #6b7280;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .nav-button:hover {
            background: #4b5563;
        }
        
        .primary-button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 1rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        }
        
        .primary-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
        }
        
        .name-input {
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 1rem;
            font-size: 1.1rem;
            width: 100%;
            margin: 1rem 0;
            transition: border-color 0.2s ease;
        }
        
        .name-input:focus {
            border-color: #2563eb;
            outline: none;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ---- Leadership Data with 4-color system ----
leadership_styles = {
    "Red Energy": {
        "traits": ["Competitive", "Results-Oriented", "Strong-Willed", "Risk-Taker", "Direct"],
        "description": "You lead with intensity and drive, focusing on results and pushing boundaries",
        "strengths": "Drives performance, makes tough decisions, creates urgency, delivers results",
        "development": "Balance directness with empathy, involve others in decision-making"
    },
    "Blue Energy": {
        "traits": ["Analytical", "Diplomatic", "Precise", "Questioning", "Conventional"],
        "description": "You lead through careful analysis and systematic approaches",
        "strengths": "Makes data-driven decisions, ensures quality, manages risk effectively",
        "development": "Speed up decision-making, embrace creative solutions, trust intuition"
    },
    "Yellow Energy": {
        "traits": ["Expressive", "Inspiring", "Trusting", "Talkative", "Sociable"],
        "description": "You lead by energizing others and building enthusiasm around shared goals",
        "strengths": "Motivates teams, builds relationships, drives innovation, creates positive culture",
        "development": "Focus on follow-through, pay attention to details, balance optimism with realism"
    },
    "Green Energy": {
        "traits": ["Patient", "Steady", "Systematic", "Good Listener", "Caring"],
        "description": "You lead through stability and genuine care for your team members",
        "strengths": "Builds trust, ensures team cohesion, provides consistent support, maintains stability",
        "development": "Embrace change more readily, make decisions faster, assert when necessary"
    }
}

educational_content = {
    "intro": {
        "title": "Understanding Leadership Energy",
        "content": """Leadership isn't one-size-fits-all. Research shows that effective leaders adapt their approach based on the situation and the people they're leading. 

The 4 Colors of Leadership Energy model helps identify your natural tendencies:
• **Red Energy** - Direct, results-focused leadership
• **Blue Energy** - Analytical, process-oriented leadership  
• **Yellow Energy** - Inspirational, people-focused leadership
• **Green Energy** - Supportive, relationship-focused leadership

Understanding your dominant style helps you leverage your strengths while developing flexibility in other approaches."""
    },
    "scenarios": [
        {
            "learning_point": "**Crisis Leadership**: When team members are struggling, different leadership energies respond differently. Red energy takes charge, Blue analyzes the situation, Yellow focuses on morale, and Green provides support.",
            "context": "You're leading a product team at a growing startup. Your senior engineer, Sarah, just informed you she's burned out and considering stepping back. She's crucial to next week's investor demo."
        },
        {
            "learning_point": "**Remote Team Dynamics**: Leading distributed teams requires intentional connection. Some leaders excel at virtual relationship-building, others at structure and process, still others at motivation and energy.",
            "context": "You're managing a remote marketing team. Your weekly check-ins have become quiet and unproductive, with team morale noticeably declining."
        },
        {
            "learning_point": "**Change Management**: During organizational uncertainty, team members need different types of support. Understanding how to provide both security and direction is crucial for maintaining performance.",
            "context": "You're leading a finance team during company-wide budget cuts. One of your top performers, Michael, is worried about job security and his productivity is suffering."
        },
        {
            "learning_point": "**Conflict Resolution**: When tensions arise, leaders can choose multiple approaches - from direct intervention to collaborative problem-solving. The key is matching your response to the situation.",
            "context": "At your fast-paced design agency, deadlines are tight and tensions high. You've overheard two team leads arguing publicly in a shared Slack channel."
        },
        {
            "learning_point": "**Cross-Cultural Leadership**: Global teams bring diverse communication styles and expectations. Effective leaders bridge these differences while maintaining team cohesion and productivity.",
            "context": "You're overseeing an international project. A European manager complains that the American team is being too direct and aggressive in their communication style."
        }
    ]
}

scenarios = [
    {
        "options": {
            "Red Energy": "Address the situation directly - remind Sarah of her critical role and the importance of delivering for the demo.",
            "Blue Energy": "Analyze the root causes of her burnout and create a structured plan to address them systematically.",
            "Yellow Energy": "Inspire Sarah by connecting her work to the bigger vision and the exciting future ahead.",
            "Green Energy": "Focus on Sarah's wellbeing - offer support, time off, and reassurance about her value to the team."
        }
    },
    {
        "options": {
            "Red Energy": "Set clear expectations for participation and establish mandatory engagement in team meetings.",
            "Blue Energy": "Survey the team to understand the specific issues and develop a data-driven improvement plan.",
            "Yellow Energy": "Inject energy and enthusiasm - host engaging activities to rebuild team spirit and motivation.",
            "Green Energy": "Create safe spaces for connection through casual virtual coffee chats and one-on-one check-ins."
        }
    },
    {
        "options": {
            "Red Energy": "Be direct about the business reality while emphasizing Michael's value and his secure position.",
            "Blue Energy": "Provide Michael with detailed information about the cuts and help him develop new skills for security.",
            "Yellow Energy": "Reassure Michael by painting a positive picture of the team's future and his role in it.",
            "Green Energy": "Listen to Michael's concerns and create a supportive environment where he feels heard and valued."
        }
    },
    {
        "options": {
            "Red Energy": "Immediately call both leads into a private meeting and establish clear ground rules for professional communication.",
            "Blue Energy": "Investigate the root cause of the conflict and implement systematic processes to prevent future issues.",
            "Yellow Energy": "Refocus both leads on the shared vision and organize team activities to rebuild positive relationships.",
            "Green Energy": "Mediate between the leads to understand both perspectives and help them find common ground."
        }
    },
    {
        "options": {
            "Red Energy": "Set clear, non-negotiable communication protocols that everyone must follow regardless of cultural background.",
            "Blue Energy": "Research cultural communication differences and implement structured guidelines for cross-cultural interaction.",
            "Yellow Energy": "Organize team-building activities that celebrate cultural diversity and create enthusiasm for collaboration.",
            "Green Energy": "Facilitate open dialogue where team members can share their communication preferences and find mutual understanding."
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
    # Hero Section
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">4 Colors of Leadership Insights</h1>
        <p class="hero-subtitle">
            Discover your natural leadership energy and learn to adapt your style for maximum impact
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction Content
    st.markdown(f"""
    <div class="info-card blue-energy">
        <h2>{educational_content['intro']['title']}</h2>
        <p style="line-height: 1.8; color: #374151;">{educational_content['intro']['content']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Benefits Section
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-card red-energy">
            <h3>Why This Matters</h3>
            <ul style="line-height: 1.6; color: #374151;">
                <li>Understand your natural leadership strengths</li>
                <li>Learn when to adapt your approach</li>
                <li>Improve team dynamics and performance</li>
                <li>Build more effective relationships</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card yellow-energy">
            <h3>What You'll Experience</h3>
            <ul style="line-height: 1.6; color: #374151;">
                <li>5 realistic workplace scenarios</li>
                <li>Insights into your leadership energy</li>
                <li>Personalized development recommendations</li>
                <li>Practical application strategies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Name Input
    st.markdown("<br>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="Enter your name to begin your leadership journey", 
                        key="name_input", help="We'll personalize your learning experience")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Leadership Assessment", key="start_btn", use_container_width=True):
            if name.strip():
                st.session_state.user_name = name.strip()
                st.session_state.app_started = True
                st.rerun()
            else:
                st.error("Please enter your name to continue")

# ---- Main Application ----
elif st.session_state.current_scenario < len(scenarios):
    # Navigation
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("← Restart", key="restart", help="Start over"):
            restart_app()
    with col3:
        if st.button("Exit →", key="exit", help="Exit assessment"):
            exit_app()
    
    # Progress
    progress = (st.session_state.current_scenario + 1) / len(scenarios)
    st.markdown(f"""
    <div class="progress-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-weight: 600; color: #374151;">Progress</span>
            <span style="color: #6b7280;">Scenario {st.session_state.current_scenario + 1} of {len(scenarios)}</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress * 100}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    scenario_data = educational_content['scenarios'][st.session_state.current_scenario]
    scenario_options = scenarios[st.session_state.current_scenario]
    
    # Greeting only for first scenario
    greeting = f"Welcome, {st.session_state.user_name}! " if st.session_state.current_scenario == 0 else ""
    
    # Learning Point
    st.markdown(f"""
    <div class="scenario-info">
        <h3>Leadership Insight</h3>
        <p style="margin: 0; line-height: 1.6;">{greeting}{scenario_data['learning_point']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Scenario Context
    st.markdown(f"""
    <div class="scenario-container">
        <h3>Scenario {st.session_state.current_scenario + 1}</h3>
        <div class="scenario-context">
            {scenario_data['context']}
        </div>
        <p><strong>How would you respond in this situation?</strong></p>
    """, unsafe_allow_html=True)
    
    # Options in 2x2 grid
    col1, col2 = st.columns(2)
    styles = list(scenario_options['options'].keys())
    colors = ['red', 'blue', 'yellow', 'green']
    
    for i, (style, response) in enumerate(scenario_options['options'].items()):
        color = colors[i]
        col = col1 if i < 2 else col2
        
        with col:
            if st.button(response, key=f"{style}_{i}", use_container_width=True, 
                        help=f"{style} approach"):
                st.session_state.last_choice = style
                st.session_state.responses.append(style)
                st.session_state.show_feedback = True

    # Feedback
    if st.session_state.show_feedback and st.session_state.last_choice:
        chosen_style = st.session_state.last_choice
        style_info = leadership_styles[chosen_style]
        
        st.markdown(f"""
        <div class="feedback-card">
            <h3>Your Choice: {chosen_style}</h3>
            <p style="font-size: 1.1rem; margin-bottom: 1rem;">{style_info['description']}</p>
            <div class="insight-box">
                <strong>Core Traits:</strong> {', '.join(style_info['traits'])}<br><br>
                <strong>Key Strengths:</strong> {style_info['strengths']}<br><br>
                <strong>Development Focus:</strong> {style_info['development']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            if st.button("Continue", key="next", use_container_width=True):
                st.session_state.current_scenario += 1
                st.session_state.show_feedback = False
                st.session_state.last_choice = None
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Results Screen ----
else:
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("← Start Over", key="restart_final"):
            restart_app()
    
    # Calculate results
    style_counts = {style: st.session_state.responses.count(style) for style in leadership_styles.keys()}
    total = len(st.session_state.responses)
    dominant_style = max(style_counts, key=style_counts.get)
    
    st.markdown(f"""
    <div class="results-container">
        <h1 style="text-align: center; margin-bottom: 2rem;">
            {st.session_state.user_name}'s Leadership Energy Profile
        </h1>
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #fbbf24;">Primary Energy: {dominant_style}</h2>
            <p style="font-size: 1.1rem; opacity: 0.9; line-height: 1.6;">
                {leadership_styles[dominant_style]['description']}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Your Leadership Energy Distribution")
    
    colors = ['red', 'blue', 'yellow', 'green']
    for i, (style, count) in enumerate(style_counts.items()):
        percentage = int((count / total) * 100) if total > 0 else 0
        color = colors[i]
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <strong>{style}</strong>
                <span>{percentage}% ({count} scenarios)</span>
            </div>
            <div class="{color}-bar" style="width: {max(percentage, 5)}%;">
                {percentage}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Development Insights
    st.markdown("### Your Development Focus")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="info-card green-energy">
            <h4>Leverage Your Strengths</h4>
            <p>{leadership_styles[dominant_style]['strengths']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-card yellow-energy">
            <h4>Growth Opportunity</h4>
            <p>{leadership_styles[dominant_style]['development']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Final insights
    least_used = min(style_counts, key=style_counts.get)
    if style_counts[least_used] == 0:
        st.markdown(f"""
        <div class="info-card blue-energy">
            <h4>Expand Your Range</h4>
            <p>You didn't select any <strong>{least_used}</strong> responses. Consider exploring when this energy might be most effective: {leadership_styles[least_used]['description'].lower()}.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    ---
    **Congratulations, {st.session_state.user_name}!** 
    
    Remember: The most effective leaders can access all four energies depending on what the situation demands. Use this assessment as a starting point for developing your leadership flexibility and impact.
    """)
