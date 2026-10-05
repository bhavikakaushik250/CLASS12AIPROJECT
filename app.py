
import streamlit as st
import streamlit.components.v1 as components
import pickle
import pandas as pd
import random
import time

# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Pause | Student Wellbeing",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LOAD MODELS
# =========================================================

with open("anomaly_model.pkl", "rb") as f:
    anomaly_model = pickle.load(f)

with open("stress_model.pkl", "rb") as f:
    stress_model = pickle.load(f)

from chatbot import generate_response, detect_category, safety_check


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "stress_level": None,
    "stress_index": 0,
    "anomaly_result": None,

    "chat_history": [],
    "previous_category": None,

    "selected_theme": "Navy & Mauve",
    "appearance": "🌙 Dark",

    "memory_cards": [],
    "memory_flipped": [],
    "memory_matched": set(),
    "memory_attempts": 0,
    "memory_message": "",
    "memory_started": False,

    "focus_running": False,
    "focus_start_time": None,
    "focus_score": 0,
    "focus_round": 0,
    "focus_position": random.randint(0, 5),
    "focus_finished": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# THEMES
# =========================================================

THEMES = {
    "Navy & Mauve": {
        "dark": "linear-gradient(135deg, #171A2B 0%, #25243A 48%, #352B3C 100%)",
        "light": "linear-gradient(135deg, #F7F0EF 0%, #F2E6E7 48%, #E8DDE4 100%)",
        "accent": "#BD8E89",
        "accent_light": "#D9AAA3",
    },

    "Forest": {
        "dark": "linear-gradient(135deg, #16231E 0%, #20372E 50%, #2D4339 100%)",
        "light": "linear-gradient(135deg, #F0F5F0 0%, #E4EEE7 50%, #DCE8DF 100%)",
        "accent": "#7F9D89",
        "accent_light": "#A9C2AF",
    },

    "Lavender": {
        "dark": "linear-gradient(135deg, #211D30 0%, #302942 50%, #3B3150 100%)",
        "light": "linear-gradient(135deg, #F7F2FA 0%, #EEE6F4 50%, #E7DDF0 100%)",
        "accent": "#9B83B5",
        "accent_light": "#BBA8D0",
    },

    "Rose": {
        "dark": "linear-gradient(135deg, #281C22 0%, #3B252F 50%, #492D38 100%)",
        "light": "linear-gradient(135deg, #FBF1F3 0%, #F4E2E7 50%, #ECD8DE 100%)",
        "accent": "#B77C8D",
        "accent_light": "#D49AAA",
    },
}

theme = THEMES[st.session_state.selected_theme]


# =========================================================
# APPEARANCE
# =========================================================

if st.session_state.appearance == "☀️ Light":
    page_bg = theme["light"]
    text_color = "#241E1D"
    card_bg = "rgba(255,255,255,0.72)"
else:
    page_bg = theme["dark"]
    text_color = "#F7F1EF"
    card_bg = "rgba(255,255,255,0.07)"


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    f"""
<style>

[data-testid="stAppViewContainer"] {{
    background: {page_bg};
    color: {text_color};
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

[data-testid="stSidebar"] {{
    display: none;
}}

.block-container {{
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}}

h1, h2, h3, h4, h5, h6 {{
    color: {text_color} !important;
}}

p, label {{
    color: {text_color};
}}

.hero-box {{
    background: {card_bg};
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 28px;
    padding: 42px;
    margin: 10px 0 28px 0;
}}

.small-label {{
    color: {theme["accent_light"]};
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}}

.soft-box {{
    background: {card_bg};
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 24px;
    margin: 12px 0;
}}

div.stButton > button {{
    border-radius: 14px;
    min-height: 42px;
    font-weight: 600;
}}


/* =========================================================
   SAHAARA
   ========================================================= */

[data-testid="stChatMessage"] {{
    color: #FFFFFF !important;
}}

[data-testid="stChatMessageContent"] {{
    color: #FFFFFF !important;
}}

[data-testid="stChatMessageContent"] p {{
    color: #FFFFFF !important;
}}

[data-testid="stChatMessageContent"] strong {{
    color: #FFFFFF !important;
}}

[data-testid="stChatMessageContent"] li {{
    color: #FFFFFF !important;
}}

[data-testid="stChatMessageContent"] span {{
    color: #FFFFFF !important;
}}

[class*="st-key-sahaara_form"] input {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    caret-color: #FFFFFF !important;
}}

[class*="st-key-sahaara_form"] input::placeholder {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 0.65 !important;
}}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SAHAARA FOLLOW-UPS
# =========================================================

FOLLOW_UPS = {

    "exams":
        "What feels heavier right now: the amount you have to study, or the fear of how you'll perform?",

    "marks":
        "Is it the marks themselves bothering you, or what you feel they say about you?",

    "study":
        "Which subject or topic is taking up most of your mental space right now?",

    "deadlines":
        "What's the one deadline that feels most urgent at the moment?",

    "procrastination":
        "When you put the work off, is it usually because you're tired, overwhelmed, or don't know where to start?",

    "focus":
        "What usually breaks your concentration first: your phone, thoughts, tiredness, or something else?",

    "memory":
        "Are you struggling more with remembering things, or with understanding them in the first place?",

    "parents":
        "Do you feel like you can actually explain what you're going through to them?",

    "friends":
        "Do you want help with what happened, or mostly want somewhere to talk about it?",

    "bullying":
        "Is this something that happens repeatedly, or was there one particular incident?",

    "lonely":
        "Do you feel lonely even when you're around people, or are you actually spending a lot of time alone?",

    "overthinking":
        "Is there one particular thought that keeps coming back?",

    "future":
        "Is the uncertainty itself bothering you, or are you worried about choosing the wrong path?",

    "career":
        "Are you unsure about what you want, or do you already have an idea but feel pressured about it?",

    "college":
        "What's stressing you most about college right now?",

    "sleep":
        "Has your sleep been affected more by your schedule or by your thoughts at night?",

    "anxiety":
        "What tends to make that feeling stronger for you?",

    "low_mood":
        "Has this been more of a today problem, or has it been sitting with you for a while?",

    "family":
        "Do you want to talk about what happened, or figure out what you want to do next?",

    "perfectionism":
        "What feels like it would happen if you didn't do something perfectly?",
}


# =========================================================
# SAHAARA CHAT
# =========================================================

with st.popover("💬 Sahaara"):

    st.markdown("### 💬 Sahaara")

    st.caption(
        "A quiet space to talk things through."
    )

    if not st.session_state.chat_history:

        st.info(
            "You can talk about school, stress, friendships, "
            "future plans, or anything that's weighing on you."
        )

    for role, message in st.session_state.chat_history:

        with st.chat_message(role):
            st.write(message)

    with st.form(
        "sahaara_form",
        clear_on_submit=True
    ):

        user_message = st.text_input(
            "Message Sahaara",
            placeholder="What's on your mind?"
        )

        send = st.form_submit_button("Send")

        if send and user_message.strip():

            message = user_message.strip()

            st.session_state.chat_history.append(
                ("user", message)
            )

            if safety_check(message):

                response = (
                    "I'm really glad you said something. "
                    "Please tell a trusted adult who can stay with you "
                    "and help you get support right now."
                )

                category = "generic"

            else:

                category = detect_category(message)

                response = generate_response(
                    message,
                    st.session_state.stress_level,
                    st.session_state.previous_category
                )

                if category in FOLLOW_UPS:

                    response += (
                        "\n\n" +
                        FOLLOW_UPS[category]
                    )

            st.session_state.previous_category = category

            st.session_state.chat_history.append(
                ("assistant", response)
            )

            st.rerun()


# =========================================================
# MAIN TABS
# =========================================================

tab_home, tab_ground, tab_daily, tab_comfort = st.tabs(
    [
        "🏠 Home",
        "🌿 Ground Reset",
        "📊 Daily Check-In",
        "🎮 Comfort Corner",
    ]
)


# =========================================================
# HOME
# =========================================================

with tab_home:

    st.markdown(
        '<div class="hero-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="small-label">PAUSE</div>',
        unsafe_allow_html=True
    )

    st.title(
        "You don't have to have everything figured out."
    )

    st.write(
        "A student wellbeing space designed to help you "
        "pause, understand what you're feeling, and take "
        "one manageable step at a time."
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="soft-box">',
            unsafe_allow_html=True
        )

        st.subheader("🌿 Ground Reset")

        st.write(
            "Use breathing, grounding, or a thought dump "
            "when your mind feels overloaded."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            '<div class="soft-box">',
            unsafe_allow_html=True
        )

        st.subheader("📊 Daily Check-In")

        st.write(
            "Reflect on sleep, workload, mood, social time, "
            "screen time and other everyday factors."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.subheader("🎨 Personalise your space")

    col1, col2 = st.columns(2)

    with col1:

        selected_theme = st.selectbox(
            "Theme",
            list(THEMES.keys()),
            index=list(THEMES.keys()).index(
                st.session_state.selected_theme
            )
        )

        if selected_theme != st.session_state.selected_theme:

            st.session_state.selected_theme = selected_theme
            st.rerun()

    with col2:

        appearance = st.selectbox(
            "Appearance",
            ["🌙 Dark", "☀️ Light"],
            index=[
                "🌙 Dark",
                "☀️ Light"
            ].index(st.session_state.appearance)
        )

        if appearance != st.session_state.appearance:

            st.session_state.appearance = appearance
            st.rerun()

    st.markdown("---")

    st.info(
        "💬 Sahaara is available from the button above "
        "whenever you want to talk something through."
    )


# =========================================================
# GROUND RESET
# =========================================================

with tab_ground:

    st.header("🌿 Ground Reset")

    st.write(
        "A small pause for moments when your mind feels too full."
    )

    ground_reset_html = """
<!DOCTYPE html>

<html>

<head>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 2px;
    font-family: Arial, sans-serif;
    background: transparent;
    color: #2B2524;
}

.container {
    width: 100%;
}

.card {
    background: rgba(255,255,255,0.80);
    border: 1px solid rgba(100,80,80,0.15);
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 4px 14px rgba(50,30,30,0.05);
}

.card h3 {
    margin: 0 0 7px 0;
    color: #3B3030;
    font-size: 18px;
}

.card p {
    color: #5A4D4D;
    line-height: 1.35;
    margin: 6px 0;
    font-size: 14px;
}


/* BREATHING */

.breath-area {
    text-align: center;
    padding: 2px 0;
}

.breath-circle {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: linear-gradient(
        135deg,
        #BD8E89,
        #9E7370
    );
    margin: 12px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 700;
    box-shadow:
        0 0 0 0 rgba(189,142,137,0.35),
        0 6px 18px rgba(100,60,60,0.18);
    transform: scale(1);
}

.breath-circle.breathe-in {
    animation: breatheIn 4s ease-in-out forwards;
}

.breath-circle.breathe-out {
    animation: breatheOut 4s ease-in-out forwards;
}

@keyframes breatheIn {
    0% {
        transform: scale(0.82);
    }

    100% {
        transform: scale(1.25);
    }
}

@keyframes breatheOut {
    0% {
        transform: scale(1.25);
    }

    100% {
        transform: scale(0.82);
    }
}


/* BUTTONS */

button {
    border: 1px solid #BD8E89;
    border-radius: 10px;
    padding: 9px 16px;
    cursor: pointer;
    font-weight: 700;
    font-size: 13px;
    background: #BD8E89;
    color: #FFFFFF;
    box-shadow: 0 3px 9px rgba(0,0,0,0.10);
    transition:
        transform 0.15s ease,
        background 0.15s ease;
}

button:hover {
    background: #7F6269;
    color: #FFFFFF;
    transform: translateY(-1px);
}

button:active {
    transform: translateY(0);
}


/* GROUNDING */

.ground-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 7px;
    margin-top: 10px;
}

.sense {
    background: rgba(189,142,137,0.13);
    border-radius: 11px;
    padding: 9px 5px;
    text-align: center;
    color: #5A4D4D;
    font-size: 12px;
    line-height: 1.25;
}

.sense strong {
    display: block;
    color: #3B3030;
    font-size: 19px;
    margin-bottom: 2px;
}


/* THOUGHT DUMP */

textarea {
    width: 100%;
    min-height: 100px;
    border-radius: 11px;
    border: 1px solid rgba(100,80,80,0.25);
    padding: 11px;
    font-family: Arial, sans-serif;
    font-size: 13px;
    resize: none;
    color: #2B2524;
    background: rgba(255,255,255,0.92);
}

textarea::placeholder {
    color: #7B6A68;
}

.thought-actions {
    display: flex;
    gap: 9px;
    margin-top: 9px;
    flex-wrap: wrap;
}


/* ANIMATION */

.animation-box {
    display: none;
    margin-top: 10px;
    padding: 10px;
    border-radius: 13px;
    text-align: center;
    background: rgba(189,142,137,0.08);
    overflow: visible;
    min-height: 105px;
}

.animation-box.active {
    display: block;
}

.paper {
    width: 150px;
    min-height: 55px;
    margin: 0 auto 5px;
    padding: 10px;
    border-radius: 6px;
    background: #FFFDF8;
    color: #4D403E;
    font-size: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.12);
    position: relative;
}

.paper.burning {
    animation: burnPaper 2.2s ease-in forwards;
}

@keyframes burnPaper {

    0% {
        transform: translateY(0) rotate(0deg) scale(1);
        opacity: 1;
        filter: brightness(1);
    }

    30% {
        transform: translateY(-4px) rotate(-2deg) scale(1);
        opacity: 1;
        filter: brightness(1.1) sepia(0.2);
    }

    60% {
        transform: translateY(-12px) rotate(3deg) scale(0.85);
        opacity: 0.7;
        filter: brightness(1.3) sepia(0.55);
    }

    100% {
        transform: translateY(-30px) rotate(8deg) scale(0.35);
        opacity: 0;
        filter: brightness(1.7) sepia(1);
    }
}

.flames {
    height: 24px;
    margin-top: -4px;
    font-size: 20px;
    opacity: 0;
}

.flames.show {
    animation: flameShow 2.1s ease-in-out forwards;
}

@keyframes flameShow {

    0% {
        opacity: 0;
        transform: scale(0.7);
    }

    20% {
        opacity: 1;
        transform: scale(1);
    }

    65% {
        opacity: 1;
        transform: scale(1.08);
    }

    100% {
        opacity: 0;
        transform: scale(0.7);
    }
}


/* SHRED */

.shred-paper {
    width: 150px;
    min-height: 55px;
    margin: 0 auto 5px;
    padding: 10px;
    border-radius: 6px;
    background: #FFFDF8;
    color: #4D403E;
    font-size: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.12);
}

.shred-paper.shredding {
    animation: shredPaper 1.9s ease-in forwards;
}

@keyframes shredPaper {

    0% {
        transform: translateX(0) rotate(0deg) scaleY(1);
        opacity: 1;
        clip-path: inset(0 0 0 0);
    }

    30% {
        transform: translateX(-5px) rotate(-2deg);
        opacity: 0.9;
    }

    60% {
        transform: translateX(7px) rotate(3deg) scaleY(0.65);
        opacity: 0.55;
        clip-path: inset(0 20% 0 20%);
    }

    100% {
        transform: translateX(10px) rotate(6deg) scaleY(0.2);
        opacity: 0;
        clip-path: inset(0 50% 0 50%);
    }
}

.status {
    margin-top: 6px;
    font-weight: 600;
    font-size: 12px;
    color: #7F6269;
    min-height: 16px;
}

@media (max-width: 800px) {

    .ground-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .thought-actions {
        flex-direction: row;
    }

    .thought-actions button {
        flex: 1;
    }

}

</style>

</head>

<body>

<div class="container">


<div class="card">

    <h3>🌬️ One-Minute Breathing Reset</h3>

    <p>
        Follow the circle. Breathe in as it expands
        and breathe out as it contracts.
    </p>

    <div class="breath-area">

        <div
            id="breathCircle"
            class="breath-circle"
        >
            Ready
        </div>

        <button onclick="startBreathing()">
            Start Breathing
        </button>

        <div
            id="breathStatus"
            class="status"
        ></div>

    </div>

</div>


<div class="card">

    <h3>🌱 5-4-3-2-1 Grounding</h3>

    <p>
        Notice the world around you without judging
        what you're feeling.
    </p>

    <div class="ground-grid">

        <div class="sense">
            <strong>5</strong>
            See
        </div>

        <div class="sense">
            <strong>4</strong>
            Touch
        </div>

        <div class="sense">
            <strong>3</strong>
            Hear
        </div>

        <div class="sense">
            <strong>2</strong>
            Smell
        </div>

        <div class="sense">
            <strong>1</strong>
            Taste
        </div>

    </div>

</div>


<div class="card">

    <h3>📝 Thought Dump</h3>

    <p>
        Write whatever is taking up space in your head.
    </p>

    <textarea
        id="thoughtBox"
        placeholder="Write it all out here..."
    ></textarea>

    <div class="thought-actions">

        <button onclick="burnThoughts()">
            🔥 Burn
        </button>

        <button onclick="shredThoughts()">
            ✂️ Shred
        </button>

    </div>

    <div
        id="animationBox"
        class="animation-box"
    >

        <div
            id="paperAnimation"
            class="paper"
        >
            Your thought
        </div>

        <div
            id="flames"
            class="flames"
        >
            🔥 🔥 🔥
        </div>

        <div
            id="animationStatus"
            class="status"
        ></div>

    </div>

    <div
        id="thoughtStatus"
        class="status"
    ></div>

</div>


</div>


<script>

function startBreathing() {

    const circle =
        document.getElementById("breathCircle");

    const status =
        document.getElementById("breathStatus");

    let round = 0;

    const totalRounds = 7;

    function breathe() {

        if (round >= totalRounds) {

            circle.className =
                "breath-circle";

            circle.innerText =
                "Done";

            status.innerText =
                "🌿 You made space for one quiet minute.";

            return;
        }

        round++;

        circle.className =
            "breath-circle breathe-in";

        circle.innerText =
            "Breathe in";

        status.innerText =
            "Slowly breathe in...";

        setTimeout(function() {

            circle.className =
                "breath-circle breathe-out";

            circle.innerText =
                "Breathe out";

            status.innerText =
                "Slowly breathe out...";

        }, 4000);

        setTimeout(function() {

            breathe();

        }, 8000);
    }

    status.innerText =
        "Take it slowly. There is nowhere else to be.";

    breathe();
}


function burnThoughts() {

    const box =
        document.getElementById("thoughtBox");

    const animationBox =
        document.getElementById("animationBox");

    const paper =
        document.getElementById("paperAnimation");

    const flames =
        document.getElementById("flames");

    const animationStatus =
        document.getElementById("animationStatus");

    const thoughtStatus =
        document.getElementById("thoughtStatus");

    const thought =
        box.value.trim();

    if (!thought) {

        thoughtStatus.innerText =
            "Write something first.";

        return;
    }

    animationBox.classList.add("active");

    paper.className =
        "paper";

    flames.className =
        "flames";

    paper.innerText =
        thought.length > 70
        ? thought.substring(0, 70) + "..."
        : thought;

    animationStatus.innerText =
        "🔥 Letting this thought go...";

    void paper.offsetWidth;
    void flames.offsetWidth;

    paper.classList.add("burning");
    flames.classList.add("show");

    setTimeout(function() {

        box.value = "";

        animationStatus.innerText =
            "✨ It's okay to let some thoughts leave.";

    }, 2200);
}


function shredThoughts() {

    const box =
        document.getElementById("thoughtBox");

    const animationBox =
        document.getElementById("animationBox");

    const paper =
        document.getElementById("paperAnimation");

    const flames =
        document.getElementById("flames");

    const animationStatus =
        document.getElementById("animationStatus");

    const thoughtStatus =
        document.getElementById("thoughtStatus");

    const thought =
        box.value.trim();

    if (!thought) {

        thoughtStatus.innerText =
            "Write something first.";

        return;
    }

    animationBox.classList.add("active");

    flames.className =
        "flames";

    paper.className =
        "shred-paper";

    paper.innerText =
        thought.length > 70
        ? thought.substring(0, 70) + "..."
        : thought;

    animationStatus.innerText =
        "✂️ Shredding that thought...";

    void paper.offsetWidth;

    paper.classList.add("shredding");

    setTimeout(function() {

        box.value = "";

        animationStatus.innerText =
            "✨ That thought doesn't have to stay with you.";

    }, 1900);
}

</script>

</body>

</html>
"""

    components.html(
        ground_reset_html,
        height=760,
        scrolling=False
    )


# =========================================================
# DAILY CHECK-IN
# =========================================================

with tab_daily:

    st.header("📊 Daily Check-In")

    st.write(
        "Answer based on how today has actually been."
    )

    col1, col2 = st.columns(2)

    with col1:

        sleep_hrs = st.slider(
            "Sleep hours",
            2.0,
            12.0,
            7.0,
            0.5
        )

        sleep_quality = st.slider(
            "Sleep quality",
            1,
            5,
            3
        )

        exercise_mins = st.slider(
            "Exercise / movement minutes",
            0,
            180,
            30,
            10
        )

        academic_hrs = st.slider(
            "Academic hours",
            0.0,
            14.0,
            6.0,
            0.5
        )

        workload_pressure = st.slider(
            "Workload pressure",
            1,
            5,
            3
        )

    with col2:

        caffeine_mg = st.slider(
            "Caffeine intake (mg)",
            0,
            800,
            150,
            50
        )

        screen_hrs = st.slider(
            "Screen time",
            0.0,
            14.0,
            4.0,
            0.5
        )

        mood_rating = st.slider(
            "Mood today",
            1,
            5,
            3
        )

        social_hrs = st.slider(
            "Social time",
            0.0,
            30.0,
            8.0,
            1.0
        )

        social_quality = st.slider(
            "Quality of social connection",
            1,
            5,
            3
        )

    st.markdown("---")

    if st.button(
        "🔎 Run AI Factor Analysis",
        use_container_width=True
    ):

        feature_names = [
            "sleep_hrs",
            "sleep_quality",
            "academic_hrs",
            "caffeine_mg",
            "screen_hrs",
            "exercise_mins",
            "mood_rating",
            "social_hrs",
            "social_quality",
            "workload_pressure",
        ]

        input_data = pd.DataFrame(
            [[
                sleep_hrs,
                sleep_quality,
                academic_hrs,
                caffeine_mg,
                screen_hrs,
                exercise_mins,
                mood_rating,
                social_hrs,
                social_quality,
                workload_pressure,
            ]],
            columns=feature_names
        )

        prediction = stress_model.predict(
            input_data
        )[0]

        anomaly = anomaly_model.predict(
            input_data
        )[0]

        stress_index = {
            "Low": random.randint(15, 35),
            "Moderate": random.randint(36, 65),
            "High": random.randint(66, 90),
        }.get(prediction, 50)

        st.session_state.stress_level = prediction
        st.session_state.stress_index = stress_index
        st.session_state.anomaly_result = anomaly

        st.success(
            "Analysis complete."
        )

    if st.session_state.stress_level:

        level = st.session_state.stress_level
        index = st.session_state.stress_index
        anomaly = st.session_state.anomaly_result

        st.markdown("---")

        st.markdown(
            "### 📊 Your Current Model Result"
        )

        st.markdown(
            "**EXPERIMENTAL MODEL**"
        )

        st.subheader(
            level.upper()
        )

        st.write(
            f"Current model stress index: **{index}/100**"
        )

        st.progress(
            min(index, 100) / 100
        )

        if anomaly == -1:

            st.warning(
                "Today's combination of inputs looked "
                "somewhat unusual compared with the model's "
                "training patterns."
            )

        else:

            st.info(
                "Today's input pattern did not appear unusual "
                "to the model's anomaly detector."
            )

        st.caption(
            "This is an experimental wellbeing model, "
            "not a medical diagnosis."
        )

        st.markdown(
            "### Factors in today's check-in"
        )

        factor_data = pd.DataFrame(
            {
                "Factor": [
                    "Sleep",
                    "Sleep quality",
                    "Academic load",
                    "Caffeine",
                    "Screen time",
                    "Exercise",
                    "Mood",
                    "Social time",
                    "Social quality",
                    "Workload",
                ],

                "Value": [
                    sleep_hrs,
                    sleep_quality,
                    academic_hrs,
                    caffeine_mg / 100,
                    screen_hrs,
                    exercise_mins / 10,
                    mood_rating,
                    social_hrs / 2,
                    social_quality,
                    workload_pressure,
                ],
            }
        ).set_index("Factor")

        st.bar_chart(
            factor_data
        )


# =========================================================
# COMFORT CORNER
# =========================================================

with tab_comfort:

    st.header("🎮 Comfort Corner")

    st.write(
        "Small things to help you pause, reset, or simply "
        "give your brain a break."
    )


    # =====================================================
    # MEMORY MATCH
    # =====================================================

    st.subheader("🌸 Memory Match")

    st.write(
        "Double-click a card to reveal it and find its match!"
     )

    if not st.session_state.memory_cards:

        symbols = [
            "🌸",
            "⭐",
            "🌙",
            "🍀"
        ]

        cards = symbols * 2

        random.shuffle(cards)

        st.session_state.memory_cards = cards
        st.session_state.memory_flipped = []
        st.session_state.memory_matched = set()
        st.session_state.memory_attempts = 0
        st.session_state.memory_message = ""
        st.session_state.memory_started = True

    cards = st.session_state.memory_cards

    cols = st.columns(4)

    for i, symbol in enumerate(cards):

        with cols[i % 4]:

            is_flipped = (
                i in st.session_state.memory_flipped
                or i in st.session_state.memory_matched
            )

            if i in st.session_state.memory_matched:

                label = symbol

            elif is_flipped:

                label = symbol

            else:

                label = "?"

            disabled = (
                i in st.session_state.memory_matched
                or i in st.session_state.memory_flipped
                or len(st.session_state.memory_flipped) >= 2
            )

            if st.button(
                label,
                key=f"memory_card_{i}",
                use_container_width=True,
                disabled=disabled
            ):

                st.session_state.memory_flipped.append(i)

                if len(st.session_state.memory_flipped) == 2:

                    first, second = (
                        st.session_state.memory_flipped
                    )

                    st.session_state.memory_attempts += 1

                    if cards[first] == cards[second]:

                        st.session_state.memory_matched.add(
                            first
                        )

                        st.session_state.memory_matched.add(
                            second
                        )

                        st.session_state.memory_message = (
                            "✨ Match!"
                        )

                        st.session_state.memory_flipped = []

                    else:

                        st.session_state.memory_message = (
                            "Not a match yet. Press Continue."
                        )

    if st.session_state.memory_message:

        st.info(
            st.session_state.memory_message
        )

    if len(st.session_state.memory_flipped) == 2:

        if st.button(
            "Continue",
            key="memory_continue"
        ):

            st.session_state.memory_flipped = []

            st.session_state.memory_message = ""

            st.rerun()

    st.write(
        f"Attempts: {st.session_state.memory_attempts}"
    )

    if len(st.session_state.memory_matched) == len(cards):

        st.success(
            "🌸 You found all the pairs!"
        )

        if st.button(
            "Play Again",
            key="memory_play_again"
        ):

            symbols = [
                "🌸",
                "⭐",
                "🌙",
                "🍀"
            ]

            new_cards = symbols * 2

            random.shuffle(new_cards)

            st.session_state.memory_cards = new_cards
            st.session_state.memory_flipped = []
            st.session_state.memory_matched = set()
            st.session_state.memory_attempts = 0
            st.session_state.memory_message = ""

            st.rerun()

    else:

        if st.button(
            "Restart Memory Match",
            key="memory_restart"
        ):

            symbols = [
                "🌸",
                "⭐",
                "🌙",
                "🍀"
            ]

            new_cards = symbols * 2

            random.shuffle(new_cards)

            st.session_state.memory_cards = new_cards
            st.session_state.memory_flipped = []
            st.session_state.memory_matched = set()
            st.session_state.memory_attempts = 0
            st.session_state.memory_message = ""

            st.rerun()


    # =====================================================
    # FOCUS CHALLENGE
    # =====================================================

    st.markdown("---")

    st.subheader("🎯 Focus Challenge")

    st.write(
        "Find the target as quickly as you can."
    )

    if not st.session_state.focus_running:

        if not st.session_state.focus_finished:

            if st.button(
                "Start Focus Challenge",
                key="focus_start"
            ):

                st.session_state.focus_running = True
                st.session_state.focus_start_time = time.time()
                st.session_state.focus_score = 0
                st.session_state.focus_round = 0
                st.session_state.focus_position = random.randint(
                    0,
                    5
                )

                st.rerun()

        else:

            st.success(
                f"Challenge complete! "
                f"Your score: {st.session_state.focus_score}"
            )

            if st.button(
                "Play Again",
                key="focus_again"
            ):

                st.session_state.focus_running = True
                st.session_state.focus_finished = False
                st.session_state.focus_start_time = time.time()
                st.session_state.focus_score = 0
                st.session_state.focus_round = 0
                st.session_state.focus_position = random.randint(
                    0,
                    5
                )

                st.rerun()

    else:

        elapsed = (
            time.time()
            - st.session_state.focus_start_time
        )

        remaining = max(
            0,
            30 - int(elapsed)
        )

        st.write(
            f"⏱️ Time remaining: **{remaining} seconds**"
        )

        cols = st.columns(6)

        for i in range(6):

            with cols[i]:

                if i == st.session_state.focus_position:

                    button_label = "🎯"

                else:

                    button_label = "•"

                if st.button(
                    button_label,
                    key=f"focus_{st.session_state.focus_round}_{i}",
                    use_container_width=True
                ):

                    if i == st.session_state.focus_position:

                        st.session_state.focus_score += 1

                        st.session_state.focus_round += 1

                        st.session_state.focus_position = random.randint(
                            0,
                            5
                        )

                    st.rerun()

        if elapsed >= 30:

            st.session_state.focus_running = False
            st.session_state.focus_finished = True

            st.rerun()

        st.write(
            f"Score: **{st.session_state.focus_score}**"
        )

        if st.button(
            "Restart Challenge",
            key="focus_restart"
        ):

            st.session_state.focus_running = True
            st.session_state.focus_finished = False
            st.session_state.focus_start_time = time.time()
            st.session_state.focus_score = 0
            st.session_state.focus_round = 0
            st.session_state.focus_position = random.randint(
                0,
                5
            )

            st.rerun()


    # =====================================================
    # LITTLE THINGS THAT HELP
    # =====================================================

    st.markdown("---")

    st.subheader("🌷 Little Things That Help")

    st.write(
        "You don't always have to fix the problem. "
        "Sometimes you just need a small pause."
    )

    video1, video2, video3 = st.columns(3)


    # -----------------------------------------------------
    # PUPPY
    # -----------------------------------------------------

    with video1:

        st.markdown("### 🐶 Puppy Therapy")

        st.caption(
            "A little dose of puppy chaos."
        )

        st.video(
            "https://www.youtube.com/watch?v=sYaq3WWyW8w"
        )


    # -----------------------------------------------------
    # BABY
    # -----------------------------------------------------

    with video2:

        st.markdown("### 👶 Baby Giggles")

        st.caption(
            "Wholesome baby moments for a quick reset."
        )

        st.video(
            "https://www.youtube.com/watch?v=8PHbr2m7auo"
        )


    # -----------------------------------------------------
    # ASMR
    # -----------------------------------------------------

    with video3:

        st.markdown("### 🎧 ASMR Reset")

        st.caption(
            "Relaxing sounds when you just need to slow down."
        )

        st.video(
            "https://www.youtube.com/watch?v=TTXcHEMfLb4"
        )
