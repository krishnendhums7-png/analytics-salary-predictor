import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Analytics Salary Predictor",
    page_icon="💰",
    layout="wide"
)

# ==================================================
# LOAD FILES
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

jobs = pd.read_csv(
    BASE_DIR / "data" / "processed" / "analytics_jobs.csv"
)

model = joblib.load(
    BASE_DIR / "models" / "salary_predictor.pkl"
)

model_columns = joblib.load(
    BASE_DIR / "models" / "model_columns.pkl"
)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("💰 Salary Predictor")

    page = st.radio(
        "Navigation",
        [
            "Salary Predictor",
            "About Model"
        ]
    )

# ==================================================
# SALARY PREDICTOR PAGE
# ==================================================

if page == "Salary Predictor":

    st.title("💰 Analytics Salary Predictor")

    st.caption(
        "AI-Powered Salary Estimation for Analytics Careers"
    )

    st.markdown("---")

    left, right = st.columns([3, 1])

    # =============================================
    # INPUT SECTION
    # =============================================

    with left:

        st.subheader("Job Information")

        job_title = st.selectbox(
            "Job Title",
            sorted(
                jobs["title"]
                .dropna()
                .unique()
            )
        )

        experience = st.selectbox(
            "Experience Level",
            sorted(
                jobs["formatted_experience_level"]
                .dropna()
                .unique()
            )
        )

        work_type = st.selectbox(
            "Work Type",
            sorted(
                jobs["work_type"]
                .dropna()
                .unique()
            )
        )

        location = st.selectbox(
            "Location",
            sorted(
                jobs["location"]
                .dropna()
                .unique()
            )
        )

        predict = st.button(
            "🚀 Predict Salary",
            use_container_width=True
        )

    # =============================================
    # MODEL INFO
    # =============================================

    with right:

        st.subheader("Model")

        st.metric(
            "Algorithm",
            "Random Forest"
        )

        st.metric(
            "Training Jobs",
            "2,098"
        )

        st.metric(
            "MAE",
            "$25.9K"
        )

        st.metric(
            "R² Score",
            "0.234"
        )

    # =============================================
    # PREDICTION
    # =============================================

    if predict:

        input_df = pd.DataFrame({
            "title": [job_title],
            "formatted_experience_level": [experience],
            "work_type": [work_type],
            "location": [location]
        })

        input_encoded = pd.get_dummies(
            input_df
        )

        input_encoded = input_encoded.reindex(
            columns=model_columns,
            fill_value=0
        )

        prediction = model.predict(
            input_encoded
        )[0]

        st.markdown("---")

        with st.container(border=True):

            st.subheader("💰 Predicted Annual Salary")

            st.markdown(
                f"# ${prediction:,.0f}"
            )

            st.write(f"**Job Title:** {job_title}")
            st.write(f"**Location:** {location}")
            st.write(f"**Experience Level:** {experience}")
            st.write(f"**Work Type:** {work_type}")

        st.caption(
            "Prediction generated using a Random Forest model trained on LinkedIn Analytics job postings."
        )

# ==================================================
# ABOUT PAGE
# ==================================================

if page == "About Model":

    st.title("📊 About The Model")

    st.markdown("---")

    st.subheader("Project Overview")

    st.write("""
This project analyzes LinkedIn job postings and predicts salaries
for analytics-related roles using Machine Learning.
""")

    st.subheader("Dataset")

    st.write("""
- Total LinkedIn Job Postings: 123,849
- Analytics Jobs Identified: 2,098
- Salary Records Used for Training: 435
""")

    st.subheader("Features Used")

    st.write("""
- Job Title
- Experience Level
- Work Type
- Location
""")

    st.subheader("Model Performance")

    st.write("""
**Random Forest Regressor**

- Mean Absolute Error (MAE): $25,882
- R² Score: 0.234

The Random Forest model outperformed Linear Regression and was selected as the final model.
""")

    st.subheader("Technology Stack")

    st.write("""
- Python
- Pandas
- NumPy
- Scikit-Learn
- Streamlit
- Jupyter Notebook
""")

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Developed by Krishnendhu M S"
)