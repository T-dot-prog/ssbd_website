"""
Certificate Download Portion
"""

import streamlit as st 
from PIL import Image
import warnings
import io, base64

warnings.filterwarnings("ignore")

from logger import logger
from helper import helper
from utils import redis_db

def download_main(key: str):
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

            # Store into DB
            status = redis_db.save_info(key="participant_info", info=data)

            if not status:
                logger.error(f'Refuse connection from Source Site')
                st.error("A Exception occured while connecting with redis server")
            else:
                logger.info("Succesfully saved the information")
                st.success("Connection Built up sucessfully")
            
            # Load the same key we used to save (e.g., "participant_info" passed into this function)
            info: dict = redis_db.load_info(key= key)

            # Validate info is a dict before subscripting
            if not isinstance(info, dict):
                logger.error("Loaded participant info is not a dict or is None")
                st.error("No participant data available. Please try again later.")
                return

            # Data structure is column-oriented: { 'ID': {row:'id'}, 'Name ': {row:'name'}, ... }
            ids: dict = info.get('ID', {})
            names: dict = info.get('Name ', {})  # note the trailing space in column name

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

            pdfin_bytes = helper.name_to_pptx_to_pdf(name= name)


            # 5. Preview section
            if hasattr(st, "pdf"):
                # For Streamlit 1.38+
                st.pdf(pdfin_bytes)
            else:
                # Fallback for older versions
                st.markdown(
                    f'<iframe src="data:application/pdf;base64,{pdfin_bytes.hex()}" width="700" height="500"></iframe>',
                    unsafe_allow_html=True
                )

            col1, col2, col3 = st.columns([1,2,1])

            with col2:
                st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
                st.download_button(
                    "Download Certificate",
                    data=pdfin_bytes,
                    file_name="sample.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)



if __name__ == '__main__':
    download_main(key= "participant_info")