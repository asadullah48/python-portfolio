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
        1. Select a folder containing your files
        2. Set your renaming preferences
        3. Preview changes before executing
        4. Click 'Rename Files' button
        """)
    
    # 📂 Folder selection
    st.subheader("1. Select Folder")
    folder_path = st.text_input("Folder path:", help="Paste the full path to your folder")
    
    if not folder_path:
        st.warning("Please enter a folder path")
        return
    
    if not os.path.exists(folder_path):
        st.error("❌ Folder does not exist!")
        return
    
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