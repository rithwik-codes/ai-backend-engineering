from flask import Blueprint, request, jsonify

from services.career.career_service import analyze_career
from utils.auth_helper import verify_token


career_bp = Blueprint(
    "career",
    __name__
)


def require_auth(func):

    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):

        token = request.headers.get(
            "Authorization"
        )

        if not token or not verify_token(token):

            return jsonify({
                "success": False,
                "error": "Unauthorized"
            }), 401

        return func(*args, **kwargs)

    return wrapper


@career_bp.route(
    "/career/analyze",
    methods=["POST"]
)
@require_auth
def analyze():

    # --------------------------------------------------
    # Step 1: Get uploaded resume
    # --------------------------------------------------

    resume_file = request.files.get("resume")

    if not resume_file:

        return jsonify({
            "success": False,
            "error": "Resume PDF is required"
        }), 400

    # --------------------------------------------------
    # Step 2: Validate file type
    # --------------------------------------------------

    if not resume_file.filename.lower().endswith(".pdf"):

        return jsonify({
            "success": False,
            "error": "Only PDF resumes are supported"
        }), 400

    # --------------------------------------------------
    # Step 3: Get job description
    # --------------------------------------------------

    job_description = request.form.get(
        "job_description"
    )

    if not job_description:

        return jsonify({
            "success": False,
            "error": "Job description is required"
        }), 400

    try:

        # --------------------------------------------------
        # Step 4: Extract resume text
        # --------------------------------------------------

        from utils.pdf_extractor import (
            extract_text_from_pdf
        )

        resume_text = extract_text_from_pdf(
            resume_file
        )

        # --------------------------------------------------
        # Step 5: Send extracted text to service
        # --------------------------------------------------

        analysis = analyze_career(
            resume_text,
            job_description
        )

        # --------------------------------------------------
        # Step 6: Return response
        # --------------------------------------------------

        return jsonify({
            "success": True,
            "data": analysis["data"],
            "source": analysis["source"]
        }), 200

    except ValueError as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:

        print("CAREER ERROR:", e)

        return jsonify({
            "success": False,
            "error": "Career analysis failed"
        }), 500