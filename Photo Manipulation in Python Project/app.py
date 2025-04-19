import streamlit as st
from PIL import Image
import io
import os
import sys
import tempfile
from image_editor import ImageEditor

def load_image(image_file):
    """Load and return a PIL Image from a file upload"""
    img = Image.open(image_file)
    return img

def main():
    """Main Streamlit app function"""
    st.set_page_config(
        page_title="Image Editor App",
        page_icon="📸",
        layout="wide"
    )
    
    st.title("📸 Image Editor App")
    st.write("Upload an image and apply various filters to enhance it!")
    
    # Initialize session state for history tracking
    if 'editor' not in st.session_state:
        st.session_state.editor = None
    if 'temp_file_path' not in st.session_state:
        st.session_state.temp_file_path = None
    if 'original_image' not in st.session_state:
        st.session_state.original_image = None
    if 'edited_image' not in st.session_state:
        st.session_state.edited_image = None
    if 'filter_history' not in st.session_state:
        st.session_state.filter_history = []
    
    # File uploader
    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    
    # Display image editing interface if image is uploaded
    if image_file is not None:
        # Load image on first upload or when a new image is uploaded
        if st.session_state.editor is None or image_file.name != getattr(st.session_state.get('last_uploaded_file', None), 'name', None):
            # Save uploaded image to a temp file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{image_file.name.split('.')[-1]}")
            temp_file.write(image_file.getvalue())
            temp_file.close()
            
            # Initialize image editor
            try:
                st.session_state.editor = ImageEditor(temp_file.name)
                st.session_state.temp_file_path = temp_file.name
                st.session_state.original_image = st.session_state.editor.original.copy()
                st.session_state.edited_image = st.session_state.editor.edited.copy()
                st.session_state.filter_history = []
                st.session_state.last_uploaded_file = image_file
            except Exception as e:
                st.error(f"Error loading image: {e}")
                return
        
        # Create a two-column layout
        col1, col2 = st.columns([1, 2])
        
        # Sidebar for filters and adjustments
        with col1:
            st.subheader("Filters & Adjustments")
            
            # Get image info
            if st.session_state.editor:
                info = st.session_state.editor.get_image_info()
                st.write(f"📊 Image size: {info['size'][0]}x{info['size'][1]}")
                st.write(f"📊 Format: {info['format']}")
            
            # Filter tabs
            filter_tab, adjust_tab, transform_tab = st.tabs(["Filters", "Adjustments", "Tools"])
            
            with filter_tab:
                if st.button("🔲 Black & White"):
                    st.session_state.editor.apply("apply_black_and_white")
                    st.session_state.edited_image = st.session_state.editor.edited.copy()
                    st.session_state.filter_history.append("Black & White")
                
                if st.button("🌫️ Blur"):
                    blur_radius = st.slider("Blur Radius", 0.0, 10.0, 2.0, step=0.5)
                    st.session_state.editor.apply("apply_blur", blur_radius)
                    st.session_state.edited_image = st.session_state.editor.edited.copy()
                    st.session_state.filter_history.append(f"Blur (radius={blur_radius})")
                
                if st.button("✨ Sharpen"):
                    sharpen_factor = st.slider("Sharpen Factor", 1, 5, 2, step=1)
                    st.session_state.editor.apply("apply_sharpen", sharpen_factor)
                    st.session_state.edited_image = st.session_state.editor.edited.copy()
                    st.session_state.filter_history.append(f"Sharpen (factor={sharpen_factor})")
                
                if st.button("🧱 Sepia"):
                    st.session_state.editor.apply("apply_sepia")
                    st.session_state.edited_image = st.session_state.editor.edited.copy()
                    st.session_state.filter_history.append("Sepia")
                
                if st.button("🔄 Invert Colors"):
                    st.session_state.editor.apply("apply_invert")
                    st.session_state.edited_image = st.session_state.editor.edited.copy()
                    st.session_state.filter_history.append("Invert Colors")
            
            with adjust_tab:
                if st.button("☀️ Apply Brightness"):
                    brightness = st.slider("Brightness", 0.0, 2.0, 1.0, step=0.1)
                    st.session_state.editor.apply("apply_brightness", brightness)
                    st.session_state.edited_image = st.session_state.editor.edited.copy()
                    st.session_state.filter_history.append(f"Brightness (factor={brightness})")
                
                if st.button("📊 Apply Contrast"):
                    contrast = st.slider("Contrast", 0.0, 2.0, 1.0, step=0.1)
                    st.session_state.editor.apply("apply_contrast", contrast)
                    st.session_state.edited_image = st.session_state.editor.edited.copy()
                    st.session_state.filter_history.append(f"Contrast (factor={contrast})")
            
            with transform_tab:
                if st.button("🔄 Rotate"):
                    degrees = st.slider("Degrees", -180, 180, 0, step=90)
                    st.session_state.editor.apply("apply_rotate", degrees)
                    st.session_state.edited_image = st.session_state.editor.edited.copy()
                    st.session_state.filter_history.append(f"Rotate (degrees={degrees})")
            
            # History and undo/redo options
            st.subheader("History")
            history_container = st.container()
            with history_container:
                for i, filter_name in enumerate(st.session_state.filter_history):
                    st.text(f"{i+1}. {filter_name}")
            
            # Undo, redo, and reset buttons
            col_undo, col_redo = st.columns(2)
            with col_undo:
                if st.button("↩️ Undo"):
                    if st.session_state.editor.undo():
                        st.session_state.edited_image = st.session_state.editor.edited.copy()
                        if st.session_state.filter_history:
                            st.session_state.filter_history.pop()
            
            with col_redo:
                if st.button("↪️ Redo"):
                    if st.session_state.editor.redo():
                        st.session_state.edited_image = st.session_state.editor.edited.copy()
            
            if st.button("🔄 Reset to Original"):
                st.session_state.editor.reset()
                st.session_state.edited_image = st.session_state.editor.edited.copy()
                st.session_state.filter_history = []
            
            # Save button
            if st.button("💾 Save Image"):
                # Create a byte buffer for the image
                buf = io.BytesIO()
                st.session_state.edited_image.save(buf, format="PNG")
                buf.seek(0)
                
                # Provide download button
                st.download_button(
                    label="📥 Download Edited Image",
                    data=buf,
                    file_name=f"edited_{image_file.name}",
                    mime="image/png"
                )
        
        # Main image display area
        with col2:
            st.subheader("Image Preview")
            
            # Toggle between original and edited
            show_original = st.checkbox("Show Original for Comparison")
            
            if show_original:
                # Display original and edited side by side
                orig_col, edit_col = st.columns(2)
                with orig_col:
                    st.text("Original Image")
                    st.image(st.session_state.original_image, use_column_width=True)
                
                with edit_col:
                    st.text("Edited Image")
                    st.image(st.session_state.edited_image, use_column_width=True)
            else:
                # Display only edited image
                st.image(st.session_state.edited_image, use_column_width=True)
    
    else:
        # No image uploaded yet
        st.info("👆 Please upload an image to start editing")
        
        # Display example images
        st.subheader("Example Features")
        st.write("This app allows you to:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("☀️ Adjust brightness and contrast")
        with col2:
            st.write("🌫️ Apply filters like blur and sharpen")
        with col3:
            st.write("🔲 Convert to black & white or sepia")
        
        # Footer
        st.markdown("---")
        st.markdown("📸 Created by [Asadullah](https://github.com/asadullah48)")

if __name__ == "__main__":
    main()