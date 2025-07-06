import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import re
from collections import Counter
import warnings
from scipy import stats
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from textstat import textstat

warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class EnhancedHealthAnalysis:
    def __init__(self, data_path=None):
        """Initialize the analysis with data path"""
        if data_path is None:
            self.data_path = Path(__file__).resolve().parent.parent / "data"
        else:
            self.data_path = Path(data_path)
        
        self.questions = None
        self.evaluations = None
        self.df = None
        self.models = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo']
        self.criteria = ['factual_accuracy', 'clarity', 'neutrality', 'helpfulness']
        
        # Set up plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 11
    
    def load_data(self):
        """Load questions and evaluations data"""
        try:
            with open(self.data_path / "questions.json") as f:
                self.questions = json.load(f)
            
            # Try to load restructured evaluations first
            try:
                with open(self.data_path / "evaluations_restructured.json") as f:
                    self.evaluations = json.load(f)
                print("✅ Loaded restructured evaluations")
            except FileNotFoundError:
                # Fall back to original evaluations
                with open(self.data_path / "evaluations.json") as f:
                    self.evaluations = json.load(f)
                print("⚠️  Using original evaluations (restructure recommended)")
            
            print(f"📊 Loaded {len(self.questions)} questions")
            print(f"📊 Loaded {len(self.evaluations)} evaluations")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
        
        return True
    
    def create_analysis_dataframe(self):
        """Create comprehensive analysis dataframe from restructured evaluations"""
        if not self.evaluations:
            print("❌ No evaluations loaded")
            return None
        
        analysis_data = []
        
        for eval_item in self.evaluations:
            question_id = eval_item['id']
            question_text = eval_item['question']
            ground_truth = eval_item['ground_truth']
            
            # Categorize question type
            category = self._categorize_question(question_text)
            
            # Process each model's evaluation
            for model_name, model_eval in eval_item.get('evaluations', {}).items():
                response = model_eval.get('response', '')
                
                # Calculate response characteristics
                response_length = len(response.split())
                ground_truth_length = len(ground_truth.split())
                
                # Calculate readability scores
                readability_scores = self._calculate_readability(response)
                
                # Calculate vocabulary diversity
                vocab_diversity = self._calculate_vocabulary_diversity(response)
                
                analysis_data.append({
                    'id': question_id,
                    'question': question_text[:100] + '...' if len(question_text) > 100 else question_text,
                    'category': category,
                    'model': model_name,
                    'factual_accuracy': model_eval.get('factual_accuracy'),
                    'clarity': model_eval.get('clarity'),
                    'neutrality': model_eval.get('neutrality'),
                    'helpfulness': model_eval.get('helpfulness'),
                    'justification': model_eval.get('justification', ''),
                    'response': response,
                    'ground_truth': ground_truth,
                    'response_length': response_length,
                    'ground_truth_length': ground_truth_length,
                    'flesch_reading_ease': readability_scores['flesch_reading_ease'],
                    'flesch_kincaid_grade': readability_scores['flesch_kincaid_grade'],
                    'vocab_diversity': vocab_diversity,
                    'sentence_count': len(sent_tokenize(response)),
                    'avg_sentence_length': response_length / max(len(sent_tokenize(response)), 1)
                })
        
        self.df = pd.DataFrame(analysis_data)
        
        # Calculate overall score
        self.df['overall_score'] = self.df[self.criteria].mean(axis=1)
        
        print(f"📊 Created analysis dataframe with {len(self.df)} entries")
        print(f"📈 Models: {self.df['model'].unique()}")
        print(f"🏥 Categories: {self.df['category'].value_counts().to_dict()}")
        
        return self.df
    
    def _categorize_question(self, question):
        """Categorize question based on content"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['pregnant', 'pregnancy', 'birth', 'c section', 'uterus', 'iud']):
            return 'Pregnancy/Reproductive Health'
        elif any(word in question_lower for word in ['psychologist', 'meds', 'medication', 'antidepressant', 'mental']):
            return 'Mental Health'
        elif any(word in question_lower for word in ['surgery', 'mri', 'doctor', 'medical', 'procedure', 'vaccine']):
            return 'Medical Procedures'
        elif any(word in question_lower for word in ['blood pressure', 'diabetes', 'stroke', 'heart']):
            return 'Cardiovascular Health'
        elif any(word in question_lower for word in ['nutrient', 'vitamin', 'diet', 'food', 'water', 'sleep']):
            return 'Nutrition/Lifestyle'
        else:
            return 'General Health'
    
    def _calculate_readability(self, text):
        """Calculate readability scores for text"""
        try:
            return {
                'flesch_reading_ease': textstat.flesch_reading_ease(text),
                'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text)
            }
        except:
            return {'flesch_reading_ease': 0, 'flesch_kincaid_grade': 0}
    
    def _calculate_vocabulary_diversity(self, text):
        """Calculate vocabulary diversity (type-token ratio)"""
        try:
            tokens = word_tokenize(text.lower())
            if len(tokens) == 0:
                return 0
            return len(set(tokens)) / len(tokens)
        except:
            return 0
    
    def model_comparison_analysis(self):
        """Perform comprehensive model comparison analysis"""
        if self.df is None:
            print("❌ No data loaded. Run create_analysis_dataframe() first.")
            return
        
        print("\n🔍 MODEL COMPARISON ANALYSIS")
        print("=" * 50)
        
        # 1. Overall performance comparison
        model_performance = self.df.groupby('model')[self.criteria + ['overall_score']].mean()
        print("\n📊 Overall Performance by Model:")
        print(model_performance.round(3))
        
        # 2. Statistical significance testing
        print("\n📈 Statistical Significance Tests:")
        for criterion in self.criteria + ['overall_score']:
            print(f"\n{criterion.replace('_', ' ').title()}:")
            for i, model1 in enumerate(self.models):
                for model2 in self.models[i+1:]:
                    scores1 = self.df[self.df['model'] == model1][criterion].dropna()
                    scores2 = self.df[self.df['model'] == model2][criterion].dropna()
                    
                    if len(scores1) > 0 and len(scores2) > 0:
                        t_stat, p_value = stats.ttest_ind(scores1, scores2)
                        print(f"  {model1} vs {model2}: p={p_value:.4f} {'***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else ''}")
        
        # 3. Performance by category
        print("\n🏥 Performance by Category:")
        category_performance = self.df.groupby(['category', 'model'])['overall_score'].mean().unstack()
        print(category_performance.round(3))
        
        return model_performance, category_performance
    
    def response_quality_analysis(self):
        """Analyze response quality characteristics"""
        if self.df is None:
            print("❌ No data loaded. Run create_analysis_dataframe() first.")
            return
        
        print("\n📝 RESPONSE QUALITY ANALYSIS")
        print("=" * 50)
        
        # 1. Length analysis
        print("\n📏 Response Length Analysis:")
        length_stats = self.df.groupby('model')['response_length'].agg(['mean', 'std', 'min', 'max'])
        print(length_stats.round(1))
        
        # 2. Readability analysis
        print("\n📖 Readability Analysis:")
        readability_stats = self.df.groupby('model')[['flesch_reading_ease', 'flesch_kincaid_grade']].mean()
        print(readability_stats.round(2))
        
        # 3. Vocabulary diversity
        print("\n📚 Vocabulary Diversity:")
        vocab_stats = self.df.groupby('model')['vocab_diversity'].mean()
        print(vocab_stats.round(3))
        
        # 4. Correlation analysis
        print("\n🔗 Quality vs. Characteristics Correlations:")
        correlations = {}
        for criterion in self.criteria + ['overall_score']:
            corr_with_length = self.df[criterion].corr(self.df['response_length'])
            corr_with_readability = self.df[criterion].corr(self.df['flesch_reading_ease'])
            corr_with_vocab = self.df[criterion].corr(self.df['vocab_diversity'])
            
            correlations[criterion] = {
                'length': corr_with_length,
                'readability': corr_with_readability,
                'vocabulary': corr_with_vocab
            }
            
            print(f"  {criterion.replace('_', ' ').title()}:")
            print(f"    Length: {corr_with_length:.3f}")
            print(f"    Readability: {corr_with_readability:.3f}")
            print(f"    Vocabulary: {corr_with_vocab:.3f}")
        
        return correlations
    
    def safety_and_bias_analysis(self):
        """Analyze potential safety issues and bias"""
        if self.df is None:
            print("❌ No data loaded. Run create_analysis_dataframe() first.")
            return
        
        print("\n⚠️  SAFETY AND BIAS ANALYSIS")
        print("=" * 50)
        
        # 1. Low accuracy responses (potential safety issues)
        low_accuracy = self.df[self.df['factual_accuracy'] <= 2]
        print(f"\n❌ Low Accuracy Responses (≤2): {len(low_accuracy)}")
        if not low_accuracy.empty:
            for _, row in low_accuracy.iterrows():
                print(f"  Q{row['id']} ({row['model']}): {row['question'][:50]}...")
                print(f"    Score: {row['factual_accuracy']}/5")
        
        # 2. Neutrality concerns
        low_neutrality = self.df[self.df['neutrality'] <= 3]
        print(f"\n⚠️  Potential Bias Concerns (neutrality ≤3): {len(low_neutrality)}")
        if not low_neutrality.empty:
            for _, row in low_neutrality.iterrows():
                print(f"  Q{row['id']} ({row['model']}): {row['question'][:50]}...")
                print(f"    Neutrality Score: {row['neutrality']}/5")
        
        # 3. Model-specific safety patterns
        print(f"\n🔍 Safety Patterns by Model:")
        for model in self.models:
            model_data = self.df[self.df['model'] == model]
            low_acc_count = len(model_data[model_data['factual_accuracy'] <= 2])
            low_help_count = len(model_data[model_data['helpfulness'] <= 2])
            
            print(f"  {model}:")
            print(f"    Low accuracy responses: {low_acc_count}")
            print(f"    Low helpfulness responses: {low_help_count}")
    
    def create_visualizations(self, output_dir=None):
        """Create comprehensive visualizations"""
        if self.df is None:
            print("❌ No data loaded. Run create_analysis_dataframe() first.")
            return
        
        if output_dir is None:
            output_dir = Path(__file__).resolve().parent.parent / "results" / "figures"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📊 Creating visualizations in: {output_dir}")
        
        # 1. Model Performance Comparison
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Radar chart for model comparison
        model_scores = self.df.groupby('model')[self.criteria].mean()
        
        angles = np.linspace(0, 2 * np.pi, len(self.criteria), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        for i, model in enumerate(self.models):
            values = model_scores.loc[model].values.tolist()
            values += values[:1]  # Complete the circle
            ax1.plot(angles, values, 'o-', linewidth=2, label=model)
            ax1.fill(angles, values, alpha=0.25)
        
        ax1.set_xticks(angles[:-1])
        ax1.set_xticklabels([c.replace('_', ' ').title() for c in self.criteria])
        ax1.set_ylim(0, 5)
        ax1.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True)
        
        # Overall score distribution
        for model in self.models:
            model_data = self.df[self.df['model'] == model]['overall_score']
            ax2.hist(model_data, alpha=0.7, label=model, bins=10)
        ax2.set_xlabel('Overall Score')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Overall Score Distribution by Model', fontsize=14, fontweight='bold')
        ax2.legend()
        
        # Performance by category
        category_scores = self.df.groupby(['category', 'model'])['overall_score'].mean().unstack()
        category_scores.plot(kind='bar', ax=ax3)
        ax3.set_title('Performance by Category and Model', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Category')
        ax3.set_ylabel('Average Overall Score')
        ax3.tick_params(axis='x', rotation=45)
        ax3.legend(title='Model')
        
        # Response length vs quality
        for model in self.models:
            model_data = self.df[self.df['model'] == model]
            ax4.scatter(model_data['response_length'], model_data['overall_score'], 
                       alpha=0.6, label=model)
        ax4.set_xlabel('Response Length (words)')
        ax4.set_ylabel('Overall Score')
        ax4.set_title('Response Length vs Quality', fontsize=14, fontweight='bold')
        ax4.legend()
        
        plt.tight_layout()
        plt.savefig(output_dir / 'model_comparison_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Detailed criteria analysis
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.ravel()
        
        for i, criterion in enumerate(self.criteria):
            criterion_data = [self.df[self.df['model'] == model][criterion].values 
                            for model in self.models]
            
            axes[i].boxplot(criterion_data, labels=self.models)
            axes[i].set_title(f'{criterion.replace("_", " ").title()} Distribution', 
                            fontsize=12, fontweight='bold')
            axes[i].set_ylabel('Score')
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_dir / 'criteria_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Visualizations saved successfully!")
    
    def export_results(self, output_dir=None):
        """Export analysis results to files"""
        if self.df is None:
            print("❌ No data loaded. Run create_analysis_dataframe() first.")
            return
        
        if output_dir is None:
            output_dir = Path(__file__).resolve().parent.parent / "results"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export detailed scores
        export_df = self.df[['id', 'category', 'model', 'factual_accuracy', 'clarity', 
                           'neutrality', 'helpfulness', 'overall_score', 'response_length',
                           'flesch_reading_ease', 'vocab_diversity']].copy()
        
        export_df.to_csv(output_dir / 'enhanced_scores.csv', index=False)
        
        # Create summary report
        with open(output_dir / 'enhanced_analysis_summary.txt', 'w') as f:
            f.write("ENHANCED LLM HEALTH EVALUATION - ANALYSIS SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Dataset: {len(self.df)} model evaluations across {len(self.df['id'].unique())} questions\n")
            f.write(f"Models: {', '.join(self.models)}\n\n")
            
            # Overall statistics
            f.write("OVERALL STATISTICS:\n")
            f.write(f"• Average Overall Score: {self.df['overall_score'].mean():.2f}/5.0\n")
            f.write(f"• Standard Deviation: {self.df['overall_score'].std():.2f}\n\n")
            
            # Model comparison
            f.write("MODEL COMPARISON:\n")
            model_performance = self.df.groupby('model')['overall_score'].agg(['mean', 'std'])
            for model, stats in model_performance.iterrows():
                f.write(f"• {model}: {stats['mean']:.2f} ± {stats['std']:.2f}\n")
            f.write("\n")
            
            # Category performance
            f.write("CATEGORY PERFORMANCE:\n")
            category_performance = self.df.groupby('category')['overall_score'].mean().sort_values(ascending=False)
            for category, score in category_performance.items():
                f.write(f"• {category}: {score:.2f}/5.0\n")
            f.write("\n")
            
            # Safety analysis
            f.write("SAFETY ANALYSIS:\n")
            low_accuracy_count = len(self.df[self.df['factual_accuracy'] <= 2])
            low_helpfulness_count = len(self.df[self.df['helpfulness'] <= 2])
            f.write(f"• Low accuracy responses (≤2): {low_accuracy_count}\n")
            f.write(f"• Low helpfulness responses (≤2): {low_helpfulness_count}\n")
        
        print(f"✅ Results exported to: {output_dir}")
        print("  • enhanced_scores.csv - Detailed scores for each model evaluation")
        print("  • enhanced_analysis_summary.txt - Comprehensive analysis summary")

def main():
    """Main analysis function"""
    analyzer = EnhancedHealthAnalysis()
    
    if not analyzer.load_data():
        return
    
    # Create analysis dataframe
    analyzer.create_analysis_dataframe()
    
    # Perform analyses
    analyzer.model_comparison_analysis()
    analyzer.response_quality_analysis()
    analyzer.safety_and_bias_analysis()
    
    # Create visualizations
    analyzer.create_visualizations()
    
    # Export results
    analyzer.export_results()
    
    print("\n🎯 ANALYSIS COMPLETE!")
    print("Check the results/ directory for detailed outputs and visualizations.")

if __name__ == "__main__":
    main() 