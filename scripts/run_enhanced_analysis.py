#!/usr/bin/env python3
"""
Enhanced LLM Health Evaluation Analysis Pipeline

This script runs the complete analysis pipeline:
1. Restructure evaluations (if needed)
2. Run enhanced analysis
3. Generate visualizations and reports
"""

import sys
from pathlib import Path

# Add the scripts directory to the path
scripts_dir = Path(__file__).resolve().parent
sys.path.append(str(scripts_dir))

from restructure_evaluations import restructure_evaluations
from enhanced_analysis import EnhancedHealthAnalysis

def main():
    """Run the complete enhanced analysis pipeline"""
    
    print("🚀 Starting Enhanced LLM Health Evaluation Analysis Pipeline")
    print("=" * 60)
    
    # Step 1: Check if restructured evaluations exist
    data_path = Path(__file__).resolve().parent.parent / "data"
    restructured_path = data_path / "evaluations_restructured.json"
    
    if not restructured_path.exists():
        print("\n📋 Step 1: Restructuring evaluations...")
        print("This will convert the current string-based evaluations to structured JSON format.")
        print("This process may take some time as it evaluates all model responses.")
        
        response = input("Do you want to proceed with restructuring? (y/n): ")
        if response.lower() in ['y', 'yes']:
            try:
                restructured_evaluations = restructure_evaluations()
                print("✅ Restructuring completed successfully!")
            except Exception as e:
                print(f"❌ Error during restructuring: {e}")
                print("Continuing with existing evaluations...")
        else:
            print("⏭️  Skipping restructuring. Using existing evaluations.")
    else:
        print("✅ Restructured evaluations already exist.")
    
    # Step 2: Run enhanced analysis
    print("\n📊 Step 2: Running enhanced analysis...")
    
    try:
        analyzer = EnhancedHealthAnalysis()
        
        if not analyzer.load_data():
            print("❌ Failed to load data. Exiting.")
            return
        
        # Create analysis dataframe
        analyzer.create_analysis_dataframe()
        
        # Perform analyses
        print("\n🔍 Running model comparison analysis...")
        analyzer.model_comparison_analysis()
        
        print("\n📝 Running response quality analysis...")
        analyzer.response_quality_analysis()
        
        print("\n⚠️  Running safety and bias analysis...")
        analyzer.safety_and_bias_analysis()
        
        # Create visualizations
        print("\n📊 Creating visualizations...")
        analyzer.create_visualizations()
        
        # Export results
        print("\n📁 Exporting results...")
        analyzer.export_results()
        
        print("\n🎯 ANALYSIS COMPLETE!")
        print("=" * 60)
        print("📊 Results available in:")
        print("  • data/enhanced_scores.csv - Detailed scores")
        print("  • results/enhanced_analysis_summary.txt - Summary report")
        print("  • results/figures/ - Visualizations")
        
        # Print key insights
        print("\n🔍 KEY INSIGHTS:")
        df = analyzer.df
        if df is not None:
            print(f"• Total evaluations: {len(df)}")
            print(f"• Average overall score: {df['overall_score'].mean():.2f}/5.0")
            print(f"• Best performing model: {df.groupby('model')['overall_score'].mean().idxmax()}")
            print(f"• Most challenging category: {df.groupby('category')['overall_score'].mean().idxmin()}")
            print(f"• Safety concerns: {len(df[df['factual_accuracy'] <= 2])} low-accuracy responses")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 