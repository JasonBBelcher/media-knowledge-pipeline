"""
Prompt Templates Module

Contains reusable prompt templates for knowledge synthesis from transcripts.

This module provides a collection of pre-defined prompt templates that can be
used to extract different types of knowledge from transcribed audio/video content.
Templates are organized by use case and can be easily extended.
"""

from typing import Dict, Optional


class PromptTemplates:
    """
    Collection of prompt templates for knowledge synthesis.
    
    Each template uses the {transcript} placeholder which will be replaced
    with the actual transcript content during synthesis.
    """
    
    # Basic Templates
    BASIC_SUMMARY = """Extract the core thesis, key insights, and actionable takeaways from this transcript:

{transcript}

Please structure your response with:
1. Core Thesis (1-2 sentences)
2. Key Insights (3-5 bullet points)
3. Actionable Takeaways (3-5 bullet points)"""
    
    MEETING_MINUTES = """Act as a professional secretary. From this meeting transcript, create structured meeting minutes:

{transcript}

Please organize your response with these sections:
1. Meeting Overview (date, participants, topic)
2. Decisions Made (with brief rationale)
3. Action Items (owner, task, deadline)
4. Open Questions (unresolved issues)
5. Next Steps"""
    
    # Educational Templates
    LECTURE_SUMMARY = """Summarize this lecture transcript for educational purposes:

{transcript}

Please provide:
1. Main Topic and Learning Objectives
2. Key Concepts Explained (with brief definitions)
3. Important Examples or Case Studies
4. Key Takeaways for Students
5. Suggested Further Reading or Resources"""
    
    TUTORIAL_GUIDE = """Convert this tutorial transcript into a step-by-step guide:

{transcript}

Please structure as:
1. Overview (what this tutorial covers)
2. Prerequisites (what you need before starting)
3. Step-by-Step Instructions (numbered, clear and concise)
4. Common Issues and Solutions
5. Summary"""
    
    # Business Templates
    PROJECT_UPDATE = """Create a professional project status update from this transcript:

{transcript}

Include:
1. Executive Summary (2-3 sentences)
2. Progress Made (completed tasks, milestones)
3. Current Status (on track, at risk, delayed)
4. Blockers and Challenges
5. Next Steps and Timeline"""
    
    CUSTOMER_FEEDBACK = """Analyze this customer feedback transcript:

{transcript}

Provide:
1. Customer Sentiment (positive, neutral, negative)
2. Key Themes and Topics Mentioned
3. Specific Pain Points or Issues
4. Positive Feedback Highlights
5. Actionable Recommendations for Improvement"""
    
    # Research Templates
    RESEARCH_SUMMARY = """Summarize this research discussion transcript:

{transcript}

Include:
1. Research Question or Problem Statement
2. Methodology or Approach Discussed
3. Key Findings or Insights
4. Limitations or Challenges
5. Future Research Directions"""
    
    INTERVIEW_SUMMARY = """Summarize this interview transcript:

{transcript}

Provide:
1. Interview Overview (interviewee, topic, duration)
2. Main Themes Discussed
3. Key Quotes or Notable Statements
4. Important Insights or Revelations
5. Conclusion or Final Thoughts"""
    
    # Content Creation Templates
    BLOG_POST_OUTLINE = """Create a blog post outline from this transcript:

{transcript}

Structure as:
1. Catchy Title
2. Engaging Introduction (hook)
3. Main Sections (3-5 with subheadings)
4. Key Points for Each Section
5. Conclusion and Call to Action"""
    
    SOCIAL_MEDIA_CONTENT = """Extract key points from this transcript for social media content:

{transcript}

Provide:
1. 3-5 Tweet-length quotes (280 characters max)
2. 2-3 LinkedIn post ideas (professional tone)
3. Key hashtags relevant to the content
4. Suggested visuals or graphics"""
    
    # Technical Templates
    TECHNICAL_DOCUMENTATION = """Create technical documentation from this transcript:

{transcript}

Include:
1. Overview and Purpose
2. Technical Specifications or Requirements
3. Implementation Details
4. Code Examples or Commands (if applicable)
5. Troubleshooting or FAQ"""
    
    BUG_REPORT_SUMMARY = """Summarize this bug report or technical discussion:

{transcript}

Provide:
1. Issue Summary (what's broken)
2. Reproduction Steps (how to reproduce)
3. Expected vs Actual Behavior
4. Root Cause Analysis (if discussed)
5. Proposed Solutions or Workarounds"""
    
    # Utility template for generating descriptive filenames
    FILENAME_SUBJECT = """Based on the synthesized content below, provide a short, descriptive subject line that would be suitable as a filename (3-5 words maximum). Focus on the core topic or main concept discussed:

{synthesis}

Examples of good subjects:
- "second_brain_productivity"
- "ai_meeting_summarization"
- "cognitive_offloading_systems"
- "productivity_workflow_optimization"

Respond with ONLY the subject, no other text."""


# Dictionary mapping template keys to templates
PROMPT_TEMPLATES: Dict[str, str] = {
    # Basic templates
    "basic_summary": PromptTemplates.BASIC_SUMMARY,
    "meeting_minutes": PromptTemplates.MEETING_MINUTES,
    
    # Educational templates
    "lecture_summary": PromptTemplates.LECTURE_SUMMARY,
    "tutorial_guide": PromptTemplates.TUTORIAL_GUIDE,
    
    # Business templates
    "project_update": PromptTemplates.PROJECT_UPDATE,
    "customer_feedback": PromptTemplates.CUSTOMER_FEEDBACK,
    
    # Research templates
    "research_summary": PromptTemplates.RESEARCH_SUMMARY,
    "interview_summary": PromptTemplates.INTERVIEW_SUMMARY,
    
    # Content creation templates
    "blog_post_outline": PromptTemplates.BLOG_POST_OUTLINE,
    "social_media_content": PromptTemplates.SOCIAL_MEDIA_CONTENT,
    
    # Technical templates
    "technical_documentation": PromptTemplates.TECHNICAL_DOCUMENTATION,
    "bug_report_summary": PromptTemplates.BUG_REPORT_SUMMARY,
    "filename_subject": PromptTemplates.FILENAME_SUBJECT,
}


def get_template(template_key: str) -> Optional[str]:
    """
    Get a prompt template by its key.
    
    Args:
        template_key: The key identifying the template (e.g., "basic_summary").
    
    Returns:
        The prompt template string, or None if not found.
    
    Example:
        >>> template = get_template("meeting_minutes")
        >>> print(template[:50])
        Act as a professional secretary. From this meeting...
    """
    return PROMPT_TEMPLATES.get(template_key.lower())


def list_templates() -> list:
    """
    List all available template keys.
    
    Returns:
        List of template keys.
    
    Example:
        >>> templates = list_templates()
        >>> print(templates)
        ['basic_summary', 'meeting_minutes', 'lecture_summary', ...]
    """
    return sorted(PROMPT_TEMPLATES.keys())


def format_template(template_key: str, transcript: str) -> str:
    """
    Format a template with the provided transcript.
    
    Args:
        template_key: The key identifying the template.
        transcript: The transcript text to insert into the template.
    
    Returns:
        The formatted prompt with transcript inserted.
    
    Raises:
        ValueError: If the template key is not found.
    
    Example:
        >>> prompt = format_template("basic_summary", "This is a transcript...")
        >>> print(prompt)
        Extract the core thesis, key insights, and actionable...
    """
    template = get_template(template_key)
    if template is None:
        available = ", ".join(list_templates())
        raise ValueError(
            f"Template '{template_key}' not found. "
            f"Available templates: {available}"
        )
    
    return template.format(transcript=transcript)


def add_custom_template(key: str, template: str) -> None:
    """
    Add a custom prompt template to the collection.
    
    Args:
        key: The key to identify the template.
        template: The template string (must include {transcript} placeholder).
    
    Raises:
        ValueError: If the template doesn't contain {transcript} placeholder.
    
    Example:
        >>> add_custom_template("my_template", "Summarize: {transcript}")
        >>> get_template("my_template")
        'Summarize: {transcript}'
    """
    if "{transcript}" not in template:
        raise ValueError(
            f"Template must contain '{{transcript}}' placeholder"
        )
    
    PROMPT_TEMPLATES[key.lower()] = template