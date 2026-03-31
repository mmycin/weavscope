"""
WeavScope Installation Guide

This module provides comprehensive installation instructions for WeavScope,
including all available installation methods and dependencies.
"""

def get_installation_guide() -> dict:
    """Get complete installation guide for WeavScope.
    
    Returns:
        Dictionary containing all installation methods and requirements.
    """
    return {
        "title": "WeavScope Installation Guide",
        "description": "Complete installation instructions for WeavScope multi-tenant Weaviate wrapper",
        "installation_methods": {
            "pip_install": {
                "title": "Standard pip Installation",
                "command": "pip install weavscope",
                "description": "Install the latest stable version from PyPI",
                "requirements": [
                    "Python 3.8 or higher",
                    "pip package manager"
                ]
            },
            "pip_install_specific_version": {
                "title": "Install Specific Version",
                "command": "pip install weavscope==1.0.0",
                "description": "Install a specific version of WeavScope",
                "note": "Replace 1.0.0 with your desired version"
            },
            "pip_install_from_git": {
                "title": "Install from Git Repository",
                "command": "pip install git+https://github.com/mmycin/weavscope.git",
                "description": "Install the latest development version from GitHub",
                "requirements": [
                    "Git installed on your system",
                    "Internet connection"
                ]
            },
            "pip_install_from_git_branch": {
                "title": "Install from Specific Git Branch",
                "command": "pip install git+https://github.com/mmycin/weavscope.git@main",
                "description": "Install from a specific branch or tag",
                "note": "Replace 'main' with your desired branch name"
            },
            "local_development": {
                "title": "Local Development Installation",
                "steps": [
                    "git clone https://github.com/mmycin/weavscope.git",
                    "cd weavscope",
                    "pip install -e ."
                ],
                "description": "Install in editable mode for local development",
                "requirements": [
                    "Git installed on your system",
                    "Python development environment"
                ]
            },
            "poetry_install": {
                "title": "Poetry Installation",
                "steps": [
                    "git clone https://github.com/mmycin/weavscope.git",
                    "cd weavscope",
                    "poetry install"
                ],
                "description": "Install using Poetry dependency manager",
                "requirements": [
                    "Poetry installed",
                    "Git installed on your system"
                ]
            }
        },
        "dependencies": {
            "core_dependencies": [
                "weaviate-client>=4.0.0",
                "pydantic>=2.0.0",
                "typing-extensions>=4.0.0"
            ],
            "optional_dependencies": {
                "openai": ["openai>=1.0.0"],
                "azure": ["azure-identity>=1.0.0"],
                "google": ["google-auth>=2.0.0"],
                "cohere": ["cohere>=4.0.0"],
                "huggingface": ["transformers>=4.0.0", "torch>=2.0.0"],
                "dev": ["pytest>=7.0.0", "black>=23.0.0", "mypy>=1.0.0"]
            }
        },
        "system_requirements": {
            "python": "3.8 or higher",
            "operating_systems": [
                "Windows 10 or later",
                "macOS 10.15 or later", 
                "Linux (Ubuntu 18.04+, CentOS 7+, etc.)"
            ],
            "memory": "Minimum 4GB RAM (8GB+ recommended)",
            "storage": "Minimum 100MB free space"
        },
        "verification": {
            "title": "Verify Installation",
            "steps": [
                {
                    "command": "python -c \"import weavscope; print('WeavScope installed successfully')\"",
                    "description": "Test basic import"
                },
                {
                    "command": "python -c \"from weavscope import WeavScope, WeaviateConfig; print('Core classes imported successfully')\"",
                    "description": "Test core class imports"
                },
                {
                    "command": "pip show weavscope",
                    "description": "Check installed version and details"
                }
            ]
        },
        "troubleshooting": {
            "common_issues": [
                {
                    "issue": "ImportError: No module named 'weavscope'",
                    "solution": "Ensure WeavScope is installed and Python path is correct"
                },
                {
                    "issue": "pip: command not found",
                    "solution": "Install pip or use python -m pip install"
                },
                {
                    "issue": "Permission denied during installation",
                    "solution": "Use pip install --user or virtual environment"
                },
                {
                    "issue": "SSL certificate errors",
                    "solution": "Use pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org"
                }
            ]
        },
        "next_steps": {
            "title": "After Installation",
            "steps": [
                "Set up your Weaviate instance (local or cloud)",
                "Get API keys for your chosen embedding provider",
                "Check out the Getting Started guide",
                "Review the API documentation"
            ]
        }
    }

def get_quick_install() -> dict:
    """Get quick installation commands.
    
    Returns:
        Dictionary with the most common installation methods.
    """
    return {
        "title": "Quick Install",
        "methods": [
            {
                "name": "Latest Stable",
                "command": "pip install weavscope"
            },
            {
                "name": "Development Version", 
                "command": "pip install git+https://github.com/mmycin/weavscope.git"
            },
            {
                "name": "With OpenAI Support",
                "command": "pip install weavscope[openai]"
            },
            {
                "name": "Full Dependencies",
                "command": "pip install weavscope[all]"
            }
        ]
    }

def get_requirements() -> dict:
    """Get detailed requirements information.
    
    Returns:
        Dictionary containing all requirements and dependencies.
    """
    return {
        "python_version": ">=3.8",
        "required_packages": [
            "weaviate-client>=4.0.0",
            "pydantic>=2.0.0", 
            "typing-extensions>=4.0.0"
        ],
        "optional_providers": {
            "openai": "openai>=1.0.0",
            "azure": "azure-identity>=1.0.0",
            "google": "google-auth>=2.0.0",
            "cohere": "cohere>=4.0.0",
            "huggingface": ["transformers>=4.0.0", "torch>=2.0.0"],
            "gemini": "google-generativeai>=0.3.0",
            "voyageai": "voyageai>=0.2.0",
            "mistral": "mistral>=1.0.0",
            "jinaai": "jina>=3.0.0"
        }
    }