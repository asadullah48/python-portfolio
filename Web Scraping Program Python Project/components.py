"""
UI components for the GitHub Profile Explorer application.
Contains functions for rendering different sections of the UI.
"""
import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional

# Try to import plotly, but provide fallback if not available
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # We'll use Streamlit's built-in charts as a fallback

from utils import (
    format_date,
    get_csv_download_link,
    get_json_download_link,
    create_language_chart,
    create_activity_chart,
    create_stars_forks_chart
)

def render_profile_card(user_data: Dict[str, Any], username: str):
    """
    Render the user profile card with avatar and basic information

    Args:
        user_data: Dictionary containing user data
        username: GitHub username
    """
    with st.container():
        st.markdown('<div class="stcard fade-in">', unsafe_allow_html=True)

        # Profile image with custom styling
        st.markdown(
            f'<img src="{user_data.get("avatar_url")}" width="200" class="profile-img">',
            unsafe_allow_html=True
        )

        # Basic profile information
        st.markdown(f"""
        ### {user_data.get('name', username)}
        **@{username}**

        {user_data.get('bio', 'No bio available')}
        """)

        # Contact and additional information
        if user_data.get('company'):
            st.markdown(f"🏢 **Company:** {user_data['company']}")

        if user_data.get('location'):
            st.markdown(f"📍 **Location:** {user_data['location']}")

        if user_data.get('email'):
            st.markdown(f"📧 **Email:** {user_data['email']}")

        if user_data.get('blog'):
            st.markdown(f"🔗 **Website:** [{user_data['blog']}]({user_data['blog']})")

        st.markdown(f"🔗 [Visit GitHub Profile]({user_data['html_url']})")

        st.markdown('</div>', unsafe_allow_html=True)

def render_stats_metrics(user_data: Dict[str, Any]):
    """
    Render metrics showing user statistics

    Args:
        user_data: Dictionary containing user data
    """
    with st.container():
        st.markdown('<div class="stcard fade-in">', unsafe_allow_html=True)

        # Stats in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👥 Followers", user_data.get('followers', 0))

        with col2:
            st.metric("👣 Following", user_data.get('following', 0))

        with col3:
            st.metric("📚 Repositories", user_data.get('public_repos', 0))

        with col4:
            st.metric("📝 Gists", user_data.get('public_gists', 0))

        st.markdown('</div>', unsafe_allow_html=True)

def render_profile_details(user_data: Dict[str, Any]):
    """
    Render additional profile details

    Args:
        user_data: Dictionary containing user data
    """
    with st.container():
        st.markdown('<div class="stcard fade-in">', unsafe_allow_html=True)

        st.subheader("📅 Profile Information")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Created:** {format_date(user_data.get('created_at'))}")
            if user_data.get('hireable'):
                st.markdown("✅ **Available for hire**")

        with col2:
            st.markdown(f"**Last Updated:** {format_date(user_data.get('updated_at'))}")
            st.markdown(f"**Type:** {user_data.get('type', 'User')}")

        st.markdown('</div>', unsafe_allow_html=True)

def render_repositories_table(repos_df: pd.DataFrame, show_filters: bool = True):
    """
    Render a table of repositories with optional filtering

    Args:
        repos_df: DataFrame containing repository information
        show_filters: Whether to show filtering options
    """
    if len(repos_df) == 0:
        st.info("No repositories found or unable to fetch repository data.")
        return

    with st.container():
        st.markdown('<div class="stcard fade-in">', unsafe_allow_html=True)

        st.subheader("📚 Repositories")

        if show_filters:
            # Add filtering options
            col1, col2, col3 = st.columns(3)

            with col1:
                # Filter by language
                languages = ["All"] + sorted(repos_df["Language"].unique().tolist())
                selected_language = st.selectbox("Filter by Language", languages)

            with col2:
                # Sort options
                sort_options = ["Stars ↓", "Last Updated ↓", "Forks ↓", "Name (A-Z)"]
                sort_by = st.selectbox("Sort by", sort_options)

            with col3:
                # Show forks option
                show_forks = st.checkbox("Show Forks", value=True)

            # Apply filters
            filtered_df = repos_df.copy()

            if selected_language != "All":
                filtered_df = filtered_df[filtered_df["Language"] == selected_language]

            if not show_forks:
                filtered_df = filtered_df[~filtered_df["Is Fork"]]

            # Apply sorting
            if sort_by == "Stars ↓":
                filtered_df = filtered_df.sort_values("Stars", ascending=False)
            elif sort_by == "Last Updated ↓":
                filtered_df = filtered_df.sort_values("Last Updated", ascending=False)
            elif sort_by == "Forks ↓":
                filtered_df = filtered_df.sort_values("Forks", ascending=False)
            elif sort_by == "Name (A-Z)":
                filtered_df = filtered_df.sort_values("Name")
        else:
            filtered_df = repos_df

        # Display repositories as a table
        st.dataframe(
            filtered_df[["Name", "Description", "Language", "Stars", "Forks", "Last Updated"]],
            column_config={
                "Name": st.column_config.LinkColumn(),
                "Stars": st.column_config.NumberColumn(format="%d ⭐"),
                "Forks": st.column_config.NumberColumn(format="%d 🍴"),
            },
            hide_index=True,
            use_container_width=True
        )

        # Add download options
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(get_csv_download_link(filtered_df, "github_repositories"), unsafe_allow_html=True)
        with col2:
            st.markdown(get_json_download_link(filtered_df.to_dict('records'), "github_repositories"), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

def render_language_chart(repos_df: pd.DataFrame):
    """
    Render a chart showing language distribution

    Args:
        repos_df: DataFrame containing repository information
    """
    if len(repos_df) == 0:
        return

    with st.container():
        st.markdown('<div class="stcard fade-in">', unsafe_allow_html=True)

        st.subheader("🔤 Languages Used")

        chart_data = create_language_chart(repos_df)
        if chart_data is not None:
            if PLOTLY_AVAILABLE and hasattr(chart_data, 'update_layout'):
                # It's a Plotly figure
                st.plotly_chart(chart_data, use_container_width=True)
            else:
                # It's a pandas Series or DataFrame
                st.bar_chart(chart_data)
        else:
            st.info("No language data available.")

        st.markdown('</div>', unsafe_allow_html=True)

def render_activity_chart(events_data: List[Dict[str, Any]]):
    """
    Render a chart showing user activity

    Args:
        events_data: List of event data dictionaries
    """
    if not events_data:
        return

    with st.container():
        st.markdown('<div class="stcard fade-in">', unsafe_allow_html=True)

        st.subheader("📊 Recent Activity")

        chart_data = create_activity_chart(events_data)
        if chart_data is not None:
            if PLOTLY_AVAILABLE and hasattr(chart_data, 'update_layout'):
                # It's a Plotly figure
                st.plotly_chart(chart_data, use_container_width=True)
            else:
                # It's a pandas DataFrame
                st.bar_chart(chart_data)
        else:
            st.info("No activity data available.")

        st.markdown('</div>', unsafe_allow_html=True)

def render_stars_forks_chart(repos_df: pd.DataFrame):
    """
    Render a chart showing stars and forks for top repositories

    Args:
        repos_df: DataFrame containing repository information
    """
    if len(repos_df) == 0:
        return

    with st.container():
        st.markdown('<div class="stcard fade-in">', unsafe_allow_html=True)

        st.subheader("⭐ Top Repositories")

        chart_data = create_stars_forks_chart(repos_df)
        if chart_data is not None:
            if PLOTLY_AVAILABLE and hasattr(chart_data, 'update_layout'):
                # It's a Plotly figure
                st.plotly_chart(chart_data, use_container_width=True)
            else:
                # It's a pandas DataFrame
                st.bar_chart(chart_data)
        else:
            st.info("No repository data available.")

        st.markdown('</div>', unsafe_allow_html=True)

def render_organizations(orgs_data: List[Dict[str, Any]]):
    """
    Render user's organizations

    Args:
        orgs_data: List of organization data dictionaries
    """
    if not orgs_data:
        return

    with st.container():
        st.markdown('<div class="stcard fade-in">', unsafe_allow_html=True)

        st.subheader("🏢 Organizations")

        # Display organizations in a grid
        cols = st.columns(min(4, len(orgs_data)))

        for i, org in enumerate(orgs_data):
            with cols[i % len(cols)]:
                st.image(org.get("avatar_url", ""), width=80)
                st.markdown(f"**[{org.get('login')}]({org.get('html_url')})**")

        st.markdown('</div>', unsafe_allow_html=True)

def render_sidebar_info():
    """Render information in the sidebar"""
    st.sidebar.header("About")
    st.sidebar.info("""
    This application uses the GitHub API to fetch and display public information
    about GitHub users. It shows profile details, repositories, and activity statistics.

    Rate limits apply when using the GitHub API without authentication.
    """)

    st.sidebar.header("Features")
    st.sidebar.markdown("""
    - 👤 Profile information
    - 📊 Activity statistics
    - 📚 Public repositories
    - 📈 Language usage
    - 🏢 Organizations
    - 📥 Data export
    """)

    # Add theme toggle
    st.sidebar.header("Settings")
    theme = st.sidebar.radio("Theme", ["Light", "Dark"], horizontal=True)

    if theme == "Dark":
        st.markdown("""
        <script>
            document.body.classList.add('dark-mode');
        </script>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <script>
            document.body.classList.remove('dark-mode');
        </script>
        """, unsafe_allow_html=True)

    # Add GitHub API rate limit info
    st.sidebar.header("API Usage")
    st.sidebar.markdown("""
    GitHub API has a rate limit of 60 requests per hour for unauthenticated users.

    To increase this limit:
    1. Create a GitHub personal access token
    2. Add it to your Streamlit secrets
    """)

    # Add footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    Made with ❤️ using [Streamlit](https://streamlit.io)

    [View Source Code](https://github.com/yourusername/github-profile-explorer)
    """)
