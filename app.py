import streamlit as st
import pandas as pd
import time

# -------------------- TIME FORMAT FUNCTION --------------------
def format_hour(hour):
    if hour == 0:
        return "12 AM"
    elif hour < 12:
        return f"{hour} AM"
    elif hour == 12:
        return "12 PM"
    else:
        return f"{hour-12} PM"

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="⚡ EV Smart Scheduler", layout="wide")

# -------------------- WOW CSS --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Glass cards */
.metric-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Hover effect */
.metric-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0px 10px 30px rgba(0,255,200,0.2);
}

/* Text */
.big-font {
    font-size: 22px !important;
    font-weight: bold;
}

/* Fade animation */
.fade-in {
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# -------------------- LOADING EFFECT --------------------
with st.spinner("⚡ Optimizing charging schedule..."):
    time.sleep(1)

# -------------------- SIDEBAR --------------------
st.sidebar.title("⚙️ Controls")

charging_rate = st.sidebar.slider("⚡ Charging Speed (% per hour)", 10, 50, 20)

st.sidebar.markdown("---")

# -------------------- 🚐 INPUT --------------------
st.sidebar.subheader("🚐 Fleet Manager")

if "fleet_data" not in st.session_state:
    st.session_state.fleet_data = [
        {"Vehicle_ID": "Van_1", "Current_Battery_Pct": 20, "Required_Battery_Pct": 80}
    ]

if st.sidebar.button("➕ Add Vehicle"):
    st.session_state.fleet_data.append({
        "Vehicle_ID": f"Van_{len(st.session_state.fleet_data)+1}",
        "Current_Battery_Pct": 20,
        "Required_Battery_Pct": 80
    })

if st.sidebar.button("❌ Remove Last Vehicle") and len(st.session_state.fleet_data) > 1:
    st.session_state.fleet_data.pop()

if st.sidebar.button("⚡ Load Sample Fleet"):
    st.session_state.fleet_data = [
        {"Vehicle_ID": "Van_1", "Current_Battery_Pct": 10, "Required_Battery_Pct": 90},
        {"Vehicle_ID": "Van_2", "Current_Battery_Pct": 40, "Required_Battery_Pct": 80},
        {"Vehicle_ID": "Van_3", "Current_Battery_Pct": 60, "Required_Battery_Pct": 100},
    ]

st.sidebar.markdown("---")

updated_data = []

for i, v in enumerate(st.session_state.fleet_data):
    st.sidebar.markdown(f"### 🚐 Vehicle {i+1}")

    vid = st.sidebar.text_input(f"ID {i}", v["Vehicle_ID"], key=f"id_{i}")
    cur = st.sidebar.slider(f"Current % {i}", 0, 100, v["Current_Battery_Pct"], key=f"cur_{i}")
    req = st.sidebar.slider(f"Required % {i}", 0, 100, v["Required_Battery_Pct"], key=f"req_{i}")

    updated_data.append({
        "Vehicle_ID": vid,
        "Current_Battery_Pct": cur,
        "Required_Battery_Pct": req
    })

st.session_state.fleet_data = updated_data
fleet_df = pd.DataFrame(updated_data)

st.sidebar.success(f"Total Vehicles: {len(fleet_df)} 🚐")

# -------------------- PRICE DATA --------------------
prices_df = pd.DataFrame({
    "Hour": list(range(24)),
    "Price_per_kWh": [
        0.25,0.25,0.20,0.20,0.15,0.10,0.08,0.05,0.05,0.05,
        0.08,0.10,0.12,0.15,0.18,0.22,0.25,0.30,0.28,0.26,
        0.24,0.22,0.20,0.18
    ]
})

prices_df = prices_df.sort_values(by="Price_per_kWh")

# -------------------- LOGIC --------------------
def calculate_schedule(fleet_df, prices_df, rate):
    schedule = []
    total_optimized_cost = 0
    total_normal_cost = 0

    for _, row in fleet_df.iterrows():
        needed = row['Required_Battery_Pct'] - row['Current_Battery_Pct']
        hours_needed = max(1, int(needed / rate))

        cheapest = prices_df.head(hours_needed)
        cheapest_hours = sorted(cheapest['Hour'].tolist())

        optimized_cost = cheapest['Price_per_kWh'].sum()
        normal_cost = prices_df['Price_per_kWh'].mean() * hours_needed

        total_optimized_cost += optimized_cost
        total_normal_cost += normal_cost

        formatted_hours = [format_hour(h) for h in cheapest_hours]

        is_continuous = all(
            cheapest_hours[i] + 1 == cheapest_hours[i+1]
            for i in range(len(cheapest_hours) - 1)
        )

        if len(cheapest_hours) > 1 and is_continuous:
            best_time_display = f"{format_hour(cheapest_hours[0])} → {format_hour(cheapest_hours[-1])}"
        else:
            best_time_display = ", ".join(formatted_hours)

        schedule.append({
            "Vehicle": row['Vehicle_ID'],
            "Hours": hours_needed,
            "Best Hours": best_time_display,
            "Battery Needed (%)": needed,
            "Cost": round(optimized_cost, 2)
        })

    return pd.DataFrame(schedule), total_optimized_cost, total_normal_cost

result, opt_cost, normal_cost = calculate_schedule(fleet_df, prices_df, charging_rate)

# -------------------- HEADER --------------------
st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background: linear-gradient(135deg, #1e293b, #020617);
margin-bottom:20px;
">
<h1 style="margin:0;">⚡ EcoCharge Dashboard</h1>
<p style="color:#94a3b8;">Smart EV Charging Optimization System</p>
</div>
""", unsafe_allow_html=True)

# -------------------- METRICS --------------------
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='metric-card fade-in'><p class='big-font'>🚐 Vehicles</p><h2>{len(fleet_df)}</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-card fade-in'><p class='big-font'>⚡ Avg Price</p><h2>{prices_df['Price_per_kWh'].mean():.2f}</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-card fade-in'><p class='big-font'>💸 Cheapest</p><h2>{prices_df['Price_per_kWh'].min():.2f}</h2></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-card fade-in'><p class='big-font'>🔥 Peak</p><h2>{prices_df['Price_per_kWh'].max():.2f}</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------- BEST TIME BANNER --------------------
cheapest = prices_df.iloc[0]
best_time = format_hour(int(cheapest['Hour']))

st.markdown(f"""
<div style='
background: linear-gradient(90deg, #22c55e, #4ade80);
padding: 15px;
border-radius: 12px;
color: black;
font-weight: bold;
text-align: center;
'>
💡 Best Time to Charge: {best_time} ⚡
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -------------------- CHART --------------------
st.subheader("📊 Electricity Price Curve")
st.area_chart(prices_df.set_index("Hour"))

st.markdown("---")

# -------------------- TABLES --------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚐 Fleet Overview")
    st.dataframe(fleet_df, use_container_width=True, height=300)

with col2:
    st.subheader("⚡ Smart Schedule")
    st.dataframe(result, use_container_width=True, height=300)

st.markdown("---")

# -------------------- COST --------------------
st.subheader("💰 Smart Cost Comparison")

c1, c2, c3 = st.columns(3)

c1.metric("⚡ Optimized Cost", f"{opt_cost:.2f}")
c2.metric("📊 Normal Cost", f"{normal_cost:.2f}")

savings = ((normal_cost - opt_cost) / normal_cost) * 100 if normal_cost != 0 else 0
c3.metric("💸 Savings %", f"{savings:.1f}%")

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("Team Techies 🚀")