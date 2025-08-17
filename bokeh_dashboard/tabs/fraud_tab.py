import os
import pandas as pd
import numpy as np
import joblib
from math import pi
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Slider, Button, Div, Select, TabPanel
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.transform import cumsum

# === Base Path ===
base_path = os.path.dirname(os.path.dirname(__file__))

# === Load Models & Data ===
X_test_no_iso = joblib.load(os.path.join(base_path, "saved_models", "X_test_scaled.pkl"))
X_test_with_iso = joblib.load(os.path.join(base_path, "saved_models", "X_test_with_iso.pkl"))
model_no_iso = joblib.load(os.path.join(base_path, "saved_models", "xgb_model_without_iso.pkl"))
model_with_iso = joblib.load(os.path.join(base_path, "saved_models", "xgb_model_with_iso_thresh_0033.pkl"))
y_test = joblib.load(os.path.join(base_path, "saved_models", "y_test.pkl"))

# === Default Theme ===
curdoc().theme = "dark_minimal"

# === Feature Setup ===
input_feature_map = {
    "Time of Day (Encoded)": "hour_sin",
    "Time Pattern": "hour_cos",
    "Time Slot": "hour_category",
    "Transaction Hour": "transaction_hour",
    "Sender History": "sender_txn_count",
    "Weekend Transaction?": "is_weekend",
    "Receiver Activity": "receiver_txn_count"
}

# === Full feature lists ===
feature_list_with_iso = [
    'transaction_type', 'amount', 'location_sender', 'location_receiver',
    'device_type', 'is_international', 'transaction_hour', 'hour', 'dayofweek',
    'day', 'is_weekend', 'is_night', 'hour_sin', 'hour_cos', 'log_amount',
    'is_high_amount', 'same_location', 'hour_category', 'sender_txn_count',
    'receiver_txn_count', 'any_numeric_outlier', 'amount_z', 'amount_outlier',
    'amount_capped', 'iso_score', 'iso_flag'
]

feature_list_no_iso = feature_list_with_iso.copy()
feature_list_no_iso.remove('iso_score')
feature_list_no_iso.remove('iso_flag')

# === Default Values ===
default_values = {f: 0 for f in feature_list_with_iso}
default_values.update({
    "same_location": 1,
    "transaction_hour": 10,
    "is_weekend": 0,
    "any_numeric_outlier": 0
})

# === Classification ===
def classify(probs, threshold):
    return (probs >= threshold).astype(int)

# === UI Elements ===
model_select = Select(title="Choose Model", value="XGBOOST_Without_ISO", options=["XGBOOST_Without_ISO", "XGBOOST_With_ISO"])
threshold_slider = Slider(start=0.0, end=1.0, step=0.01, value=0.5, title="Classification Threshold")
source = ColumnDataSource(data=dict(index=[], y_true=[], y_prob=[], y_pred=[]))

# === Fraud Probability Plot ===
plot = figure(title="Fraud Probability", x_axis_label='Index', y_axis_label='Probability', height=300, width=700)
plot.scatter(x='index', y='y_prob', source=source, size=6, color="#f54291", alpha=0.6)

# === Pie Chart ===
fraud_ratio = sum(y_test) / len(y_test)
pie_data = pd.Series({'Fraud': fraud_ratio, 'Legit': 1 - fraud_ratio}).reset_index(name='value')
pie_data = pie_data.rename(columns={'index': 'type'})
pie_data['angle'] = pie_data['value'] * 2 * pi
pie_data['color'] = ['#f54242', '#42f54e']
pie_chart = figure(height=250, title="Fraud vs Legit Distribution", toolbar_location=None,
                   tools="hover", tooltips="@type: @value", x_range=(-0.5, 1.0))
pie_chart.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True),
                end_angle=cumsum('angle'),
                line_color="white", fill_color='color',
                legend_field='type', source=ColumnDataSource(pie_data))

# === Data Table ===
columns = [
    TableColumn(field="index", title="Index"),
    TableColumn(field="y_true", title="Actual"),
    TableColumn(field="y_pred", title="Predicted"),
    TableColumn(field="y_prob", title="Probability")
]
data_table = DataTable(source=source, columns=columns, width=800, height=250)

# === Dropdown Input Widgets ===
input_widgets = {
    "Time of Day (Encoded)": Select(title="Time of Day (Encoded)", value="0.0", options=["0.0", "0.5", "1.0"]),
    "Time Pattern": Select(title="Time Pattern", value="0.0", options=["-1.0", "0.0", "1.0"]),
    "Time Slot": Select(title="Time Slot", value="Morning", options=["Morning", "Afternoon", "Evening", "Night"]),
    "Transaction Hour": Select(title="Transaction Hour", value="10", options=[str(i) for i in range(24)]),
    "Sender History": Select(title="Sender History", value="5", options=["1", "5", "10", "20", "50"]),
    "Weekend Transaction?": Select(title="Weekend Transaction?", value="No", options=["Yes", "No"]),
    "Receiver Activity": Select(title="Receiver Activity", value="5", options=["1", "5", "10", "20", "50"])
}

input_tooltips = {
    "Time of Day (Encoded)": "⏰ Encoded sine value of time (0 = midnight, 0.5 = noon)",
    "Time Pattern": "🔄 Cosine encoding: -1 = early morning, 1 = late night",
    "Time Slot": "🕒 Time category of transaction",
    "Transaction Hour": "📆 Exact hour of transaction (0 to 23)",
    "Sender History": "📤 Transactions sent by this user before",
    "Weekend Transaction?": "📅 Did it happen on weekend?",
    "Receiver Activity": "📥 Past transactions received"
}

row_inputs, temp_row = [], []
for label, widget in input_widgets.items():
    tooltip_div = Div(text=f"<div style='font-size:13px; color:#ccc;'>{input_tooltips[label]}</div>")
    temp_row.append(column(tooltip_div, widget))
    if len(temp_row) == 3:
        row_inputs.append(row(*temp_row))
        temp_row = []
if temp_row:
    row_inputs.append(row(*temp_row))

# === Predict Button ===
predict_button = Button(label="🔍 Predict Transaction", button_type="success")
prediction_result = Div(text="<b>Prediction:</b> Not available")

# === Prediction Update ===
def update_data():
    threshold = threshold_slider.value
    model = model_no_iso if model_select.value == "XGBOOST_Without_ISO" else model_with_iso
    X = X_test_no_iso if model_select.value == "XGBOOST_Without_ISO" else X_test_with_iso
    probs = model.predict_proba(X)[:, 1]
    preds = classify(probs, threshold)
    source.data = {"index": list(range(len(y_test))), "y_true": y_test, "y_prob": probs, "y_pred": preds}

# === Predict Logic ===
def make_prediction():
    try:
        input_data = default_values.copy()
        for readable, widget in input_widgets.items():
            feature = input_feature_map[readable]
            val = widget.value
            val = 1 if val == "Yes" else 0 if val == "No" else ["Morning", "Afternoon", "Evening", "Night"].index(val) if val in ["Morning", "Afternoon", "Evening", "Night"] else float(val)
            input_data[feature] = val

        model = model_with_iso if model_select.value == "XGBOOST_With_ISO" else model_no_iso
        features = feature_list_with_iso if model_select.value == "XGBOOST_With_ISO" else feature_list_no_iso
        input_df = pd.DataFrame([[input_data[f] for f in features]], columns=features)

        prob = model.predict_proba(input_df)[0, 1]
        threshold = threshold_slider.value
        label = "🔴 Fraud" if prob >= threshold else "✅ Legit"

        if label == "🔴 Fraud":
            emoji = "🚨"
            color = "#ff0033"
            msg = "⚠️ Suspicious Transaction Detected!"
        else:
            emoji = "🟢"
            color = "#33cc33"
            msg = "✅ Transaction Looks Safe"

        prediction_result.text = f"""
        <div style="font-size:18px; padding:15px; border-radius:10px; 
                    background: {color}20; border-left: 6px solid {color};
                    color: {color}; font-weight:bold;">
            {emoji} <b>{label}</b><br>
            <span style="font-size:16px;">🔢 <b>Probability:</b> {prob:.3f}</span><br>
            <span style="font-size:14px;">{msg}</span>
        </div>
        """
    except Exception as e:
        prediction_result.text = f"<b style='color:red;'>❌ Error:</b> {str(e)}"


# === Events ===
threshold_slider.on_change("value", lambda attr, old, new: update_data())
model_select.on_change("value", lambda attr, old, new: update_data())
predict_button.on_click(make_prediction)
update_data()

# === Layout ===
summary_text = """
<div>
  <h2 style='color:#00ccff;'>🚨 Fraud Detection Dashboard</h2>
  <p style='font-size:17px; color:#0f52ba; line-height:1.6;'>
    ✔️ <b>XGBOOST_Without_ISO</b>: SMOTE-balanced high precision.<br>
    🔍 <b>XGBOOST_With_ISO</b>: Isolation Forest + threshold = 0.033 (recall focused)<br>
    🧠 Use smart <b>7-input form</b> to simulate predictions.
  </p>
</div>
"""

fraud_dashboard = column(
    Div(text=summary_text),
    row(model_select, threshold_slider),
    plot,
    pie_chart,
    data_table,
    Div(text="<h3 style='color:#00ffaa;'>🧪 Real-Time Prediction</h3>"),
    column(*row_inputs),
    predict_button,
    prediction_result,
    sizing_mode="stretch_both"
)

fraud_tab = TabPanel(child=fraud_dashboard,title="📊 Fraud Detection")