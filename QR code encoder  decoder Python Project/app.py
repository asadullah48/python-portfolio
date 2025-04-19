import streamlit as st
from PIL import Image
import qrcode
import cv2
import numpy as np
import os
import io
import base64
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="QR Code Generator & Scanner",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve appearance
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E88E5;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #333;
            margin-top: 2rem;
        }
        .success-msg {
            color: #4CAF50;
            font-weight: bold;
        }
        .stButton>button {
            background-color: #1E88E5;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }
        .footer {
            text-align: center;
            margin-top: 3rem;
            font-size: 0.8rem;
            color: #666;
        }
    </style>
    <h1 class="main-header">🔍 QR Code Generator & Scanner</h1>
""", unsafe_allow_html=True)

# Create directory for saving QR codes if it doesn't exist
if not os.path.exists("generated_qr_codes"):
    os.makedirs("generated_qr_codes")

def generate_download_link(img, filename, text):
    """Generate a download link for a PIL image"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def generate_qr_code(data, box_size=10, border=4, fill_color="black", back_color="white"):
    """Generate QR code with custom parameters"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_qr_codes/qr_code_{timestamp}.png"
    
    # Save the image
    img.save(filename)
    
    return img, filename

def scan_qr_code(image):
    """Scan QR code from uploaded image"""
    # Convert PIL Image to numpy array for OpenCV
    if isinstance(image, Image.Image):
        image = np.array(image.convert('RGB'))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Create QR code detector
    detector = cv2.QRCodeDetector()
    
    # Detect and decode
    try:
        data, bbox, _ = detector.detectAndDecode(image)
        if data:
            return True, data
        return False, "No QR code found in the image."
    except Exception as e:
        return False, f"Error scanning QR code: {str(e)}"

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose a mode:", ["Generate QR Code", "Scan QR Code"])

# About section in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This app allows you to generate custom QR codes and scan existing ones. "
    "Built with Streamlit, OpenCV, and qrcode libraries."
)
st.sidebar.markdown("### Developer")
st.sidebar.info(
    "Created by [Asadullah](https://github.com/asadullah48)"
)

# Generate QR Code Page
if app_mode == "Generate QR Code":
    st.markdown('<h2 class="sub-header">✨ Generate QR Code</h2>', unsafe_allow_html=True)
    
    # Input text or URL
    data = st.text_area("Enter text or URL:", height=100)
    
    # QR code customization options
    st.markdown("### Customize Your QR Code")
    col1, col2 = st.columns(2)
    
    with col1:
        box_size = st.slider("Box Size:", 5, 20, 10)
        border = st.slider("Border Size:", 1, 10, 4)
    
    with col2:
        fill_color = st.color_picker("QR Code Color:", "#000000")
        back_color = st.color_picker("Background Color:", "#FFFFFF")
    
    # Generate button
    if st.button("Generate QR Code", key="generate"):
        if data:
            # Generate QR code
            img, filename = generate_qr_code(data, box_size, border, fill_color, back_color)
            
            # Display generated QR code
            st.image(img, caption="Generated QR Code", use_column_width=True)
            
            # Create download link
            st.markdown(
                generate_download_link(img, os.path.basename(filename), "📥 Download QR Code"),
                unsafe_allow_html=True
            )
            
            # Show success message
            st.markdown(f'<p class="success-msg">✅ QR code successfully generated!</p>', unsafe_allow_html=True)
            
            # Display the encoded data
            st.write("**Encoded Data:**")
            st.code(data)
        else:
            st.error("⚠️ Please enter some text or URL to generate a QR code.")

# Scan QR Code Page
else:
    st.markdown('<h2 class="sub-header">🔎 Scan QR Code</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload QR Code Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Scan button
        if st.button("Scan QR Code"):
            # Process the image
            success, result = scan_qr_code(image)
            
            if success:
                st.markdown(f'<p class="success-msg">✅ QR code successfully scanned!</p>', unsafe_allow_html=True)
                st.write("**Decoded Data:**")
                
                # Check if result is a URL
                if result.startswith(('http://', 'https://')):
                    st.markdown(f"[{result}]({result})")
                else:
                    st.code(result)
                
                # Copy button
                st.text_area("Copy this data:", value=result, height=100)
            else:
                st.error(f"⚠️ {result}")

# Footer
st.markdown("""
    <div class="footer">
        Developed with ❤️ by Asadullah | <a href="https://github.com/asadullah48">GitHub</a>
    </div>
""", unsafe_allow_html=True)