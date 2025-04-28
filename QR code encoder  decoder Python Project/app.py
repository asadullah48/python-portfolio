import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import qrcode
import cv2
import numpy as np
import os
import io
import base64
import time
import uuid
from datetime import datetime
import json
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="QR Code Generator & Scanner",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve appearance with gradient background and modern styling
st.markdown("""
    <style>
        /* Main background with gradient */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }

        /* Card styling */
        .css-1r6slb0, .css-1vq4p4l, .css-18e3th9 {
            background-color: rgba(255, 255, 255, 0.8) !important;
            border-radius: 10px !important;
            padding: 1rem !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
            backdrop-filter: blur(10px) !important;
        }

        /* Headers */
        .main-header {
            font-size: 2.8rem;
            background: linear-gradient(90deg, #1E88E5, #5E35B1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        .sub-header {
            font-size: 1.8rem;
            color: #333;
            margin-top: 2rem;
            margin-bottom: 1.5rem;
            font-weight: 600;
        }

        /* Success message */
        .success-msg {
            color: #4CAF50;
            font-weight: bold;
            padding: 0.5rem;
            border-radius: 5px;
            background-color: rgba(76, 175, 80, 0.1);
            border-left: 4px solid #4CAF50;
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #1E88E5, #5E35B1);
            color: white;
            font-weight: bold;
            padding: 0.6rem 1.2rem;
            border-radius: 50px;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 3rem;
            font-size: 0.9rem;
            color: #555;
            padding: 1rem;
            border-top: 1px solid rgba(0, 0, 0, 0.1);
        }

        /* Input fields */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius: 5px;
            border: 1px solid #ddd;
            padding: 0.5rem;
        }

        /* File uploader */
        .stFileUploader>div>button {
            background: linear-gradient(90deg, #1E88E5, #5E35B1);
            color: white;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: rgba(255, 255, 255, 0.5);
            border-radius: 5px 5px 0 0;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
        }

        .stTabs [aria-selected="true"] {
            background-color: rgba(255, 255, 255, 0.9);
            border-bottom: 2px solid #1E88E5;
        }

        /* Animation for cards */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .animated-card {
            animation: fadeIn 0.5s ease-out forwards;
        }

        /* Gallery styling */
        .gallery-item {
            transition: all 0.3s ease;
            border-radius: 10px;
            overflow: hidden;
        }

        .gallery-item:hover {
            transform: scale(1.03);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }

        /* Tooltip styling */
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
        }

        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>

    <div class="animated-card">
        <h1 class="main-header">🔍 QR Code Studio Pro</h1>
    </div>
""", unsafe_allow_html=True)

# Create directory for saving QR codes if it doesn't exist
if not os.path.exists("generated_qr_codes"):
    os.makedirs("generated_qr_codes")

def generate_download_link(img, filename, text, file_format="PNG"):
    """Generate a download link for a PIL image with specified format"""
    buffered = io.BytesIO()
    img.save(buffered, format=file_format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    mime_type = f"image/{file_format.lower()}" if file_format != "PDF" else "application/pdf"
    href = f'<a href="data:{mime_type};base64,{img_str}" download="{filename}" class="download-link">{text}</a>'
    return href

def save_qr_history(data, filename, qr_type="standard"):
    """Save QR code generation history to a JSON file"""
    history_file = Path("generated_qr_codes/history.json")

    # Create history entry
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "data": data,
        "filename": filename,
        "type": qr_type
    }

    # Load existing history or create new
    if history_file.exists():
        with open(history_file, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = {"qr_codes": []}
    else:
        history = {"qr_codes": []}

    # Add new entry and save
    history["qr_codes"].insert(0, entry)  # Add to beginning for newest first

    # Keep only the last 50 entries
    history["qr_codes"] = history["qr_codes"][:50]

    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

    return entry["id"]

def load_qr_history():
    """Load QR code generation history from JSON file"""
    history_file = Path("generated_qr_codes/history.json")

    if history_file.exists():
        with open(history_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"qr_codes": []}
    else:
        return {"qr_codes": []}

def apply_qr_style(qr_img, style="standard", corner_radius=30):
    """Apply styling to QR code image"""
    if style == "standard":
        return qr_img

    # Convert to RGBA if not already
    if qr_img.mode != 'RGBA':
        qr_img = qr_img.convert('RGBA')

    if style == "rounded":
        # Create rounded corners
        mask = Image.new('L', qr_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), qr_img.size], corner_radius, fill=255)

        # Apply mask
        result = Image.new('RGBA', qr_img.size, (255, 255, 255, 0))
        result.paste(qr_img, (0, 0), mask)
        return result

    elif style == "circular":
        # Create circular mask
        mask = Image.new('L', qr_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + qr_img.size, fill=255)

        # Apply mask
        result = Image.new('RGBA', qr_img.size, (255, 255, 255, 0))
        result.paste(qr_img, (0, 0), mask)
        return result

    return qr_img

def add_logo_to_qr(qr_img, logo_path, logo_size_factor=0.25):
    """Add a logo to the center of QR code"""
    # Open logo image
    try:
        logo = Image.open(logo_path)

        # Calculate logo size (25% of QR code by default)
        qr_width, qr_height = qr_img.size
        logo_size = int(min(qr_width, qr_height) * logo_size_factor)

        # Resize logo
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        # Calculate position to place logo at center
        position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

        # Convert QR to RGBA if it's not
        if qr_img.mode != 'RGBA':
            qr_img = qr_img.convert('RGBA')

        # Create a mask for rounded logo
        mask = Image.new('L', logo.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, logo_size, logo_size), fill=255)

        # Apply the mask to the logo
        logo = logo.convert('RGBA')

        # Paste the logo onto the QR code
        qr_img.paste(logo, position, mask)

        return qr_img
    except Exception as e:
        st.error(f"Error adding logo: {str(e)}")
        return qr_img

def generate_qr_code(data, box_size=10, border=4, fill_color="black", back_color="white",
                    style="standard", corner_radius=30, logo_path=None, logo_size_factor=0.25):
    """Generate QR code with custom parameters and styling"""
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo
        box_size=box_size,
        border=border
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create QR code image
    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    # Apply styling
    img = apply_qr_style(img, style, corner_radius)

    # Add logo if provided
    if logo_path:
        img = add_logo_to_qr(img, logo_path, logo_size_factor)

    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_qr_codes/qr_code_{timestamp}.png"

    # Save the image
    img.save(filename)

    # Save to history
    qr_type = "standard"
    if style != "standard":
        qr_type = style
    if logo_path:
        qr_type += "_with_logo"

    save_qr_history(data, filename, qr_type)

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

        # If data is found, return it
        if data:
            return True, data, bbox

        # Try with ZBar if OpenCV fails (more robust for some QR codes)
        try:
            from pyzbar.pyzbar import decode
            decoded_objects = decode(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if decoded_objects:
                for obj in decoded_objects:
                    if obj.type == 'QRCODE':
                        return True, obj.data.decode('utf-8'), None
        except ImportError:
            # pyzbar not installed, continue with OpenCV only
            pass

        return False, "No QR code found in the image.", None
    except Exception as e:
        return False, f"Error scanning QR code: {str(e)}", None

def visualize_qr_detection(image, bbox):
    """Visualize the detected QR code by drawing a bounding box"""
    if bbox is None:
        return image

    # Convert PIL Image to numpy array for OpenCV if needed
    if isinstance(image, Image.Image):
        image_cv = np.array(image.convert('RGB'))
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)
    else:
        image_cv = image.copy()

    # Draw bounding box
    bbox = bbox.astype(int)
    n = len(bbox[0])

    for i in range(n):
        # Draw lines between points
        cv2.line(image_cv,
                tuple(bbox[0][i]),
                tuple(bbox[0][(i+1) % n]),
                (0, 255, 0), 3)

    # Convert back to PIL for Streamlit
    image_pil = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
    return image_pil

def capture_from_webcam():
    """Capture image from webcam for QR code scanning"""
    # Create a placeholder for the webcam feed
    webcam_placeholder = st.empty()

    # Add a stop button
    stop_button_col, status_col = st.columns([1, 3])
    stop_button = stop_button_col.button("Stop Camera")
    status_text = status_col.empty()

    # Try to access the webcam
    try:
        # Initialize webcam
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Could not access webcam. Please make sure it's connected and not being used by another application.")
            return None

        # QR code detector
        detector = cv2.QRCodeDetector()

        # For tracking when a QR code was last detected
        last_detection_time = 0
        detected_data = None
        detection_confirmed = False

        while not stop_button:
            # Read frame from webcam
            ret, frame = cap.read()

            if not ret:
                status_text.error("Failed to capture image from webcam")
                break

            # Convert to RGB for display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Try to detect QR code
            try:
                data, bbox, _ = detector.detectAndDecode(frame)

                current_time = time.time()

                # If QR code is detected
                if data:
                    # Draw green rectangle around QR code
                    if bbox is not None:
                        # Convert to integer points
                        bbox = bbox.astype(int)
                        n = len(bbox[0])

                        for i in range(n):
                            # Draw lines between points (green)
                            cv2.line(frame_rgb,
                                    tuple(bbox[0][i]),
                                    tuple(bbox[0][(i+1) % n]),
                                    (0, 255, 0), 3)

                    # Show detected data
                    cv2.putText(frame_rgb, "QR Code Detected", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # If this is a new detection or the same code has been detected for a while
                    if detected_data != data:
                        detected_data = data
                        last_detection_time = current_time
                    elif current_time - last_detection_time > 1.5:  # Confirm after 1.5 seconds of stable detection
                        detection_confirmed = True
                        break

                # Display the frame
                webcam_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

                # Update status
                if detected_data:
                    remaining = max(0, 1.5 - (current_time - last_detection_time))
                    status_text.info(f"QR Code detected! Confirming in {remaining:.1f}s... Hold steady.")
                else:
                    status_text.info("Point camera at a QR code")

            except Exception as e:
                status_text.error(f"Error: {str(e)}")

            # Check if stop button was pressed
            if stop_button:
                break

        # Release webcam
        cap.release()

        # Return the detected data if confirmed
        if detection_confirmed and detected_data:
            return detected_data

        return None

    except Exception as e:
        st.error(f"Error accessing webcam: {str(e)}")
        return None

# Sidebar for navigation
with st.sidebar:
    st.title("QR Code Studio Pro")

    # App modes
    st.header("Navigation")
    app_mode = st.radio("", ["Generate QR Code", "Scan QR Code", "QR Gallery", "Batch Generator"])

    # About section in sidebar
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("""
    - ✨ Custom QR code generation
    - 🎨 Multiple styling options
    - 🖼️ Logo embedding
    - 📷 Webcam scanning
    - 📊 QR code history
    - 📦 Batch generation
    """)

    st.markdown("---")
    st.markdown("### About")
    st.info(
        "This app allows you to generate custom QR codes and scan existing ones. "
        "Built with Streamlit, OpenCV, and qrcode libraries."
    )
    st.markdown("### Developer")
    st.info(
        "Created by [Asadullah](https://github.com/asadullah48)"
    )

# Generate QR Code Page
if app_mode == "Generate QR Code":
    st.markdown('<div class="animated-card"><h2 class="sub-header">✨ Generate QR Code</h2></div>', unsafe_allow_html=True)

    # Create tabs for different QR code types
    tabs = st.tabs(["Standard QR", "Styled QR", "QR with Logo"])

    # Input text or URL (shared across tabs)
    data = st.text_area("Enter text or URL:", height=100,
                        help="Enter the text or URL you want to encode in the QR code")

    # Tab 1: Standard QR Code
    with tabs[0]:
        st.markdown("### Basic Customization")
        col1, col2 = st.columns(2)

        with col1:
            box_size = st.slider("Box Size:", 5, 20, 10,
                                help="Controls the size of each box in the QR code",
                                key="standard_box_size")
            border = st.slider("Border Size:", 1, 10, 4,
                              help="Controls the size of the border around the QR code",
                              key="standard_border")

        with col2:
            fill_color = st.color_picker("QR Code Color:", "#000000", key="standard_fill_color")
            back_color = st.color_picker("Background Color:", "#FFFFFF", key="standard_back_color")

        # Generate button
        if st.button("Generate Standard QR Code", key="generate_standard"):
            if data:
                with st.spinner("Generating QR code..."):
                    # Generate QR code
                    img, filename = generate_qr_code(data, box_size, border, fill_color, back_color)

                    # Create columns for display and download options
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        # Display generated QR code
                        st.image(img, caption="Generated QR Code", use_column_width=True)

                    with col2:
                        st.markdown("### Download Options")
                        # Create download links for different formats
                        st.markdown(
                            generate_download_link(img, os.path.basename(filename), "📥 Download PNG"),
                            unsafe_allow_html=True
                        )

                        # Display the encoded data
                        st.markdown("### Encoded Data")
                        if len(data) > 100:
                            st.code(data[:100] + "...")
                        else:
                            st.code(data)

                # Show success message
                st.markdown(f'<p class="success-msg">✅ QR code successfully generated!</p>', unsafe_allow_html=True)
            else:
                st.error("⚠️ Please enter some text or URL to generate a QR code.")

    # Tab 2: Styled QR Code
    with tabs[1]:
        st.markdown("### Style Options")

        col1, col2 = st.columns(2)

        with col1:
            style = st.selectbox("QR Style:", ["standard", "rounded", "circular"],
                                help="Choose the style of your QR code",
                                key="styled_style")
            corner_radius = st.slider("Corner Radius:", 10, 50, 30,
                                     help="Controls the roundness of corners (for rounded style)",
                                     key="styled_corner_radius")

        with col2:
            fill_color_styled = st.color_picker("QR Code Color:", "#1E88E5", key="styled_fill_color")
            back_color_styled = st.color_picker("Background Color:", "#FFFFFF", key="styled_back_color")

        # Generate button
        if st.button("Generate Styled QR Code", key="generate_styled"):
            if data:
                with st.spinner("Generating styled QR code..."):
                    # Generate QR code with styling
                    img, filename = generate_qr_code(
                        data, 10, 4, fill_color_styled, back_color_styled,
                        style=style, corner_radius=corner_radius
                    )

                    # Create columns for display and download options
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        # Display generated QR code
                        st.image(img, caption=f"{style.title()} QR Code", use_column_width=True)

                    with col2:
                        st.markdown("### Download Options")
                        # Create download links for different formats
                        st.markdown(
                            generate_download_link(img, os.path.basename(filename), "📥 Download PNG"),
                            unsafe_allow_html=True
                        )

                        # Display the encoded data
                        st.markdown("### Encoded Data")
                        if len(data) > 100:
                            st.code(data[:100] + "...")
                        else:
                            st.code(data)

                # Show success message
                st.markdown(f'<p class="success-msg">✅ Styled QR code successfully generated!</p>', unsafe_allow_html=True)
            else:
                st.error("⚠️ Please enter some text or URL to generate a QR code.")

    # Tab 3: QR with Logo
    with tabs[2]:
        st.markdown("### Logo Options")

        # Logo upload
        uploaded_logo = st.file_uploader("Upload Logo (PNG or JPG)", type=["png", "jpg", "jpeg"])

        col1, col2 = st.columns(2)

        with col1:
            logo_size = st.slider("Logo Size:", 10, 40, 25,
                                 help="Logo size as percentage of QR code",
                                 key="logo_size")
            style_with_logo = st.selectbox("QR Style:", ["standard", "rounded", "circular"],
                                          help="Choose the style of your QR code",
                                          key="logo_style")

        with col2:
            fill_color_logo = st.color_picker("QR Code Color:", "#000000", key="logo_fill_color")
            back_color_logo = st.color_picker("Background Color:", "#FFFFFF", key="logo_back_color")

        # Warning about logo
        st.info("⚠️ Adding a logo may reduce QR code readability. Test the QR code after generation.")

        # Generate button
        if st.button("Generate QR Code with Logo", key="generate_logo"):
            if data:
                if uploaded_logo is not None:
                    with st.spinner("Generating QR code with logo..."):
                        # Save the uploaded logo temporarily
                        temp_logo_path = f"generated_qr_codes/temp_logo_{uuid.uuid4()}.png"
                        with open(temp_logo_path, "wb") as f:
                            f.write(uploaded_logo.getbuffer())

                        # Generate QR code with logo
                        img, filename = generate_qr_code(
                            data, 10, 4, fill_color_logo, back_color_logo,
                            style=style_with_logo, logo_path=temp_logo_path,
                            logo_size_factor=logo_size/100
                        )

                        # Remove temporary logo file
                        try:
                            os.remove(temp_logo_path)
                        except:
                            pass

                        # Create columns for display and download options
                        col1, col2 = st.columns([2, 1])

                        with col1:
                            # Display generated QR code
                            st.image(img, caption="QR Code with Logo", use_column_width=True)

                        with col2:
                            st.markdown("### Download Options")
                            # Create download links
                            st.markdown(
                                generate_download_link(img, os.path.basename(filename), "📥 Download PNG"),
                                unsafe_allow_html=True
                            )

                            # Display the encoded data
                            st.markdown("### Encoded Data")
                            if len(data) > 100:
                                st.code(data[:100] + "...")
                            else:
                                st.code(data)

                    # Show success message
                    st.markdown(f'<p class="success-msg">✅ QR code with logo successfully generated!</p>', unsafe_allow_html=True)
                else:
                    st.error("⚠️ Please upload a logo image.")
            else:
                st.error("⚠️ Please enter some text or URL to generate a QR code.")

# Scan QR Code Page
elif app_mode == "Scan QR Code":
    st.markdown('<div class="animated-card"><h2 class="sub-header">🔎 Scan QR Code</h2></div>', unsafe_allow_html=True)

    # Create tabs for different scanning methods
    scan_tabs = st.tabs(["Upload Image", "Use Webcam"])

    # Tab 1: Upload Image
    with scan_tabs[0]:
        uploaded_file = st.file_uploader("Upload QR Code Image", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Scan button
            if st.button("Scan QR Code", key="scan_uploaded"):
                with st.spinner("Scanning QR code..."):
                    # Process the image
                    success, result, bbox = scan_qr_code(image)

                    if success:
                        # If bbox is available, visualize the detection
                        if bbox is not None:
                            detected_image = visualize_qr_detection(image, bbox)
                            st.image(detected_image, caption="Detected QR Code", use_column_width=True)

                        st.markdown(f'<p class="success-msg">✅ QR code successfully scanned!</p>', unsafe_allow_html=True)
                        st.write("**Decoded Data:**")

                        # Check if result is a URL
                        if result.startswith(('http://', 'https://')):
                            st.markdown(f"🔗 **URL detected:** [{result}]({result})")
                            st.info("Click the link above to open the URL")
                        else:
                            st.code(result)

                        # Copy button
                        st.text_area("Copy this data:", value=result, height=100)
                    else:
                        st.error(f"⚠️ {result}")

    # Tab 2: Use Webcam
    with scan_tabs[1]:
        st.markdown("### Scan QR Code with Webcam")
        st.info("Make sure your webcam is connected and accessible.")

        # Start webcam button
        if st.button("Start Webcam", key="start_webcam"):
            with st.spinner("Accessing webcam..."):
                # Capture from webcam
                result = capture_from_webcam()

                if result:
                    st.markdown(f'<p class="success-msg">✅ QR code successfully scanned!</p>', unsafe_allow_html=True)
                    st.write("**Decoded Data:**")

                    # Check if result is a URL
                    if result.startswith(('http://', 'https://')):
                        st.markdown(f"🔗 **URL detected:** [{result}]({result})")
                        st.info("Click the link above to open the URL")
                    else:
                        st.code(result)

                    # Copy button
                    st.text_area("Copy this data:", value=result, height=100)

# QR Gallery Page
elif app_mode == "QR Gallery":
    st.markdown('<div class="animated-card"><h2 class="sub-header">🖼️ QR Code Gallery</h2></div>', unsafe_allow_html=True)

    # Load QR history
    history = load_qr_history()

    if history["qr_codes"]:
        st.info(f"Showing your {len(history['qr_codes'])} most recent QR codes")

        # Create a grid layout
        cols = st.columns(3)

        for i, qr_entry in enumerate(history["qr_codes"]):
            col_idx = i % 3

            with cols[col_idx]:
                # Create a card for each QR code
                st.markdown(f"""
                <div class="gallery-item">
                    <h4>{qr_entry['type'].replace('_', ' ').title()} QR</h4>
                </div>
                """, unsafe_allow_html=True)

                # Display the QR code
                try:
                    img = Image.open(qr_entry["filename"])
                    st.image(img, use_column_width=True)

                    # Show data preview
                    data_preview = qr_entry["data"]
                    if len(data_preview) > 30:
                        data_preview = data_preview[:30] + "..."

                    st.markdown(f"**Data:** `{data_preview}`")

                    # Show timestamp
                    timestamp = datetime.fromisoformat(qr_entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
                    st.caption(f"Created: {timestamp}")

                    # Download button
                    if os.path.exists(qr_entry["filename"]):
                        with open(qr_entry["filename"], "rb") as file:
                            btn = st.download_button(
                                label="Download",
                                data=file,
                                file_name=os.path.basename(qr_entry["filename"]),
                                mime="image/png"
                            )
                except Exception as e:
                    st.error(f"Could not load image: {str(e)}")
    else:
        st.warning("No QR codes have been generated yet. Generate some QR codes to see them here!")

# Batch Generator Page
elif app_mode == "Batch Generator":
    st.markdown('<div class="animated-card"><h2 class="sub-header">📦 Batch QR Code Generator</h2></div>', unsafe_allow_html=True)

    st.markdown("""
    Generate multiple QR codes at once by entering one item per line.
    Perfect for creating QR codes for lists, inventories, or event tickets.
    """)

    # Input for batch data
    batch_data = st.text_area("Enter one item per line:", height=200,
                             help="Each line will generate a separate QR code")

    # Style options
    col1, col2 = st.columns(2)

    with col1:
        batch_style = st.selectbox("QR Style:", ["standard", "rounded", "circular"],
                                  help="Choose the style for all QR codes",
                                  key="batch_style")
        batch_fill_color = st.color_picker("QR Code Color:", "#000000", key="batch_fill_color")

    with col2:
        batch_box_size = st.slider("Box Size:", 5, 15, 8,
                                  help="Controls the size of each box in the QR codes",
                                  key="batch_box_size")
        batch_back_color = st.color_picker("Background Color:", "#FFFFFF", key="batch_back_color")

    # Generate button
    if st.button("Generate Batch QR Codes", key="generate_batch"):
        if batch_data:
            # Split the input by lines
            items = [line.strip() for line in batch_data.split('\n') if line.strip()]

            if items:
                with st.spinner(f"Generating {len(items)} QR codes..."):
                    # Create a progress bar
                    progress_bar = st.progress(0)

                    # Create a directory for this batch
                    batch_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    batch_dir = f"generated_qr_codes/batch_{batch_timestamp}"
                    os.makedirs(batch_dir, exist_ok=True)

                    # Generate QR codes
                    generated_files = []
                    for i, item in enumerate(items):
                        # Update progress
                        progress = (i + 1) / len(items)
                        progress_bar.progress(progress)

                        # Generate QR code
                        filename = f"{batch_dir}/qr_{i+1}_{item[:20].replace(' ', '_')}.png"
                        img, _ = generate_qr_code(
                            item, batch_box_size, 4, batch_fill_color, batch_back_color,
                            style=batch_style
                        )

                        # Save with custom filename
                        img.save(filename)
                        generated_files.append(filename)

                    # Create a zip file of all generated QR codes
                    import zipfile
                    zip_filename = f"{batch_dir}.zip"
                    with zipfile.ZipFile(zip_filename, 'w') as zipf:
                        for file in generated_files:
                            zipf.write(file, os.path.basename(file))

                    # Show success message
                    st.markdown(f'<p class="success-msg">✅ Successfully generated {len(items)} QR codes!</p>', unsafe_allow_html=True)

                    # Provide download link for the zip file
                    with open(zip_filename, "rb") as f:
                        st.download_button(
                            label="📥 Download All QR Codes (ZIP)",
                            data=f,
                            file_name=f"qr_batch_{batch_timestamp}.zip",
                            mime="application/zip"
                        )

                    # Show preview of first few QR codes
                    st.markdown("### Preview")
                    preview_cols = st.columns(min(3, len(generated_files)))
                    for i, filename in enumerate(generated_files[:3]):
                        preview_cols[i].image(filename, caption=f"QR Code {i+1}", use_column_width=True)

                    if len(generated_files) > 3:
                        st.info(f"Showing 3 of {len(generated_files)} generated QR codes. Download the ZIP file to get all.")
            else:
                st.error("⚠️ No valid items found. Please enter at least one item.")
        else:
            st.error("⚠️ Please enter some data to generate QR codes.")

# Footer
st.markdown("""
    <div class="footer">
        <p>QR Code Studio Pro v1.0 | Developed with ❤️ by Asadullah</p>
        <p><a href="https://github.com/asadullah48" target="_blank">GitHub</a> |
        <a href="https://github.com/asadullah48/qr-code-studio-pro" target="_blank">Project Repository</a></p>
    </div>
""", unsafe_allow_html=True)