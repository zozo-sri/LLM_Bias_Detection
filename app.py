import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

from evaluator.bias import detect_bias
from evaluator.toxicity import detect_toxicity
from evaluator.factual import check_factual_accuracy
from evaluator.scoring import calculate_safety_score

st.set_page_config(
    page_title="LLM Evaluation Framework",
    page_icon="🌌",
    layout="wide"
)

st.sidebar.title("🌌 LLM Evaluation Framework")

st.sidebar.info("""
This framework evaluates LLM responses based on:

• Bias Detection
• Toxicity Detection
• Factual Accuracy
• Hallucination Risk
• Overall Evaluation Score
""")

st.title("🌌 LLM Evaluation & Bias Detection Framework")
st.caption(
    "Evaluating Large Language Model responses for Bias, Toxicity, "
    "Factual Accuracy, Hallucination Risk, and Overall Evaluation."
)

st.write(
    "Evaluate Large Language Model (LLM) responses for bias, toxicity, "
    "factual accuracy, hallucination risk, and generate an overall evaluation score."
)

prompt = st.text_input("Enter Prompt")

response = st.text_area("Paste LLM Response")

topic = st.text_input(
    "Wikipedia Topic (Example: Isaac Newton)"
)

if st.button("Evaluate"):

    if response.strip() == "":
        st.warning("Please enter an LLM response.")
        st.stop()

    bias = detect_bias(response)

    toxicity = detect_toxicity(response)

    factual = check_factual_accuracy(topic, response)
    hallucination_risk = 100 - factual["accuracy_score"]
    
    safety = calculate_safety_score(
        bias["bias_score"],
        toxicity["toxicity_score"],
        factual["accuracy_score"]
    )

    st.subheader("Evaluation Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Bias Score", bias["bias_score"])
        st.metric("Toxicity Score", toxicity["toxicity_score"])

    with col2:
        st.metric("Accuracy Score", factual["accuracy_score"])
        st.metric("Hallucination Risk", f"{hallucination_risk:.2f}%")
        st.metric("Overall Evaluation Score", safety)

    st.subheader("Overall Evaluation")

    if safety >= 80:
        st.success("🟢 Reliable")

    elif safety >= 60:
        st.warning("🟡 Needs Review")

    else:
        st.error("🔴 High Risk")

    st.subheader("Hallucination Analysis")

    if hallucination_risk <= 20:
       st.success("🟢 Low Hallucination Risk")

    elif hallucination_risk <= 50:
       st.warning("🟡 Moderate Hallucination Risk")

    else:
       st.error("🔴 High Hallucination Risk")

    st.subheader("Evaluation Verdicts")

    col3, col4 = st.columns(2)

    with col3:

        if bias["verdict"] == "Low Bias":
            st.success(f"Bias Verdict : {bias['verdict']}")

        elif bias["verdict"] == "Moderate Bias":
            st.warning(f"Bias Verdict : {bias['verdict']}")

        else:
            st.error(f"Bias Verdict : {bias['verdict']}")

    with col4:

        if toxicity["verdict"] == "Low Toxicity":
            st.success(f"Toxicity Verdict : {toxicity['verdict']}")

        elif toxicity["verdict"] == "Moderately Toxic":
            st.warning(f"Toxicity Verdict : {toxicity['verdict']}")

        else:
            st.error(f"Toxicity Verdict : {toxicity['verdict']}")

    st.subheader("Bias Keywords")

    if bias["keywords"]:
        st.write(", ".join(bias["keywords"]))
    else:
        st.success("No Bias Keywords Detected")

    st.subheader("Toxic Words")

    if toxicity["detected_words"]:
        st.write(", ".join(toxicity["detected_words"]))
    else:
        st.success("No Toxic Words Detected")

    st.subheader("Wikipedia Reference")

    st.write(factual["reference"])

    st.subheader("Evaluation Graph")

    fig, ax = plt.subplots(figsize=(7, 4))

    labels = ["Bias", "Toxicity", "Accuracy", "Hallucination Risk"]

    values = [
        bias["bias_score"],
        toxicity["toxicity_score"],
        factual["accuracy_score"],
        hallucination_risk,
    ]

    bars = ax.bar(labels, values, color=["orange", "red", "green", "blue"])
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score")
    ax.set_title("LLM Response Evaluation Metrices")

    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 2,
            f"{height:.1f}",
            ha="center"
        )

    st.pyplot(fig)

    os.makedirs("reports", exist_ok=True)

    report = pd.DataFrame([{
        "Timestamp": datetime.now(),
        "Prompt": prompt,
        "Response": response,
        "Bias Score": bias["bias_score"],
        "Toxicity Score": toxicity["toxicity_score"],
        "Accuracy Score": factual["accuracy_score"],
        "Hallucination Risk": hallucination_risk,
        "Safety Score": safety,
        "Bias Verdict": bias["verdict"],
        "Toxicity Verdict": toxicity["verdict"]
    }])

    report_path = "reports/report.csv"

    if os.path.exists(report_path):

        try:
            old = pd.read_csv(report_path)
            report = pd.concat(
                [old, report],
                ignore_index=True
            )

        except pd.errors.EmptyDataError:
            pass

    report.to_csv(report_path, index=False)

    st.success("Evaluation report saved successfully!")

    csv = report.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Evaluation Report",
        data=csv,
        file_name="report.csv",
        mime="text/csv"
    )