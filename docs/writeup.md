# LLM Health Advice Evaluation: A Study on Factual Accuracy and Bias

## Abstract

This study evaluates the factual accuracy and potential bias in GPT-4-generated health advice by comparing responses to 20 common health questions against verified sources from the CDC, WHO, and medical communities. Using a multi-criteria evaluation framework, we assess responses on factual accuracy, clarity, neutrality, and helpfulness. Our findings reveal an overall score of 4.56/5.0, with excellent clarity and neutrality scores but room for improvement in factual accuracy, particularly for pregnancy-related advice.

## 1. Introduction

### 1.1 Research Motivation

As large language models (LLMs) become increasingly integrated into healthcare applications, ensuring their reliability and safety is paramount. Health misinformation can have serious consequences, making it crucial to evaluate the factual accuracy and potential biases in AI-generated health advice.

### 1.2 Research Question

**How factually accurate and unbiased are GPT-4's responses to common health questions compared to information from authoritative sources like the CDC and WHO?**

### 1.3 Significance

This research contributes to:

- **AI Safety**: Understanding potential risks in healthcare AI applications
- **Trust Building**: Establishing confidence in AI health advice systems
- **Policy Development**: Informing guidelines for AI in healthcare
- **Model Improvement**: Identifying areas for enhancement in health-related responses

## 2. Methodology

### 2.1 Dataset Construction

We curated 20 health questions spanning multiple categories:

- **Pregnancy/Reproductive Health** (5 questions)
- **Mental Health** (1 question)
- **Medical Procedures** (3 questions)
- **Vaccination** (5 questions)
- **Nutrition** (2 questions)
- **General Health** (4 questions)

### 2.2 Data Collection Process

1. **Question Selection**: Chose questions representing common health concerns
2. **GPT-4 Response Generation**: Generated responses using GPT-4 with health-focused prompting
3. **Ground Truth Collection**: Compiled verified answers from CDC, WHO, Mayo Clinic, and medical communities
4. **Evaluation**: Used GPT-4 as evaluator with structured criteria

### 2.3 Evaluation Framework

We evaluated each response on four criteria using a 1-5 scale:

1. **Factual Accuracy**: Is the response factually correct compared to ground truth?
2. **Clarity**: Is the response clearly written and easy to understand?
3. **Neutrality**: Is it unbiased and culturally sensitive?
4. **Helpfulness**: Does it provide useful and safe information?

### 2.4 Analysis Methods

- **Descriptive Statistics**: Mean scores, distributions, category comparisons
- **Correlation Analysis**: Relationships between evaluation criteria
- **Statistical Testing**: Significance testing between categories
- **Qualitative Analysis**: Detailed examination of concerning cases

## 3. Results

### 3.1 Overall Performance

| Criterion        | Mean Score   | Standard Deviation |
| ---------------- | ------------ | ------------------ |
| Factual Accuracy | 4.08/5.0     | 1.12               |
| Clarity          | 5.00/5.0     | 0.00               |
| Neutrality       | 5.00/5.0     | 0.00               |
| Helpfulness      | 4.15/5.0     | 1.07               |
| **Overall**      | **4.56/5.0** | **0.54**           |

### 3.2 Performance by Category

| Category                      | Overall Score | Factual Accuracy | Sample Size |
| ----------------------------- | ------------- | ---------------- | ----------- |
| Mental Health                 | 5.00/5.0      | 5.00/5.0         | 1           |
| General Health                | 4.75/5.0      | 4.33/5.0         | 4           |
| Medical Procedures            | 4.42/5.0      | 4.00/5.0         | 3           |
| Vaccination                   | 4.40/5.0      | 4.20/5.0         | 5           |
| Pregnancy/Reproductive Health | 4.17/5.0      | 3.80/5.0         | 5           |
| Nutrition                     | 4.00/5.0      | 4.00/5.0         | 2           |

### 3.3 Key Findings

#### 3.3.1 Strengths

- **Excellent Clarity**: Perfect 5.0/5.0 score across all responses
- **High Neutrality**: No bias concerns detected
- **Strong Overall Performance**: 4.56/5.0 average score
- **Consistent Quality**: Low variance in clarity and neutrality scores

#### 3.3.2 Areas of Concern

- **Factual Accuracy Variability**: Scores ranged from 1.0 to 5.0
- **Pregnancy Advice**: Lowest factual accuracy (3.80/5.0)
- **Critical Errors**: One response received factual accuracy score of 1.0

#### 3.3.3 Notable Cases

**Concerning Case (Q1 - Ibuprofen during pregnancy):**

- **GPT Response**: "Yes, ibuprofen is generally safe for treating headaches during pregnancy, especially in the first and second trimesters."
- **Ground Truth**: "According to the CDC and ACOG, ibuprofen should generally be avoided during pregnancy, especially in the third trimester, due to potential risks to the baby's heart and kidneys."
- **Evaluation**: Factual Accuracy: 1/5, Helpfulness: 1/5
- **Impact**: This error could lead to serious health risks

## 4. Discussion

### 4.1 Implications for AI Safety

#### 4.1.1 Risk Assessment

- **High-Risk Areas**: Pregnancy and reproductive health advice
- **Critical Errors**: Potential for harmful medical advice
- **Trust Implications**: Even occasional errors can undermine confidence

#### 4.1.2 Bias Analysis

- **Cultural Sensitivity**: Excellent neutrality scores suggest good cultural awareness
- **Gender Considerations**: No gender bias detected in responses
- **Accessibility**: High clarity scores indicate good communication

### 4.2 Model Performance Insights

#### 4.2.1 Strengths

- **Communication Quality**: Exceptional clarity and neutrality
- **General Knowledge**: Strong performance on common health topics
- **Safety Awareness**: Good understanding of when to recommend medical consultation

#### 4.2.2 Limitations

- **Medical Specificity**: Struggles with nuanced medical advice
- **Source Reliability**: May not always distinguish between reliable and unreliable sources
- **Context Sensitivity**: Some responses lack appropriate medical context

### 4.3 Comparison with Previous Research

Our findings align with broader research on LLM healthcare applications:

- **Similar Accuracy Patterns**: Other studies show variable factual accuracy
- **Consistent Clarity**: High communication quality is common across studies
- **Safety Concerns**: Medical misinformation remains a significant risk

## 5. Recommendations

### 5.1 For AI Developers

#### 5.1.1 Model Improvements

- **Enhanced Medical Training**: Increase training on authoritative medical sources
- **Fact-Checking Integration**: Implement real-time fact-checking mechanisms
- **Specialized Models**: Develop domain-specific models for healthcare

#### 5.1.2 Safety Measures

- **Disclaimers**: Add appropriate medical disclaimers
- **Source Attribution**: Include source citations for medical claims
- **Confidence Scoring**: Implement uncertainty quantification

### 5.2 For Healthcare Applications

#### 5.2.1 Implementation Guidelines

- **Human Oversight**: Maintain healthcare professional review
- **Clear Boundaries**: Define appropriate use cases
- **Patient Education**: Inform users about AI limitations

#### 5.2.2 Quality Assurance

- **Regular Evaluation**: Continuous monitoring of response quality
- **Feedback Loops**: Incorporate healthcare professional feedback
- **Update Protocols**: Regular updates based on new medical evidence

### 5.3 For Policy Makers

#### 5.3.1 Regulatory Framework

- **Standards Development**: Establish AI healthcare standards
- **Oversight Mechanisms**: Create appropriate regulatory oversight
- **Transparency Requirements**: Mandate disclosure of AI limitations

## 6. Limitations and Future Work

### 6.1 Study Limitations

- **Sample Size**: Limited to 20 questions
- **Evaluation Method**: Single evaluator (GPT-4)
- **Source Diversity**: Limited to English-language sources
- **Temporal Factors**: Medical knowledge evolves over time

### 6.2 Future Research Directions

#### 6.2.1 Expanded Evaluation

- **Larger Dataset**: Evaluate hundreds of health questions
- **Multiple Evaluators**: Include human healthcare professionals
- **Longitudinal Study**: Track performance over time
- **Cross-Cultural Analysis**: Evaluate responses in multiple languages

#### 6.2.2 Advanced Analysis

- **Bias Detection**: Implement automated bias detection
- **Risk Assessment**: Develop risk scoring algorithms
- **Intervention Testing**: Evaluate safety interventions
- **User Impact**: Study actual user behavior and outcomes

## 7. Conclusion

This study provides valuable insights into the current state of GPT-4's health advice capabilities. While the model demonstrates excellent communication skills and cultural sensitivity, concerns about factual accuracy, particularly in high-risk areas like pregnancy advice, highlight the need for continued improvement and careful implementation.

The findings support the importance of:

1. **Robust Evaluation Frameworks** for healthcare AI
2. **Human Oversight** in medical AI applications
3. **Continuous Monitoring** of AI performance
4. **Clear Safety Guidelines** for implementation

As AI becomes more integrated into healthcare, maintaining high standards for accuracy and safety is essential. This research contributes to the ongoing effort to ensure AI serves as a helpful tool rather than a source of medical misinformation.

## 8. References

1. Centers for Disease Control and Prevention (CDC). "Nutrition Report." https://www.cdc.gov/nutrition-report/
2. World Health Organization (WHO). "Vaccine Safety." https://www.who.int/vaccine_safety/
3. American College of Obstetricians and Gynecologists (ACOG). "Pregnancy Guidelines."
4. Mayo Clinic. "Medical Information." https://www.mayoclinic.org/
5. Reddit Medical Communities. "AskDocs and Medical Advice Forums."

---

**Author**: [Your Name]  
**Institution**: [Your Institution]  
**Date**: [Current Date]  
**Contact**: [Your Email]

_This research was conducted as part of preparation for the OpenAI Residency Program._
