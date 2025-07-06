# LLM Health Advice Evaluation: A Comprehensive Multi-Model Assessment

This project provides a comprehensive evaluation of Large Language Model (LLM) performance in health advice scenarios, comparing GPT-3.5-turbo, GPT-4, and GPT-4-turbo across 30 diverse health questions against authoritative medical sources.

**Research Question:** How do different LLM models perform in providing accurate, safe, and helpful health advice compared to verified sources such as CDC, WHO, and medical institutions?

## 🎯 Project Overview

This research evaluates three leading LLM models on 30 health-related questions across multiple categories:

- **Pregnancy/Reproductive Health** (5 questions)
- **Mental Health** (1 question)
- **Medical Procedures** (8 questions)
- **Cardiovascular Health** (3 questions)
- **Nutrition/Lifestyle** (6 questions)
- **General Health** (7 questions)

## 📊 Key Results

| Model             | Overall Score | Factual Accuracy | Clarity   | Neutrality | Helpfulness |
| ----------------- | ------------- | ---------------- | --------- | ---------- | ----------- |
| **GPT-4**         | **4.853/5.0** | 4.586/5.0        | 4.966/5.0 | 5.000/5.0  | 4.862/5.0   |
| **GPT-3.5-turbo** | 4.833/5.0     | 4.500/5.0        | 5.000/5.0 | 5.000/5.0  | 4.833/5.0   |
| **GPT-4-turbo**   | 4.808/5.0     | 4.517/5.0        | 4.966/5.0 | 5.000/5.0  | 4.800/5.0   |

### 🚨 Critical Findings

- **GPT-4 emerges as the top performer** across all evaluation criteria
- **Perfect neutrality scores** across all models (5.0/5.0) - no harmful bias detected
- **High clarity scores** (4.97-5.0/5.0) ensure patient understanding
- **Factual accuracy shows most variation** (4.5-4.6/5.0) - primary area for improvement
- **Only 4 low-accuracy instances** (≤2/5) out of 90 total responses (4.4%)

## 🏗️ Project Structure

```
llm-health-eval/
├── data/                           # Data files
│   ├── questions.json              # 30 health questions with ground truth
│   ├── evaluations.json            # Original string-based evaluations
│   ├── evaluations_restructured.json # Enhanced structured evaluations
│   └── scores.csv                  # Processed evaluation scores
├── scripts/                        # Analysis and automation scripts
│   ├── evaluate_responses.py       # GPT-4 evaluation pipeline
│   ├── generate_answers.py         # AI response generation
│   ├── restructure_evaluations.py  # Convert to structured format
│   ├── enhanced_analysis.py        # Comprehensive analysis pipeline
│   └── quick_analysis.py           # Fast results summary
├── notebooks/                      # Jupyter analysis notebooks
│   └── analysis.ipynb              # Interactive comprehensive analysis
├── results/                        # Output files and visualizations
│   ├── figures/                    # 9 comprehensive visualizations
│   │   ├── overall_performance.png
│   │   ├── category_comparison.png
│   │   ├── performance_trends.png
│   │   ├── risk_assessment.png
│   │   ├── correlation_matrix.png
│   │   ├── length_analysis.png
│   │   ├── category_heatmap.png
│   │   ├── performance_dashboard.png
│   │   └── model_comparison_analysis.png
│   ├── analysis_summary.txt        # Summary statistics
│   └── multi_model_summary.txt     # Multi-model comparison summary
└── docs/                           # Documentation
    ├── comprehensive_summary.md    # Detailed project summary
    └── writeup_template.md         # Research writeup template
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key
- Required packages (see `requirements.txt`)

### Installation

```bash
git clone https://github.com/ayobami-at-daylight/llm-health-eval.git
cd llm-health-eval
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file with your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

### Running the Enhanced Analysis

```bash
# Generate AI responses for questions
python scripts/generate_answers.py

# Evaluate responses using GPT-4
python scripts/evaluate_responses.py

# Restructure evaluations into structured format
python scripts/restructure_evaluations.py

# Run comprehensive analysis with visualizations
python scripts/enhanced_analysis.py

# Quick results summary
python scripts/quick_analysis.py
```

## 📈 Enhanced Analysis Results

### Performance by Category

- **Mental Health**: 5.000/5.0 (Perfect score across all models)
- **Pregnancy/Reproductive Health**: 4.867/5.0
- **Cardiovascular Health**: 4.889/5.0
- **Medical Procedures**: 4.837/5.0
- **Nutrition/Lifestyle**: 4.653/5.0

### Response Characteristics

| Model             | Average Words | Response Style          |
| ----------------- | ------------- | ----------------------- |
| **GPT-3.5-turbo** | 70.9          | Concise, direct         |
| **GPT-4**         | 100.7         | Balanced, comprehensive |
| **GPT-4-turbo**   | 132.1         | Detailed, thorough      |

### Safety Assessment

- **Safe responses** (4-5 accuracy): 95.6%
- **Low risk** (3-4 accuracy): 0%
- **Medium risk** (2-3 accuracy): 4.4%
- **High risk** (1-2 accuracy): 0%

## 🔍 Key Insights

### Strengths

- **Excellent safety standards**: Perfect neutrality scores across all models
- **High clarity**: All models communicate health information clearly
- **Strong general performance**: GPT-4 leads with 4.853/5.0 overall score
- **Consistent helpfulness**: All models provide practical, actionable advice

### Areas for Improvement

- **Factual accuracy variability**: Scores range from 1.0 to 5.0
- **Response length consistency**: Significant variation in detail level
- **Domain-specific gaps**: Some medical areas show lower accuracy

### Notable Findings

**Model Comparison:**

- **GPT-4** excels in factual accuracy and helpfulness
- **GPT-3.5-turbo** shows strong performance despite being older
- **GPT-4-turbo** provides most detailed responses but slightly lower scores

**Safety Analysis:**

- All models maintain high safety standards
- No instances of harmful or biased advice
- Appropriate medical disclaimers consistently included

## 🛡️ AI Safety Implications

### Risk Factors

1. **Factual Accuracy Gaps**: Some responses contain medical inaccuracies
2. **Response Length Variation**: Inconsistent detail levels may confuse users
3. **Domain-Specific Limitations**: Certain medical areas need improvement

### Recommendations

1. **Implement GPT-4 for Critical Health Information**: Best overall performance
2. **Establish Fact-Checking Protocols**: Automated verification for low-accuracy responses
3. **Standardize Response Length**: Consistent detail levels for user experience
4. **Maintain Human Oversight**: Healthcare professional review for complex cases
5. **Continuous Monitoring**: Ongoing evaluation as models evolve

## 📚 Research Contributions

This project contributes to:

- **Multi-Model Comparison**: First comprehensive comparison of GPT-3.5-turbo, GPT-4, and GPT-4-turbo in healthcare
- **Structured Evaluation Framework**: Enhanced methodology with individual criterion scoring
- **Safety Assessment**: Comprehensive analysis of AI safety in health contexts
- **Implementation Guidelines**: Practical recommendations for healthcare AI deployment
- **Policy Development**: Evidence-based insights for AI healthcare regulations

## 🔬 Enhanced Methodology

### Evaluation Framework

Each response evaluated on 4 criteria (1-5 scale):

1. **Factual Accuracy**: Correctness vs. authoritative medical sources
2. **Clarity**: Communication quality and understandability
3. **Neutrality**: Absence of bias and harmful content
4. **Helpfulness**: Practical value and actionable advice

### Data Sources

- **CDC**: Official health guidelines and recommendations
- **WHO**: International health standards and protocols
- **Mayo Clinic**: Medical expertise and clinical guidelines
- **ACOG**: Obstetric and gynecological standards
- **Medical Communities**: Reddit AskDocs and medical forums

### Statistical Analysis

- **Multi-model comparison** with statistical significance testing
- **Response quality metrics** (readability, vocabulary diversity)
- **Safety and bias detection** algorithms
- **Category-based performance analysis**
- **Correlation analysis** between evaluation criteria

## 📄 Documentation

- **Comprehensive Summary**: `docs/comprehensive_summary.md` - Detailed project overview
- **Analysis Notebook**: `notebooks/analysis.ipynb` - Interactive exploration
- **Visualizations**: `results/figures/` - 9 comprehensive charts and graphs
- **Structured Data**: `data/evaluations_restructured.json` - Enhanced evaluation format

## 🤝 Contributing

This research contributes to the growing body of work on AI safety and reliability in healthcare applications. For questions, collaboration opportunities, or to contribute to this research, please reach out.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📊 Data Availability

The evaluation data, including structured assessments and visualizations, is available in the `data/` and `results/` directories. The enhanced evaluation framework and analysis scripts are provided for reproducibility and further research.

---

**Author**: Usman Ayobami  
**Institution**: Western Michigan University
**Research Area**: AI Safety, Healthcare AI, LLM Evaluation, Multi-Model Comparison

_This research provides critical insights into LLM performance in healthcare contexts and contributes to the development of safe, reliable AI systems for medical information delivery._
