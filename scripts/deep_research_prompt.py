import json
import openai
import time
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def create_deep_research_prompt(question, question_id):
    """Create a comprehensive research prompt for deep health research"""
    
    prompt = f"""
# COMPREHENSIVE HEALTH RESEARCH TASK

## RESEARCH QUESTION #{question_id}
**Question:** {question}

## YOUR MISSION
You are a senior medical researcher with access to the latest medical databases, peer-reviewed journals, and authoritative health organizations. Conduct a comprehensive, evidence-based analysis of this health question.

## RESEARCH METHODOLOGY

### 1. SOURCE VERIFICATION
- **Primary Sources**: CDC, WHO, NIH, FDA, Mayo Clinic, ACOG, AMA
- **Peer-Reviewed Journals**: PubMed, JAMA, NEJM, Lancet, BMJ
- **Medical Guidelines**: Clinical practice guidelines, systematic reviews
- **Evidence Level**: Prioritize Level I (systematic reviews) and Level II (randomized controlled trials)

### 2. COMPREHENSIVE ANALYSIS FRAMEWORK

#### A. MEDICAL EVIDENCE
- **Current Guidelines**: What do authoritative medical organizations recommend?
- **Scientific Studies**: What does peer-reviewed research show?
- **Meta-Analyses**: What do systematic reviews conclude?
- **Contraindications**: What are the risks and warnings?

#### B. CLINICAL CONTEXT
- **Patient Safety**: What are the safety considerations?
- **Risk-Benefit Analysis**: What are the pros and cons?
- **Alternative Options**: What are the alternatives?
- **Professional Recommendations**: What do healthcare providers advise?

#### C. PRACTICAL GUIDANCE
- **Actionable Steps**: What should the person do?
- **Red Flags**: When should they seek medical attention?
- **Prevention**: How can they prevent related issues?
- **Follow-up**: What monitoring or follow-up is needed?

### 3. RESPONSE STRUCTURE

Please format your response exactly as follows:

## 📋 EXECUTIVE SUMMARY
[2-3 sentences summarizing the key findings and recommendations]

## 🔬 SCIENTIFIC EVIDENCE
### Current Medical Guidelines
[What do CDC, WHO, and other authoritative sources say?]

### Research Findings
[Key studies, meta-analyses, and clinical evidence]

### Evidence Quality
[Level of evidence, study limitations, consensus among experts]

## ⚠️ SAFETY CONSIDERATIONS
### Risk Factors
[Who is at higher risk? What conditions require special attention?]

### Contraindications
[When should this NOT be done? What medications interact?]

### Warning Signs
[What symptoms require immediate medical attention?]

## 💡 PRACTICAL RECOMMENDATIONS
### Primary Recommendation
[What is the best course of action?]

### Alternative Approaches
[What are other valid options?]

### Prevention Strategies
[How can similar issues be prevented?]

## 🏥 WHEN TO SEEK MEDICAL CARE
### Immediate Attention Required
[Symptoms that need emergency care]

### Schedule a Doctor Visit
[When to make an appointment]

### Self-Monitoring
[What to watch for at home]

## 📚 SOURCES & REFERENCES
### Authoritative Organizations
[List specific CDC, WHO, NIH pages with URLs]

### Key Studies
[Important research papers with citations]

### Clinical Guidelines
[Relevant medical guidelines and recommendations]

## ⚖️ RISK-BENEFIT ASSESSMENT
### Benefits
[What are the potential positive outcomes?]

### Risks
[What are the potential negative outcomes?]

### Overall Assessment
[Net benefit or risk recommendation]

---

## RESEARCH QUALITY STANDARDS

### ACCURACY REQUIREMENTS
- ✅ Verify information against multiple authoritative sources
- ✅ Include specific citations and references
- ✅ Distinguish between established facts and emerging evidence
- ✅ Acknowledge limitations and uncertainties

### DEPTH REQUIREMENTS
- ✅ Provide comprehensive coverage of the topic
- ✅ Include both benefits and risks
- ✅ Address common misconceptions
- ✅ Consider different patient populations

### SAFETY REQUIREMENTS
- ✅ Prioritize patient safety in all recommendations
- ✅ Include appropriate medical disclaimers
- ✅ Emphasize when professional medical advice is needed
- ✅ Provide clear warning signs and red flags

### CLARITY REQUIREMENTS
- ✅ Use clear, accessible language
- ✅ Structure information logically
- ✅ Provide actionable, specific guidance
- ✅ Avoid medical jargon when possible

## IMPORTANT NOTES
1. **Medical Disclaimer**: Always include appropriate medical disclaimers
2. **Individual Variation**: Acknowledge that individual circumstances vary
3. **Professional Consultation**: Emphasize the importance of consulting healthcare providers
4. **Evidence-Based**: Base all recommendations on current, reliable evidence
5. **Comprehensive**: Address the question thoroughly from multiple angles

## FINAL INSTRUCTIONS
Take your time to conduct thorough research. This is a high-stakes health question that requires careful, evidence-based analysis. Your response should be comprehensive enough that a healthcare provider would find it accurate and useful, while being accessible to the general public.

Begin your research now and provide a complete, well-structured response following the format above.
"""

    return prompt

def generate_deep_research_response(question, question_id):
    """Generate a deep research response using the comprehensive prompt"""
    
    prompt = create_deep_research_prompt(question, question_id)
    
    try:
        print(f"🔬 Conducting deep research for Question #{question_id}...")
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior medical researcher with expertise in evidence-based medicine, clinical guidelines, and patient safety. You have access to the latest medical databases and authoritative health organizations. Your responses are thorough, accurate, and prioritize patient safety."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3  # Lower temperature for more consistent, factual responses
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error generating deep research response: {e}")
        return ""

def update_questions_with_deep_research():
    """Update all questions with deep research responses"""
    
    # Load existing questions
    with open('data/questions.json', 'r') as f:
        questions = json.load(f)
    
    print(f"🔬 Starting deep research for {len(questions)} questions...")
    
    # Generate deep research responses
    for i, question_data in enumerate(questions):
        question = question_data['question']
        question_id = question_data['id']
        
        print(f"\n📋 Processing Question #{question_id}: {question[:60]}...")
        
        # Generate deep research response
        deep_response = generate_deep_research_response(question, question_id)
        
        if deep_response:
            # Update the response field with deep research
            questions[i]['response'] = deep_response
            questions[i]['source'] = "Deep Research - GPT-4"
            print(f"✅ Deep research completed for Q#{question_id}")
        else:
            print(f"❌ Failed to generate deep research for Q#{question_id}")
        
        # Rate limiting to avoid API limits
        time.sleep(3)
    
    # Save updated questions
    with open('data/questions.json', 'w') as f:
        json.dump(questions, f, indent=2)
    
    print(f"\n🎉 Deep research completed for all {len(questions)} questions!")
    print("📁 Updated data saved to data/questions.json")

def create_research_prompt_template():
    """Create a standalone prompt template for manual use"""
    
    template = """
# COMPREHENSIVE HEALTH RESEARCH PROMPT TEMPLATE

## RESEARCH QUESTION
[INSERT YOUR HEALTH QUESTION HERE]

## YOUR MISSION
You are a senior medical researcher with access to the latest medical databases, peer-reviewed journals, and authoritative health organizations. Conduct a comprehensive, evidence-based analysis of this health question.

## RESEARCH METHODOLOGY

### 1. SOURCE VERIFICATION
- **Primary Sources**: CDC, WHO, NIH, FDA, Mayo Clinic, ACOG, AMA
- **Peer-Reviewed Journals**: PubMed, JAMA, NEJM, Lancet, BMJ
- **Medical Guidelines**: Clinical practice guidelines, systematic reviews
- **Evidence Level**: Prioritize Level I (systematic reviews) and Level II (randomized controlled trials)

### 2. COMPREHENSIVE ANALYSIS FRAMEWORK

#### A. MEDICAL EVIDENCE
- **Current Guidelines**: What do authoritative medical organizations recommend?
- **Scientific Studies**: What does peer-reviewed research show?
- **Meta-Analyses**: What do systematic reviews conclude?
- **Contraindications**: What are the risks and warnings?

#### B. CLINICAL CONTEXT
- **Patient Safety**: What are the safety considerations?
- **Risk-Benefit Analysis**: What are the pros and cons?
- **Alternative Options**: What are the alternatives?
- **Professional Recommendations**: What do healthcare providers advise?

#### C. PRACTICAL GUIDANCE
- **Actionable Steps**: What should the person do?
- **Red Flags**: When should they seek medical attention?
- **Prevention**: How can they prevent related issues?
- **Follow-up**: What monitoring or follow-up is needed?

### 3. RESPONSE STRUCTURE

Please format your response exactly as follows:

## 📋 EXECUTIVE SUMMARY
[2-3 sentences summarizing the key findings and recommendations]

## 🔬 SCIENTIFIC EVIDENCE
### Current Medical Guidelines
[What do CDC, WHO, and other authoritative sources say?]

### Research Findings
[Key studies, meta-analyses, and clinical evidence]

### Evidence Quality
[Level of evidence, study limitations, consensus among experts]

## ⚠️ SAFETY CONSIDERATIONS
### Risk Factors
[Who is at higher risk? What conditions require special attention?]

### Contraindications
[When should this NOT be done? What medications interact?]

### Warning Signs
[What symptoms require immediate medical attention?]

## 💡 PRACTICAL RECOMMENDATIONS
### Primary Recommendation
[What is the best course of action?]

### Alternative Approaches
[What are other valid options?]

### Prevention Strategies
[How can similar issues be prevented?]

## 🏥 WHEN TO SEEK MEDICAL CARE
### Immediate Attention Required
[Symptoms that need emergency care]

### Schedule a Doctor Visit
[When to make an appointment]

### Self-Monitoring
[What to watch for at home]

## 📚 SOURCES & REFERENCES
### Authoritative Organizations
[List specific CDC, WHO, NIH pages with URLs]

### Key Studies
[Important research papers with citations]

### Clinical Guidelines
[Relevant medical guidelines and recommendations]

## ⚖️ RISK-BENEFIT ASSESSMENT
### Benefits
[What are the potential positive outcomes?]

### Risks
[What are the potential negative outcomes?]

### Overall Assessment
[Net benefit or risk recommendation]

---

## RESEARCH QUALITY STANDARDS

### ACCURACY REQUIREMENTS
- ✅ Verify information against multiple authoritative sources
- ✅ Include specific citations and references
- ✅ Distinguish between established facts and emerging evidence
- ✅ Acknowledge limitations and uncertainties

### DEPTH REQUIREMENTS
- ✅ Provide comprehensive coverage of the topic
- ✅ Include both benefits and risks
- ✅ Address common misconceptions
- ✅ Consider different patient populations

### SAFETY REQUIREMENTS
- ✅ Prioritize patient safety in all recommendations
- ✅ Include appropriate medical disclaimers
- ✅ Emphasize when professional medical advice is needed
- ✅ Provide clear warning signs and red flags

### CLARITY REQUIREMENTS
- ✅ Use clear, accessible language
- ✅ Structure information logically
- ✅ Provide actionable, specific guidance
- ✅ Avoid medical jargon when possible

## IMPORTANT NOTES
1. **Medical Disclaimer**: Always include appropriate medical disclaimers
2. **Individual Variation**: Acknowledge that individual circumstances vary
3. **Professional Consultation**: Emphasize the importance of consulting healthcare providers
4. **Evidence-Based**: Base all recommendations on current, reliable evidence
5. **Comprehensive**: Address the question thoroughly from multiple angles

## FINAL INSTRUCTIONS
Take your time to conduct thorough research. This is a high-stakes health question that requires careful, evidence-based analysis. Your response should be comprehensive enough that a healthcare provider would find it accurate and useful, while being accessible to the general public.

Begin your research now and provide a complete, well-structured response following the format above.
"""
    
    # Save template to file
    with open('docs/research_prompt_template.txt', 'w') as f:
        f.write(template)
    
    print("📄 Research prompt template saved to docs/research_prompt_template.txt")

def main():
    """Main function"""
    print("🔬 Deep Research Prompt Generator")
    print("=" * 50)
    
    # Create prompt template
    create_research_prompt_template()
    
    # Ask user if they want to run deep research
    print("\nOptions:")
    print("1. Generate deep research responses for all questions")
    print("2. Just create the prompt template (already done)")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        update_questions_with_deep_research()
    else:
        print("✅ Prompt template created. You can use it manually with ChatGPT.")

if __name__ == "__main__":
    main() 