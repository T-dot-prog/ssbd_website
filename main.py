"""
Main page for SSBD Profile verification Site
"""
import streamlit as st

def render_portal_info_card():
    """
    Renders a visually attractive information card about the SSBD Participant Portal
    using Streamlit native components with custom CSS styling.
    """

    # --- Initialize theme
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    def toggle_theme():
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

    # --- Inject global CSS (base design + toggle positioning)
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');

        .stApp {
            background-color: #ffffff;
            font-family: 'Bebas Neue', sans-serif;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        .theme-toggle {
            position: fixed;
            top: 15px;
            right: 25px;
            z-index: 9999;
            background: #f2f2f2;
            border-radius: 30px;
            padding: 5px 12px;
            cursor: pointer;
            border: 1px solid #ccc;
            font-size: 1.1rem;
            transition: background 0.3s;
        }

        .theme-toggle:hover {
            background: #ddd;
        }

        .main-card-container {
            background: #ffffff;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1),
                        0 0 0 1px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.1);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        h1, h2, h3 {
            color: #000 !important;
            font-family: 'Bebas Neue', sans-serif !important;
        }

        p, li {
            color: #000;
            font-family: 'JetBrains Mono', monospace !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Toggle button rendered top-right
    st.markdown('<div class="theme-toggle">', unsafe_allow_html=True)
    if st.button("🌙" if st.session_state.theme == "light" else "☀️", key="theme_switch"):
        toggle_theme()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Apply theme dynamically
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
            .stApp { background-color: #0E1117; color: white; }
            h1, h2, h3, p, li, strong { color: #f5f5f5 !important; }
            .main-card-container { background: #1E1E1E; box-shadow: 0 0 20px rgba(255,255,255,0.05); }
            .theme-toggle { background: #333; color: white; border-color: #555; }
            .theme-toggle:hover { background: #444; }
        </style>
        """, unsafe_allow_html=True)

    # --- Main card
    st.markdown('<div class="main-card-container">', unsafe_allow_html=True)
    st.markdown("# SSBD Participant Portal: Your Profile Verification And Certificate Download Hub")

    st.markdown("""
    <p class="intro-paragraph">
    The <strong>SSBD Participant Portal</strong> is a secure web application designed to streamline 
    administrative tasks for participants of the Student Skill/Success Battle Development initiative. 
    It acts as your central hub for instantly verifying official status and accessing essential documentation.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p class="intro-paragraph">
    Built using Streamlit, this portal provides a clean, interactive interface with all navigation 
    managed via the left sidebar. It operates entirely based on your unique <code>Participant ID</code>.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<div></div>", unsafe_allow_html= True)
    st.markdown("<div></div>", unsafe_allow_html= True)
    st.markdown("<div></div>", unsafe_allow_html= True)

    st.markdown("## Core Features and Benefits")
    st.info("### 1. Secure Profile Verification Portal\nConfirm enrollment status instantly using your Participant ID.")
    st.info("### 2. Official Certificate Download Portal\nGenerate and securely download your official digital certificates anytime.")

    st.markdown("<div></div>", unsafe_allow_html= True)
    st.markdown("<div></div>", unsafe_allow_html= True)
    st.markdown("<div></div>", unsafe_allow_html= True)
    
    st.markdown("## Step-by-Step Guide")
    st.markdown("1️⃣ **Identify Your Need:** Select the appropriate service from the sidebar.")
    st.markdown("2️⃣ **Select a Service:** Choose either *Profile Verification* or *Certificate Download.*")
    st.markdown("3️⃣ **Authenticate:** Enter your Participant ID.")
    st.markdown("4️⃣ **View or Download:** Get your verified data or certificate immediately.")

    st.markdown('</div>', unsafe_allow_html=True)


# --- Run the app
if __name__ == "__main__":
    st.set_page_config(
        page_title="SSBD Portal Info",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    render_portal_info_card()
