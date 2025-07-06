# Contributing to LLM Health Evaluation

Thank you for your interest in contributing to the LLM Health Evaluation project! This document provides guidelines for contributing to this research project.

## 🤝 How to Contribute

### Types of Contributions

We welcome contributions in the following areas:

1. **Research & Analysis**

   - Expanding the evaluation dataset
   - Improving evaluation criteria
   - Adding new LLM models for comparison
   - Enhancing statistical analysis methods

2. **Code & Tools**

   - Bug fixes and improvements
   - New analysis scripts
   - Enhanced visualizations
   - Performance optimizations

3. **Documentation**

   - Improving README and documentation
   - Adding code comments
   - Creating tutorials or guides
   - Translating documentation

4. **Data & Resources**
   - Additional health questions
   - New authoritative sources
   - Enhanced ground truth data
   - Cross-validation datasets

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API key (for running evaluations)

### Setup

1. **Fork the repository**

   ```bash
   git clone https://github.com/yourusername/llm-health-eval.git
   cd llm-health-eval
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**

   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

4. **Run tests**
   ```bash
   python -m pytest tests/
   ```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise

### Testing

- Write tests for new functionality
- Ensure all tests pass before submitting
- Include both unit tests and integration tests
- Test with different Python versions (3.8+)

### Documentation

- Update README.md for significant changes
- Add docstrings to new functions
- Include examples in documentation
- Update requirements.txt for new dependencies

## 🔬 Research Contributions

### Adding New Questions

1. **Question Format**

   ```json
   {
     "id": 31,
     "question": "Your health question here?",
     "answer": "Authoritative answer from CDC/WHO/etc.",
     "source": "Source name",
     "link": "URL to source"
   }
   ```

2. **Evaluation Criteria**
   - Ensure questions cover diverse health topics
   - Include questions with clear authoritative answers
   - Consider questions that test model limitations

### Adding New Models

1. **Model Integration**

   - Add model to the evaluation pipeline
   - Ensure consistent API usage
   - Handle rate limits and errors gracefully

2. **Evaluation Consistency**
   - Use same evaluation criteria
   - Maintain consistent scoring methodology
   - Include model in all comparative analyses

## 📊 Data Guidelines

### Data Quality

- Verify all ground truth answers with authoritative sources
- Ensure questions are clear and unambiguous
- Maintain consistency in evaluation criteria
- Document any changes to evaluation methodology

### Privacy & Ethics

- Do not include personally identifiable information
- Ensure compliance with medical ethics guidelines
- Respect patient privacy in all data handling
- Follow responsible AI development practices

## 🐛 Bug Reports

### Reporting Issues

When reporting bugs, please include:

1. **Environment details**

   - Python version
   - Operating system
   - Package versions

2. **Steps to reproduce**

   - Clear, step-by-step instructions
   - Expected vs. actual behavior
   - Error messages and stack traces

3. **Additional context**
   - Screenshots if applicable
   - Related issues or discussions
   - Potential workarounds

## 💡 Feature Requests

### Suggesting Features

When suggesting new features:

1. **Clear description** of the proposed feature
2. **Use case** and expected benefits
3. **Implementation approach** if possible
4. **Related work** or references

## 🔄 Pull Request Process

### Before Submitting

1. **Test your changes**

   - Run the full analysis pipeline
   - Ensure all tests pass
   - Check for any new warnings

2. **Update documentation**

   - Update README if needed
   - Add docstrings for new code
   - Update requirements.txt

3. **Follow commit conventions**
   - Use clear, descriptive commit messages
   - Reference issues when applicable
   - Keep commits focused and atomic

### Pull Request Guidelines

1. **Title and description**

   - Clear, descriptive title
   - Detailed description of changes
   - Reference related issues

2. **Code review**

   - Address reviewer feedback
   - Ensure code quality standards
   - Update based on suggestions

3. **Testing**
   - All tests must pass
   - New functionality should be tested
   - Performance impact considered

## 📋 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Focus on constructive feedback
- Respect different viewpoints
- Maintain professional behavior

### Enforcement

- Unacceptable behavior will not be tolerated
- Maintainers will address issues promptly
- Focus on resolution and learning

## 📞 Getting Help

### Questions and Support

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For sensitive or private matters

### Resources

- [Project Documentation](docs/)
- [Analysis Notebook](notebooks/analysis.ipynb)
- [Research Summary](docs/comprehensive_summary.md)

## 🏆 Recognition

Contributors will be recognized in:

- Project README
- Release notes
- Academic publications (if applicable)
- Conference presentations

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AI safety and healthcare research! 🎉
