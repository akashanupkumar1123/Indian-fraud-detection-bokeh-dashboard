import os
import pandas as pd
from bokeh.models import ColumnDataSource, TableColumn, DataTable, Div, TabPanel
from bokeh.layouts import column

# === Load dashboard summary data ===
base_path = os.path.dirname(os.path.dirname(__file__))
df_summary = pd.read_csv(os.path.join(base_path, "saved_models", "df_dashboard_summary.csv"))
summary_src = ColumnDataSource(df_summary)

# === Table Columns ===
summary_cols = [TableColumn(field=col, title=col) for col in df_summary.columns]
summary_table = DataTable(
    source=summary_src,
    columns=summary_cols,
    width=1000,
    height=300,
    css_classes=["styled-summary-table"]
)

# === Inject Custom CSS for Table + GIF Animation ===
custom_css = """
<style>
    .styled-summary-table .bk-cell {
        font-size: 17px !important;
        font-weight: bold !important;
        color: #003366 !important;
    }
    .styled-summary-table .bk-header {
        background-color: #e6f0ff !important;
        font-size: 18px !important;
        font-weight: bold !important;
        color: #001f4d !important;
    }
    @keyframes softGlow {
        0%   { box-shadow: 0 0 10px #0077ff; }
        50%  { box-shadow: 0 0 25px #0077ff, 0 0 35px #aaddff; }
        100% { box-shadow: 0 0 10px #0077ff; }
    }
</style>
"""
style_injection = Div(text=custom_css)

# === Description / Summary Text ===
summary_text = Div(text="""
<div style="font-size:17px; line-height:1.7; color:#003366; padding: 15px;
background: rgba(255,255,255,0.08); border-radius: 12px;
box-shadow: 0 0 10px rgba(0,0,0,0.1); text-shadow: 0 0 1px #000;">
    <h2 style="color:#002b5c;">📁 Dashboard Summary</h2>
    📊 This section provides an overview of the fraud detection pipeline results.<br>
    🧠 It includes key distributions, counts, and summary metrics captured after predictions.<br>
    🔍 Use this section to interpret global behaviors of the model on the test data.
</div>
""")

# === ML GIF Block (centered + animated glow) ===
ml_gif_block = Div(text="""
<div style="
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 30px 0;
">
  <img src='/bokeh_dashboard/static/ml.gif'
       style="
           width: 480px;
           max-width: 90%;
           height: auto;
           border-radius: 14px;
           animation: softGlow 3s infinite;
       ">
</div>
""")

# === Layout ===
dashboard_summary_page = column(
    style_injection,
    summary_text,
    ml_gif_block,
    summary_table,
    sizing_mode="stretch_both"
)

# === Tab Export ===
summary_tab = TabPanel(child=dashboard_summary_page, title="📁 Dashboard Summary")
