import streamlit as st
import requests

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="CampusConnect — Find Your Tribe",
    page_icon="🎓",
    layout="wide",
)

# ── Massive custom CSS for premium look ──────────────────────
st.markdown("""
<style>
/* ─── Import Google Font ─────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ─── Global overrides ───────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Hide default Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ─── Main container background ──────────────────────────── */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
}

/* ─── Hero banner ────────────────────────────────────────── */
.hero-section {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem 1rem;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
    letter-spacing: -1px;
    animation: fadeInDown 0.8s ease-out;
}
.hero-subtitle {
    font-size: 1.15rem;
    color: #9ca3af;
    font-weight: 400;
    letter-spacing: 0.5px;
    animation: fadeInUp 0.8s ease-out;
}
.hero-emoji {
    font-size: 3rem;
    display: block;
    margin-bottom: 0.5rem;
    animation: bounce 2s infinite;
}

/* ─── Animations ─────────────────────────────────────────── */
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-10px); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4); }
    50%      { box-shadow: 0 0 0 12px rgba(102, 126, 234, 0); }
}
@keyframes cardEntry {
    from { opacity: 0; transform: translateY(20px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ─── Tab styling ────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,0.03);
    border-radius: 16px;
    padding: 6px;
    border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 0.95rem;
    color: #9ca3af;
    transition: all 0.3s ease;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}
.stTabs [data-baseweb="tab"]:hover {
    color: #e0e0e0;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 2rem;
}

/* ─── Glass card ─────────────────────────────────────────── */
.glass-card {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 2rem;
    margin-bottom: 1.2rem;
    transition: all 0.3s ease;
    animation: cardEntry 0.6s ease-out;
}
.glass-card:hover {
    border-color: rgba(102, 126, 234, 0.3);
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
    transform: translateY(-2px);
}
.glass-card h3 {
    font-size: 1.3rem;
    font-weight: 700;
    color: #e0e7ff;
    margin-bottom: 0.5rem;
}
.glass-card p {
    color: #9ca3af;
    font-size: 0.92rem;
    line-height: 1.6;
}

/* ─── Buttons ────────────────────────────────────────────── */
.stButton button {
    width: 100%;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.3s ease !important;
    border: none !important;
    letter-spacing: 0.3px;
}
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
}
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    animation: pulse 2.5s infinite;
}

/* ─── Input fields ───────────────────────────────────────── */
.stTextInput input {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: #e0e0e0 !important;
    padding: 0.7rem 1rem !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
}
.stTextInput input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
}
.stTextInput label {
    color: #9ca3af !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
}

/* ─── Match card ─────────────────────────────────────────── */
.match-card {
    background: linear-gradient(145deg, rgba(30, 30, 60, 0.9), rgba(40, 40, 70, 0.9));
    backdrop-filter: blur(12px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 1.8rem;
    margin-bottom: 1rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    animation: cardEntry 0.5s ease-out;
}
.match-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 16px 48px rgba(102, 126, 234, 0.25);
    border-color: rgba(102, 126, 234, 0.4);
}
.match-score {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00d2ff, #667eea, #f093fb);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
    margin-bottom: 0.3rem;
}
.match-users {
    font-size: 1.15rem;
    font-weight: 600;
    color: #e0e7ff;
    margin-top: 0.4rem;
}
.match-shared {
    display: inline-block;
    margin-top: 0.8rem;
    padding: 4px 14px;
    background: rgba(102, 126, 234, 0.15);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 20px;
    color: #a5b4fc;
    font-size: 0.82rem;
    font-weight: 500;
}

/* ─── Profile card ───────────────────────────────────────── */
.profile-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 0.8rem;
    transition: all 0.3s ease;
    animation: cardEntry 0.5s ease-out;
}
.profile-card:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(102, 126, 234, 0.25);
}
.profile-name {
    font-size: 1.2rem;
    font-weight: 700;
    color: #e0e7ff;
    margin-bottom: 0.6rem;
}
.profile-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    font-weight: 800;
    color: white;
    margin-right: 12px;
    vertical-align: middle;
}

/* ─── Interest chip ──────────────────────────────────────── */
.chip {
    display: inline-block;
    padding: 5px 14px;
    margin: 3px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 500;
    transition: all 0.2s ease;
}
.chip-purple {
    background: rgba(118, 75, 162, 0.2);
    border: 1px solid rgba(118, 75, 162, 0.4);
    color: #c4b5fd;
}
.chip-blue {
    background: rgba(102, 126, 234, 0.15);
    border: 1px solid rgba(102, 126, 234, 0.35);
    color: #a5b4fc;
}
.chip-pink {
    background: rgba(240, 147, 251, 0.15);
    border: 1px solid rgba(240, 147, 251, 0.35);
    color: #f0abfc;
}
.chip-teal {
    background: rgba(0, 210, 255, 0.12);
    border: 1px solid rgba(0, 210, 255, 0.3);
    color: #67e8f9;
}

/* ─── Stats bar ──────────────────────────────────────────── */
.stat-box {
    text-align: center;
    padding: 1.2rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}
.stat-number {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label {
    font-size: 0.82rem;
    color: #6b7280;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* ─── Section headers ────────────────────────────────────── */
.section-header {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e0e7ff;
    margin-bottom: 0.3rem;
}
.section-desc {
    color: #6b7280;
    font-size: 0.92rem;
    margin-bottom: 1.5rem;
}

/* ─── Divider ────────────────────────────────────────────── */
.gradient-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(102,126,234,0.4), transparent);
    border: none;
    margin: 1.5rem 0;
}

/* ─── Streamlit container borders ────────────────────────── */
[data-testid="stVerticalBlock"] > div:has(> [data-testid="stVerticalBlockBorderWrapper"]) {
    border-radius: 20px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 20px !important;
}

/* ─── Success / info / warning / error alerts ────────────── */
.stAlert {
    border-radius: 12px !important;
}

/* ─── Expander ───────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

/* ─── Scrollbar ──────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(102, 126, 234, 0.3);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(102, 126, 234, 0.5);
}
</style>
""", unsafe_allow_html=True)

BASE_URL = "http://localhost:8000"

CHIP_COLORS = ["chip-purple", "chip-blue", "chip-pink", "chip-teal"]

# ── Hero Section ─────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <span class="hero-emoji">🎓</span>
    <div class="hero-title">CampusConnect</div>
    <div class="hero-subtitle">Find your tribe — connect with college peers who share your passions</div>
</div>
<div class="gradient-divider"></div>
""", unsafe_allow_html=True)

# ── Stats bar ────────────────────────────────────────────────
try:
    users_list = requests.get(f"{BASE_URL}/users", timeout=2).json()
    total_users = len(users_list)
    matches_data = requests.get(f"{BASE_URL}/match", timeout=2).json()
    total_matches = len(matches_data)
except Exception:
    total_users = 0
    total_matches = 0
    users_list = []
    matches_data = []

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{total_users}</div>
        <div class="stat-label">Students Registered</div>
    </div>""", unsafe_allow_html=True)
with col_s2:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{total_matches}</div>
        <div class="stat-label">Connections Found</div>
    </div>""", unsafe_allow_html=True)
with col_s3:
    top_score = int(matches_data[0]["similarity"] * 100) if matches_data else 0
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{top_score}%</div>
        <div class="stat-label">Best Match Score</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🚀  Join / Add Interests", "🔗  Discover Matches", "👥  Student Profiles"])

# ╭─────────────────────────────────────────────────────────╮
# │  TAB 1 — Register & Add Interests                      │
# ╰─────────────────────────────────────────────────────────╯
with tab1:
    st.markdown("""
    <div class="section-header">🌟 Build Your Profile</div>
    <div class="section-desc">Register yourself and tell us what you're into — from coding to cricket, art to astronomy!</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>👤 Register as a Student</h3>
            <p>Enter your name to join the CampusConnect community.</p>
        </div>
        """, unsafe_allow_html=True)

        name = st.text_input("Your Name", placeholder="e.g., Aarnav, Priya, Rahul…", key="user_input")

        if st.button("🎓  Join CampusConnect", key="btn_add_user"):
            if name:
                try:
                    res = requests.post(f"{BASE_URL}/add_user", json={"name": name})
                    msg = res.json().get("status", "Done")
                    if "added" in msg.lower():
                        st.success(f"🎉 Welcome aboard, **{name}**!")
                        st.balloons()
                    else:
                        st.info(msg)
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Backend server is not running!")
            else:
                st.warning("Please enter your name.")

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>💡 Add an Interest</h3>
            <p>Tell us what excites you — the more interests you add, the better your matches!</p>
        </div>
        """, unsafe_allow_html=True)

        interest_user = st.text_input("Your Name", placeholder="e.g., Aarnav", key="int_user")
        interest = st.text_input("Interest / Hobby", placeholder="e.g., Hiking, AI, Photography…", key="int_name")

        if st.button("✨  Add Interest", key="btn_add_interest"):
            if interest and interest_user:
                try:
                    res = requests.post(
                        f"{BASE_URL}/add_interest",
                        json={"user": interest_user, "interest": interest},
                    )
                    msg = res.json().get("status", "Done")
                    if "added" in msg.lower():
                        st.success(f"Added **{interest}** to {interest_user}'s profile!")
                    else:
                        st.info(msg)
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Backend server is not running!")
            else:
                st.warning("Fill in both fields.")

    # Quick-add popular interests
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">🔥 Popular Interests on Campus</div>
    <div class="section-desc">Tap any to copy — then paste it in the interest field above!</div>
    """, unsafe_allow_html=True)

    popular = [
        "🎮 Gaming", "💻 Coding", "📸 Photography", "🎵 Music",
        "⚽ Football", "🏏 Cricket", "🎨 Art", "📚 Reading",
        "🧪 Science", "🤖 AI/ML", "🎬 Movies", "✈️ Travel",
        "🧘 Yoga", "🍳 Cooking", "🎤 Singing", "💃 Dance"
    ]
    chips_html = " ".join(
        f'<span class="chip {CHIP_COLORS[i % len(CHIP_COLORS)]}">{p}</span>'
        for i, p in enumerate(popular)
    )
    st.markdown(f'<div style="line-height: 2.4;">{chips_html}</div>', unsafe_allow_html=True)


# ╭─────────────────────────────────────────────────────────╮
# │  TAB 2 — Discover Matches                              │
# ╰─────────────────────────────────────────────────────────╯
with tab2:
    st.markdown("""
    <div class="section-header">🔗 Your Connections</div>
    <div class="section-desc">We use Jaccard similarity to find students who share the most interests with each other.</div>
    """, unsafe_allow_html=True)

    if st.button("🚀  Find My Matches", type="primary", key="btn_match"):
        with st.spinner("Analyzing shared interests across all students…"):
            try:
                res = requests.get(f"{BASE_URL}/match")

                if res.status_code == 200:
                    matches = res.json()

                    if matches:
                        st.success(f"🎉 Found **{len(matches)}** connection(s)!")
                        st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)

                        cols = st.columns(2, gap="large")
                        for idx, m in enumerate(matches):
                            score_pct = int(m["similarity"] * 100)

                            # Determine color tier
                            if score_pct >= 75:
                                tier_emoji = "🔥"
                                tier_label = "Perfect Match"
                            elif score_pct >= 50:
                                tier_emoji = "⚡"
                                tier_label = "Strong Match"
                            elif score_pct >= 25:
                                tier_emoji = "✨"
                                tier_label = "Good Match"
                            else:
                                tier_emoji = "🌱"
                                tier_label = "Potential Match"

                            col = cols[idx % 2]
                            with col:
                                html = f"""
                                <div class="match-card" style="animation-delay: {idx * 0.1}s;">
                                    <div class="match-score">{score_pct}%</div>
                                    <div class="match-users">
                                        {m['user1']} &nbsp; ↔ &nbsp; {m['user2']}
                                    </div>
                                    <div class="match-shared">{tier_emoji} {tier_label}</div>
                                </div>
                                """
                                st.markdown(html, unsafe_allow_html=True)
                    else:
                        st.info("No matches yet — add more students and shared interests first!")
                else:
                    st.error("Failed to fetch matches.")

            except requests.exceptions.ConnectionError:
                st.error("⚠️ Backend server is not running!")


# ╭─────────────────────────────────────────────────────────╮
# │  TAB 3 — Student Profiles                              │
# ╰─────────────────────────────────────────────────────────╯
with tab3:
    st.markdown("""
    <div class="section-header">👥 Campus Directory</div>
    <div class="section-desc">Browse all registered students and their interests.</div>
    """, unsafe_allow_html=True)

    if st.button("🔄  Refresh Profiles", key="btn_refresh"):
        st.rerun()

    try:
        users_res = requests.get(f"{BASE_URL}/users", timeout=2)
        if users_res.status_code == 200:
            all_users = users_res.json()
            if not all_users:
                st.markdown("""
                <div class="glass-card" style="text-align: center;">
                    <h3>🏫 No students registered yet</h3>
                    <p>Be the first to join! Head to the "Join / Add Interests" tab to get started.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                cols = st.columns(2, gap="large")
                for idx, uname in enumerate(all_users):
                    interests = requests.get(f"{BASE_URL}/users/{uname}/interests", timeout=2).json()
                    initial = uname[0].upper()

                    chips = ""
                    if interests:
                        chips = " ".join(
                            f'<span class="chip {CHIP_COLORS[i % len(CHIP_COLORS)]}">{intr}</span>'
                            for i, intr in enumerate(interests)
                        )
                    else:
                        chips = '<span style="color: #6b7280; font-size: 0.85rem;">No interests added yet</span>'

                    col = cols[idx % 2]
                    with col:
                        st.markdown(f"""
                        <div class="profile-card">
                            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                                <div class="profile-avatar">{initial}</div>
                                <div class="profile-name" style="margin-bottom: 0;">{uname}</div>
                            </div>
                            <div style="line-height: 2.2;">{chips}</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.error("Could not fetch users.")
    except requests.exceptions.ConnectionError:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3>⚠️ Backend Offline</h3>
            <p>Start the backend server to view student profiles.</p>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<div class="gradient-divider"></div>
<div style="text-align: center; padding: 1rem; color: #4b5563; font-size: 0.8rem;">
    Built with ❤️ for college students &nbsp;·&nbsp; CampusConnect © 2026
</div>
""", unsafe_allow_html=True)