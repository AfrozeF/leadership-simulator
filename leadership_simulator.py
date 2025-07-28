import streamlit as st
from collections import defaultdict
import time

st.set_page_config(page_title="Leadership Journey AI", layout="wide", initial_sidebar_state="expanded")

# ---- Forest Theme Color Palette ----
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            --forest-dark: #1a2e1a;
            --forest-medium: #2d4a2d;
            --forest-light: #4a7c59;
            --forest-accent: #7fb069;
            --forest-yellow: #d4a574;
            --forest-blue: #6b9dc2;
            --forest-red: #c85a5a;
            --forest-bg: #f8fdf8;
            --forest-white: #ffffff;
            --forest-gray: #6b7280;
        }
        
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 900px;
        }
        
        .stApp {
            background: linear-gradient(135deg, var(--forest-bg) 0%, #e8f5e8 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, var(--forest-dark) 0%, var(--forest-medium) 100%);
        }
        
        /* Chat Interface */
        .chat-container {
            background: var(--forest-white);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(26, 46, 26, 0.1);
            border: 1px solid rgba(127, 176, 105, 0.2);
        }
        
        .ai-message {
            background: linear-gradient(135deg, var(--forest-light) 0%, var(--forest-accent) 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 18px 18px 18px 4px;
            margin: 1rem 0;
            position: relative;
            font-size: 1.05rem;
            line-height: 1.6;
        }
        
        .ai-message::before {
            content: "🧭 Journey Coach";
            position: absolute;
            top: -8px;
            left: 1rem;
            background: var(--forest-dark);
            color: var(--forest-accent);
            padding: 0.3rem 0.8rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
        }
        
        .user-choice {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            color: var(--forest-dark);
            padding: 1rem 1.5rem;
            border-radius: 4px 18px 18px 18px;
            margin: 1rem 0;
            border-left: 4px solid var(--forest-blue);
            font-weight: 500;
        }
        
        .option-bubble {
            background: var(--forest-white);
            border: 2px solid rgba(127, 176, 105, 0.3);
            border-radius: 16px;
            padding: 1.2rem;
            margin: 0.8rem 0;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .option-bubble:hover {
            border-color: var(--forest-accent);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(127, 176, 105, 0.2);
        }
        
        .option-bubble::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 4px;
            transition: all 0.3s ease;
        }
        
        .red-option::before { background: var(--forest-red); }
        .blue-option::before { background: var(--forest-blue); }
        .yellow-option::before { background: var(--forest-yellow); }
        .green-option::before { background: var(--forest-accent); }
        
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--forest-gray);
            font-style: italic;
            margin: 1rem 0;
        }
        
        .typing-dots {
            display: flex;
            gap: 4px;
        }
        
        .typing-dots span {
            width: 6px;
            height: 6px;
            background: var(--forest-accent);
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }
        
        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
            30% { transform: translateY(-10px); opacity: 1; }
        }
        
        /* Progress Components */
        .progress-card {
            background: var(--forest-white);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 16px rgba(26, 46, 26, 0.1);
            border: 1px solid rgba(127, 176, 105, 0.2);
        }
        
        .points-display {
            background: linear-gradient(135deg, var(--forest-accent) 0%, var(--forest-light) 100%);
            color: white;
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            margin: 1rem 0;
            font-weight: 600;
            font-size: 1.1rem;
        }
        
        .scenario-pill {
            display: inline-block;
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            margin: 0.2rem;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .scenario-completed {
            background: var(--forest-accent);
            color: white;
        }
        
        .scenario-current {
            background: var(--forest-yellow);
            color: var(--forest-dark);
        }
        
        .scenario-pending {
            background: rgba(127, 176, 105, 0.2);
            color: var(--forest-gray);
        }
        
        .energy-bar {
            height: 8px;
            border-radius: 4px;
            margin: 0.5rem 0;
            overflow: hidden;
            background: rgba(127, 176, 105, 0.2);
        }
        
        .energy-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.8s ease;
        }
        
        .red-fill { background: linear-gradient(90deg, var(--forest-red), #e57373); }
        .blue-fill { background: linear-gradient(90deg, var(--forest-blue), #90caf9); }
        .yellow-fill { background: linear-gradient(90deg, var(--forest-yellow), #ffb74d); }
        .green-fill { background: linear-gradient(90deg, var(--forest-accent), #81c784); }
        
        /* Buttons */
        .chat-button {
            background: linear-gradient(135deg, var(--forest-accent) 0%, var(--forest-light) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.8rem 1.5rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(127, 176, 105, 0.3);
            font-family: inherit;
        }
        
        .chat-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(127, 176, 105, 0.4);
        }
        
        .welcome-header {
            background: linear-gradient(135deg, var(--forest-dark) 0%, var(--forest-medium) 100%);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .welcome-header::before {
            content: '🧭🚀🌟';
            position: absolute;
            top: 1rem;
            right: 2rem;
            font-size: 1.5rem;
            opacity: 0.3;
        }
        
        /* Sidebar specific */
        .sidebar-content {
            color: white;
            padding: 1rem;
        }
        
        .sidebar-title {
            color: var(--forest-accent);
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Enhanced Leadership Data with Points System ----
leadership_styles = {
    "Red Energy": {
        "traits": ["Competitive", "Results-Oriented", "Strong-Willed", "Risk-Taker", "Direct"],
        "description": "You lead with intensity and drive, focusing on results and pushing boundaries",
        "strengths": "Drives performance, makes tough decisions, creates urgency, delivers results",
        "development": "Balance directness with empathy, involve others in decision-making",
        "points": 15
    },
    "Blue Energy": {
        "traits": ["Analytical", "Diplomatic", "Precise", "Questioning", "Conventional"],
        "description": "You lead through careful analysis and systematic approaches",
        "strengths": "Makes data-driven decisions, ensures quality, manages risk effectively",
        "development": "Speed up decision-making, embrace creative solutions, trust intuition",
        "points": 12
    },
    "Yellow Energy": {
        "traits": ["Expressive", "Inspiring", "Trusting", "Talkative", "Sociable"],
        "description": "You lead by energizing others and building enthusiasm around shared goals",
        "strengths": "Motivates teams, builds relationships, drives innovation, creates positive culture",
        "development": "Focus on follow-through, pay attention to details, balance optimism with realism",
        "points": 18
    },
    "Green Energy": {
        "traits": ["Patient", "Steady", "Systematic", "Good Listener", "Caring"],
        "description": "You lead through stability and genuine care for your team members",
        "strengths": "Builds trust, ensures team cohesion, provides consistent support, maintains stability",
        "development": "Embrace change more readily, make decisions faster, assert when necessary",
        "points": 20
    }
}

educational_content = {
    "intro": {
        "title": "🧭 Welcome to Leadership Journey AI",
        "content": "I'm your AI leadership coach, here to guide you through real workplace scenarios. Think of this as a conversation where we'll explore how different leadership energies work in practice. You'll earn points based on your choices, and I'll help you understand your natural leadership style. Ready to begin your leadership journey? 🚀"
    },
    "scenarios": [
        {
            "ai_intro": "Let me paint you a scenario that many leaders face. Pay attention to the dynamics at play here...",
            "context": "You're leading a product team at a growing startup. Your senior engineer, Sarah, just informed you she's burned out and considering stepping back. She's crucial to next week's investor demo.",
            "ai_question": "This is a critical moment that will test your leadership instincts. How do you respond to Sarah?",
            "learning_point": "**Crisis Leadership**: When team members are struggling, different leadership energies respond differently. Red energy takes charge, Blue analyzes the situation, Yellow focuses on morale, and Green provides support."
        },
        {
            "ai_intro": "Remote leadership brings unique challenges. Let's see how you handle this delicate situation...",
            "context": "You're managing a remote marketing team. Your weekly check-ins have become quiet and unproductive, with team morale noticeably declining.",
            "ai_question": "Virtual team dynamics require intentional leadership. What's your approach to re-energize your remote team?",
            "learning_point": "**Remote Team Dynamics**: Leading distributed teams requires intentional connection. Some leaders excel at virtual relationship-building, others at structure and process, still others at motivation and energy."
        },
        {
            "ai_intro": "Uncertainty tests every leader. Your response here will reveal how you handle pressure and support your team...",
            "context": "You're leading a finance team during company-wide budget cuts. One of your top performers, Michael, is worried about job security and his productivity is suffering.",
            "ai_question": "During times of change, people need different types of support. How do you help Michael navigate this uncertainty?",
            "learning_point": "**Change Management**: During organizational uncertainty, team members need different types of support. Understanding how to provide both security and direction is crucial for maintaining performance."
        },
        {
            "ai_intro": "Conflict is inevitable in high-performing teams. The key is how you choose to address it...",
            "context": "At your fast-paced design agency, deadlines are tight and tensions high. You've overheard two team leads arguing publicly in a shared Slack channel.",
            "ai_question": "Public conflicts can damage team dynamics quickly. What's your strategy for addressing this situation?",
            "learning_point": "**Conflict Resolution**: When tensions arise, leaders can choose multiple approaches - from direct intervention to collaborative problem-solving. The key is matching your response to the situation."
        },
        {
            "ai_intro": "Global leadership requires cultural intelligence. This scenario will test your ability to bridge differences...",
            "context": "You're overseeing an international project. A European manager complains that the American team is being too direct and aggressive in their communication style.",
            "ai_question": "Cultural misunderstandings can derail projects. How do you navigate these different communication styles?",
            "learning_point": "**Cross-Cultural Leadership**: Global teams bring diverse communication styles and expectations. Effective leaders bridge these differences while maintaining team cohesion and productivity."
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
    st.session_state.total_points = 0
    st.session_state.scenario_points = []
    st.session_state.show_feedback = False
    st.session_state.last_choice = None
    st.session_state.completed = False
    st.session_state.show_typing = False

# ---- Sidebar Progress Panel ----
def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown('<h2 class="sidebar-title">🧭 Leadership Path</h2>', unsafe_allow_html=True)
        
        if st.session_state.app_started:
            # Points Display
            st.markdown(f"""
            <div class="points-display">
                ⭐ Journey Points<br>
                <span style="font-size: 1.8rem;">{st.session_state.total_points}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Scenario Progress
            st.markdown("**Journey Steps**")
            for i in range(5):
                if i < len(st.session_state.responses):
                    points = st.session_state.scenario_points[i] if i < len(st.session_state.scenario_points) else 0
                    st.markdown(f'<div class="scenario-pill scenario-completed">Step {i+1} ✓ (+{points}pts)</div>', unsafe_allow_html=True)
                elif i == st.session_state.current_scenario:
                    st.markdown(f'<div class="scenario-pill scenario-current">Step {i+1} 🔄</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="scenario-pill scenario-pending">Step {i+1}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Energy Distribution
            if st.session_state.responses:
                st.markdown("**Leadership Energy**")
                style_counts = {style: st.session_state.responses.count(style) for style in leadership_styles.keys()}
                total_responses = len(st.session_state.responses)
                
                colors = ['red', 'blue', 'yellow', 'green']
                for i, (style, count) in enumerate(style_counts.items()):
                    percentage = int((count / total_responses) * 100) if total_responses > 0 else 0
                    color = colors[i]
                    
                    st.markdown(f"""
                    <div style="margin: 0.8rem 0;">
                        <div style="font-size: 0.9rem; margin-bottom: 0.3rem; color: white;">
                            {style.replace(' Energy', '')} ({count})
                        </div>
                        <div class="energy-bar">
                            <div class="{color}-fill energy-fill" style="width: {max(percentage, 5)}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---- Typing Effect Function ----
def show_typing_effect():
    return st.markdown("""
    <div class="typing-indicator">
        Forest AI is thinking
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---- Navigation Functions ----
def restart_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ---- Welcome Screen ----
if not st.session_state.app_started:
    render_sidebar()
    
    st.markdown(f"""
    <div class="welcome-header">
        <h1>🧭 Leadership Journey AI</h1>
        <p style="font-size: 1.2rem; opacity: 0.9; margin: 0;">
            Your Personal AI Leadership Coach
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="chat-container">
        <div class="ai-message">
            {educational_content['intro']['content']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    name = st.text_input("", placeholder="What's your name? Let's begin your leadership journey! 🚀", key="name_input")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Begin Leadership Journey", key="start_btn", use_container_width=True):
            if name.strip():
                st.session_state.user_name = name.strip()
                st.session_state.app_started = True
                st.rerun()
            else:
                st.error("Please enter your name to continue")

# ---- Main Chat Interface ----
elif st.session_state.current_scenario < len(scenarios):
    render_sidebar()
    
    scenario_data = educational_content['scenarios'][st.session_state.current_scenario]
    scenario_options = scenarios[st.session_state.current_scenario]
    
    # Chat Header
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown(f"### 🧭 Leadership Journey AI - Scenario {st.session_state.current_scenario + 1}")
    with col2:
        if st.button("🔄 Restart", key="restart"):
            restart_app()
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Previous conversation if any
    if st.session_state.current_scenario > 0:
        st.markdown(f'<div class="user-choice">Previous choice: {st.session_state.responses[-1]}</div>', unsafe_allow_html=True)
    
    # AI Introduction
    greeting = f"Hi {st.session_state.user_name}! " if st.session_state.current_scenario == 0 else ""
    st.markdown(f"""
    <div class="ai-message">
        {greeting}{scenario_data['ai_intro']}
        
        <br><br><strong>The Scenario:</strong><br>
        <em>{scenario_data['context']}</em>
        
        <br><br>{scenario_data['ai_question']}
    </div>
    """, unsafe_allow_html=True)
    
    # Options
    colors = ['red', 'blue', 'yellow', 'green']
    for i, (style, response) in enumerate(scenario_options['options'].items()):
        color = colors[i]
        
        st.markdown(f"""
        <div class="option-bubble {color}-option">
            <strong>{style}</strong><br>
            {response}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Choose {style}", key=f"{style}_{i}", use_container_width=True):
            # Add points and response
            points_earned = leadership_styles[style]['points']
            st.session_state.last_choice = style
            st.session_state.responses.append(style)
            st.session_state.total_points += points_earned
            st.session_state.scenario_points.append(points_earned)
            st.session_state.show_feedback = True
            st.rerun()

    # Feedback
    if st.session_state.show_feedback and st.session_state.last_choice:
        chosen_style = st.session_state.last_choice
        style_info = leadership_styles[chosen_style]
        points_earned = st.session_state.scenario_points[-1]
        
        st.markdown(f'<div class="user-choice">You chose: {chosen_style}</div>', unsafe_allow_html=True)
        
        # Typing effect
        with st.empty():
            show_typing_effect()
            time.sleep(2)
            
            st.markdown(f"""
            <div class="ai-message">
                Excellent choice! You earned <strong>{points_earned} points</strong> ⭐
                
                <br><br><strong>Your {chosen_style} Approach:</strong><br>
                {style_info['description']}
                
                <br><br><strong>Key Strengths:</strong> {style_info['strengths']}<br>
                <strong>Growth Area:</strong> {style_info['development']}
                
                <br><br><em>{scenario_data['learning_point']}</em>
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            if st.button("🚀 Continue Journey", key="next", use_container_width=True):
                st.session_state.current_scenario += 1
                st.session_state.show_feedback = False
                st.session_state.last_choice = None
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Results Screen ----
else:
    render_sidebar()
    
    # Calculate results
    style_counts = {style: st.session_state.responses.count(style) for style in leadership_styles.keys()}
    total = len(st.session_state.responses)
    dominant_style = max(style_counts, key=style_counts.get)
    
    st.markdown("### 🧭 Your Leadership Journey Complete!")
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="ai-message">
        Congratulations {st.session_state.user_name}! 🎉
        
        You've completed your leadership journey and earned <strong>{st.session_state.total_points} total points</strong>!
        
        <br><br><strong>Your Dominant Leadership Energy: {dominant_style}</strong><br>
        {leadership_styles[dominant_style]['description']}
        
        <br><br>Remember: The most effective leaders can access all four energies depending on what the situation demands. Your leadership journey has just begun! 🚀
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed breakdown
    st.markdown("### 📊 Your Leadership Energy Profile")
    
    colors = ['red', 'blue', 'yellow', 'green']
    for i, (style, count) in enumerate(style_counts.items()):
        percentage = int((count / total) * 100) if total > 0 else 0
        color = colors[i]
        
        st.markdown(f"""
        <div class="progress-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong>{style}</strong>
                <span>{percentage}% ({count} scenarios)</span>
            </div>
            <div class="energy-bar">
                <div class="{color}-fill energy-fill" style="width: {max(percentage, 5)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Start New Journey", key="restart_final", use_container_width=True):
            restart_app()
    
    st.markdown('</div>', unsafe_allow_html=True)
