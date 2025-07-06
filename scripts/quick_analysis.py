#!/usr/bin/env python3
"""
Quick Analysis of Restructured Evaluations
"""

import json
import pandas as pd
from pathlib import Path

def quick_analysis():
    """Perform quick analysis of restructured evaluations"""
    
    # Load data
    with open('data/evaluations_restructured.json') as f:
        data = json.load(f)
    
    print("📊 ENHANCED ANALYSIS RESULTS")
    print("=" * 60)
    print(f"Total questions: {len(data)}")
    
    # Extract all scores
    models = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo']
    criteria = ['factual_accuracy', 'clarity', 'neutrality', 'helpfulness']
    
    results = []
    for eval_item in data:
        for model in models:
            if model in eval_item['evaluations']:
                for criterion in criteria:
                    results.append({
                        'id': eval_item['id'],
                        'model': model,
                        'criterion': criterion,
                        'score': eval_item['evaluations'][model][criterion]
                    })
    
    df = pd.DataFrame(results)
    
    # Model performance
    print("\n🎯 MODEL PERFORMANCE:")
    model_perf = df.groupby('model')['score'].agg(['mean', 'std', 'count']).round(3)
    print(model_perf)
    
    # Criteria performance
    print("\n📈 CRITERIA PERFORMANCE:")
    criteria_perf = df.groupby('criterion')['score'].agg(['mean', 'std']).round(3)
    print(criteria_perf)
    
    # Best performing model by criterion
    print("\n🏆 BEST PERFORMING MODEL BY CRITERION:")
    for criterion in criteria:
        criterion_data = df[df['criterion'] == criterion]
        best_model = criterion_data.groupby('model')['score'].mean().idxmax()
        best_score = criterion_data.groupby('model')['score'].mean().max()
        print(f"  {criterion.replace('_', ' ').title()}: {best_model} ({best_score:.3f})")
    
    # Overall rankings
    print("\n🥇 OVERALL MODEL RANKINGS:")
    overall_scores = df.groupby('model')['score'].mean().sort_values(ascending=False)
    for i, (model, score) in enumerate(overall_scores.items(), 1):
        print(f"  {i}. {model}: {score:.3f}")
    
    # Safety analysis
    print("\n⚠️  SAFETY ANALYSIS:")
    low_accuracy = df[(df['criterion'] == 'factual_accuracy') & (df['score'] <= 2)]
    print(f"  Low accuracy responses (≤2): {len(low_accuracy)}")
    
    if not low_accuracy.empty:
        print("  Low accuracy cases:")
        for _, row in low_accuracy.iterrows():
            print(f"    Q{row['id']} ({row['model']}): {row['score']}/5")
    
    # Response length analysis
    print("\n📏 RESPONSE CHARACTERISTICS:")
    response_lengths = []
    for eval_item in data:
        for model in models:
            if model in eval_item['evaluations']:
                response = eval_item['evaluations'][model]['response']
                length = len(response.split())
                response_lengths.append({'model': model, 'length': length})
    
    length_df = pd.DataFrame(response_lengths)
    length_stats = length_df.groupby('model')['length'].agg(['mean', 'std', 'min', 'max']).round(1)
    print(length_stats)
    
    # Category analysis
    print("\n🏥 CATEGORY ANALYSIS:")
    categories = {
        'Pregnancy/Reproductive Health': ['pregnant', 'pregnancy', 'birth', 'uterus', 'iud'],
        'Mental Health': ['psychologist', 'meds', 'medication', 'antidepressant'],
        'Medical Procedures': ['surgery', 'mri', 'doctor', 'medical', 'procedure', 'vaccine'],
        'Cardiovascular Health': ['blood pressure', 'diabetes', 'stroke', 'heart'],
        'Nutrition/Lifestyle': ['nutrient', 'vitamin', 'diet', 'food', 'water', 'sleep']
    }
    
    for category, keywords in categories.items():
        category_questions = []
        for eval_item in data:
            question_lower = eval_item['question'].lower()
            if any(keyword in question_lower for keyword in keywords):
                category_questions.append(eval_item['id'])
        
        if category_questions:
            category_scores = df[df['id'].isin(category_questions)]
            avg_score = category_scores['score'].mean()
            print(f"  {category}: {avg_score:.3f} ({len(category_questions)} questions)")
    
    print("\n✅ Analysis complete!")
    print("📁 Check results/figures/ for visualizations")
    print("📄 Check data/evaluations_restructured.json for structured data")

if __name__ == "__main__":
    quick_analysis() 