import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import cv2
from datetime import datetime

st.set_page_config(page_title="CSRIS - Enhanced Crowd Risk Dashboard", layout="wide")
st.title("🚨 CSRIS - Enhanced Crowd Intelligence System")

# Time Display
st.sidebar.markdown(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Multi-Zone Density Monitoring
st.header("📊 Multi-Zone Live Crowd Density Monitor")
zone_count = st.slider("Number of zones to simulate", 1, 9, 4)
zones_data = []
grid_data = np.zeros((3, 3))

for i in range(zone_count):
    zone_name = f"Zone-{i+1}"
    people = st.number_input(f"{zone_name} - People Count", min_value=0, value=3000, key=f"people_{i}")
    area = st.number_input(f"{zone_name} - Area (m²)", min_value=1, value=1000, key=f"area_{i}")
    density = people / area
    risk_label = "🟢 Safe" if density <= 4 else "🟡 Warning" if density <= 7 else "🔴 High Risk"
    zones_data.append((zone_name, people, area, round(density, 2), risk_label))

    row, col = divmod(i, 3)
    grid_data[row][col] = density

st.subheader("🧮 Zone Risk Table")
df_zones = pd.DataFrame(zones_data, columns=["Zone", "People", "Area (m²)", "Density", "Risk Level"])
st.dataframe(df_zones, use_container_width=True)

# Heatmap
st.subheader("🌡️ Zone-Based Risk Heatmap")
fig_heatmap, ax_heatmap = plt.subplots()
heatmap = ax_heatmap.imshow(grid_data, cmap='hot', interpolation='nearest')
plt.colorbar(heatmap, ax=ax_heatmap, label='Crowd Density')
ax_heatmap.set_title('Multi-Zone Density Heatmap')
st.pyplot(fig_heatmap)

# Simulation Mode
st.header("🎮 Simulation Mode")
simulate = st.checkbox("Enable Simulation")
if simulate:
    sim_time = st.slider("Simulation time steps", 1, 10, 3)
    sim_result = []
    for t in range(sim_time):
        sim_density = np.random.uniform(2, 10, size=(zone_count,))
        sim_result.append(sim_density)
    st.line_chart(pd.DataFrame(sim_result, columns=[f"Zone-{i+1}" for i in range(zone_count)]))

# Post-Incident Playback (Conceptual)
st.header("⏮️ Post-Incident Playback")
st.info("Feature logs crowd density and allows frame-level review. Coming soon!")

# Alert Integration (Placeholder)
st.header("📱 Telegram / WhatsApp Alerts")
st.warning("Integration with alert systems like Telegram or WhatsApp Bots will be implemented with APIs.")

# Guidelines & Summary
st.header("📋 NDMA Guidelines Summary")
st.markdown("""
- Safe: **≤ 4 people/m²**  
- Warning: **4–7 people/m²**  
- High risk: **> 7 people/m²**  

**Recommendations:**  
- Integrate cameras with AI analytics  
- Set up emergency evacuation protocols  
- Auto-alert local emergency responders  
""")
