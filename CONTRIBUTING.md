# Contributing to TerraGuard

Thank you for your interest in contributing to TerraGuard! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### **Reporting Issues**
- Use GitHub Issues to report bugs or request features
- Provide detailed information about the problem
- Include steps to reproduce the issue
- Attach relevant files or error messages

### **Suggesting Enhancements**
- Open a GitHub Issue with the "enhancement" label
- Describe the proposed feature in detail
- Explain the benefits and use cases
- Consider implementation complexity

### **Code Contributions**
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add tests** for new functionality
5. **Ensure all tests pass**
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to your branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

## 🛠️ Development Setup

### **Prerequisites**
- Python 3.8 or higher
- Git
- Gemini API key (for testing)

### **Local Development**
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/terraguard.git
cd TerraGuard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Set up environment variables
cp env.example .env
# Edit .env with your Gemini API key
```

### **Running Tests**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=analyzer

# Run specific test file
pytest tests/test_ai_suggester.py
```

### **Code Quality**
```bash
# Format code
black analyzer/ app.py run_analysis.py

# Lint code
flake8 analyzer/ app.py run_analysis.py

# Type checking
mypy analyzer/
```

## 📋 Coding Standards

### **Python Style**
- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Write docstrings for all functions and classes
- Keep functions small and focused

### **Code Organization**
- Place new analyzers in the `analyzer/` directory
- Add corresponding tests in `tests/`
- Update documentation for new features
- Maintain backward compatibility when possible

### **Commit Messages**
- Use clear, descriptive commit messages
- Start with a verb in imperative mood
- Examples:
  - `Add support for CloudFormation analysis`
  - `Fix S3 bucket ACL detection logic`
  - `Update README with installation instructions`

## 🧪 Testing Guidelines

### **Test Structure**
- Create test files in the `tests/` directory
- Use descriptive test function names
- Test both success and failure cases
- Mock external API calls

### **Example Test**
```python
import pytest
from unittest.mock import patch, MagicMock
from analyzer.ai_suggester import analyze_with_gpt4

def test_analyze_with_gpt4_success():
    """Test successful Gemini analysis."""
    with patch('analyzer.ai_suggester.client') as mock_client:
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '[{"type": "Security Risk", "line": 1, "message": "Test issue"}]'
        mock_client.chat.completions.create.return_value = mock_response
        
        result = analyze_with_gpt4("test_file.tf")
        
        assert len(result) == 1
        assert result[0]["type"] == "Security Risk"
```

## 🎯 Areas for Contribution

### **High Priority**
- **New AI Models**: Integrate additional analysis models (Claude, Gemini, etc.)
- **Enhanced CodeBERT**: Improve Terraform-specific analysis
- **Multi-file Support**: Analyze entire Terraform modules/projects
- **Custom Rules**: Allow users to define their own security rules
- **CI/CD Integration**: REST API for pipeline integration

### **Medium Priority**
- **Cost Analysis**: Infrastructure cost optimization recommendations
- **Compliance Mapping**: Map findings to frameworks (CIS, NIST, SOC2)
- **Performance Optimization**: Caching, parallel processing
- **UI Improvements**: Better visualization, dark mode, mobile support

### **Low Priority**
- **Documentation**: More examples, tutorials, video guides
- **Internationalization**: Multi-language support
- **Plugin System**: Extensible architecture for custom analyzers

## 🔍 Review Process

### **Pull Request Requirements**
- All tests must pass
- Code must be properly formatted and linted
- Documentation must be updated
- New features must include tests
- Breaking changes must be clearly documented

### **Review Criteria**
- **Functionality**: Does the code work as intended?
- **Code Quality**: Is the code clean, readable, and maintainable?
- **Testing**: Are there adequate tests for the changes?
- **Documentation**: Is the documentation updated appropriately?
- **Performance**: Are there any performance implications?

## 📚 Documentation

### **Code Documentation**
- Use docstrings for all public functions and classes
- Include parameter descriptions and return value information
- Provide usage examples where helpful

### **User Documentation**
- Update README.md for new features
- Add examples to the `examples/` directory
- Create tutorials for complex features

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Python version
   - Operating system
   - TerraGuard version

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Sample Terraform files (if applicable)
   - Expected vs actual behavior

3. **Additional Context**
   - Error messages or logs
   - Screenshots (for UI issues)
   - Related issues or discussions

## 💡 Feature Requests

When suggesting features, please include:

1. **Problem Description**
   - What problem does this solve?
   - Who would benefit from this feature?

2. **Proposed Solution**
   - How should this feature work?
   - Any specific requirements or constraints?

3. **Alternatives Considered**
   - What other solutions have you considered?
   - Why is this approach preferred?

## 📞 Getting Help

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bug reports and feature requests
- **Pull Requests**: For code contributions

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to TerraGuard! 🚀
