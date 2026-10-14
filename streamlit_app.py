import io
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.set_page_config(
    page_title="Blank Graph Generator", page_icon="📈", layout="wide"
)

st.title("📊 Student Practice Graph Generator")
st.write(
    "Configure your parameters in the sidebar and download your blank graph instantly."
)

# --- Sidebar Controls ---
st.sidebar.header("Graph Settings")

title = st.sidebar.text_input("Graph Title", "[Graph Title]")
x_label = st.sidebar.text_input("X-Axis Label", "X Values")
y_label = st.sidebar.text_input("Y-Axis Label", "Y Values")

st.sidebar.subheader("Axis Ranges")
col1, col2 = st.sidebar.columns(2)
with col1:
  x_min_str = st.text_input("X Min", "-10")
  y_min_str = st.text_input("Y Min", "-10")
with col2:
  x_max_str = st.text_input("X Max", "10")
  y_max_str = st.text_input("Y Max", "10")

# Safely parse text inputs into numbers with fallback error handling
try:
  x_min = float(x_min_str)
  x_max = float(x_max_str)
  y_min = float(y_min_str)
  y_max = float(y_max_str)
except ValueError:
  st.sidebar.error("⚠️ Please enter valid numbers for axis bounds.")
  st.stop()

if x_min >= x_max or y_min >= y_max:
  st.sidebar.warning("⚠️ Max values must be greater than Min values.")
  st.stop()

st.sidebar.subheader("Grid Settings")
major_interval = st.sidebar.number_input(
    "Major Gridline Interval", min_value=0.1, max_value=100.0, value=5.0
)
minor_subdivisions = st.sidebar.selectbox(
    "Minor Gridlines per Interval", [1, 2, 5], index=1
)

# --- Main Preview Area ---
fig, ax = plt.subplots(figsize=(8, 6))

# Set limits and labels
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_title(title, fontsize=14, fontweight="bold")
ax.set_xlabel(x_label, fontsize=12)
ax.set_ylabel(y_label, fontsize=12)

# Set Major Ticks & Grid (using a robust range step)
major_xticks = np.arange(x_min, x_max + (major_interval * 0.001), major_interval)
major_yticks = np.arange(y_min, y_max + (major_interval * 0.001), major_interval)
ax.set_xticks(major_xticks)
ax.set_yticks(major_yticks)

# Set Minor Ticks & Grid for difficulty adjustment
minor_interval = major_interval / minor_subdivisions
minor_xticks = np.arange(x_min, x_max + (minor_interval * 0.001), minor_interval)
minor_yticks = np.arange(y_min, y_max + (minor_interval * 0.001), minor_interval)
ax.set_xticks(minor_xticks, minor=True)
ax.set_yticks(minor_yticks, minor=True)

# Grid styles
ax.grid(which="major", color="#2b5c8f", linestyle="-", linewidth=0.8)
ax.grid(which="minor", color="#a3c1e0", linestyle=":", linewidth=0.5)

# Center spines (axes lines through 0,0 if within range)
ax.axhline(0, color="black", linewidth=1.2)
ax.axvline(0, color="black", linewidth=1.2)

# Display in Streamlit
st.pyplot(fig)

# --- Export Option ---
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
buf.seek(0)

st.download_button(
    label="📥 Download High-Res Graph (PNG)",
    data=buf,
    file_name="blank_practice_graph.png",
    mime="image/png",
)
