# TerraGuard AI Model Comparison Report

## Model: Gemini
**File Analyzed:** `main.tf`
**Issues Detected:** 4

- 🔍 **Security Risk** at line 8: S3 bucket has public-read ACL which can expose sensitive data to the public.
- 🔍 **Best Practice** at line 17: Hardcoded AMI ID can lead to issues if the AMI is deregistered or deleted.
- 🔍 **Best Practice** at line 18: Instance type is hardcoded, consider making it a variable for flexibility.
- 🔍 **Best Practice** at line 1: AWS region is hardcoded, consider making it a variable for flexibility.

---

## Model: CodeBERT
**File Analyzed:** `main.tf`
**Issues Detected:** 1

- 🔍 **None** at line N/A: CodeBERT classified the file as 'None'

---
