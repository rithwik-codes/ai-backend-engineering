import os
import json
import logging

from google import genai


# --------------------------------------------------
# Gemini Configuration
# --------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(
    api_key=GEMINI_API_KEY
)


# --------------------------------------------------
# Validate Career Analysis Structure
# --------------------------------------------------

def validate_career_analysis(data):

    required_keys = [
        "resume_score",
        "job_match_score",
        "summary",
        "strengths",
        "weaknesses",
        "matching_skills",
        "missing_skills",
        "recommendations",
        "confidence_level"
    ]

    for key in required_keys:

        if key not in data:
            return False

    return True


# --------------------------------------------------
# Call Gemini
# --------------------------------------------------

def analyze_resume_with_ai(
    resume_text,
    job_description
):

    prompt = f"""
You are an AI Career Intelligence Assistant.

Analyze the candidate's resume against the
provided job description.

Your analysis must be useful, specific,
and based only on information available
in the resume and job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    try:

        logging.info(
            "Calling Gemini for career analysis"
        )

        # --------------------------------------------------
        # Structured Output Schema
        # --------------------------------------------------

        response_schema = {

            "type": "object",

            "properties": {

                "resume_score": {
                    "type": "integer"
                },

                "job_match_score": {
                    "type": "integer"
                },

                "summary": {
                    "type": "string"
                },

                "strengths": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },

                "weaknesses": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },

                "matching_skills": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },

                "missing_skills": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },

                "recommendations": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },

                "confidence_level": {
                    "type": "string",
                    "enum": [
                        "low",
                        "medium",
                        "high"
                    ]
                }
            },

            "required": [
                "resume_score",
                "job_match_score",
                "summary",
                "strengths",
                "weaknesses",
                "matching_skills",
                "missing_skills",
                "recommendations",
                "confidence_level"
            ]
        }

        # --------------------------------------------------
        # Gemini Request
        # --------------------------------------------------

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt,

            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema
            }
        )

        # --------------------------------------------------
        # Extract Response
        # --------------------------------------------------

        raw_response = response.text.strip()

        logging.info(
            "Career AI response received"
        )

        # --------------------------------------------------
        # Convert JSON → Python Dictionary
        # --------------------------------------------------

        parsed_response = json.loads(
            raw_response
        )

        # --------------------------------------------------
        # Validate Structure
        # --------------------------------------------------

        if not validate_career_analysis(
            parsed_response
        ):

            logging.error(
                "Invalid career analysis structure"
            )

            raise ValueError(
                "Invalid career analysis structure"
            )

        logging.info(
            "Career AI response validated successfully"
        )

        return parsed_response

    except json.JSONDecodeError:

        logging.error(
            "Career AI returned invalid JSON"
        )

        raise

    except Exception as e:

        logging.error(
            f"Career AI processing failed: {e}"
        )

        raise