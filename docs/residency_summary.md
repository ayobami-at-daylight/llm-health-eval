# LLM Health Advice Evaluation - OpenAI Residency Application Summary

## Project Overview

**Research Question**: How factually accurate and unbiased are GPT-4's responses to common health questions compared to authoritative medical sources?

**Key Finding**: GPT-4 achieves 4.66/5.0 overall performance but shows concerning factual accuracy gaps in high-risk areas like pregnancy advice.

## Technical Implementation

### Data Pipeline

- **20 health questions** across 6 categories (pregnancy, mental health, medical procedures, vaccination, nutrition, general health)
- **Automated evaluation** using GPT-4 as evaluator with structured criteria
- **Multi-criteria assessment**: Factual accuracy, clarity, neutrality, helpfulness (1-5 scale)
- **Ground truth validation** against CDC, WHO, Mayo Clinic, and medical communities

### Code Architecture

```python
# Core evaluation pipeline
def evaluate_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

# Multi-criteria scoring
criteria = ['factual_accuracy', 'clarity', 'neutrality', 'helpfulness']
df['overall_score'] = df[criteria].mean(axis=1)
```

### Analysis Framework

- **Statistical analysis**: Descriptive statistics, correlation analysis, category comparisons
- **Risk assessment**: Identification of concerning cases (accuracy ≤2/5)
- **Visualization suite**: 7 comprehensive charts including performance dashboards, heatmaps, and risk assessments
- **Qualitative analysis**: Detailed examination of critical errors

## Key Results

### Performance Metrics

| Criterion        | Score        | Standard Deviation |
| ---------------- | ------------ | ------------------ |
| **Overall**      | **4.66/5.0** | 0.54               |
| Factual Accuracy | 4.25/5.0     | 1.12               |
| Clarity          | 5.00/5.0     | 0.00               |
| Neutrality       | 5.00/5.0     | 0.00               |
| Helpfulness      | 4.35/5.0     | 1.07               |

### Category Performance

- **Mental Health**: 5.00/5.0 (Perfect)
- **General Health**: 4.75/5.0
- **Vaccination**: 4.40/5.0
- **Medical Procedures**: 4.42/5.0
- **Pregnancy/Reproductive Health**: 4.17/5.0 (Lowest)
- **Nutrition**: 4.00/5.0

### Critical Findings

- **2 concerning cases** with factual accuracy ≤2/5
- **Perfect clarity and neutrality** across all responses
- **Pregnancy advice** shows highest risk for medical misinformation

## AI Safety Implications

### Risk Assessment

- **High-Risk Areas**: Pregnancy and reproductive health advice
- **Critical Errors**: Potential for harmful medical advice
- **False Confidence**: High clarity may mask inaccuracies

### Safety Recommendations

1. **Enhanced Fact-Checking**: Real-time verification mechanisms
2. **Medical Disclaimers**: Appropriate warnings and limitations
3. **Human Oversight**: Healthcare professional review
4. **Source Attribution**: Citations for medical claims

## Technical Contributions

### Evaluation Methodology

- **Structured prompting** for consistent evaluation
- **Multi-dimensional scoring** beyond simple accuracy
- **Automated pipeline** for scalable assessment
- **Risk categorization** for safety monitoring

### Code Quality

- **Modular design** with clear separation of concerns
- **Comprehensive testing** of evaluation criteria
- **Reproducible analysis** with version-controlled data
- **Professional documentation** and visualization

### Research Rigor

- **Authoritative sources** for ground truth validation
- **Statistical significance** testing between categories
- **Qualitative analysis** of concerning cases
- **Transparent methodology** with detailed documentation

## Relevance to OpenAI Residency

### AI Safety Focus

This project directly addresses OpenAI's mission of ensuring AI systems are safe and beneficial. The research identifies specific risks in healthcare AI applications and proposes concrete safety measures.

### Technical Skills Demonstrated

- **LLM Evaluation**: Comprehensive assessment of GPT-4 performance
- **Data Analysis**: Statistical analysis and visualization
- **Safety Engineering**: Risk assessment and mitigation strategies
- **Research Methodology**: Rigorous experimental design and documentation

### Potential Impact

- **Healthcare AI Guidelines**: Informs safety standards for medical AI
- **Model Improvement**: Identifies specific areas for enhancement
- **Policy Development**: Supports regulatory frameworks for AI in healthcare
- **Trust Building**: Establishes confidence in AI health applications

## Future Work

### Immediate Extensions

- **Larger Dataset**: Evaluate hundreds of health questions
- **Human Evaluators**: Include healthcare professionals
- **Multiple Models**: Compare GPT-4 with other LLMs
- **Intervention Testing**: Evaluate safety measures

### Long-term Research

- **Real-time Monitoring**: Continuous evaluation systems
- **Cross-cultural Analysis**: Multi-language assessment
- **User Impact Studies**: Actual patient outcomes
- **Automated Safety**: Real-time risk detection

## Code Repository

**GitHub**: https://github.com/ayobamiu/llm-health-eval

**Key Files**:

- `scripts/evaluate_responses.py`: Core evaluation pipeline
- `notebooks/analysis.ipynb`: Comprehensive analysis
- `docs/writeup.md`: Detailed research paper
- `results/figures/`: 7 professional visualizations

## Conclusion

This research demonstrates strong technical skills in LLM evaluation, data analysis, and AI safety assessment. The findings provide valuable insights for improving healthcare AI systems and contribute to the broader AI safety community. The project showcases the ability to conduct rigorous research with real-world impact, making it highly relevant for the OpenAI Residency Program.

---

**Technical Stack**: Python, OpenAI API, Pandas, Matplotlib, Seaborn, Jupyter  
**Research Area**: AI Safety, Healthcare AI, LLM Evaluation  
**Impact**: Direct contribution to AI safety in healthcare applications
