# main.py

from bokeh.io import curdoc
from bokeh.models import Div, Tabs
from tabs.fraud_tab import fraud_tab
from tabs.metrics_tab import metrics_tab
from tabs.summary_tab import summary_tab

# === CSS + HTML Background ===
background_html = """
<style>
html, body {
  background-color: #ffe6f0 !important;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.bk-root {
  background-color: transparent !important;
  font-family: 'Segoe UI', sans-serif;
  font-weight: bold;
  padding-top: 100px;
  color: #333 !important;
}

/* Floating Emojis */
@keyframes floatEmoji {
  0%   { transform: translateY(0); opacity: 0.3; }
  100% { transform: translateY(-100vh); opacity: 0; }
}
.floating-emoji {
  position: fixed;
  bottom: 0;
  font-size: 42px;
  animation: floatEmoji 16s linear infinite;
  z-index: -5;
  opacity: 0.2;
  filter: blur(1px);
  pointer-events: none;
}
.floating-emoji:nth-child(1) { left: 12%; animation-delay: 0s; }
.floating-emoji:nth-child(2) { left: 30%; animation-delay: 5s; }
.floating-emoji:nth-child(3) { left: 55%; animation-delay: 10s; }
.floating-emoji:nth-child(4) { left: 80%; animation-delay: 2s; }

/* Top Navbar */
.top-nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px 20px;
  z-index: 999;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
}

/* Glowing Header */
@keyframes glow {
  0% { text-shadow: 0 0 5px #fff; }
  50% { text-shadow: 0 0 20px #00f, 0 0 30px #0ff; }
  100% { text-shadow: 0 0 5px #fff; }
}
.glow-text {
  font-size: 26px;
  font-weight: bold;
  color: #000;
  text-align: center;
  animation: glow 3s ease-in-out infinite;
  padding-top: 60px;
}
</style>

<!-- Floating Emojis -->
<div class="floating-emoji">💸</div>
<div class="floating-emoji">🚨</div>
<div class="floating-emoji">📈</div>
<div class="floating-emoji">🧠</div>

<!-- Top Navbar -->
<div class="top-nav">
  <div><b>💼 FraudAI Dashboard</b></div>
  <div><i>Powered by XGBoost + Isolation Forest + Bokeh</i></div>
</div>

<!-- Glowing Header -->
<div class="glow-text">📊 Real-Time Fraud Detection System</div>
"""

# === Optional: Sample GIF Test Div ===
test_gif = Div(text="""
<div style="text-align:center; margin-top:30px;">
  <img src="static/fraud_alert.gif" style="max-width:50%; border-radius:10px;">
  <p style="font-size:14px; color:#444;">(Sample GIF test from /static/ folder)</p>
</div>
""")

# === Inject Background & Add Tabs ===
curdoc().add_root(Div(text=background_html))
# curdoc().add_root(test_gif)  # Uncomment to test gif rendering
curdoc().add_root(Tabs(tabs=[fraud_tab, metrics_tab, summary_tab], sizing_mode="stretch_both"))
curdoc().title = "Fraud Detection Dashboard"
