"""
Verification Site portal
"""
import streamlit as st
from PIL import Image
import requests
import io, base64
import warnings

warnings.filterwarnings("ignore")

from logger import logger
from config import config
from helper import helper, initialize_theme, is_dark_theme, get_dark_theme_css, get_light_theme_css, render_theme_toggle


def main():
    # Initialize theme
    initialize_theme()
    
    # Glossy Theme Custom CSS
    st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Apply theme CSS
    if is_dark_theme():
        st.markdown(get_dark_theme_css(), unsafe_allow_html=True)
    else:
        st.markdown(get_light_theme_css(), unsafe_allow_html=True)
    
    # Render theme toggle
    render_theme_toggle()

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

            if not (data and isinstance(data, dict)):
                logger.error(f'Data is not in valid format: {data}')
                st.error("Problem loading data. Please try again later")
            else:
                logger.info("Data is formatted correctly")
                st.success("Data loaded Sucessfully")

            id_columns: dict = data.get(config.KEY_STR)
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
                    name_map = data[other_columns[0]]
                    email_map = data[other_columns[1]]
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
                        course_duration = "20th January, 2026 to 20th February, 2026"
                        total_session = 12
                        participant_display_id = participant_id

                        # Attempt to load an avatar/profile image via helper if available; otherwise fallback to logo
                        avatar_b64 = None
                        profile_picture_map = data.get('Formal Photo')
                        if profile_picture_map:
                            profile_picture_url = profile_picture_map.get(index_number)
                            if profile_picture_url and isinstance(profile_picture_url, str):
                                try:
                                    # Convert Drive share link to direct download link
                                    profile_picture_url = helper.convert_drive_url(profile_picture_url)
                                    # Fetch image
                                    avatar_pil = Image.open(io.BytesIO(requests.get(profile_picture_url, allow_redirects=True).content))
                                    avatar_buffer = io.BytesIO()
                                    avatar_pil.save(avatar_buffer, format="PNG")
                                    avatar_b64 = base64.b64encode(avatar_buffer.getvalue()).decode()
                                except Exception as e:
                                    logger.error(f"Failed to load profile picture from image link: {e}")
                                    avatar_b64 = None

                        if avatar_b64 is None:
                            # Fallback to logo
                            avatar_img_np = helper.load_logo()
                            avatar_pil = Image.fromarray(avatar_img_np)  # FIX: was Image(avatar_img_np)
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
                                    font-family: 'Times New Roman', Times, serif;
                                    color: #9ecbff;
                                    font-weight: 600;
                                    letter-spacing: 0.5px;
                                    text-transform: uppercase;
                                    font-size: 0.85rem;
                                }}
                                .value {{
                                    font-family: 'Times New Roman', Times, serif;
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
                            unsafe_allow_html=True,  # FIX: was unsafe_follow_html
                        )

if __name__ == "__main__":
    main()