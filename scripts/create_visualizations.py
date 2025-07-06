import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import re

# Set styling
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

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

def load_and_process_data():
    """Load and process evaluation data"""
    data_path = Path("data")
    
    with open(data_path / "evaluations.json") as f:
        evaluations_data = json.load(f)
    
    analysis_data = []
    for eval_item in evaluations_data:
        scores = parse_evaluation_scores(eval_item['evaluation'])
        
        # Categorize question type
        question = eval_item['question'].lower()
        if any(word in question for word in ['pregnant', 'pregnancy', 'birth', 'c section', 'uterus']):
            category = 'Pregnancy/Reproductive Health'
        elif any(word in question for word in ['psychologist', 'meds', 'medication', 'antidepressant']):
            category = 'Mental Health'
        elif any(word in question for word in ['surgery', 'mri', 'iud', 'doctor', 'medical', 'procedure']):
            category = 'Medical Procedures'
        elif any(word in question for word in ['vaccine', 'vaccination', 'autism']):
            category = 'Vaccination'
        elif any(word in question for word in ['nutrient', 'vitamin', 'deficiency']):
            category = 'Nutrition'
        else:
            category = 'General Health'
        
        gpt_response_length = len(eval_item['gpt_response'].split())
        ground_truth_length = len(eval_item['ground_truth'].split())
        
        analysis_data.append({
            'id': eval_item['id'],
            'question': eval_item['question'][:100] + '...' if len(eval_item['question']) > 100 else eval_item['question'],
            'category': category,
            'factual_accuracy': scores['factual_accuracy'],
            'clarity': scores['clarity'],
            'neutrality': scores['neutrality'],
            'helpfulness': scores['helpfulness'],
            'gpt_response_length': gpt_response_length,
            'ground_truth_length': ground_truth_length,
            'evaluation_text': eval_item['evaluation']
        })
    
    df = pd.DataFrame(analysis_data)
    df['overall_score'] = df[['factual_accuracy', 'clarity', 'neutrality', 'helpfulness']].mean(axis=1)
    
    return df

def create_comprehensive_visualizations(df):
    """Create all visualizations"""
    
    # Create results directory if it doesn't exist
    results_dir = Path("results/figures")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Overall Performance Dashboard
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Criteria scores distribution
    criteria = ['factual_accuracy', 'clarity', 'neutrality', 'helpfulness']
    titles = ['Factual Accuracy', 'Clarity', 'Neutrality', 'Helpfulness']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    for i, (criterion, title, color) in enumerate(zip(criteria, titles, colors)):
        ax = [ax1, ax2, ax3, ax4][i]
        df[criterion].value_counts().sort_index().plot(kind='bar', ax=ax, color=color, alpha=0.7)
        ax.set_title(f'{title} Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel('Score')
        ax.set_ylabel('Count')
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for j, v in enumerate(df[criterion].value_counts().sort_index()):
            ax.text(j, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(results_dir / 'performance_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Category Performance Heatmap
    plt.figure(figsize=(12, 8))
    category_scores = df.groupby('category')[['factual_accuracy', 'clarity', 'neutrality', 'helpfulness', 'overall_score']].mean()
    
    sns.heatmap(category_scores.T, annot=True, cmap='RdYlGn', center=3, 
                fmt='.2f', cbar_kws={'label': 'Average Score'})
    plt.title('Performance by Category and Criteria', fontsize=16, fontweight='bold')
    plt.xlabel('Category')
    plt.ylabel('Evaluation Criteria')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(results_dir / 'category_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Response Length Analysis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # GPT vs Ground Truth length
    ax1.scatter(df['ground_truth_length'], df['gpt_response_length'], alpha=0.7, s=100)
    ax1.plot([0, df['ground_truth_length'].max()], [0, df['ground_truth_length'].max()], 'r--', alpha=0.5)
    ax1.set_xlabel('Ground Truth Length (words)')
    ax1.set_ylabel('GPT Response Length (words)')
    ax1.set_title('Response Length Comparison')
    ax1.grid(True, alpha=0.3)
    
    # Length by category
    df.boxplot(column='gpt_response_length', by='category', ax=ax2)
    ax2.set_title('GPT Response Length by Category')
    ax2.set_xlabel('Category')
    ax2.set_ylabel('Length (words)')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(results_dir / 'length_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Score Correlation Matrix
    plt.figure(figsize=(10, 8))
    correlation_matrix = df[['factual_accuracy', 'clarity', 'neutrality', 'helpfulness', 'gpt_response_length']].corr()
    
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                fmt='.3f', square=True, cbar_kws={'label': 'Correlation Coefficient'})
    plt.title('Correlation Matrix of Evaluation Criteria', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(results_dir / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Risk Assessment Chart
    plt.figure(figsize=(12, 8))
    
    # Create risk categories
    df['risk_level'] = pd.cut(df['factual_accuracy'], 
                             bins=[0, 2, 3, 4, 5], 
                             labels=['High Risk', 'Medium Risk', 'Low Risk', 'Safe'])
    
    risk_counts = df['risk_level'].value_counts()
    colors = ['#FF6B6B', '#FFA500', '#FFD700', '#90EE90']
    
    plt.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%', 
            colors=colors, startangle=90)
    plt.title('Risk Assessment Based on Factual Accuracy', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(results_dir / 'risk_assessment.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Performance Trends
    plt.figure(figsize=(12, 8))
    
    # Sort by ID for trend analysis
    df_sorted = df.sort_values('id')
    
    plt.plot(df_sorted['id'], df_sorted['factual_accuracy'], 'o-', label='Factual Accuracy', linewidth=2)
    plt.plot(df_sorted['id'], df_sorted['helpfulness'], 's-', label='Helpfulness', linewidth=2)
    plt.plot(df_sorted['id'], df_sorted['overall_score'], '^-', label='Overall Score', linewidth=2)
    
    plt.xlabel('Question ID')
    plt.ylabel('Score')
    plt.title('Performance Trends Across Questions', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(results_dir / 'performance_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 7. Category Comparison Bar Chart
    plt.figure(figsize=(12, 8))
    
    category_means = df.groupby('category')['overall_score'].mean().sort_values(ascending=True)
    
    bars = plt.barh(range(len(category_means)), category_means.values, color='skyblue', alpha=0.7)
    plt.yticks(range(len(category_means)), category_means.index)
    plt.xlabel('Average Overall Score')
    plt.title('Performance by Category', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='x')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{width:.2f}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(results_dir / 'category_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Created 7 comprehensive visualizations in {results_dir}")

def main():
    """Main function to create all visualizations"""
    print("📊 Loading and processing data...")
    df = load_and_process_data()
    
    print(f"📈 Creating visualizations for {len(df)} evaluations...")
    create_comprehensive_visualizations(df)
    
    # Print summary statistics
    print("\n📋 Summary Statistics:")
    print(f"Total Questions: {len(df)}")
    print(f"Average Overall Score: {df['overall_score'].mean():.2f}/5.0")
    print(f"Average Factual Accuracy: {df['factual_accuracy'].mean():.2f}/5.0")
    print(f"Categories: {df['category'].value_counts().to_dict()}")
    
    # Identify concerning cases
    low_accuracy = df[df['factual_accuracy'] <= 2]
    if len(low_accuracy) > 0:
        print(f"\n🚨 Concerning Cases (Factual Accuracy ≤2): {len(low_accuracy)}")
        for _, row in low_accuracy.iterrows():
            print(f"  - Q{row['id']}: {row['question'][:60]}... (Score: {row['factual_accuracy']})")

if __name__ == "__main__":
    main() 