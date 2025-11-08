"""
Verification Site portal
"""
import streamlit as st
from PIL import Image
import io, base64
import warnings

warnings.filterwarnings("ignore")

from logger import logger
from config import config
from helper import helper
from utils import redis_db


def main(key: str):
    # Glossy Theme Custom CSS
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600&display=swap');
        
        * {
            margin: 0;
            padding: 0;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .main {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 25%, #2d1b4e 50%, #1a1f3a 75%, #0a0e27 100%);
            min-height: 100vh;
            padding: 0;
            position: relative;
            overflow: hidden;
        }
        
        .main::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 50%, rgba(100, 181, 246, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(129, 199, 132, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }
        
        .block-container {
            padding-top: 0;
            padding-bottom: 2rem;
            max-width: 100%;
            color: white;
            position: relative;
            z-index: 1;
        }
        
        .brand-title {
            font-family: "Bebas Neue", cursive;
            font-weight: 400;
            font-size: 3rem;
            color: #64b5f6;
            letter-spacing: 1px;
            margin: 0;
            text-transform: uppercase;
            text-shadow: 0 0 20px rgba(100, 181, 246, 0.3);
        }
        
        .header-container {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.08) 100%);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 30px;
            padding: 2.5rem 3rem;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 1px rgba(255, 255, 255, 0.3),
                inset 0 -1px 1px rgba(0, 0, 0, 0.2);
            margin: 1.5rem;
            position: relative;
            overflow: hidden;
        }
        
        .header-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
            animation: glossShine 3s infinite;
        }
        
        @keyframes glossShine {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        /* Input Card Styling */
        .input-card {
            background: linear-gradient(135deg, rgba(100, 181, 246, 0.15) 0%, rgba(129, 199, 132, 0.1) 100%);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 2px solid rgba(100, 181, 246, 0.3);
            border-radius: 25px;
            padding: 2.5rem;
            margin: 2rem 1.5rem;
            box-shadow: 
                0 10px 40px rgba(100, 181, 246, 0.2),
                inset 0 1px 2px rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .input-card:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 15px 50px rgba(100, 181, 246, 0.3),
                inset 0 1px 2px rgba(255, 255, 255, 0.3);
        }
        
        .input-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s ease;
        }
        
        .input-card:hover::before {
            left: 100%;
        }
        
        .input-label {
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: #64b5f6;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 0 2px 10px rgba(100, 181, 246, 0.3);
        }
        
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 2px solid rgba(100, 181, 246, 0.4) !important;
            border-radius: 15px !important;
            color: white !important;
            font-size: 1.1rem !important;
            padding: 1rem 1.5rem !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease !important;
            box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.2) !important;
        }
        
        .stTextInput > div > div > input:focus {
            background: rgba(255, 255, 255, 0.15) !important;
            border: 2px solid rgba(100, 181, 246, 0.8) !important;
            box-shadow: 
                inset 0 2px 10px rgba(0, 0, 0, 0.2),
                0 0 20px rgba(100, 181, 246, 0.4) !important;
            outline: none !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.5) !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #64b5f6 0%, #81c784 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 15px !important;
            padding: 1rem 3rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 
                0 8px 25px rgba(100, 181, 246, 0.4),
                inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 
                0 12px 35px rgba(100, 181, 246, 0.5),
                inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
        }
        
        .stButton > button:active {
            transform: translateY(-1px) !important;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        /* Icon styling */
        .icon-container {
            display: inline-block;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, rgba(100, 181, 246, 0.3), rgba(129, 199, 132, 0.3));
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
            box-shadow: 0 5px 15px rgba(100, 181, 246, 0.3);
        }
       
    </style>
    """, unsafe_allow_html=True)

    # Load logo
    logo_img = helper.load_logo()
    pil_img = Image.fromarray(logo_img)

    # Convert logo to base64 for embedding
    buffered = io.BytesIO()
    pil_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Determine profile view state
    in_profile_view = st.session_state.get("profile_view", False)

    if not in_profile_view:
        # Header with logo and title
        st.markdown(f"""
        <div class="header-container" style="display: flex; align-items: center; gap: 3rem;">
            <div style="flex: 0 0 200px;">
                <img src="data:image/png;base64,{img_str}" width="200" style="border-radius: 20px; box-shadow: 0 20px 60px rgba(100, 181, 246, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.3); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            </div>
            <div style="flex: 1; display: flex; align-items: center; justify-content: center;">
                <h1 class="brand-title">PROFILE VERIFICATION PORTAL</h1>
            </div>
        </div>
        """, unsafe_allow_html=True)

        logger.info("Verification Page sucessfully loaded")

        # Input Card Section
        st.markdown("""
        <div class="input-card">
            <div class="icon-container">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#64b5f6" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
            <div class="input-label">Enter Participant ID</div>
        </div>
        """, unsafe_allow_html=True)

        # Create input field
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            participant_id = st.text_input(
                "",
                placeholder="Enter your unique ID...",
                key="participant_id",
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Center the button
            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
            with btn_col2:
                submit_button = st.button("🔍 VERIFY", use_container_width=True)
    else:
        participant_id = st.session_state.get("participant_id_value")
        submit_button = False

    # Handle submission
    if (not in_profile_view and submit_button and participant_id) or in_profile_view:
        with st.spinner("Verifying..."):
            logger.info(f"Verifying participant ID: {participant_id}")
            
            # Load data in json format
            data = helper.convert_into_dict()

            # Store into DB
            status = redis_db.save_info(key="participant_info", info=data)

            if not status:
                logger.error(f'Refuse connection from Source Site')
                st.error("A Exception occured while connecting with redis server")
            else:
                logger.info("Succesfully saved the information")
                st.success("Connection Built up sucessfully")

            info: dict = redis_db.load_info(key=key)

            logger.info(f'Info section: {info}')

            id_columns: dict = info[config.KEY_STR]
            other_columns = config.OTHER_INFO

            index_number = None
            for key, value in id_columns.items():
                if participant_id == value:
                    logger.debug(f'Found matching key: {key}')
                    st.success("Verification successful!")
                    index_number = key
                    break

            if index_number is None:
                st.error("No matching record found")
            else:
                
                try:
                    name_map = info[other_columns[0]]
                    email_map = info[other_columns[1]]
                except Exception as e:
                    logger.exception(f"Failed to access name/email from info using OTHER_INFO keys {e}")
                    st.error("Internal error while accessing profile details")
                else:
                    # If data is stored as dicts keyed by index_number
                    if isinstance(name_map, dict) and isinstance(email_map, dict):
                        name_val = name_map.get(index_number)
                        email_val = email_map.get(index_number)
                    else:
                        # Fallback: treat as lists where index_number is an integer-like key
                        try:
                            idx = int(index_number)
                            name_val = name_map[idx]
                            email_val = email_map[idx]
                        except Exception:
                            name_val = None
                            email_val = None

                    if name_val is None and email_val is None:
                        st.error("Profile details not found for the matched record")
                    else:
                        # Prepare additional info
                        course_name = "ANSYS Fluent Course (CFD & Heat Transfer)"
                        course_duration = "17th October,2025 to 13th November,2025"
                        total_session = 12
                        participant_display_id = participant_id

                        # Attempt to load an avatar/profile image via helper if available; otherwise fallback to logo
                        avatar_b64 = None
                        profile_picture_map = info.get('Profile_picture')
                        if profile_picture_map:
                            profile_picture_url = profile_picture_map.get(index_number)
                            if profile_picture_url and isinstance(profile_picture_url, str):
                                try:
                                    # Extract ID from 'https://drive.google.com/open?id=...'
                                    image_id = profile_picture_url.split('id=')[-1]
                                    image_bytes = helper.drivelink_to_image(image_id)
                                    avatar_pil = Image.open(io.BytesIO(image_bytes))
                                    avatar_buffer = io.BytesIO()
                                    avatar_pil.save(avatar_buffer, format="PNG")
                                    avatar_b64 = base64.b64encode(avatar_buffer.getvalue()).decode()
                                except Exception as e:
                                    logger.error(f"Failed to load profile picture from google drive: {e}")
                                    avatar_b64 = None

                        if avatar_b64 is None:
                            # Fallback to logo
                            avatar_img_np = helper.load_logo()
                            avatar_pil = Image.fromarray(avatar_img_np)
                            avatar_buffer = io.BytesIO()
                            avatar_pil.save(avatar_buffer, format="PNG")
                            avatar_b64 = base64.b64encode(avatar_buffer.getvalue()).decode()

                        # Card layout using columns and custom HTML
                        st.markdown(
                            f"""
                            <style>
                                .profile-card {{
                                    background: linear-gradient(135deg, rgba(100, 181, 246, 0.15) 0%, rgba(129, 199, 132, 0.1) 100%);
                                    backdrop-filter: blur(20px);
                                    -webkit-backdrop-filter: blur(20px);
                                    border: 2px solid rgba(100, 181, 246, 0.3);
                                    border-radius: 24px;
                                    padding: 1.5rem;
                                    margin: 1rem 0 2rem 0;
                                    box-shadow: 0 10px 40px rgba(100, 181, 246, 0.2), inset 0 1px 2px rgba(255, 255, 255, 0.2);
                                }}
                                .profile-grid {{
                                    display: grid;
                                    grid-template-columns: 160px 1fr;
                                    gap: 1.5rem;
                                    align-items: center;
                                }}
                                .avatar-wrap {{
                                    width: 160px;
                                    height: 160px;
                                    border-radius: 20px;
                                    overflow: hidden;
                                    background: rgba(255,255,255,0.08);
                                    border: 1px solid rgba(255,255,255,0.2);
                                    box-shadow: 0 8px 24px rgba(0,0,0,0.35);
                                }}
                                .avatar-img {{
                                    width: 100%;
                                    height: 100%;
                                    object-fit: cover;
                                }}
                                .detail-row {{
                                    display: grid;
                                    grid-template-columns: 180px 1fr;
                                    gap: 0.75rem;
                                    margin: 0.25rem 0;
                                }}
                                .label {{
                                    font-family: 'Inter', sans-serif;
                                    color: #9ecbff;
                                    font-weight: 600;
                                    letter-spacing: 0.5px;
                                    text-transform: uppercase;
                                    font-size: 0.85rem;
                                }}
                                .value {{
                                    font-family: 'Inter', sans-serif;
                                    color: #ffffff;
                                    font-weight: 600;
                                    font-size: 1.05rem;
                                }}
                            </style>
                            <div class="profile-card">
                                <div class="profile-grid">
                                    <div class="avatar-wrap">
                                        <img class="avatar-img" src="data:image/png;base64,{avatar_b64}" alt="avatar" />
                                    </div>
                                    <div>
                                        <div class="detail-row"><div class="label">Name</div><div class="value">{name_val if name_val is not None else '-'}
                                        </div></div>
                                        <div class="detail-row"><div class="label">Email</div><div class="value">{email_val if email_val is not None else '-'}
                                        </div></div>
                                        <div class="detail-row"><div class="label">Participant ID</div><div class="value">{participant_display_id}</div></div>
                                        <div class="detail-row"><div class="label">Participated Course</div><div class="value">{course_name}</div></div>
                                        <div class="detail-row"><div class="label">Course Duration</div><div class="value">{course_duration}</div></div>
                                        <div class="detail-row"><div class="label">Total Sessions</div><div class="value">{total_session}</div></div>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

if __name__ == "__main__":
    main(key="participant_info")