import streamlit as st
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random
import textwrap
import matplotlib.pyplot as plt

# =============================
# App Config
# =============================
st.set_page_config(
    page_title="Leadership Journey — Simulator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================
# Brand / Theme (Soothing blues/teals, no pink/purple)
# =============================
PALETTE = {
    "bg": "#F5F9FC",
    "panel": "#FFFFFF",
    "ink": "#0F1D2B",
    "muted": "#556575",
    "primary": "#1B4965",   # deep blue
    "accent": "#5FA8D3",    # light blue
    "soft": "#CAE9FF",      # very light blue
    "success": "#2E7D32",   # green for positive feedback
    "warning": "#B26A00",   # amber for caution
    "danger": "#9A0007",    # deep red for negative
}

FONT_STACK = "-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

# =============================
# Global Styles (Rise-like polish)
# =============================
st.markdown(
    f"""
    <style>
        :root {{
            --bg: {PALETTE['bg']};
            --panel: {PALETTE['panel']};
            --ink: {PALETTE['ink']};
            --muted: {PALETTE['muted']};
            --primary: {PALETTE['primary']};
            --accent: {PALETTE['accent']};
            --soft: {PALETTE['soft']};
            --success: {PALETTE['success']};
        }}
        .stApp {{
            background: var(--bg);
            color: var(--ink);
            font-family: {FONT_STACK};
        }}
        /* Cards */
        .card {{
            background: var(--panel);
            border: 1px solid rgba(16,24,40,.06);
            border-radius: 16px;
            padding: 20px 22px;
            box-shadow: 0 1px 2px rgba(16,24,40,.06), 0 8px 24px rgba(16,24,40,.06);
        }}
        .pill {{
            display:inline-block; padding:6px 10px; border-radius:999px;
            background: var(--soft); color: var(--primary); font-weight:600; font-size:12px;
        }}
        .kpi {{
            border-radius: 12px; padding: 10px 12px; background: #ECF5FF; display:inline-block; font-weight:700;
        }}
        /* Button polish */
        .stButton > button {{
            background: linear-gradient(180deg, var(--accent), {PALETTE['primary']});
            border: none; color: white; font-weight: 700; border-radius: 12px; padding: 10px 16px;
            box-shadow: 0 6px 16px rgba(27,73,101,.25);
        }}
        .stButton > button:hover {{ filter: brightness(1.05); }}
        .choice button {{ width: 100%; text-align: left; }}
        /* Top bar */
        .topbar {{ position: sticky; top: 0; z-index: 5; background: var(--bg); padding: 8px 0 14px 0; }}
        /* Cinematic loader */
        .loader-wrap {{
            display:flex; align-items:center; justify-content:center; height: 55vh; flex-direction:column;
            background: radial-gradient(1200px 400px at 50% -20%, #E9F4FF 10%, rgba(255,255,255,0) 60%);
            border-radius: 20px; border:1px solid rgba(16,24,40,.06);
        }}
        .loader-bar {{
            height: 6px; width: 280px; background: #E6EEF7; border-radius: 999px; overflow: hidden; margin-top: 14px;
        }}
        .loader-bar::before {{
            content: ""; display:block; height: 100%; width: 40%; background: linear-gradient(90deg, {PALETTE['soft']}, {PALETTE['accent']});
            border-radius: 999px; animation: slide 1.2s infinite;
        }}
        @keyframes slide {{
            0% {{ transform: translateX(-40%); }}
            100% {{ transform: translateX(240px); }}
        }}
        .lead-in {{ color: var(--muted); max-width: 70ch; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================
# Data Model
# =============================
@dataclass
class Option:
    label: str
    impact: Dict[str, int]  # morale, delivery, trust
    style_tag: str          # for summary tendency
    next_id: Optional[str]  # next scenario id
    feedback: str

@dataclass
class Scenario:
    id: str
    title: str
    situation: str
    prompt: str
    tips: str
    options: List[Option] = field(default_factory=list)

# Scenario Graph (branching)
SCENARIOS: Dict[str, Scenario] = {}

SCENARIOS["S1"] = Scenario(
    id="S1",
    title="Sprint Crunch & Burnout",
    situation=(
        "One week before a high-stakes demo, your senior engineer signals burnout and requests relief."
    ),
    prompt="What do you do next?",
    tips="Crisis moments test your balance of delivery, empathy, and risk.",
    options=[
        Option(
            label="Reassign workload and give recovery time",
            impact={"morale": +3, "delivery": -1, "trust": +3},
            style_tag="Stabilizer",
            next_id="S2A",
            feedback="You protect long-term sustainability; short-term delivery takes a small hit.",
        ),
        Option(
            label="Push through and keep demo scope as-is",
            impact={"morale": -2, "delivery": +2, "trust": -1},
            style_tag="Driver",
            next_id="S2B",
            feedback="You optimize for the deadline, but at a cultural cost.",
        ),
        Option(
            label="Rescope the demo and reduce complexity",
            impact={"morale": +1, "delivery": +1, "trust": +1},
            style_tag="Strategist",
            next_id="S2C",
            feedback="A balanced call; expectation management becomes key.",
        ),
    ],
)

SCENARIOS["S2A"] = Scenario(
    id="S2A",
    title="Team Rally & Redistribution",
    situation=(
        "You pull the team for a quick stand-up to redistribute tasks and protect recovery time."
    ),
    prompt="How do you communicate the plan?",
    tips="Clarity plus empathy builds credibility.",
    options=[
        Option(
            label="Explain constraints transparently and invite support",
            impact={"morale": +2, "delivery": 0, "trust": +2},
            style_tag="Motivator",
            next_id="S3",
            feedback="People step up when they understand the why.",
        ),
        Option(
            label="Quietly shuffle tasks without discussing burnout",
            impact={"morale": -1, "delivery": 0, "trust": -1},
            style_tag="Controller",
            next_id="S3",
            feedback="You avoid discomfort but miss a culture opportunity.",
        ),
    ],
)

SCENARIOS["S2B"] = Scenario(
    id="S2B",
    title="Deadline First",
    situation=(
        "You refocus the team on the deadline and promise recognition after the demo."
    ),
    prompt="What mechanism do you add to reduce risk?",
    tips="High pace needs clear guardrails.",
    options=[
        Option(
            label="Add twice-daily checkpoints with blockers surfaced",
            impact={"morale": -1, "delivery": +2, "trust": 0},
            style_tag="Driver",
            next_id="S3",
            feedback="Tighter loops increase delivery probability, at some morale cost.",
        ),
        Option(
            label="Pair a senior with the burned-out engineer",
            impact={"morale": 0, "delivery": +1, "trust": -1},
            style_tag="Fixer",
            next_id="S3",
            feedback="You patch capacity, but miss the root-cause signal.",
        ),
    ],
)

SCENARIOS["S2C"] = Scenario(
    id="S2C",
    title="Rescoped Narrative",
    situation=(
        "You pitch a leaner demo narrative to stakeholders that highlights outcomes over features."
    ),
    prompt="What do you change first?",
    tips="Rescoping is an expectation game.",
    options=[
        Option(
            label="Define a must-have slice and cut the rest",
            impact={"morale": +1, "delivery": +2, "trust": +1},
            style_tag="Strategist",
            next_id="S3",
            feedback="A crisp MVP creates focus and confidence.",
        ),
        Option(
            label="Keep features, trim testing time",
            impact={"morale": -1, "delivery": 0, "trust": -2},
            style_tag="Risk-Taker",
            next_id="S3",
            feedback="You trade future risk for appearance of progress.",
        ),
    ],
)

SCENARIOS["S3"] = Scenario(
    id="S3",
    title="Creative Feedback Moment",
    situation=(
        "In a brainstorming session, a teammate shares a rough idea. The room goes quiet."
    ),
    prompt="How do you respond?",
    tips="Safety fuels innovation.",
    options=[
        Option(
            label="Thank them and ask two clarifying questions",
            impact={"morale": +2, "delivery": +1, "trust": +3},
            style_tag="Coach",
            next_id=None,
            feedback="You normalize vulnerability and curiosity.",
        ),
        Option(
            label="Move on quickly to stay on schedule",
            impact={"morale": -2, "delivery": +1, "trust": -2},
            style_tag="Task-First",
            next_id=None,
            feedback="You protect time but dent psychological safety.",
        ),
    ],
)

STYLE_WEIGHTS = {
    "Stabilizer": 0,
    "Driver": 0,
    "Strategist": 0,
    "Motivator": 0,
    "Controller": 0,
    "Fixer": 0,
    "Coach": 0,
    "Task-First": 0,
}

METRICS = {"morale": 0, "delivery": 0, "trust": 0}

# =============================
# Session State
# =============================
if "loader_shown" not in st.session_state:
    st.session_state.loader_shown = False
if "node_id" not in st.session_state:
    st.session_state.node_id = "INTRO"
if "metrics" not in st.session_state:
    st.session_state.metrics = METRICS.copy()
if "styles" not in st.session_state:
    st.session_state.styles = STYLE_WEIGHTS.copy()
if "history" not in st.session_state:
    st.session_state.history = []  # [(scenario_id, option_label)]

# =============================
# Helper UI bits
# =============================
def topbar(score: Dict[str, int]):
    morale = score["morale"]; delivery = score["delivery"]; trust = score["trust"]
    cols = st.columns([3, 1.2, 1.2, 1.2])
    with cols[0]:
        st.markdown(
            """
            <div class="topbar">
                <span class="pill">Leadership Journey</span>
                <h2 style="margin:6px 0 0 0;">Interactive Leadership Simulator</h2>
                <p class="lead-in">Make choices, see consequences, and reflect on your leadership tendencies.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.metric("Morale", morale)
    with cols[2]:
        st.metric("Delivery", delivery)
    with cols[3]:
        st.metric("Trust", trust)


def cinematic_loader():
    st.markdown(
        """
        <div class="card loader-wrap">
            <div>
                <div class="pill">Loading</div>
            </div>
            <h2 style="margin: 12px 0 6px 0;">Preparing your leadership journey…</h2>
            <p class="lead-in">We’re setting the stage and shuffling scenarios to keep the experience fresh.</p>
            <div class="loader-bar"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    pb = st.progress(0, text="Initializing…")
    for i in range(100):
        time.sleep(0.01)
        pb.progress(i + 1, text=f"Loading… {i+1}%")
    st.session_state.loader_shown = True


def card(title: str, body_md: str, tip: Optional[str] = None):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin-top:0'>{title}</h3>", unsafe_allow_html=True)
    st.markdown(body_md)
    if tip:
        st.markdown(f"<div class='pill'>Pro Tip</div>  <span style='color:var(--muted)'>{tip}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# =============================
# Sidebar Navigation (Dashboard-style)
# =============================
with st.sidebar:
    st.markdown("""<h2 style='margin-bottom:0'>🧭 Journey Map</h2>""", unsafe_allow_html=True)
    st.write("\n")

    steps = [
        ("INTRO", "Introduction"),
        ("S1", "Scenario 1"),
        ("S2", "Scenario 2"),
        ("S3", "Scenario 3"),
        ("SUMMARY", "Summary"),
    ]

    # compute current unlocked step
    unlocked = {"INTRO": True, "S1": False, "S2": False, "S3": False, "SUMMARY": False}
    # Unlock based on history
    if st.session_state.history:
        unlocked["S1"] = True
    if any(sid in ["S2A", "S2B", "S2C", "S3"] for sid, _ in st.session_state.history):
        unlocked["S2"] = True
    if any(sid == "S3" for sid, _ in st.session_state.history):
        unlocked["S3"] = True
    if st.session_state.node_id == "SUMMARY":
        unlocked["SUMMARY"] = True

    for sid, label in steps:
        disabled = not unlocked[sid]
        if st.button(f"{label}", disabled=disabled, key=f"nav_{sid}"):
            st.session_state.node_id = sid

    st.divider()
    st.caption("Palette: deep blue • light blue • soft sky • neutral ink")

# =============================
# Main Flow
# =============================

# 1) Loader (once per session)
if not st.session_state.loader_shown:
    cinematic_loader()

# 2) Topbar with KPIs
topbar(st.session_state.metrics)

# 3) Routing
node = st.session_state.node_id

if node == "INTRO":
    card(
        "Welcome",
        textwrap.dedent(
            """
            **What to expect**  
            This short, interactive journey plays like a modern micro-course. You’ll step through realistic moments, make decisions, and instantly see how each choice nudges team **morale**, **delivery**, and **trust**.

            **How to play**  
            • Read the situation  
            • Choose an action  
            • Review consequences  
            • Continue to the next moment  
            """
        ),
        tip="There’s no perfect path. Explore trade-offs and notice your patterns.",
    )
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("Start Journey →"):
            st.session_state.node_id = "S1"
            st.rerun()
    with c2:
        st.write("")

elif node in {"S1", "S2", "S3", "S2A", "S2B", "S2C"}:
    # Map the abstract step label to an actual scenario id
    if node == "S2":
        # Depending on history, decide which S2 we came from; fallback S2A
        # Find the last S2* if any
        last_s2 = None
        for sid, _ in st.session_state.history[::-1]:
            if sid.startswith("S2"):
                last_s2 = sid
                break
        effective = last_s2 or "S2A"
    else:
        effective = node

    sc = SCENARIOS[effective]

    # Scenario Header Card
    card(
        sc.title,
        f"**Situation** — {sc.situation}\n\n**Challenge** — {sc.prompt}",
        tip=sc.tips,
    )

    # Decision Buttons
    st.write("")
    cols = st.columns(2)
    picked_index = st.session_state.get(f"picked_{effective}")

    for i, opt in enumerate(sc.options):
        col = cols[i % 2]
        with col:
            btn = st.button(opt.label, key=f"btn_{effective}_{i}")
        if btn:
            # Apply impact
            for k, v in opt.impact.items():
                st.session_state.metrics[k] += v
            st.session_state.styles[opt.style_tag] = st.session_state.styles.get(opt.style_tag, 0) + 1
            st.session_state.history.append((effective, opt.label))
            st.session_state[f"picked_{effective}"] = i

            # Feedback toast
            st.toast(opt.feedback)

            # Move to next
            st.session_state.node_id = opt.next_id or "SUMMARY"
            st.rerun()

    # If already picked, show a small acknowledgement card
    if picked_index is not None:
        chosen = sc.options[picked_index]
        st.info(f"You chose: **{chosen.label}** — {chosen.feedback}")

elif node == "SUMMARY":
    # Summary / Debrief
    card(
        "Your Debrief",
        "Here’s a quick snapshot of how your choices influenced the journey.",
    )

    m = st.session_state.metrics
    s = st.session_state.styles

    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.subheader("Team Signals")
        fig, ax = plt.subplots(figsize=(5.5, 3.2))
        ax.bar(["Morale", "Delivery", "Trust"], [m["morale"], m["delivery"], m["trust"]])
        ax.set_ylim([-3, 8])
        ax.set_ylabel("Relative impact")
        ax.set_title("Your impact across key dimensions")
        st.pyplot(fig, clear_figure=True)

    with c2:
        st.subheader("Style Tendencies")
        # Show the top 3 style tags by count
        top_styles = sorted(s.items(), key=lambda x: x[1], reverse=True)
        if top_styles and top_styles[0][1] > 0:
            for tag, cnt in top_styles[:3]:
                if cnt == 0:
                    continue
                st.write(f"**{tag}** — chosen {cnt} time(s)")
        else:
            st.caption("No strong signal yet — replay with different choices.")

    st.divider()
    st.subheader("What this suggests")
    takeaways = []
    if m["trust"] >= 3:
        takeaways.append("You deliberately cultivate psychological safety and credibility.")
    if m["delivery"] >= 3:
        takeaways.append("You keep outcomes visible and manage execution risk well.")
    if m["morale"] >= 3:
        takeaways.append("You sustain energy by pacing the team and addressing overload.")
    if not takeaways:
        takeaways = [
            "Your results were mixed. Consider balancing pace with wellbeing and clarity.",
        ]
    for t in takeaways:
        st.success(t)

    st.write("")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Replay from Start"):
            for key in list(st.session_state.keys()):
                if key.startswith("picked_"):
                    del st.session_state[key]
            st.session_state.node_id = "INTRO"
            st.session_state.metrics = METRICS.copy()
            st.session_state.styles = STYLE_WEIGHTS.copy()
            st.session_state.history = []
            st.rerun()
    with col2:
        if st.button("Shuffle Scenarios"):
            # Simple shuffle cue (for future extensibility)
            random.shuffle(SCENARIOS["S1"].options)
            st.toast("Decision order shuffled for S1.")
    with col3:
        st.caption("Tip: In an interview, narrate *why* you chose each path and what you’d try next.")

else:
    st.session_state.node_id = "INTRO"
    st.rerun()
