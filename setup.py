from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="terraguard",
    version="1.0.0",
    author="TerraGuard Team",
    author_email="contact@terraguard.dev",
    description="AI Mentor for Infrastructure-as-Code - Terraform Analysis Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/terraguard",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/terraguard/issues",
        "Source": "https://github.com/yourusername/terraguard",
        "Documentation": "https://github.com/yourusername/terraguard/wiki",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: System :: Systems Administration",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "pre-commit>=2.0",
        ],
        "docker": [
            "docker>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "terraguard=run_analysis:main",
            "terraguard-web=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "terraguard": [
            "assets/*",
            "examples/*",
            "outputs/*",
        ],
    },
    keywords=[
        "terraform",
        "infrastructure-as-code",
        "iac",
        "security",
        "ai",
        "gemini",
        "codebert",
        "devops",
        "cloud",
        "aws",
        "analysis",
        "linting",
    ],
)
