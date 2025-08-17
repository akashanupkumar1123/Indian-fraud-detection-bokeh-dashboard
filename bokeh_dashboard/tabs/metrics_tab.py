import os
import pandas as pd
from bokeh.models import ColumnDataSource, TableColumn, DataTable, Div, TabPanel
from bokeh.layouts import column

# === Load metrics data ===
base_path = os.path.dirname(os.path.dirname(__file__))
metrics_summary = pd.read_csv(os.path.join(base_path, "saved_models", "metrics_summary.csv"))
metrics_src = ColumnDataSource(metrics_summary)

# === Define Table Columns ===
metric_cols = [TableColumn(field=col, title=col) for col in metrics_summary.columns]

# === Custom CSS Styles for Table and GIF Animation ===
custom_css = """
<style>
    .styled-metrics-table .bk-cell {
        font-size: 17px !important;
        font-weight: bold !important;
        color: #003366 !important;
    }
    .styled-metrics-table .bk-header {
        background-color: #f0f8ff !important;
        font-size: 18px !important;
        font-weight: bold !important;
        color: #002244 !important;
    }

    @keyframes glowPulse {
        0%   { box-shadow: 0 0 10px #ff5555; }
        50%  { box-shadow: 0 0 25px #ff5555, 0 0 35px #ff9999; }
        100% { box-shadow: 0 0 10px #ff5555; }
    }
</style>
"""
style_div = Div(text=custom_css)

# === Page Title ===
header = Div(text="""
<div style="font-size:26px; color:#002b5c; font-weight:bold; margin-top:10px; margin-bottom:8px;
text-align:center; text-shadow: 0 0 2px #000;">
📋 <u>Model Metrics Summary</u>
</div>
""")

# === Styled Data Table ===
metrics_table = DataTable(
    source=metrics_src,
    columns=metric_cols,
    width=950,
    height=280,
    css_classes=["styled-metrics-table"]
)

# === Fraud Alert GIF Block ===
fraud_gif_block = Div(text="""
<div style="
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 30px 0;
">
  <img src='/bokeh_dashboard/static/fraud_alert.gif'
       style="
           width: 500px;
           max-width: 90%;
           height: auto;
           border-radius: 16px;
           animation: glowPulse 3s infinite;
       ">
</div>
""")

# === Insight Box ===
insight_html = """
<div style="font-size:17px; color:#004080; line-height:1.7; margin-top:25px;
background: rgba(255,255,255,0.08); padding: 20px; border-radius: 12px;
box-shadow: 0 0 10px rgba(0,0,0,0.2); text-shadow: 0 0 1px #000;">
<h2 style="color:#003366;">📌 Model Insight Summary</h2>
✅ <b>XGBOOST_Without_ISO</b>: High Precision — fewer false positives.<br>
🔍 <b>XGBOOST_With_ISO</b>: High Recall — better fraud coverage, more alerts.<br>
⚠️ ISO model may raise false alarms — manual validation recommended.<br>
📊 Use models depending on business goals: precision vs recall.
</div>
"""

# === Final Layout ===
metrics_page = column(
    style_div,
    header,
    metrics_table,       # Table comes first
    fraud_gif_block,     # GIF comes after table
    Div(text=insight_html),  # Then insight text
    sizing_mode="stretch_both"
)

# === Export as Tab ===
metrics_tab = TabPanel(child=metrics_page, title="📋 Metrics Summary")
