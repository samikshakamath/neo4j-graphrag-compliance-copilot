import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv

import os

# -----------------------------
# Load OpenAI
# -----------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)

# -----------------------------
# Load Results
# -----------------------------

df = pd.read_csv(
    "evaluation/results.csv"
)

evaluation_results = []

# -----------------------------
# Evaluate Each Answer
# -----------------------------

for index, row in df.iterrows():

    question = row["question"]
    ground_truth = row["ground_truth"]
    answer = row["answer"]

    print(
        f"\nEvaluating Question {index+1}"
    )

    prompt = f"""
You are evaluating a compliance AI system.

Question:
{question}

Ground Truth:
{ground_truth}

Generated Answer:
{answer}

Score the answer on:

1. Correctness (1-5)
2. Completeness (1-5)
3. Grounding (1-5)

Grounding means:
Does the answer stay close to the expected facts?

Return ONLY:

Correctness: X
Completeness: X
Grounding: X
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    evaluation = (
        response
        .choices[0]
        .message
        .content
    )

    print(evaluation)

    evaluation_results.append(
        {
            "question": question,
            "evaluation": evaluation
        }
    )

# -----------------------------
# Save Results
# -----------------------------

pd.DataFrame(
    evaluation_results
).to_csv(
    "evaluation/evaluation_report.csv",
    index=False
)

print("\n")
print("=" * 60)
print("EVALUATION COMPLETE")
print("=" * 60)

print(
    "Saved to evaluation/evaluation_report.csv"
)