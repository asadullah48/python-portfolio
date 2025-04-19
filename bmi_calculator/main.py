import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config with better layout and metadata
st.set_page_config(
    page_title="BMI Calculator & Health Tracker",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .title {
        text-align: center;
        color: #2e86ab;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    .description {
        text-align: center;
        color: #5c6784;
        margin-bottom: 2em;
    }
    .result-box {
        border-radius: 10px;
        padding: 1.5em;
        margin: 1em 0;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .healthy-range {
        background-color: #d4edda;
        color: #155724;
    }
    .warning-range {
        background-color: #fff3cd;
        color: #856404;
    }
    .danger-range {
        background-color: #f8d7da;
        color: #721c24;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True
)

# Initialize session state for history tracking
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar with additional features
with st.sidebar:
    st.markdown('<h1 class="title">BMI Tracker</h1>', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3048/3048127.png", use_column_width=True)
    
    st.markdown("---")
    st.subheader("Additional Options")
    unit_system = st.radio("Measurement System", ["Metric (kg/m)", "Imperial (lbs/ft)"])
    show_history = st.checkbox("Show History", value=True)
    show_chart = st.checkbox("Show Progress Chart", value=True)
    st.markdown("---")
    st.markdown("**About BMI**")
    st.markdown("""
    - Underweight: < 18.5
    - Normal: 18.5-24.9
    - Overweight: 25-29.9
    - Obese: ≥ 30
    """)

# Main content area
st.markdown('<h1 class="title">BMI Calculator & Health Tracker</h1>', unsafe_allow_html=True)
st.markdown('<p class="description">Track your Body Mass Index and monitor your health progress over time</p>', unsafe_allow_html=True)

# Layout for input fields
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Dynamic input fields based on unit system
    if unit_system == "Metric (kg/m)":
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, step=0.1)
        height = st.number_input("Height (meters)", min_value=0.5, max_value=2.5, step=0.01)
    else:
        weight = st.number_input("Weight (lbs)", min_value=1.0, max_value=660.0, step=0.1)
        height_feet = st.number_input("Height (feet)", min_value=1.0, max_value=8.0, step=0.1)
        height_inch = st.number_input("Height (inches)", min_value=0.0, max_value=11.0, step=0.1)
        height = height_feet * 0.3048 + height_inch * 0.0254  # Convert to meters
        weight = weight * 0.453592  # Convert to kg

    # Enhanced BMI calculation function
    def calculate_bmi(weight, height):
        try:
            if height <= 0:
                raise ValueError("Height must be positive")
            bmi = weight / (height ** 2)
            return round(bmi, 1)
        except:
            return None

    # Calculate button with better feedback
    if st.button("Calculate BMI", key="calculate"):
        bmi = calculate_bmi(weight, height)
        
        if bmi is not None:
            # Determine BMI category and styling
            if bmi < 18.5:
                category = "Underweight"
                css_class = "warning-range"
                advice = "Consider consulting a nutritionist to develop a healthy weight gain plan."
            elif 18.5 <= bmi < 24.9:
                category = "Normal weight"
                css_class = "healthy-range"
                advice = "Maintain your healthy lifestyle with balanced diet and regular exercise."
            elif 25 <= bmi < 29.9:
                category = "Overweight"
                css_class = "warning-range"
                advice = "Consider increasing physical activity and adjusting your diet for gradual weight loss."
            else:
                category = "Obese"
                css_class = "danger-range"
                advice = "Consult with a healthcare professional for personalized weight management advice."
            
            # Store the result in history
            st.session_state.history.append({
                "date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "weight": weight,
                "height": height,
                "bmi": bmi,
                "category": category
            })
            
            # Display results with better visualization
            st.markdown(f"""
            <div class="result-box {css_class}">
                <h3 style="text-align: center;">Your Results</h3>
                <p style="text-align: center; font-size: 2em; font-weight: bold;">BMI: {bmi}</p>
                <p style="text-align: center; font-size: 1.5em;">Category: {category}</p>
                <p style="text-align: center;">{advice}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display BMI range visualization
            ranges = pd.DataFrame({
                "Category": ["Underweight", "Normal", "Overweight", "Obese"],
                "Min": [0, 18.5, 25, 30],
                "Max": [18.5, 24.9, 29.9, 40],
                "Color": ["#FFC107", "#28A745", "#FFC107", "#DC3545"]
            })
            
            fig = px.bar(ranges, x="Category", y="Max", color="Color", 
                         title="BMI Categories with Your Position",
                         labels={"Max": "BMI Range"},
                         color_discrete_map={
                            "#FFC107": "#FFC107",
                            "#28A745": "#28A745",
                            "#DC3545": "#DC3545"
                         })
            
            fig.add_vline(x=bmi, line_dash="dot", 
                          annotation_text=f"Your BMI: {bmi}", 
                          annotation_position="top right")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Please enter valid height and weight values.")

# History section
if show_history and st.session_state.history:
    st.markdown("---")
    st.subheader("Your BMI History")
    
    history_df = pd.DataFrame(st.session_state.history)
    
    # Display history table
    st.dataframe(
        history_df.style.apply(lambda x: [
            'background-color: #d4edda' if x.category == 'Normal weight' 
            else 'background-color: #fff3cd' if x.category == 'Overweight' 
            else 'background-color: #f8d7da'
            for i in x
        ], axis=1),
        use_container_width=True
    )
    
    # Progress chart if enabled
    if show_chart and len(st.session_state.history) > 1:
        st.subheader("BMI Progress Over Time")
        progress_fig = px.line(
            history_df, 
            x="date", 
            y="bmi", 
            markers=True,
            title="Your BMI Trend",
            labels={"date": "Date", "bmi": "BMI"}
        )
        
        # Add healthy range markers
        progress_fig.add_hrect(
            y0=18.5, y1=24.9, 
            fillcolor="green", opacity=0.1,
            annotation_text="Healthy Range", 
            annotation_position="top left"
        )
        
        st.plotly_chart(progress_fig, use_container_width=True)

# Add some health tips
st.markdown("---")
st.subheader("Health Tips")
tips = [
    "🍎 Eat a balanced diet with plenty of fruits and vegetables",
    "💧 Stay hydrated by drinking enough water throughout the day",
    "🏃‍♂️ Get at least 150 minutes of moderate exercise per week",
    "😴 Aim for 7-9 hours of quality sleep each night",
    "🧘‍♀️ Manage stress through meditation or relaxation techniques"
]

for tip in tips:
    st.markdown(f"- {tip}")