import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)
import streamlit as st

from src.retrieval.compliance_engine import (
    get_compliance_answer
)

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Enterprise Compliance Copilot",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------

st.title(
    "Enterprise Compliance Copilot"
)

st.markdown(
    "GraphRAG + Neo4j + FAISS + OpenAI"
)

# -----------------------------
# User Input
# -----------------------------

question = st.text_input(
    "Ask a compliance question"
)

# -----------------------------
# Submit Button
# -----------------------------

if st.button("Submit"):

    if question:

        with st.spinner(
            "Running GraphRAG..."
        ):

            answer, paths, citations = (
                get_compliance_answer(
                    question
                )
            )

        # -----------------------------
        # Answer
        # -----------------------------

        st.success(
            "Answer generated successfully"
        )

        st.subheader(
            "Answer"
        )

        st.write(
            answer
        )

        # -----------------------------
        # Reasoning Paths
        # -----------------------------

        st.subheader(
            "Reasoning Paths"
        )

        for path in paths:

            st.write(
                f"• {path}"
            )

        # -----------------------------
        # Citations
        # -----------------------------

        st.subheader(
            "Citations"
        )

        for citation in citations:

            st.write(
                f"• {citation}"
            )