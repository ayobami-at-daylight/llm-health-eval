import json
import re
import time
from pathlib import Path
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_evaluation_scores(evaluation_text):
    """Extract numerical scores from evaluation text"""
    scores = {}
    
    patterns = {
        'factual_accuracy': r'(?:Factual\s+)?Accuracy:\s*(\d+)',
        'clarity': r'Clarity:\s*(\d+)',
        'neutrality': r'Neutrality:\s*(\d+)',
        'helpfulness': r'Helpfulness:\s*(\d+)'
    }
    
    for criterion, pattern in patterns.items():
        match = re.search(pattern, evaluation_text, re.IGNORECASE)
        if match:
            scores[criterion] = int(match.group(1))
        else:
            scores[criterion] = None
    
    # Extract justification
    justification_match = re.search(r'Justification:\s*(.+)', evaluation_text, re.DOTALL | re.IGNORECASE)
    justification = justification_match.group(1).strip() if justification_match else ""
    
    return scores, justification

def build_evaluation_prompt(question, response, ground_truth):
    """Build prompt for evaluating a specific model response"""
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

AI Response: {response}

Ground Truth Reference: {ground_truth}
"""

def evaluate_with_gpt(prompt):
    """Send evaluation request to GPT"""
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

def restructure_evaluations():
    """Restructure evaluations to include multi-model assessments"""
    
    # Load data
    data_path = Path(__file__).resolve().parent.parent / "data"
    
    with open(data_path / "questions.json") as f:
        questions = json.load(f)
    
    with open(data_path / "evaluations.json") as f:
        current_evaluations = json.load(f)
    
    # Create lookup for existing evaluations
    existing_evaluations = {ev.get("id"): ev for ev in current_evaluations if "id" in ev}
    
    # New structured evaluations
    restructured_evaluations = []
    
    for question in questions:
        question_id = question.get("id")
        question_text = question.get("question")
        ground_truth = question.get("answer")
        ai_responses = question.get("aiResponse", {})
        
        print(f"Processing Question {question_id}: {question_text[:60]}...")
        
        # Initialize evaluation structure
        evaluation_entry = {
            "id": question_id,
            "question": question_text,
            "ground_truth": ground_truth,
            "evaluations": {}
        }
        
        # Process each model response
        for model_name, response in ai_responses.items():
            print(f"  Evaluating {model_name}...")
            
            # Check if we already have an evaluation for this model
            existing_eval = None
            if question_id in existing_evaluations:
                existing_eval = existing_evaluations[question_id]
                # If this is the original single response, use it
                if existing_eval.get("gpt_response") == response:
                    eval_text = existing_eval.get("evaluation")
                    if eval_text:
                        scores, justification = parse_evaluation_scores(eval_text)
                        evaluation_entry["evaluations"][model_name] = {
                            "factual_accuracy": scores["factual_accuracy"],
                            "clarity": scores["clarity"],
                            "neutrality": scores["neutrality"],
                            "helpfulness": scores["helpfulness"],
                            "justification": justification,
                            "response": response
                        }
                        print(f"    Using existing evaluation for {model_name}")
                        continue
            
            # Generate new evaluation
            prompt = build_evaluation_prompt(question_text, response, ground_truth)
            eval_result = evaluate_with_gpt(prompt)
            
            if eval_result:
                scores, justification = parse_evaluation_scores(eval_result)
                evaluation_entry["evaluations"][model_name] = {
                    "factual_accuracy": scores["factual_accuracy"],
                    "clarity": scores["clarity"],
                    "neutrality": scores["neutrality"],
                    "helpfulness": scores["helpfulness"],
                    "justification": justification,
                    "response": response
                }
                print(f"    Generated new evaluation for {model_name}")
            else:
                print(f"    Failed to generate evaluation for {model_name}")
            
            time.sleep(2)  # Rate limiting
        
        restructured_evaluations.append(evaluation_entry)
    
    # Save restructured evaluations
    output_path = data_path / "evaluations_restructured.json"
    with open(output_path, "w") as f:
        json.dump(restructured_evaluations, f, indent=2)
    
    print(f"\n✅ Restructured evaluations saved to: {output_path}")
    print(f"📊 Processed {len(restructured_evaluations)} questions")
    
    # Print summary statistics
    total_evaluations = sum(len(entry["evaluations"]) for entry in restructured_evaluations)
    print(f"📈 Total model evaluations: {total_evaluations}")
    
    return restructured_evaluations

if __name__ == "__main__":
    restructure_evaluations() 