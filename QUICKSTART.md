# TerraGuard Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### **Step 1: Clone and Install**
```bash
git clone https://github.com/yourusername/terraguard.git
cd TerraGuard
pip install -r requirements.txt
```

### **Step 2: Set Up Environment**
```bash
cp env.example .env
# Edit .env and add your Gemini API key
echo "GEMINI_API_KEY=your-gemini-key-here" > .env
```

### **Step 3: Run Analysis**
```bash
python run_analysis.py
```

### **Step 4: View Results**
```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

## 🐳 Docker Quick Start

### **Using Docker Compose**
```bash
# Set your API key
export GEMINI_API_KEY=your-gemini-key-here

# Start TerraGuard
docker-compose up -d

# View at http://localhost:8501
```

### **Using Docker**
```bash
# Build image
docker build -t terraguard .

# Run container
docker run -p 8501:8501 -e GEMINI_API_KEY=your-gemini-key-here terraguard
```

## 📊 Understanding the Results

### **Issue Types**
- **🔴 Security Risk**: Critical vulnerabilities that could expose your infrastructure
- **🟡 Best Practice**: Recommendations for better code quality and maintainability
- **🟠 Warning**: Potential issues that should be reviewed

### **Model Comparison**
- **Gemini**: Detailed, contextual analysis with specific line numbers
- **CodeBERT**: File-level classification (currently limited)
- **Rule Engine**: Traditional pattern-based checks

## 🔧 Customization

### **Adding Custom Rules**
Edit `analyzer/rule_engine.py` to add your own security checks:

```python
def check_custom_rule(resources):
    issues = []
    # Your custom logic here
    return issues
```

### **Modifying AI Prompts**
Edit `analyzer/ai_suggester.py` to customize Gemini analysis:

```python
prompt = f"""
Your custom prompt here...
Terraform Code:
```hcl
{code}
```"""
```

## 🚨 Troubleshooting

### **Common Issues**

1. **API Key Error**
   - Ensure your Gemini API key is valid
   - Check that the `.env` file is in the project root
   - Verify the key has sufficient credits

2. **Import Errors**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **Streamlit Issues**
   - Clear browser cache
   - Try a different port: `streamlit run app.py --server.port 8502`

4. **Docker Issues**
   - Ensure Docker is running
   - Check port 8501 is not in use
   - Verify API key is set in environment

### **Getting Help**
- Check the [GitHub Issues](https://github.com/yourusername/terraguard/issues)
- Join [GitHub Discussions](https://github.com/yourusername/terraguard/discussions)
- Read the [full documentation](README.md)

## 🎯 Next Steps

1. **Analyze Your Own Files**: Upload `.tf` files through the web interface
2. **Integrate with CI/CD**: Use the analysis pipeline in your deployment process
3. **Customize Rules**: Add domain-specific security checks
4. **Contribute**: Help improve TerraGuard by submitting issues and pull requests

## 📚 Additional Resources

- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)
- [AWS Security Best Practices](https://aws.amazon.com/security/security-resources/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
