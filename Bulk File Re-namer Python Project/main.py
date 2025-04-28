import os
import streamlit as st
from pathlib import Path

# 🎨 Streamlit UI Configuration
st.set_page_config(
    page_title="📁 Bulk File Renamer",
    page_icon="🔠",
    layout="centered"
)

# 📁 Main function
def main():
    st.title("📁 Bulk File Renamer 🔄")
    st.markdown("### Batch rename files with custom prefixes and sequential numbering")

    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. Select a folder by either:
           - Entering the folder path directly, OR
           - Dragging and dropping any file from your target folder
        2. Set your renaming preferences
        3. Preview changes before executing
        4. Click 'Rename Files' button
        """)

    # 📂 Folder selection
    st.subheader("1. Select Folder")

    # Option 1: Manual folder path input
    folder_path = st.text_input("Enter folder path:", help="Paste the full path to your folder")

    # Option 2: File uploader to help users find their folder
    st.markdown("**OR**")
    st.markdown("Drag and drop a file from the folder you want to work with:")

    uploaded_file = st.file_uploader(
        "This will help identify the folder containing your files",
        type=None,  # Accept all file types
        help="We'll use this file to locate your folder"
    )

    # If a file was uploaded, extract the folder path
    if uploaded_file and not folder_path:
        # Create a temporary directory to save the file
        import tempfile
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, uploaded_file.name)

        # Save the uploaded file
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Ask user to confirm the folder path
        suggested_path = os.path.dirname(temp_path)
        st.info(f"Suggested folder path: {suggested_path}")

        # Let the user edit the suggested path if needed
        folder_path = st.text_input("Confirm or edit folder path:", suggested_path)

        # Clean up
        os.remove(temp_path)
        os.rmdir(temp_dir)

    if not folder_path:
        st.warning("Please enter a folder path or upload a file")
        return

    if not os.path.exists(folder_path):
        st.error("❌ Folder does not exist!")
        return

    # Show folder contents
    if folder_path and os.path.exists(folder_path):
        files = os.listdir(folder_path)
        st.success(f"Found {len(files)} items in the selected folder")
        with st.expander("Show folder contents"):
            st.write(files)

    # ✏️ Renaming options
    st.subheader("2. Renaming Options")
    col1, col2 = st.columns(2)
    with col1:
        prefix = st.text_input("Filename prefix:", "File_", help="e.g., 'Vacation_'")
    with col2:
        extension = st.text_input("File extension:", ".jpg", help="e.g., .jpg, .png, .pdf")

    # 🛠️ Process files
    st.subheader("3. Preview Changes")
    if st.button("🔍 Preview Renaming"):
        try:
            # Ensure extension starts with dot
            extension = f".{extension.strip('.')}"

            # Get files from the folder that match the extension
            files_to_rename = []
            for file in os.listdir(folder_path):
                if file.lower().endswith(extension.lower()):
                    files_to_rename.append(file)

            if not files_to_rename:
                st.warning(f"No {extension} files found in directory!")
                return

            # Display preview
            st.success(f"Found {len(files_to_rename)} {extension} files")
            preview_data = []

            for i, filename in enumerate(sorted(files_to_rename), 1):
                new_name = f"{prefix}{i}{extension}"
                preview_data.append([filename, new_name])

            st.table({
                "Current Filename": [row[0] for row in preview_data],
                "New Filename": [row[1] for row in preview_data]
            })

            # 🚀 Execute renaming
            if st.button("✅ Confirm and Rename Files", type="primary"):
                with st.spinner("Renaming files..."):
                    for i, filename in enumerate(sorted(files_to_rename), 1):
                        old_path = os.path.join(folder_path, filename)
                        new_path = os.path.join(folder_path, f"{prefix}{i}{extension}")
                        try:
                            os.rename(old_path, new_path)
                        except Exception as e:
                            st.error(f"Error renaming {filename}: {str(e)}")
                            continue

                st.balloons()
                st.success(f"Successfully renamed {len(files_to_rename)} files!")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# 🏃 Run the app
if __name__ == "__main__":
    main()