import json
import openai
import time
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

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
            # You can extend this with actual API calls when available
            return f"Response from {model_name} would be generated here with proper API integration."
    except Exception as e:
        print(f"Error generating response with {model_name}: {e}")
        return f"Error: Could not generate response with {model_name}"

def generate_multi_model_responses():
    """Generate responses from multiple models for all questions"""
    
    # Load existing questions
    with open('data/questions.json', 'r') as f:
        questions = json.load(f)
    
    # Define models to test
    models = {
        "gpt-3.5-turbo": "GPT-3.5 Turbo",
        "gpt-4": "GPT-4",
        "gpt-4-turbo": "GPT-4 Turbo"
    }
    
    # You can add more models here when you have API access
    # "claude-3-sonnet": "Claude 3 Sonnet",
    # "gemini-pro": "Gemini Pro",
    
    print(f"🤖 Generating multi-model responses for {len(questions)} questions...")
    print(f"📝 Testing {len(models)} models: {', '.join(models.values())}")
    
    # Process each question
    for i, question_data in enumerate(questions):
        question = question_data['question']
        question_id = question_data['id']
        
        print(f"\n📋 Processing Question #{question_id}: {question[:60]}...")
        
        # Generate responses from all models
        model_responses = {}
        
        for model_name, model_display in models.items():
            print(f"  🤖 Generating response with {model_display}...")
            
            response = generate_response_with_model(question, model_name)
            model_responses[model_name] = response
            
            # Rate limiting to avoid API limits
            time.sleep(2)
        
        # Update the question with multi-model responses
        questions[i]['response'] = model_responses
        questions[i]['source'] = f"Multi-Model Analysis - {', '.join(models.values())}"
        
        print(f"✅ Completed Q#{question_id} with {len(models)} model responses")
    
    # Save updated questions
    with open('data/questions_multi_model.json', 'w') as f:
        json.dump(questions, f, indent=2)
    
    print(f"\n🎉 Multi-model responses generated for all {len(questions)} questions!")
    print("📁 Results saved to data/questions_multi_model.json")
    
    return questions

def create_comparison_analysis(questions):
    """Create a simple analysis of the multi-model responses"""
    
    print("\n📊 MULTI-MODEL RESPONSE ANALYSIS")
    print("=" * 50)
    
    # Count models used
    sample_question = questions[0]
    models_used = list(sample_question['response'].keys())
    
    print(f"Models tested: {len(models_used)}")
    print(f"Questions processed: {len(questions)}")
    print(f"Total responses generated: {len(questions) * len(models_used)}")
    
    # Show sample structure
    print(f"\n📋 Sample response structure for Q#{sample_question['id']}:")
    print(f"Question: {sample_question['question'][:80]}...")
    print("Responses:")
    for model, response in sample_question['response'].items():
        print(f"  {model}: {response[:100]}...")
    
    # Save analysis summary
    summary = {
        'total_questions': len(questions),
        'models_tested': models_used,
        'total_responses': len(questions) * len(models_used),
        'sample_question_id': sample_question['id'],
        'sample_question': sample_question['question'],
        'sample_responses': sample_question['response']
    }
    
    with open('results/multi_model_summary.txt', 'w') as f:
        f.write("MULTI-MODEL RESPONSE GENERATION SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Questions: {summary['total_questions']}\n")
        f.write(f"Models Tested: {len(summary['models_tested'])}\n")
        f.write(f"Total Responses: {summary['total_responses']}\n\n")
        f.write("Models Used:\n")
        for model in summary['models_tested']:
            f.write(f"  - {model}\n")
        f.write(f"\nSample Question #{summary['sample_question_id']}:\n")
        f.write(f"  {summary['sample_question']}\n")
    
    print(f"\n📄 Analysis summary saved to results/multi_model_summary.txt")

def create_template_for_manual_use():
    """Create a template JSON structure for manual use"""
    
    template = {
        "id": 1,
        "question": "Example health question here?",
        "answer": "Ground truth answer from authoritative source",
        "response": {
            "gpt-3.5-turbo": "Response from GPT-3.5 Turbo",
            "gpt-4": "Response from GPT-4",
            "gpt-4-turbo": "Response from GPT-4 Turbo",
            "claude-3-sonnet": "Response from Claude 3 Sonnet",
            "gemini-pro": "Response from Gemini Pro"
        },
        "source": "Authoritative Source",
        "link": "https://example.com/source"
    }
    
    # Save template
    with open('docs/multi_model_template.json', 'w') as f:
        json.dump([template], f, indent=2)
    
    print("📄 Template saved to docs/multi_model_template.json")

def main():
    """Main function"""
    print("🤖 Multi-Model Response Generator")
    print("=" * 50)
    
    # Create template
    create_template_for_manual_use()
    
    print("\nOptions:")
    print("1. Generate multi-model responses for all questions")
    print("2. Just create the template (already done)")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        # Generate multi-model responses
        questions = generate_multi_model_responses()
        
        # Create analysis
        create_comparison_analysis(questions)
        
        print("\n🎉 Multi-model response generation complete!")
        print("📁 Check data/questions_multi_model.json for results")
    else:
        print("✅ Template created. You can use it for manual multi-model testing.")

if __name__ == "__main__":
    main() 