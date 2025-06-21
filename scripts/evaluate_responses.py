import openai
import json
import time
import os
from pathlib import Path
import nltk
from dotenv import load_dotenv

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from nltk.tokenize import word_tokenize

# Load environment variables from .env file
load_dotenv()

nltk.download("punkt")

# ✅ Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please create a .env file with your API key.")

# ✅ Function to build the evaluation prompt
def build_prompt(question, gpt_response, ground_truth):
    return f"""
You are an evaluator assessing an AI-generated health response.

Using a 1 to 5 scale, evaluate the response based on:
1. Factual Accuracy – Is the response factually correct compared to the ground truth?
2. Clarity – Is the response clearly written and easy to understand?
3. Neutrality – Is it unbiased and culturally sensitive?
4. Helpfulness – Does it provide useful and safe information?

Respond in the format:
Factual Accuracy: X
Clarity: Y
Neutrality: Z
Helpfulness: W
Justification: <brief explanation>

---

Question: {question}

GPT-Generated Response: {gpt_response}

Ground Truth Reference: {ground_truth}
"""

# ✅ Function to send request to GPT
def evaluate_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during evaluation: {e}")
        return None

# ✅ Load data
def load_data():
    base = Path(__file__).resolve().parent.parent / "data"
    with open(base / "questions.json") as f:
        questions = json.load(f)
    with open(base / "gpt_responses.json") as f:
        responses = json.load(f)
    with open(base / "ground_truth.json") as f:
        ground_truth = json.load(f)
    with open(base / "evaluations.json") as f:
        evaluations = json.load(f)
    return questions, responses, ground_truth, evaluations


def compute_rouge_bleu(reference, generated):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)

    ref_tokens = word_tokenize(reference.lower())
    gen_tokens = word_tokenize(generated.lower())
    bleu_score = sentence_bleu([ref_tokens], gen_tokens, smoothing_function=SmoothingFunction().method1)

    return {
        "rouge1": scores["rouge1"].fmeasure,
        "rougeL": scores["rougeL"].fmeasure,
        "bleu": bleu_score
    }


# ✅ Main script
if __name__ == "__main__":
    questions, responses, truths, evaluations = load_data()
    results = []

    for i in range(len(questions)):
        id = questions[i].get("id")
        q = questions[i].get("question")
        r = questions[i].get("response")
        gt = questions[i].get("answer")

        print(f"Evaluating Q{i + 1}: {q[:60]}...")
        # Skip if missing data or already evaluated
        if not q or not r or not gt:
            print(f"Skipping Q{i + 1} due to missing data...")
            continue
        if any(ev.get("id") == id for ev in evaluations):
            print(f"Skipping Q{i + 1} (already evaluated)")
            continue

        prompt = build_prompt(q, r, gt)
        eval_result = evaluate_with_gpt(prompt)
        # metric_scores = compute_rouge_bleu(gt, r)


        if eval_result:
            results.append({
                "id": id,
                "question": q,
                "gpt_response": r,
                "ground_truth": gt,
                "evaluation": eval_result,
                # "metrics": {
                #     "rouge1": round(metric_scores["rouge1"], 3),
                #     "rougeL": round(metric_scores["rougeL"], 3),
                #     "bleu": round(metric_scores["bleu"], 3)
                # }
            })

        time.sleep(2)  # To avoid rate limiting

    # ✅ Save evaluations
    out_path = Path(__file__).resolve().parent.parent / "data" / "evaluations.json"

    # Build a dict for fast lookup by id
    evals_by_id = {ev.get("id"): ev for ev in evaluations if "id" in ev}

    # Update or add new results by id
    for res in results:
        evals_by_id[res["id"]] = res

    # Write back the updated list
    updated_evals = list(evals_by_id.values())
    with open(out_path, "w") as f:
        json.dump(updated_evals, f, indent=2)

    print(f"\n✅ Evaluations saved to: {out_path}")
