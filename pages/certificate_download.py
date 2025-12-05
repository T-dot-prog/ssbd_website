"""
Certificate Download Portion
"""

import streamlit as st 
from PIL import Image
import warnings
import io, base64

warnings.filterwarnings("ignore")

from logger import logger
from helper import helper, initialize_theme, is_dark_theme, get_dark_theme_css, get_light_theme_css, render_theme_toggle
from config import config


def download_main():
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
    in_profile_view = st.session_state.get("certificate_download", False)

    if not in_profile_view:
        # Header with logo and title
        st.markdown(f"""
        <div class="header-container" style="display: flex; align-items: center; gap: 3rem;">
            <div style="flex: 0 0 200px;">
                <img src="data:image/png;base64,{img_str}" width="200" style="border-radius: 20px; box-shadow: 0 20px 60px rgba(100, 181, 246, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.3); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            </div>
            <div style="flex: 1; display: flex; align-items: center; justify-content: center;">
                <h1 class="brand-title">CERTIFICATE DOWNLOAD PORTAL</h1>
            </div>
        </div>
        """, unsafe_allow_html=True)

        logger.info("Certificate Download Page sucessfully loaded")

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
                submit_button = st.button("🔍 SUBMIT", use_container_width=True)
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
                logger.error(f'Data is not a dict: {data}')
                st.error('Internal data format error. Please try again later.')
                return
            else:
                logger.info("Data loaded successfully")
                st.success("Data loaded successfully")

           

            # Data structure is column-oriented: { 'ID': {row:'id'}, 'Name ': {row:'name'}, ... }
            ids: dict = data.get( config.KEY_STR, {})
            names: dict = data.get( config.OTHER_INFO[0], {})

            if not isinstance(ids, dict) or not ids:
                logger.error('ID column missing or invalid in info')
                st.error('Internal data format error: ID column missing.')
                return

            if not isinstance(names, dict) or not names:
                logger.error('Name column missing or invalid in info')
                st.error('Internal data format error: Name column missing.')
                return

            # Find row index for this participant_id
            index_number = None
            for row_idx, id_val in ids.items():
                if participant_id == id_val:
                    index_number = row_idx
                    logger.debug(f'Found matching row index: {index_number} for participant_id: {participant_id}')
                    break

            if index_number is None:
                logger.warning('Participant ID not found')
                st.error('Participant ID not found. Please check your ID and try again.')
                return

            st.success('Verification successful!')

            # Fetch name using the same row index
            name = names.get(index_number)
            if isinstance(name, str) and name.strip():
                logger.debug(f"Name found: {name}")
                st.success(f"Name Found for id: {participant_id} with the name: {name}")
            else:
                logger.error('Name not found for the matched row index')
                st.error('Could not determine participant name from records.')

            pdfin_bytes = helper.name_to_pdf(_id = id_val)

            # Show preview first
            st.subheader("Certificate Preview")
            st.pdf(pdfin_bytes)

            st.markdown("<br>", unsafe_allow_html=True)

            # Then download button (without triggering another preview)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.download_button(
                    "📥 Download Certificate",
                    data=pdfin_bytes,
                    file_name=f"certificate_{participant_id}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )



if __name__ == '__main__':
    download_main()