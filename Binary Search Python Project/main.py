# 🔍 Binary Search Visualizer (No Matplotlib Version)
import streamlit as st
import time
from typing import List, Dict, Tuple, Optional

# Configure page
st.set_page_config(
    page_title="Binary Search Visualizer",
    page_icon="🔍",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .header { font-size: 2.5em; color: #1f77b4; text-align: center; }
    .subheader { font-size: 1.2em; color: #2ca02c; }
    .success { color: #2ca02c; font-weight: bold; }
    .error { color: #d62728; font-weight: bold; }
    .pointer { font-weight: bold; }
    .left-ptr { color: green; }
    .right-ptr { color: red; }
    .mid-ptr { color: orange; }
    .target-line { border-top: 2px dashed purple; margin: 5px 0; }
    .array-display {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

def binary_search(arr: List[int], target: int) -> Tuple[Optional[int], List[Dict]]:
    """Perform binary search with visualization steps."""
    steps = []
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        current_state = {
            "left": left,
            "right": right,
            "mid": mid,
            "left_val": arr[left],
            "right_val": arr[right],
            "mid_val": arr[mid],
            "target": target,
            "array": arr.copy()
        }
        
        if arr[mid] == target:
            current_state["found"] = True
            steps.append(current_state)
            return mid, steps
        
        current_state["direction"] = "right" if arr[mid] < target else "left"
        left = mid + 1 if arr[mid] < target else left
        right = mid - 1 if arr[mid] > target else right
        
        steps.append(current_state)
    
    return None, steps

def visualize_search(steps: List[Dict], speed: float = 0.5):
    """Enhanced text-based visualization"""
    result_container = st.empty()
    
    for i, step in enumerate(steps):
        # Create visualization
        with st.container():
            st.markdown(f"### Step {i+1}")
            
            # Create array display with pointers
            display = []
            for idx in range(len(step["array"])):
                val = step["array"][idx]
                markers = []
                if idx == step["left"]:
                    markers.append('<span class="left-ptr">L</span>')
                if idx == step["right"]:
                    markers.append('<span class="right-ptr">R</span>')
                if idx == step["mid"]:
                    markers.append('<span class="mid-ptr">M</span>')
                
                if markers:
                    display.append(f"{''.join(markers)}:{val}")
                else:
                    display.append(str(val))
            
            st.markdown("""
            <div class="array-display">
                <strong>Array:</strong> [""" + ", ".join(display) + """]
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="target-line"></div>', unsafe_allow_html=True)
            st.markdown(f"**Target:** {step['target']}")
            
            # Show comparison
            st.markdown(f"""
            - **Comparing:** Middle value {step['mid_val']} vs Target {step['target']}
            - **Range:** Values [{step['left_val']}..{step['right_val']}]
            - **Indices:** Left={step['left']}, Right={step['right']}, Mid={step['mid']}
            """)
            
            if step.get("found"):
                st.success("🎯 Match found!")
            else:
                st.write(f"Moving to the **{step['direction']}** half")
            
            st.write("---")
        
        time.sleep(speed)
    
    # Show final result
    if steps and steps[-1].get("found"):
        result_container.success(f"✅ Found at index {steps[-1]['mid']}!")
    else:
        result_container.error("❌ Target not found")

def main():
    st.markdown('<div class="header">🔍 Binary Search Visualizer</div>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ How to use"):
        st.write("""
        1. Enter a sorted comma-separated list (e.g., `1, 3, 5, 7, 9`)
        2. Enter the target value to find
        3. Adjust animation speed
        4. Click 'Run Search'
        """)
    
    # Input controls
    col1, col2 = st.columns(2)
    with col1:
        arr_input = st.text_input("Sorted array:", "1, 3, 5, 7, 9, 11, 13, 15")
    with col2:
        target = st.number_input("Target value:", value=7)
    
    speed = st.slider("Animation speed:", 0.1, 2.0, 0.5)
    
    if st.button("🚀 Run Binary Search"):
        try:
            # Process input
            arr = [int(x.strip()) for x in arr_input.split(",") if x.strip()]
            
            # Validate input
            if not arr:
                st.error("Please enter some numbers!")
                return
                
            if arr != sorted(arr):
                st.error("Array must be sorted in ascending order!")
                return
            
            # Run search
            st.markdown('<div class="subheader">🔎 Search Process</div>', unsafe_allow_html=True)
            result, steps = binary_search(arr, target)
            
            # Show visualization
            visualize_search(steps, speed)
            
            # Show raw steps
            with st.expander("📝 Detailed Steps"):
                for i, step in enumerate(steps):
                    st.json({
                        "Step": i+1,
                        "Left": f"Index {step['left']} (Value {step['left_val']})",
                        "Right": f"Index {step['right']} (Value {step['right_val']})",
                        "Middle": f"Index {step['mid']} (Value {step['mid_val']})",
                        "Action": "FOUND" if step.get("found") else f"Move {step.get('direction')}"
                    })
                    
        except ValueError:
            st.error("Please enter valid numbers only!")

if __name__ == "__main__":
    main()