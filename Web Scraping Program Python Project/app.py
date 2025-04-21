# app.py
import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

def get_github_profile_data(username):
    """
    Fetch GitHub profile data using the GitHub API
    """
    api_url = f"https://api.github.com/users/{username}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        # Optional: Add your GitHub token for higher rate limits
        # "Authorization": f"token {st.secrets['github_token']}"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        
        # Check rate limiting
        rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        if rate_limit_remaining < 5:
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            reset_datetime = datetime.fromtimestamp(reset_time)
            st.warning(f"⚠️ GitHub API rate limit almost reached. Resets at {reset_datetime.strftime('%H:%M:%S')}.")
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.error("❌ GitHub user not found. Please check the username.")
            return None
        elif response.status_code == 403 and rate_limit_remaining == 0:
            st.error("❌ GitHub API rate limit exceeded. Please try again later.")
            return None
        else:
            st.error(f"❌ Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
            return None
            
    except Exception as e:
        st.error(f"🚨 An error occurred: {str(e)}")
        return None

def get_user_repositories(username, max_repos=10):
    """
    Fetch the user's repositories using the GitHub API
    """
    api_url = f"https://api.github.com/users/{username}/repos?per_page={max_repos}&sort=updated"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        # Optional: Add your GitHub token for higher rate limits
        # "Authorization": f"token {st.secrets['github_token']}"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception:
        return []

def format_date(date_str):
    """Format GitHub API date to a more readable format"""
    if not date_str:
        return "Not available"
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return date_obj.strftime("%b %d, %Y")
    except:
        return date_str

# Set page configuration
st.set_page_config(
    page_title="GitHub Profile Explorer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("🔍 GitHub Profile Explorer")
st.markdown("""
This app allows you to explore GitHub user profiles and their repositories.
Enter a GitHub username or a GitHub profile URL to get started.
""")

# Sidebar with app information
with st.sidebar:
    st.header("About")
    st.info("""
    This application uses the GitHub API to fetch and display public information 
    about GitHub users. It shows profile details and lists repositories.
    
    Rate limits apply when using the GitHub API without authentication.
    """)
    
    st.header("Features")
    st.markdown("""
    - 👤 Profile information
    - 📊 Activity statistics
    - 📚 Public repositories
    - 📈 Language usage
    """)

# Input form
input_col1, input_col2 = st.columns([3, 1])
with input_col1:
    user_input = st.text_input(
        "Enter GitHub Username or Profile URL",
        placeholder="e.g., asadullah48 or https://github.com/asadullah48"
    )

with input_col2:
    max_repos = st.number_input("Max Repositories", min_value=1, max_value=100, value=10)

# Process button
search_button = st.button("🔍 Explore Profile", use_container_width=True)

# Function to extract username from input
def extract_username(input_text):
    input_text = input_text.strip()
    if "github.com/" in input_text:
        return input_text.split("github.com/")[-1].split("/")[0]
    return input_text

# Main app logic
if search_button and user_input:
    username = extract_username(user_input)
    
    # Display loading spinner
    with st.spinner(f"Fetching data for {username}..."):
        user_data = get_github_profile_data(username)
        
    if user_data:
        # Profile section
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(user_data.get("avatar_url"), width=230)
            
            # Basic profile card
            st.markdown(f"""
            ### {user_data.get('name', username)}
            **@{username}**
            
            {user_data.get('bio', 'No bio available')}
            """)
            
            if user_data.get('company'):
                st.markdown(f"🏢 **Company:** {user_data['company']}")
                
            if user_data.get('location'):
                st.markdown(f"📍 **Location:** {user_data['location']}")
                
            if user_data.get('email'):
                st.markdown(f"📧 **Email:** {user_data['email']}")
                
            if user_data.get('blog'):
                st.markdown(f"🔗 **Website:** [{user_data['blog']}]({user_data['blog']})")
                
            st.markdown(f"🔗 [Visit GitHub Profile]({user_data['html_url']})")
        
        with col2:
            # Stats in columns
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.metric("👥 Followers", user_data.get('followers', 0))
            
            with stat_col2:
                st.metric("👣 Following", user_data.get('following', 0))
            
            with stat_col3:
                st.metric("📚 Repositories", user_data.get('public_repos', 0))
            
            with stat_col4:
                st.metric("📝 Gists", user_data.get('public_gists', 0))
            
            # Additional information
            st.subheader("📅 Profile Information")
            
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.markdown(f"**Created:** {format_date(user_data.get('created_at'))}")
                if user_data.get('hireable'):
                    st.markdown("✅ **Available for hire**")
            
            with info_col2:
                st.markdown(f"**Last Updated:** {format_date(user_data.get('updated_at'))}")
                st.markdown(f"**Type:** {user_data.get('type', 'User')}")
        
        # Repository section
        st.subheader(f"📚 Latest Repositories")
        
        with st.spinner("Fetching repositories..."):
            repos_data = get_user_repositories(username, max_repos)
            
        if repos_data:
            # Convert to DataFrame for better display
            repos_df = pd.DataFrame([
                {
                    "Name": repo["name"],
                    "Description": repo.get("description", "No description"),
                    "Language": repo.get("language", "Not specified"),
                    "Stars": repo["stargazers_count"],
                    "Forks": repo["forks_count"],
                    "Last Updated": format_date(repo["updated_at"]),
                    "Link": repo["html_url"]
                }
                for repo in repos_data
            ])
            
            # Add link to repo name
            repos_df["Name"] = repos_df.apply(
                lambda row: f"[{row['Name']}]({row['Link']})", axis=1
            )
            
            # Display repositories as a table
            st.markdown(repos_df[["Name", "Description", "Language", "Stars", "Forks", "Last Updated"]].to_markdown(index=False))
            
            # Language distribution
            languages = repos_df["Language"].value_counts()
            if len(languages) > 0 and not all(languages.index == "Not specified"):
                st.subheader("🔤 Languages Used")
                st.bar_chart(languages)
        else:
            st.info("No repositories found or unable to fetch repository data.")
else:
    if search_button and not user_input:
        st.warning("Please enter a GitHub username or profile URL.")