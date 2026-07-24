from setuptools import setup, find_packages

setup(
    name="conductor-task-queue",
    version="0.1.0",
    author="Panagiotis Panageas",
    author_email="panagiotis@conductor.sh",
    description="A lightweight, production-ready async task queue for Python teams that don't need Redis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/conductor-sh/conductor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "asyncpg>=0.27.0",
        "aiohttp>=3.8.0",
        "pydantic>=1.10.0",
        "prometheus-client>=0.14.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "conductor=conductor.cli:main",
        ],
    },
)
