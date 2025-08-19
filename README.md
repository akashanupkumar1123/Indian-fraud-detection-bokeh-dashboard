# Indian Fraud Detection Dashboard

![Indian Fraud Detection Dashboard](./fraud_banner.png)

🚀 **Live Demo:** [Click here to view the dashboard](https://indian-fraud-detection-dashboard23.onrender.com/bokeh_dashboard)

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)]()
[![Bokeh](https://img.shields.io/badge/Bokeh-v3.0-orange)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Deployed%20on%20Render-brightgreen)](https://indian-fraud.herokuapp.com/)

An interactive **Bokeh** dashboard for detecting fraudulent financial transactions in India. It provides real-time classification and performance metrics visualization. Designed for easy deployment via **Render.com**.

---



##  Project Overview

This project delivers a clean, intuitive dashboard using **Bokeh Server**, enabling users to:

- Input transaction data and receive instantaneous fraud predictions.
- View **model performance metrics**, including accuracy and confusion matrix.
- Explore **visualizations** of fraud patterns and feature importances.

---

##  Features

- **Real-time prediction** using a trained ML model.
- Interactive visualizations with **Bokeh's dynamic plots**.
- **Auto-updating statistics** on classification performance.
- Quick deployment setup with Render's free tier.
---

##  Getting Started

### Prerequisites

- Python 3.10 or higher
- A GitHub account (to connect with Render)

### Local Setup

1. **Clone the repo**:
    ```bash
    git clone https://github.com/akashanupkumar1123/indian-fraud-detection-dashboard.git
    cd indian-fraud-detection-dashboard
    cd bokeh_dashboard
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the dashboard locally**:
    ```bash
    bokeh serve --show main.py
    ```
    This will launch the dashboard at `http://localhost:5006/main`.

---

##  Deploy on Render (Free Tier)

Render offers an easy and free way to host your Bokeh app:

1. **Push your repo to GitHub** with the `bokeh_dashboard` folder at the root.
2. Log in at [Render.com](https://render.com/) and click **New → Web Service**.
3. Link your GitHub repository and select the `bokeh_dashboard/main.py` as the entry point.
4. Set the **Build Command**:
    ```
    pip install -r requirements.txt
    ```
5. Set the **Start Command**:
    ```
    bokeh serve --port 10000 --address 0.0.0.0 main.py
    ```
6. Deploy! Render gives you a public `.onrender.com` URL with HTTPS.

---

##  Screenshots

*(Add here a few snapshots or GIFs demonstrating the dashboard's UI, prediction flow, and charts.)*

---

##  Future Enhancements

- Integrate **SHAP** or **LIME** analyses for explainability.
- Add **model comparison tabs** (e.g., XGBoost vs. Isolation Forest).
- Enable **CSV upload for batch scoring**.
- Package with **Docker** for consistent, reproducible deployment.
- Add **authentication** or user login for restricted access.

---

##  License

Distributed under the MIT License. See `LICENSE` for more details.

---

##  Contact & Feedback

Built by **Akash Anup Kumar** — love to hear your thoughts!

Feel free to open an issue, submit a PR, or connect via LinkedIn or email for feedback or collaboration.

---


