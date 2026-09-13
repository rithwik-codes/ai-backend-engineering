import logging

from services.clients.career_ai_client import analyze_resume_with_ai
from database import (
    get_cached_career_analysis,
    save_career_analysis
)


def analyze_career(
    resume_text,
    job_description
):

    logging.info(
        "Career analysis request received"
    )

    # --------------------------------------------------
    # Step 1: Validate input
    # --------------------------------------------------

    if not resume_text:

        logging.warning(
            "Resume text is missing"
        )

        raise ValueError(
            "Resume text is required"
        )

    if not job_description:

        logging.warning(
            "Job description is missing"
        )

        raise ValueError(
            "Job description is required"
        )

    # --------------------------------------------------
    # Step 2: Create cache key
    # --------------------------------------------------

    cache_key = (
        f"{resume_text.strip()}"
        f"::{job_description.strip()}"
    )

    logging.info(
        "Checking career analysis cache"
    )

    # --------------------------------------------------
    # Step 3: Check cache
    # --------------------------------------------------

    cached_analysis = get_cached_career_analysis(
        cache_key
    )

    if cached_analysis:

        logging.info(
            "Career analysis cache hit"
        )

        return {
            "data": cached_analysis,
            "source": "cache"
        }

    # --------------------------------------------------
    # Step 4: Cache miss
    # --------------------------------------------------

    logging.info(
        "Career analysis cache miss - calling AI"
    )

    # --------------------------------------------------
    # Step 5: Call AI
    # --------------------------------------------------

    analysis = analyze_resume_with_ai(
        resume_text,
        job_description
    )

    # --------------------------------------------------
    # Step 6: Save analysis
    # --------------------------------------------------

    save_career_analysis(
        cache_key,
        resume_text,
        job_description,
        analysis
    )

    logging.info(
        "Career analysis saved successfully"
    )

    # --------------------------------------------------
    # Step 7: Return result
    # --------------------------------------------------

    return {
        "data": analysis,
        "source": "ai"
    }