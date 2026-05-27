# TerraGuard Examples

This directory contains example Terraform configurations for testing TerraGuard analysis capabilities.

## Files

### `main.tf` - Basic AWS Infrastructure
A simple AWS infrastructure setup with common security issues and best practice violations.

**Resources:**
- S3 bucket with public ACL (Security Risk)
- EC2 instance with hardcoded values (Best Practice violations)
- AWS provider with hardcoded region

**Issues Detected:**
- Security Risk: Public S3 bucket ACL
- Best Practice: Hardcoded AMI ID
- Best Practice: Hardcoded instance type
- Best Practice: Hardcoded AWS region

## Usage

1. **Run Analysis:**
   ```bash
   python run_analysis.py
   ```

2. **View Results:**
   ```bash
   streamlit run app.py
   ```

3. **Upload Custom Files:**
   Use the web interface to upload your own `.tf` files for analysis.

## Creating Your Own Examples

To test TerraGuard with your own Terraform files:

1. **Create a `.tf` file** with your infrastructure code
2. **Update `run_analysis.py`** to point to your file:
   ```python
   TERRAFORM_FILE = "examples/your_file.tf"
   ```
3. **Run the analysis** and view results in the web interface

## Common Patterns to Test

### Security Risks
- Public S3 bucket ACLs
- Unrestricted security groups
- Missing encryption
- Exposed secrets in code

### Best Practice Violations
- Hardcoded values (AMIs, instance types, regions)
- Missing resource tags
- Inconsistent naming conventions
- Missing variable definitions

### Quality Issues
- Unused resources
- Circular dependencies
- Missing documentation
- Inconsistent formatting
