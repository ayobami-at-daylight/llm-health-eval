import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import openai
import time
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

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
    
    return scores

def generate_response_with_model(question, model_name):
    """Generate response using specified model"""
    try:
        if "gpt" in model_name.lower():
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful health information assistant. Provide accurate, evidence-based responses to health-related questions. Be concise but informative."},
                    {"role": "user", "content": question}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        else:
            # Placeholder for other models (Claude, Gemini, etc.)
            return f"Response from {model_name} would go here"
    except Exception as e:
        print(f"Error generating response with {model_name}: {e}")
        return ""

def evaluate_response_with_model(question, response, ground_truth, evaluator_model):
    """Evaluate response using specified model as evaluator"""
    prompt = f"""
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

AI-Generated Response: {response}

Ground Truth Reference: {ground_truth}
"""
    
    try:
        if "gpt" in evaluator_model.lower():
            eval_response = openai.ChatCompletion.create(
                model=evaluator_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return eval_response.choices[0].message.content.strip()
        else:
            return f"Evaluation from {evaluator_model} would go here"
    except Exception as e:
        print(f"Error evaluating with {evaluator_model}: {e}")
        return ""

def run_model_comparison():
    """Run comprehensive model comparison"""
    
    # Load questions
    with open('data/questions.json', 'r') as f:
        questions = json.load(f)
    
    # Define models to test
    models = {
        "gpt-3.5-turbo": "GPT-3.5 Turbo",
        "gpt-4": "GPT-4", 
        "gpt-4-turbo": "GPT-4 Turbo"
    }
    
    # Use GPT-4 as the evaluator for consistency
    evaluator_model = "gpt-4"
    
    results = []
    
    print(f"🔄 Starting model comparison with {len(models)} models and {len(questions)} questions...")
    
    for model_name, model_display in models.items():
        print(f"\n📝 Testing {model_display}...")
        
        for question_data in questions:
            question = question_data['question']
            ground_truth = question_data['answer']
            
            print(f"  Generating response for Q{question_data['id']}...")
            
            # Generate response with current model
            response = generate_response_with_model(question, model_name)
            
            if response:
                # Evaluate response
                evaluation = evaluate_response_with_model(question, response, ground_truth, evaluator_model)
                
                # Parse scores
                scores = parse_evaluation_scores(evaluation)
                
                results.append({
                    'model': model_name,
                    'model_display': model_display,
                    'question_id': question_data['id'],
                    'question': question[:100] + '...' if len(question) > 100 else question,
                    'response': response,
                    'ground_truth': ground_truth,
                    'evaluation': evaluation,
                    'factual_accuracy': scores.get('factual_accuracy'),
                    'clarity': scores.get('clarity'),
                    'neutrality': scores.get('neutrality'),
                    'helpfulness': scores.get('helpfulness')
                })
                
                # Rate limiting
                time.sleep(2)
    
    # Create DataFrame
    df = pd.DataFrame(results)
    df['overall_score'] = df[['factual_accuracy', 'clarity', 'neutrality', 'helpfulness']].mean(axis=1)
    
    # Save results
    with open('data/model_comparison_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Model comparison complete! Results saved to data/model_comparison_results.json")
    
    return df

def analyze_model_comparison(df):
    """Analyze and visualize model comparison results"""
    
    # Create results directory
    results_dir = Path("results/figures")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Overall Performance Comparison
    plt.figure(figsize=(12, 8))
    
    model_performance = df.groupby('model_display')[['factual_accuracy', 'clarity', 'neutrality', 'helpfulness', 'overall_score']].mean()
    
    # Create bar chart
    ax = model_performance.plot(kind='bar', figsize=(12, 8))
    plt.title('Model Performance Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Model')
    plt.ylabel('Average Score')
    plt.legend(title='Criteria')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(results_dir / 'model_comparison_overall.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Factual Accuracy Comparison
    plt.figure(figsize=(10, 6))
    
    # Box plot for factual accuracy
    df.boxplot(column='factual_accuracy', by='model_display', figsize=(10, 6))
    plt.title('Factual Accuracy Comparison Across Models', fontsize=14, fontweight='bold')
    plt.suptitle('')  # Remove default suptitle
    plt.xlabel('Model')
    plt.ylabel('Factual Accuracy Score')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(results_dir / 'model_comparison_accuracy.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Risk Assessment by Model
    plt.figure(figsize=(12, 8))
    
    # Create risk categories
    df['risk_level'] = pd.cut(df['factual_accuracy'], 
                             bins=[0, 2, 3, 4, 5], 
                             labels=['High Risk', 'Medium Risk', 'Low Risk', 'Safe'])
    
    risk_by_model = df.groupby(['model_display', 'risk_level']).size().unstack(fill_value=0)
    
    risk_by_model.plot(kind='bar', stacked=True, figsize=(12, 8))
    plt.title('Risk Assessment by Model', fontsize=16, fontweight='bold')
    plt.xlabel('Model')
    plt.ylabel('Number of Responses')
    plt.legend(title='Risk Level')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(results_dir / 'model_comparison_risk.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Performance Heatmap
    plt.figure(figsize=(10, 8))
    
    # Create heatmap of model performance
    sns.heatmap(model_performance, annot=True, cmap='RdYlGn', center=3, 
                fmt='.2f', cbar_kws={'label': 'Average Score'})
    plt.title('Model Performance Heatmap', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(results_dir / 'model_comparison_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Statistical Analysis
    print("\n📊 MODEL COMPARISON ANALYSIS")
    print("=" * 50)
    
    print(f"\nOverall Performance by Model:")
    for model, scores in model_performance.iterrows():
        print(f"  {model}: {scores['overall_score']:.2f}/5.0")
    
    print(f"\nFactual Accuracy by Model:")
    for model, scores in model_performance.iterrows():
        print(f"  {model}: {scores['factual_accuracy']:.2f}/5.0")
    
    # Identify best and worst performing models
    best_model = model_performance['overall_score'].idxmax()
    worst_model = model_performance['overall_score'].idxmin()
    
    print(f"\n🏆 Best Overall Model: {best_model} ({model_performance.loc[best_model, 'overall_score']:.2f}/5.0)")
    print(f"⚠️  Worst Overall Model: {worst_model} ({model_performance.loc[worst_model, 'overall_score']:.2f}/5.0)")
    
    # Risk analysis
    print(f"\n🚨 Risk Analysis:")
    for model in df['model_display'].unique():
        model_data = df[df['model_display'] == model]
        high_risk = len(model_data[model_data['factual_accuracy'] <= 2])
        total = len(model_data)
        print(f"  {model}: {high_risk}/{total} high-risk responses ({high_risk/total*100:.1f}%)")
    
    # Save summary
    summary = {
        'total_responses': len(df),
        'models_tested': len(df['model_display'].unique()),
        'best_model': best_model,
        'worst_model': worst_model,
        'model_performance': model_performance.to_dict(),
        'risk_analysis': {}
    }
    
    for model in df['model_display'].unique():
        model_data = df[df['model_display'] == model]
        high_risk = len(model_data[model_data['factual_accuracy'] <= 2])
        total = len(model_data)
        summary['risk_analysis'][model] = {
            'high_risk_count': high_risk,
            'total_responses': total,
            'high_risk_percentage': high_risk/total*100
        }
    
    with open('results/model_comparison_summary.txt', 'w') as f:
        f.write("MODEL COMPARISON SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Responses: {summary['total_responses']}\n")
        f.write(f"Models Tested: {summary['models_tested']}\n\n")
        f.write("OVERALL PERFORMANCE:\n")
        for model, scores in model_performance.iterrows():
            f.write(f"  {model}: {scores['overall_score']:.2f}/5.0\n")
        f.write(f"\nBest Model: {best_model}\n")
        f.write(f"Worst Model: {worst_model}\n")
    
    print(f"\n✅ Analysis complete! Visualizations saved to {results_dir}")
    print(f"📄 Summary saved to results/model_comparison_summary.txt")

def main():
    """Main function to run model comparison"""
    print("🤖 LLM Model Comparison for Health Advice Evaluation")
    print("=" * 60)
    
    # Run comparison
    df = run_model_comparison()
    
    # Analyze results
    analyze_model_comparison(df)
    
    print("\n🎉 Model comparison study complete!")

if __name__ == "__main__":
    main() 