"""
Utility functions for the GitHub Profile Explorer application.
Contains functions for API calls, data processing, and formatting.
"""
import requests
import pandas as pd
from datetime import datetime
import streamlit as st
from typing import Dict, List, Optional, Any, Tuple
import json
import base64
from io import BytesIO

# Try to import plotly, but provide fallback if not available
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # We'll use Streamlit's built-in charts as a fallback

# Cache API responses to reduce API calls
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_github_profile_data(username: str) -> Optional[Dict[str, Any]]:
    """
    Fetch GitHub profile data using the GitHub API

    Args:
        username: GitHub username

    Returns:
        Dictionary containing user data or None if an error occurs
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

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_user_repositories(username: str, max_repos: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch the user's repositories using the GitHub API

    Args:
        username: GitHub username
        max_repos: Maximum number of repositories to fetch

    Returns:
        List of repository data dictionaries
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

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_user_organizations(username: str) -> List[Dict[str, Any]]:
    """
    Fetch the user's organizations using the GitHub API

    Args:
        username: GitHub username

    Returns:
        List of organization data dictionaries
    """
    api_url = f"https://api.github.com/users/{username}/orgs"
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

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_repository_languages(username: str, repo_name: str) -> Dict[str, int]:
    """
    Fetch the languages used in a repository

    Args:
        username: GitHub username
        repo_name: Repository name

    Returns:
        Dictionary mapping language names to bytes of code
    """
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/languages"
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
            return {}
    except Exception:
        return {}

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_user_events(username: str, max_events: int = 30) -> List[Dict[str, Any]]:
    """
    Fetch recent user events (commits, PRs, issues, etc.)

    Args:
        username: GitHub username
        max_events: Maximum number of events to fetch

    Returns:
        List of event data dictionaries
    """
    api_url = f"https://api.github.com/users/{username}/events?per_page={max_events}"
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

def format_date(date_str: str) -> str:
    """
    Format GitHub API date to a more readable format

    Args:
        date_str: Date string in ISO format

    Returns:
        Formatted date string
    """
    if not date_str:
        return "Not available"
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return date_obj.strftime("%b %d, %Y")
    except:
        return date_str

def extract_username(input_text: str) -> str:
    """
    Extract username from input text which could be a URL or username

    Args:
        input_text: Input text from user

    Returns:
        Extracted GitHub username
    """
    input_text = input_text.strip()
    if "github.com/" in input_text:
        return input_text.split("github.com/")[-1].split("/")[0]
    return input_text

def create_repo_dataframe(repos_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Create a DataFrame from repository data

    Args:
        repos_data: List of repository data dictionaries

    Returns:
        Pandas DataFrame with repository information
    """
    if not repos_data:
        return pd.DataFrame()

    return pd.DataFrame([
        {
            "Name": repo["name"],
            "Description": repo.get("description", "No description"),
            "Language": repo.get("language", "Not specified"),
            "Stars": repo["stargazers_count"],
            "Forks": repo["forks_count"],
            "Last Updated": format_date(repo["updated_at"]),
            "Link": repo["html_url"],
            "Created At": format_date(repo["created_at"]),
            "Size": repo["size"],
            "Is Fork": repo["fork"],
            "Open Issues": repo["open_issues_count"],
            "Has Wiki": repo["has_wiki"],
            "Has Pages": repo["has_pages"],
            "Default Branch": repo["default_branch"],
            "Full Name": repo["full_name"]
        }
        for repo in repos_data
    ])

def create_language_chart(repos_df: pd.DataFrame) -> Optional[Any]:
    """
    Create a pie chart of languages used across repositories

    Args:
        repos_df: DataFrame containing repository information

    Returns:
        Plotly figure object or None
    """
    languages = repos_df["Language"].value_counts()
    languages = languages[languages.index != "Not specified"]

    if len(languages) == 0:
        return None

    if PLOTLY_AVAILABLE:
        fig = px.pie(
            values=languages.values,
            names=languages.index,
            title="Language Distribution",
            color_discrete_sequence=px.colors.qualitative.Plotly,
            hole=0.4
        )

        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            showlegend=False,
            margin=dict(t=30, b=0, l=0, r=0),
            height=300
        )

        return fig
    else:
        # Return the data for Streamlit's built-in charts
        return languages

def create_activity_chart(events_data: List[Dict[str, Any]]) -> Optional[Any]:
    """
    Create a chart showing user activity over time

    Args:
        events_data: List of event data dictionaries

    Returns:
        Plotly figure object or DataFrame for Streamlit charts
    """
    if not events_data:
        return None

    # Extract dates and event types
    event_dates = []
    event_types = []

    for event in events_data:
        event_date = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()
        event_dates.append(event_date)
        event_types.append(event["type"])

    # Create DataFrame
    events_df = pd.DataFrame({
        "Date": event_dates,
        "Type": event_types
    })

    # Count events by date and type
    events_count = events_df.groupby(["Date", "Type"]).size().reset_index(name="Count")

    if PLOTLY_AVAILABLE:
        # Create figure with Plotly
        fig = px.bar(
            events_count,
            x="Date",
            y="Count",
            color="Type",
            title="Recent Activity",
            color_discrete_sequence=px.colors.qualitative.Plotly
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Events",
            legend_title="Event Type",
            margin=dict(t=30, b=0, l=0, r=0),
            height=300
        )

        return fig
    else:
        # Return the data for Streamlit's built-in charts
        return events_count.pivot(index="Date", columns="Type", values="Count").fillna(0)

def create_stars_forks_chart(repos_df: pd.DataFrame) -> Optional[Any]:
    """
    Create a chart showing stars and forks for top repositories

    Args:
        repos_df: DataFrame containing repository information

    Returns:
        Plotly figure object or DataFrame for Streamlit charts
    """
    if len(repos_df) == 0:
        return None

    # Sort by stars and take top 5
    top_repos = repos_df.sort_values("Stars", ascending=False).head(5)

    if PLOTLY_AVAILABLE:
        # Create figure with Plotly
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=top_repos["Name"],
            y=top_repos["Stars"],
            name="Stars",
            marker_color="gold"
        ))

        fig.add_trace(go.Bar(
            x=top_repos["Name"],
            y=top_repos["Forks"],
            name="Forks",
            marker_color="royalblue"
        ))

        fig.update_layout(
            title="Top Repositories by Stars",
            xaxis_title="Repository",
            yaxis_title="Count",
            barmode="group",
            margin=dict(t=30, b=0, l=0, r=0),
            height=300
        )

        return fig
    else:
        # Return the data for Streamlit's built-in charts
        return pd.DataFrame({
            "Repository": top_repos["Name"],
            "Stars": top_repos["Stars"],
            "Forks": top_repos["Forks"]
        }).set_index("Repository")

def get_csv_download_link(df: pd.DataFrame, filename: str) -> str:
    """
    Generate a download link for a DataFrame as CSV

    Args:
        df: DataFrame to download
        filename: Name of the file

    Returns:
        HTML link for downloading the CSV
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download CSV</a>'
    return href

def get_json_download_link(data: Any, filename: str) -> str:
    """
    Generate a download link for data as JSON

    Args:
        data: Data to download
        filename: Name of the file

    Returns:
        HTML link for downloading the JSON
    """
    json_str = json.dumps(data, indent=4)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{filename}.json">Download JSON</a>'
    return href

def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app"""
    st.markdown("""
    <style>
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Cards */
    div.stcard {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Dark mode adjustments */
    .dark-mode div.stcard {
        background-color: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Profile image */
    .profile-img {
        border-radius: 50%;
        border: 3px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Metrics */
    div.stmetric {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 0.5rem;
        padding: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Buttons */
    .stButton button {
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }

    /* Tables */
    .dataframe {
        border-radius: 0.5rem;
        overflow: hidden;
    }

    /* Sidebar */
    .css-1d391kg {
        padding-top: 2rem;
    }

    /* Custom badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    .badge-primary {
        background-color: #4361ee;
        color: white;
    }

    .badge-secondary {
        background-color: #3a0ca3;
        color: white;
    }

    .badge-success {
        background-color: #4cc9f0;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
