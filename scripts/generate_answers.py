import json
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_ai_response(question):
    """Generate AI response for a given question"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful health information assistant. Provide accurate, evidence-based responses to health-related questions. Be concise but informative."},
                {"role": "user", "content": question}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating response for question: {e}")
        return ""

def update_questions_with_ai_responses():
    """Update questions 15-20 with AI-generated responses"""
    
    # Load the questions data
    with open('data/questions.json', 'r') as f:
        questions = json.load(f)
    
    # Generate responses for questions 15-20
    for i in range(14, 20):  # 0-indexed, so questions 15-20 are at indices 14-19
        question = questions[i]['question']
        print(f"Generating response for question {i+1}: {question[:50]}...")
        
        # Generate AI response
        ai_response = generate_ai_response(question)
        
        # Update the response field
        questions[i]['response'] = ai_response
        print(f"Generated response: {ai_response[:100]}...")
    
    # Save the updated data
    with open('data/questions.json', 'w') as f:
        json.dump(questions, f, indent=2)
    
    print("Successfully updated questions 15-20 with AI responses!")

if __name__ == "__main__":
    update_questions_with_ai_responses()
