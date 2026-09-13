import os
import json
import logging

from google import genai


# --------------------------------------------------
# Gemini Configuration
# --------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Create Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY
)


# --------------------------------------------------
# Validate AI Response Structure
# --------------------------------------------------

def validate_structure(data):

    required_keys = [
        "summary",
        "key_points",
        "confidence_level"
    ]

    for key in required_keys:

        if key not in data:
            return False

    return True


# --------------------------------------------------
# Sanitize AI Response
# --------------------------------------------------

def sanitize_response(data):

    # Fix summary
    if not isinstance(
        data.get("summary"),
        str
    ):

        data["summary"] = (
            "Unable to process summary"
        )

    # Fix key_points
    if isinstance(
        data.get("key_points"),
        str
    ):

        data["key_points"] = [
            data["key_points"]
        ]

    elif not isinstance(
        data.get("key_points"),
        list
    ):

        data["key_points"] = []

    # Fix confidence_level
    if data.get("confidence_level") not in [
        "low",
        "medium",
        "high"
    ]:

        data["confidence_level"] = "low"

    return data


# --------------------------------------------------
# Call Gemini API
# --------------------------------------------------

def call_ai_api(user_message):

    prompt = f"""
You are an AI assistant.

Analyze the following user message.

Provide a useful analysis of the user's message.

If the message is unclear, explain that it could not
be understood clearly.

User message:
{user_message}
"""

    try:

        logging.info(
            "Calling Gemini API"
        )

        # --------------------------------------------------
        # Structured JSON Schema
        # --------------------------------------------------

        response_schema = {
            "type": "object",

            "properties": {

                "summary": {
                    "type": "string"
                },

                "key_points": {
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
                "summary",
                "key_points",
                "confidence_level"
            ]
        }

        # --------------------------------------------------
        # Send Structured Request To Gemini
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
        # Extract Gemini Response
        # --------------------------------------------------

        raw_response = response.text.strip()

        logging.info(
            "Gemini structured response received"
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

        if not validate_structure(
            parsed_response
        ):

            logging.error(
                "Invalid Gemini response structure"
            )

            raise ValueError(
                "Invalid AI response structure"
            )

        # --------------------------------------------------
        # Sanitize Response
        # --------------------------------------------------

        clean_response = sanitize_response(
            parsed_response
        )

        logging.info(
            "Gemini structured response "
            "processed successfully"
        )

        return clean_response


    # --------------------------------------------------
    # Invalid JSON
    # --------------------------------------------------

    except json.JSONDecodeError:

        logging.error(
            "Gemini returned invalid JSON"
        )

        raise


    # --------------------------------------------------
    # Any AI / API Error
    # --------------------------------------------------

    except Exception as e:

        logging.error(
            f"Gemini API error: {e}"
        )

        raise