#!/usr/bin/env python3
"""
Setup script for Media Knowledge Pipeline CLI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="media-knowledge-pipeline",
    version="2.5.2",
    description="Extract and synthesize knowledge from video/audio content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jason Belcher",
    author_email="belcher.jason@gmail.com",
    url="https://github.com/JasonBBelcher/media-knowledge-pipeline",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "openai-whisper>=20231117",
        "ffmpeg-python>=0.2.0",
        "yt-dlp>=2026.2.4",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "filetype>=1.2.0",
        "pydantic>=2.0.0",
        "watchdog>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-mock>=3.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "media-knowledge=media_knowledge.cli.app:app",
            "media-knowledge-launch=media_knowledge.cli.launcher:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="media, video, audio, transcription, knowledge, synthesis, youtube, ffmpeg",
)