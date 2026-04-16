import streamlit as st
import requests
import time

# --- Configuration ---
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Campus Connect", page_icon="✨", layout="centered")

# --- Gen-Z College Aesthetic CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Core Background with subtle neon lighting */
    .stApp {
        background-color: #0B0914; 
        color: #f8fafc;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(124, 58, 237, 0.1) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(236, 72, 153, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(56, 189, 248, 0.05) 0%, transparent 50%);
    }
    
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Modern Gradient Title */
    .exclusive-title {
        text-align: center;
        font-weight: 800;
        font-size: 3.5rem;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        line-height: 1.1;
    }
    
    .subtitle {
        text-align: center;
        font-weight: 400;
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 35px;
    }

    /* Streamlit forms container - Glassmorphism */
    [data-testid="stForm"] {
        background-color: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding-left: 14px;
        font-size: 1rem !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #ec4899 !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        box-shadow: 0 0 0 1px #ec4899 !important;
    }

    /* Vibrant Gradient Buttons */
    .stButton>button[kind="primary"], .stFormSubmitButton>button {
        background: linear-gradient(135deg, #8b5cf6, #ec4899) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border-radius: 12px !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3) !important;
        transition: all 0.3s ease !important;
        width: auto;
    }
    .stButton>button[kind="primary"]:hover, .stFormSubmitButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(236, 72, 153, 0.5) !important;
    }

    /* Statistics Boxes */
    .stat-box {
        text-align: center;
        padding: 20px 10px;
        background: rgba(30, 27, 75, 0.3);
        border-radius: 16px;
        border: 1px solid rgba(139, 92, 246, 0.2);
        backdrop-filter: blur(8px);
    }
    .stat-number {
        font-size: 2.6rem;
        font-weight: 800;
        color: #f472b6;
        line-height: 1;
        margin-bottom: 2px;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #cbd5e1;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* Fun section headers */
    .section-header {
        font-size: 1.5rem; 
        font-weight: 700; 
        color: #f8fafc; 
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-sub {
        color: #94a3b8; 
        font-size: 0.95rem; 
        margin-bottom: 20px;
    }
    
    hr {
        border-color: rgba(255, 255, 255, 0.05);
        margin: 2.5rem 0;
    }
    
    /* User Profile Info */
    .avatar-lg {
        width: 60px;
        height: 60px;
        border-radius: 30px;
        background: linear-gradient(135deg, #a855f7, #3b82f6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- Colorful CSS Generators ---
def get_pill_html(text, is_match=False):
    if is_match:
        css = "background: rgba(236, 72, 153, 0.15); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.4); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 500; margin: 4px; display: inline-block; white-space: nowrap;"
    else:
        css = "background: rgba(255, 255, 255, 0.05); color: #e2e8f0; border: 1px solid rgba(255, 255, 255, 0.1); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 500; margin: 4px; display: inline-block; white-space: nowrap;"
    return f'<span style="{css}">{text.title()}</span>'

def get_avatar(name, gradient_start="#6366f1", gradient_end="#a855f7"):
    initial = name[0].upper() if name else "?"
    return f'<div style="min-width: 50px; height: 50px; border-radius: 25px; background: linear-gradient(135deg, {gradient_start}, {gradient_end}); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 700; color: white; margin-right: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); flex-shrink: 0;">{initial}</div>'

# --- Logic ---
if "current_user" not in st.session_state:
    st.session_state.current_user = None

def login_user(username: str, email: str = "", phone: str = ""):
    try:
        res = requests.post(f"{API_URL}/users/", json={"name": username, "email": email, "phone": phone})
        if res.status_code in [200, 400]:
            st.session_state.current_user = username
            st.rerun()
        else:
            st.error("Login issue. Try again.")
    except Exception:
        st.error("Cannot reach the campus server!")

@st.cache_data(ttl=2)
def fetch_data(username):
    try:
        my_res = requests.get(f"{API_URL}/users/{username}/interests/")
        all_res = requests.get(f"{API_URL}/matching/")
        if my_res.status_code == 200 and all_res.status_code == 200:
            return my_res.json(), all_res.json()
    except Exception:
        pass
    return [], {}

if not st.session_state.current_user:
    st.markdown('<br><br><br>', unsafe_allow_html=True)
    st.markdown('<div class="exclusive-title">Campus Connect</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Find your people. Build your tribe. ✨</div>', unsafe_allow_html=True)
    
    _, col2, _ = st.columns([1, 1.3, 1])
    with col2:
        with st.form("login_form"):
            st.markdown('<div style="text-align: center; color: #f8fafc; font-size: 1.2rem; margin-bottom: 25px; font-weight: 600;">Hop in. 🚀</div>', unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed", placeholder="What's your name or Student ID?")
            email = st.text_input("Email", label_visibility="collapsed", placeholder="Campus Email (e.g., alex@edu.com)")
            phone = st.text_input("Phone", label_visibility="collapsed", placeholder="Mobile Number (e.g., +1 555-0100)")
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Join the network", use_container_width=True)
            if submit:
                if username.strip():
                    login_user(username.strip(), email.strip(), phone.strip())
                else:
                    st.warning("Please tell us your name!")

else:
    # Header Section
    cols = st.columns([4, 1])
    with cols[0]:
        initial = st.session_state.current_user[0].upper()
        # STRIPPED ALL HTML INDENTATION TO FIX RENDERING BUG
        st.markdown(f"""
<div style="display: flex; align-items: center; gap: 15px;">
<div class="avatar-lg">{initial}</div>
<div>
<div style="font-size: 1.8rem; font-weight: 800; color: #f8fafc; line-height: 1;">{st.session_state.current_user}</div>
<div style="color: #a855f7; font-size: 0.9rem; font-weight: 600; margin-top: 4px;">Student Verified ✓</div>
</div>
</div>
""", unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<br>', unsafe_allow_html=True)
        if st.button("Log out"):
            st.session_state.current_user = None
            st.rerun()
            
    my_interests, all_data = fetch_data(st.session_state.current_user)
    
    my_tags_set = set([i.lower() for i in my_interests])
    matches = []
    peers = [u for u in all_data.keys() if u != st.session_state.current_user]
    
    for user in peers:
        their_data = all_data.get(user, {})
        their_tags = set([i.lower() for i in their_data.get("interests", [])])
        shared = my_tags_set.intersection(their_tags)
        if shared:
            matches.append({"user": user, "shared": list(shared), "count": len(shared)})
            
    # Fun Dashboard Widgets
    st.markdown('<br>', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{len(peers) + 1}</div><div class="stat-label">Students</div></div>', unsafe_allow_html=True)
    with sc2:
        st.markdown(f'<div class="stat-box"><div class="stat-number" style="color: #a855f7;">{len(my_interests)}</div><div class="stat-label">Your Vibes</div></div>', unsafe_allow_html=True)
    with sc3:
        st.markdown(f'<div class="stat-box"><div class="stat-number" style="color: #38bdf8;">{len(matches)}</div><div class="stat-label">Connections</div></div>', unsafe_allow_html=True)
    
    st.write("---")
    
    # About You Profile
    st.markdown("<div class='section-header'>👋 Welcome! Add your interests</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Set up your profile traits to help the matching algorithm find your peers.</div>", unsafe_allow_html=True)
    
    if my_interests:
        tags = "".join([get_pill_html(i) for i in my_interests])
        st.markdown(f'<div style="margin-bottom: 20px;">{tags}</div>', unsafe_allow_html=True)
    else:
        st.markdown("<div style='background: rgba(236,72,153,0.1); border: 1px solid rgba(236,72,153,0.3); color: #f472b6; padding: 12px 16px; border-radius: 12px; font-weight: 500; font-size: 0.9rem; margin-bottom: 20px;'>Oops! Your profile feels empty. Add some interests below to start matching!</div>", unsafe_allow_html=True)

    with st.form("add_form", clear_on_submit=True):
        col_input, col_submit = st.columns([4, 1.2])
        with col_input:
            new_interest = st.text_input("Interest", label_visibility="collapsed", placeholder="Type a hobby, major, or interest...")
        with col_submit:
            submit_btn = st.form_submit_button("Add to Profile", use_container_width=True)
            if submit_btn:
                if new_interest.strip():
                    try:
                        requests.post(f"{API_URL}/interests/", json={"user": st.session_state.current_user, "interest": new_interest.strip()})
                        time.sleep(0.05)
                        fetch_data.clear()
                        st.rerun()
                    except Exception:
                        st.error("System Error.")

    st.write("---")
    
    # Matches (The main feature)
    st.markdown("<div class='section-header'>🤝 Your Matched Peers</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Peers who share your interests. Reach out using their contact info!</div>", unsafe_allow_html=True)
    
    if matches:
        matches.sort(key=lambda x: x["count"], reverse=True)
        for idx, m in enumerate(matches):
            
            if idx == 0:
                card_bg = "linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(30, 27, 75, 0.6) 100%)"
                border = "2px solid #ec4899"
                shadow = "box-shadow: 0 10px 30px rgba(236, 72, 153, 0.2);"
                badge = "<span style='position: absolute; top: -12px; right: 20px; background: linear-gradient(135deg, #f59e0b, #ef4444); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 800; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.4); text-transform: uppercase;'>#1 Best Match 🎯</span>"
            else:
                card_bg = "rgba(15, 23, 42, 0.6)"
                border = "1px solid rgba(139, 92, 246, 0.2)"
                shadow = ""
                badge = ""
                
            shared_tags = "".join([get_pill_html(i, is_match=True) for i in m['shared']])
            avatar_html = get_avatar(m['user'], gradient_start="#ec4899" if idx==0 else "#3b82f6", gradient_end="#a855f7")
            
            user_info = all_data.get(m['user'], {})
            real_email = user_info.get("email") or "No email shared"
            real_phone = user_info.get("phone") or "No phone connected"
            
            # STRIPPED ALL HTML INDENTATION TO FIX RENDERING BUG
            html_card = f"""
<div style="background: {card_bg}; backdrop-filter: blur(10px); border: {border}; border-radius: 16px; padding: 24px; padding-bottom: 20px; margin-bottom: 20px; display: flex; flex-direction: column; position: relative; {shadow} transition: transform 0.2s ease;">
{badge}
<div style="display: flex; flex-direction: row; align-items: center; margin-bottom: 15px;">
{avatar_html}
<div style="flex: 1;">
<div style='font-size: 1.3rem; font-weight: 700; color: #f8fafc; margin-bottom: 2px;'>{m['user']}</div>
<div style='color: #a855f7; font-size: 0.85rem; font-weight: 600;'>{m['count']} shared interests</div>
</div>
<div style="flex: 1.5; text-align: right;">
{shared_tags}
</div>
</div>
<div style='display: flex; gap: 15px; font-size: 0.85rem; color: #cbd5e1; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 12px;'>
<div style='background: rgba(255,255,255,0.05); padding: 6px 12px; border-radius: 8px;'>✉️ {real_email}</div>
<div style='background: rgba(255,255,255,0.05); padding: 6px 12px; border-radius: 8px;'>📱 {real_phone}</div>
</div>
</div>
"""
            st.markdown(html_card, unsafe_allow_html=True)
    else:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.4); border: 2px dashed rgba(255,255,255,0.1); border-radius: 16px; text-align: center; padding: 40px 20px;">
<div style="font-size: 3rem; margin-bottom: 10px;">👀</div>
<div style='color: #f8fafc; font-size: 1.1rem; font-weight: 600;'>No overlaps yet!</div>
<div style='color: #94a3b8; font-size: 0.95rem; margin-top: 5px;'>Add more common hobbies to your profile to discover friends!</div>
</div>
""", unsafe_allow_html=True)
