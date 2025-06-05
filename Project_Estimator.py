import streamlit as st

def estimate_project_cost(num_team_members, complexity, estimated_days):
    complexity_multiplier = {
        'Low': 1.0,
        'Medium': 1.5,
        'High': 2.0
    }

    daily_rate_per_member = 300  # Example daily rate per team member

    if complexity not in complexity_multiplier:
        raise ValueError("Complexity must be 'Low', 'Medium', or 'High'")

    cost = num_team_members * daily_rate_per_member * estimated_days * complexity_multiplier[complexity]
    adjusted_timeline = estimated_days * complexity_multiplier[complexity]

    return cost, adjusted_timeline

# Streamlit App UI
st.title("🛠️ Project Cost & Timeline Estimator")

st.sidebar.header("Input Parameters")

complexity = st.sidebar.selectbox(
    "Select Project Complexity:",
    options=["Low", "Medium", "High"]
)

num_team_members = st.sidebar.slider(
    "Number of Team Members:",
    min_value=1,
    max_value=20,
    value=5
)

estimated_days = st.sidebar.slider(
    "Estimated Project Duration (in days):",
    min_value=1,
    max_value=180,
    value=30
)

# Estimate cost and timeline
try:
    total_cost, total_days = estimate_project_cost(num_team_members, complexity, estimated_days)

    st.subheader("📊 Estimated Results")
    st.metric("💰 Project Cost", f"${total_cost:,.2f}")
    st.metric("⏳ Adjusted Timeline", f"{total_days:.1f} days")

except ValueError as e:
    st.error(f"Input Error: {e}")
