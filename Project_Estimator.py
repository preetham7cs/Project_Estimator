import streamlit as st
import pandas as pd
import altair as alt

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


def generate_delay_impact(num_team_members, complexity, estimated_days, max_delay=30):
    """Return a DataFrame showing cost and timeline for incremental delays."""
    rows = []
    for delay in range(max_delay + 1):
        cost, timeline = estimate_project_cost(
            num_team_members,
            complexity,
            estimated_days + delay,
        )
        rows.append({
            "Delay Days": delay,
            "Cost": cost,
            "Adjusted Timeline": timeline,
        })
    return pd.DataFrame(rows)

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

    delay_df = generate_delay_impact(num_team_members, complexity, estimated_days)
    delay_chart = (
        alt.Chart(delay_df)
        .transform_fold(["Cost", "Adjusted Timeline"], as_=["Resource", "Value"])
        .mark_line()
        .encode(
            x=alt.X("Delay Days:Q", title="Additional Delay (days)"),
            y=alt.Y("Value:Q", title="Value"),
            color="Resource:N",
        )
    )
    st.altair_chart(delay_chart, use_container_width=True)

except ValueError as e:
    st.error(f"Input Error: {e}")
