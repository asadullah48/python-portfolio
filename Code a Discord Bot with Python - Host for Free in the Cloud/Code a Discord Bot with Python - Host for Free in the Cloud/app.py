import streamlit as st
import os
from dotenv import load_dotenv

# Configure page
st.set_page_config(
    page_title="Discord Bot Dashboard",
    page_icon="🤖"
)

# Load env (for local dev)
load_dotenv()

# UI Components
st.title("🤖 Discord Bot Manager")
st.divider()

# Status section
st.header("Bot Status")
if os.getenv('DISCORD_BOT_TOKEN'):
    st.success("✅ Token loaded successfully")
    if st.button("Check Bot Availability"):
        st.warning("Note: This dashboard doesn't run the bot directly. Run bot.py separately!")
else:
    st.error("🚨 Missing token! Add DISCORD_BOT_TOKEN to environment variables")

# Command documentation
st.header("Commands Reference")
st.markdown("""
| Command | Description |
|---------|-------------|
| `!hello` | Greets the user |
| `!info`  | Shows bot details |
| `!help`  | Displays this menu |
""")

# Deployment guide
st.header("Deployment")
st.markdown("""
1. **Local Testing**:
   ```bash
   python bot.py