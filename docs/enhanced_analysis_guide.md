# Enhanced LLM Health Evaluation Analysis Guide

## Overview

This enhanced analysis system provides comprehensive evaluation and comparison of multiple AI models (GPT-3.5-turbo, GPT-4, GPT-4-turbo) on health-related questions. The system restructures evaluations from string format to structured JSON and provides advanced analysis capabilities.

## Key Improvements

### 1. **Structured Evaluation Format**

- **Before**: String-based evaluations requiring regex parsing
- **After**: Structured JSON with individual scores and justifications
- **Benefits**: Easier analysis, better data integrity, automated processing

### 2. **Multi-Model Comparison**

- Compare performance across GPT-3.5-turbo, GPT-4, and GPT-4-turbo
- Statistical significance testing
- Model evolution analysis

### 3. **Advanced Quality Metrics**

- Readability scores (Flesch Reading Ease, Flesch-Kincaid Grade)
- Vocabulary diversity analysis
- Response length and complexity metrics
- Correlation analysis between quality and characteristics

### 4. **Safety and Bias Detection**

- Identification of low-accuracy responses
- Neutrality and bias analysis
- Model-specific safety patterns

## File Structure

```
scripts/
├── restructure_evaluations.py      # Convert evaluations to structured format
├── enhanced_analysis.py            # Main analysis class and functions
└── run_enhanced_analysis.py        # Complete analysis pipeline

notebooks/
└── enhanced_analysis_notebook.ipynb # Interactive Jupyter notebook

data/
├── questions.json                  # Original questions with multi-model responses
├── evaluations.json               # Original string-based evaluations
└── evaluations_restructured.json  # New structured evaluations

results/
├── enhanced_scores.csv            # Detailed scores for each model evaluation
├── enhanced_analysis_summary.txt  # Comprehensive analysis summary
└── figures/                       # Generated visualizations
```

## Usage

### Quick Start

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run Complete Analysis**:

   ```bash
   python scripts/run_enhanced_analysis.py
   ```

3. **Interactive Analysis**:
   ```bash
   jupyter notebook notebooks/enhanced_analysis_notebook.ipynb
   ```

### Step-by-Step Process

#### Step 1: Restructure Evaluations

```python
from scripts.restructure_evaluations import restructure_evaluations

# Convert string-based evaluations to structured JSON
restructured_evaluations = restructure_evaluations()
```

#### Step 2: Run Enhanced Analysis

```python
from scripts.enhanced_analysis import EnhancedHealthAnalysis

# Initialize analyzer
analyzer = EnhancedHealthAnalysis()

# Load data
analyzer.load_data()

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
```

## Analysis Capabilities

### 1. Model Comparison Analysis

**Features**:

- Overall performance comparison across models
- Statistical significance testing (t-tests)
- Performance by question category
- Radar charts and distribution plots

**Output**:

- Model performance rankings
- P-values for statistical significance
- Category-specific insights

### 2. Response Quality Analysis

**Features**:

- Response length analysis
- Readability scoring
- Vocabulary diversity calculation
- Correlation analysis

**Metrics**:

- Flesch Reading Ease (0-100, higher = easier)
- Flesch-Kincaid Grade Level
- Type-token ratio (vocabulary diversity)
- Average sentence length

### 3. Safety and Bias Analysis

**Features**:

- Low accuracy response identification
- Neutrality concerns detection
- Model-specific safety patterns
- Risk assessment

**Thresholds**:

- Low accuracy: ≤2/5
- Neutrality concerns: ≤3/5
- Safety flags: Multiple low scores

### 4. Advanced Visualizations

**Charts Generated**:

- Radar charts for model comparison
- Box plots for criteria distribution
- Scatter plots for quality vs. characteristics
- Bar charts for category performance
- Histograms for score distributions

## Data Structure

### Restructured Evaluation Format

```json
{
  "id": 1,
  "question": "Is it safe to take ibuprofen for a headache while pregnant?",
  "ground_truth": "According to the CDC and ACOG...",
  "evaluations": {
    "gpt-3.5-turbo": {
      "factual_accuracy": 3,
      "clarity": 5,
      "neutrality": 5,
      "helpfulness": 4,
      "justification": "The AI's response is...",
      "response": "It is generally safe to take ibuprofen..."
    },
    "gpt-4": {
      "factual_accuracy": 4,
      "clarity": 5,
      "neutrality": 5,
      "helpfulness": 5,
      "justification": "The AI's response is...",
      "response": "Ibuprofen is generally not recommended..."
    },
    "gpt-4-turbo": {
      "factual_accuracy": 5,
      "clarity": 5,
      "neutrality": 5,
      "helpfulness": 5,
      "justification": "The AI's response is...",
      "response": "It is generally advised to avoid ibuprofen..."
    }
  }
}
```

### Analysis DataFrame Structure

| Column                | Description                                        |
| --------------------- | -------------------------------------------------- |
| `id`                  | Question ID                                        |
| `category`            | Question category (Pregnancy, Mental Health, etc.) |
| `model`               | AI model name                                      |
| `factual_accuracy`    | Accuracy score (1-5)                               |
| `clarity`             | Clarity score (1-5)                                |
| `neutrality`          | Neutrality score (1-5)                             |
| `helpfulness`         | Helpfulness score (1-5)                            |
| `overall_score`       | Average of all criteria                            |
| `response_length`     | Number of words in response                        |
| `flesch_reading_ease` | Readability score                                  |
| `vocab_diversity`     | Vocabulary diversity ratio                         |

## Key Insights

### Model Performance Patterns

- **GPT-4-turbo** typically performs best overall
- **GPT-3.5-turbo** shows more variability in performance
- **GPT-4** provides good balance of accuracy and clarity

### Quality Correlations

- Response length has moderate correlation with quality
- Readability scores vary by model
- Vocabulary diversity shows interesting patterns

### Safety Considerations

- Low accuracy responses are rare but important to identify
- Neutrality scores are generally high across models
- Category-specific patterns in safety concerns

## Customization

### Adding New Models

1. Update the `models` list in `EnhancedHealthAnalysis`
2. Ensure evaluations include the new model
3. Re-run analysis

### Adding New Criteria

1. Update the `criteria` list in `EnhancedHealthAnalysis`
2. Modify evaluation prompts to include new criteria
3. Update visualization functions

### Custom Analysis

```python
# Example: Custom analysis for specific category
pregnancy_data = df[df['category'] == 'Pregnancy/Reproductive Health']
pregnancy_performance = pregnancy_data.groupby('model')['overall_score'].mean()
print(pregnancy_performance)
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**:

   ```bash
   pip install textstat scipy scikit-learn
   ```

2. **NLTK Data Missing**:

   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

3. **File Not Found Errors**:
   - Ensure data files exist in correct locations
   - Check file permissions
   - Verify JSON format is valid

### Performance Tips

1. **Large Datasets**: Use pandas chunking for very large datasets
2. **Memory Usage**: Clear variables between analysis steps
3. **API Limits**: Add delays between API calls during restructuring

## Future Enhancements

### Planned Features

1. **Response Similarity Analysis**: Compare response similarity across models
2. **Temporal Analysis**: Track model performance over time
3. **Domain-Specific Metrics**: Specialized metrics for different health domains
4. **Human Evaluation Integration**: Combine with human evaluator scores
5. **Real-time Analysis**: Live analysis of new responses

### Research Applications

1. **Model Selection**: Choose best model for specific health domains
2. **Safety Monitoring**: Continuous monitoring of model safety
3. **Bias Detection**: Automated bias detection and reporting
4. **Quality Assurance**: Quality control for health AI systems

## Contributing

To contribute to the enhanced analysis:

1. Follow the existing code structure
2. Add comprehensive documentation
3. Include unit tests for new functions
4. Update this guide with new features
5. Ensure backward compatibility

## Support

For questions or issues:

1. Check the troubleshooting section
2. Review the example code
3. Examine the Jupyter notebook for usage examples
4. Contact the development team
