# app.py
import streamlit as st

# Set page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="GitHub Profile Explorer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

import time
import pandas as pd
from datetime import datetime

# Try to import plotly, but provide fallback if not available
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly is not installed. Some visualizations will use Streamlit's built-in charts instead.")
    # We'll use Streamlit's built-in charts as a fallback

# Import custom modules
from utils import (
    get_github_profile_data,
    get_user_repositories,
    get_user_organizations,
    get_user_events,
    extract_username,
    create_repo_dataframe,
    apply_custom_css
)
from components import (
    render_profile_card,
    render_stats_metrics,
    render_profile_details,
    render_repositories_table,
    render_language_chart,
    render_activity_chart,
    render_stars_forks_chart,
    render_organizations,
    render_sidebar_info
)

# Apply custom CSS
apply_custom_css()

# App title and description
st.title("🔍 GitHub Profile Explorer")
st.markdown("""
This app allows you to explore GitHub user profiles and their repositories.
Enter a GitHub username or a GitHub profile URL to get started.
""")

# Render sidebar information
render_sidebar_info()

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["🔍 Search", "📊 Dashboard", "ℹ️ Help"])

with tab1:
    # Input form with improved layout
    st.markdown('<div class="stcard">', unsafe_allow_html=True)

    input_col1, input_col2 = st.columns([3, 1])
    with input_col1:
        user_input = st.text_input(
            "Enter GitHub Username or Profile URL",
            placeholder="e.g., octocat or https://github.com/octocat",
            key="username_input"
        )

    with input_col2:
        max_repos = st.number_input("Max Repositories", min_value=1, max_value=100, value=10)

    # Process button with improved styling
    search_button = st.button("🔍 Explore Profile", use_container_width=True, type="primary")

    st.markdown('</div>', unsafe_allow_html=True)

    # Main app logic
    if search_button and user_input:
        username = extract_username(user_input)

        # Create a progress bar for better UX
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Fetch user data
        status_text.text(f"Fetching profile data for {username}...")
        user_data = get_github_profile_data(username)
        progress_bar.progress(25)

        if user_data:
            # Fetch additional data
            status_text.text("Fetching repositories...")
            repos_data = get_user_repositories(username, max_repos)
            progress_bar.progress(50)

            status_text.text("Fetching organizations...")
            orgs_data = get_user_organizations(username)
            progress_bar.progress(75)

            status_text.text("Fetching activity data...")
            events_data = get_user_events(username)
            progress_bar.progress(100)

            # Clear status indicators
            status_text.empty()
            time.sleep(0.5)  # Short delay for visual effect
            progress_bar.empty()

            # Create repository DataFrame
            repos_df = create_repo_dataframe(repos_data)

            # Display profile information in a two-column layout
            profile_col1, profile_col2 = st.columns([1, 2])

            with profile_col1:
                # Render profile card
                render_profile_card(user_data, username)

                # Render organizations if available
                if orgs_data:
                    render_organizations(orgs_data)

            with profile_col2:
                # Render stats metrics
                render_stats_metrics(user_data)

                # Render profile details
                render_profile_details(user_data)

                # Render activity chart if data available
                if events_data:
                    render_activity_chart(events_data)

            # Repository section
            if len(repos_df) > 0:
                # Render repositories table with filtering
                render_repositories_table(repos_df)

                # Create a two-column layout for charts
                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    # Render language distribution chart
                    render_language_chart(repos_df)

                with chart_col2:
                    # Render stars and forks chart
                    render_stars_forks_chart(repos_df)
            else:
                st.info("No repositories found or unable to fetch repository data.")

    elif search_button and not user_input:
        st.warning("Please enter a GitHub username or profile URL.")
    else:
        # Show sample profiles when no search is performed
        st.markdown('<div class="stcard">', unsafe_allow_html=True)
        st.subheader("🌟 Try these popular GitHub profiles")

        sample_col1, sample_col2, sample_col3, sample_col4 = st.columns(4)

        with sample_col1:
            st.markdown("### [octocat](https://github.com/octocat)")
            st.image("https://github.com/octocat.png", width=100)
            if st.button("Explore octocat", key="sample1"):
                st.session_state.username_input = "octocat"
                st.rerun()

        with sample_col2:
            st.markdown("### [torvalds](https://github.com/torvalds)")
            st.image("https://github.com/torvalds.png", width=100)
            if st.button("Explore torvalds", key="sample2"):
                st.session_state.username_input = "torvalds"
                st.rerun()

        with sample_col3:
            st.markdown("### [gvanrossum](https://github.com/gvanrossum)")
            st.image("https://github.com/gvanrossum.png", width=100)
            if st.button("Explore gvanrossum", key="sample3"):
                st.session_state.username_input = "gvanrossum"
                st.rerun()

        with sample_col4:
            st.markdown("### [yyx990803](https://github.com/yyx990803)")
            st.image("https://github.com/yyx990803.png", width=100)
            if st.button("Explore yyx990803", key="sample4"):
                st.session_state.username_input = "yyx990803"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("GitHub Trends Dashboard")

    st.markdown('<div class="stcard">', unsafe_allow_html=True)
    st.info("Enter a GitHub username in the Search tab to view detailed analytics.")

    # Show some sample GitHub statistics
    st.subheader("Most Popular Programming Languages on GitHub")

    # Sample data for demonstration
    languages_data = {
        "JavaScript": 3.1,
        "Python": 2.5,
        "Java": 2.4,
        "TypeScript": 1.9,
        "C++": 1.7,
        "C#": 1.5,
        "PHP": 1.4,
        "Go": 1.2,
        "Ruby": 1.0,
        "Swift": 0.9
    }

    languages_df = pd.DataFrame({
        "Language": languages_data.keys(),
        "Repositories (millions)": languages_data.values()
    })

    if PLOTLY_AVAILABLE:
        fig = px.bar(
            languages_df,
            x="Language",
            y="Repositories (millions)",
            color="Language",
            title="Most Popular Programming Languages on GitHub",
            color_discrete_sequence=px.colors.qualitative.Plotly
        )

        fig.update_layout(
            xaxis_title="Language",
            yaxis_title="Number of Repositories (millions)",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback to Streamlit's built-in chart
        st.bar_chart(languages_df.set_index("Language"))
    st.markdown('</div>', unsafe_allow_html=True)

    # Add more sample dashboard elements
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="stcard">', unsafe_allow_html=True)
        st.subheader("GitHub Users by Country")

        # Sample data
        countries = ["United States", "China", "India", "United Kingdom", "Germany", "Canada", "Brazil", "Japan", "Russia", "France"]
        users = [8.5, 6.7, 5.8, 3.2, 2.9, 2.7, 2.5, 2.3, 2.1, 1.9]

        countries_df = pd.DataFrame({
            "Country": countries,
            "Users (millions)": users
        })

        if PLOTLY_AVAILABLE:
            fig = px.pie(
                countries_df,
                values="Users (millions)",
                names="Country",
                title="GitHub Users by Country",
                color_discrete_sequence=px.colors.qualitative.Plotly,
                hole=0.4
            )

            fig.update_traces(textposition='inside', textinfo='percent+label')

            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback to a simple table with metrics
            st.subheader("GitHub Users by Country")
            for i, (country, users) in enumerate(zip(countries, users)):
                if i % 2 == 0:
                    cols = st.columns(2)
                cols[i % 2].metric(country, f"{users}M")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stcard">', unsafe_allow_html=True)
        st.subheader("GitHub Activity Over Time")

        # Sample data
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        commits = [2.1, 2.3, 2.7, 2.5, 2.8, 3.1, 3.0, 2.9, 3.2, 3.5, 3.3, 2.8]
        pull_requests = [0.8, 0.9, 1.1, 1.0, 1.2, 1.3, 1.2, 1.1, 1.3, 1.4, 1.3, 1.1]
        issues = [1.2, 1.3, 1.5, 1.4, 1.6, 1.7, 1.6, 1.5, 1.7, 1.8, 1.7, 1.5]

        activity_df = pd.DataFrame({
            "Month": months,
            "Commits (millions)": commits,
            "Pull Requests (millions)": pull_requests,
            "Issues (millions)": issues
        })

        if PLOTLY_AVAILABLE:
            fig = px.line(
                activity_df,
                x="Month",
                y=["Commits (millions)", "Pull Requests (millions)", "Issues (millions)"],
                title="GitHub Activity Over Time",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback to Streamlit's built-in chart
            st.subheader("GitHub Activity Over Time")

            # We need to reshape the data for Streamlit's line chart
            activity_df = activity_df.set_index("Month")
            st.line_chart(activity_df)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.header("Help & Documentation")

    st.markdown('<div class="stcard">', unsafe_allow_html=True)
    st.subheader("How to Use This App")

    st.markdown("""
    1. **Search for a GitHub User**:
       - Enter a GitHub username or profile URL in the search box
       - Click the "Explore Profile" button

    2. **View Profile Information**:
       - See basic profile details like name, bio, location
       - View statistics like followers, repositories, etc.

    3. **Explore Repositories**:
       - Browse through the user's repositories
       - Filter repositories by language
       - Sort repositories by stars, forks, or update date

    4. **Analyze Data**:
       - View language distribution charts
       - See activity patterns
       - Explore top repositories

    5. **Export Data**:
       - Download repository data as CSV or JSON
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="stcard">', unsafe_allow_html=True)
    st.subheader("About GitHub API Rate Limits")

    st.markdown("""
    The GitHub API has rate limits that restrict how many requests can be made in a certain time period:

    - **Unauthenticated requests**: 60 requests per hour
    - **Authenticated requests**: 5,000 requests per hour

    If you encounter rate limit errors, you can:

    1. Wait until the rate limit resets
    2. Use a GitHub personal access token for higher limits

    To use a personal access token:

    1. Create a token at [GitHub Developer Settings](https://github.com/settings/tokens)
    2. Add it to your Streamlit secrets.toml file
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="stcard">', unsafe_allow_html=True)
    st.subheader("Troubleshooting")

    expander1 = st.expander("User not found")
    with expander1:
        st.markdown("""
        If you receive a "User not found" error:

        - Check that the username is spelled correctly
        - Verify that the GitHub profile exists and is public
        - Try using the full GitHub URL instead of just the username
        """)

    expander2 = st.expander("Rate limit exceeded")
    with expander2:
        st.markdown("""
        If you receive a "Rate limit exceeded" error:

        - Wait until the rate limit resets (usually one hour)
        - Use a GitHub personal access token for higher limits
        - Reduce the number of requests by limiting the repositories fetched
        """)

    expander3 = st.expander("No data displayed")
    with expander3:
        st.markdown("""
        If no data is displayed after searching for a user:

        - Check your internet connection
        - Verify that the GitHub API is operational
        - Try refreshing the page and searching again
        - Check if the user has any public repositories
        """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="stcard">', unsafe_allow_html=True)
    st.subheader("Contact & Support")

    st.markdown("""
    If you encounter any issues or have suggestions for improvement:

    - Create an issue on the [GitHub repository](https://github.com/yourusername/github-profile-explorer)
    - Contact the developer at [your-email@example.com](mailto:your-email@example.com)

    This application is open source and contributions are welcome!
    """)
    st.markdown('</div>', unsafe_allow_html=True)