import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, project_root)
import pandas as pd

from src.retrieval.compliance_engine import (
    get_compliance_answer
)

# -----------------------------
# Load Evaluation Questions
# -----------------------------

questions = pd.read_csv(
    "evaluation/questions.csv"
)

results = []

# -----------------------------
# Run Evaluation
# -----------------------------

for index, row in questions.iterrows():

    question = row["question"]
    ground_truth = row["ground_truth"]

    print("=" * 80)
    print(f"Question {index + 1}")
    print("=" * 80)

    print("QUESTION:")
    print(question)

    print("\nGENERATING ANSWER...\n")

    answer, paths, citations = (
        get_compliance_answer(
            question
        )
    )

    print("ANSWER:")
    print(answer)

    print("\nGROUND TRUTH:")
    print(ground_truth)

    print("\nREASONING PATHS:")

    for path in paths:
        print("-", path)

    print("\nCITATIONS:")

    for citation in citations:
        print("-", citation)

    results.append(
        {
            "question": question,
            "ground_truth": ground_truth,
            "answer": answer,
            "reasoning_paths": " | ".join(paths),
            "citations": " | ".join(citations)
        }
    )

# -----------------------------
# Save Results
# -----------------------------

results_df = pd.DataFrame(
    results
)

results_df.to_csv(
    "evaluation/results.csv",
    index=False
)

print("\n")
print("=" * 80)
print("EVALUATION COMPLETE")
print("=" * 80)

print(
    "Results saved to evaluation/results.csv"
)