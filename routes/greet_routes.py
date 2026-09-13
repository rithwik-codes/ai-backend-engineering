from functools import wraps

from flask import Blueprint, request, jsonify

from services.greet_services import process_greet
from services.math_service import add_numbers
from services.ai_service import generate_ai_response

from utils.auth_helper import verify_token

from database import (
    create_job,
    get_chat_history,
    get_job
)


# --------------------------------------------------
# Blueprint
# --------------------------------------------------

greet_bp = Blueprint(
    "greet",
    __name__
)


# --------------------------------------------------
# Authentication Decorator
# --------------------------------------------------

def require_auth(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        token = request.headers.get(
            "Authorization"
        )

        if not token or not verify_token(token):

            return jsonify({
                "success": False,
                "error": "Unauthorised"
            }), 401

        return func(*args, **kwargs)

    return wrapper


# --------------------------------------------------
# Greet Route
# --------------------------------------------------

@greet_bp.route(
    "/greet",
    methods=["POST"]
)
@require_auth
def greet():

    data = request.get_json()

    response, status = process_greet(data)

    return jsonify(response), status


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@greet_bp.route(
    "/status",
    methods=["GET"]
)
@require_auth
def status():

    return jsonify({
        "status": "server is healthy"
    }), 200


# --------------------------------------------------
# Math Route
# --------------------------------------------------

@greet_bp.route(
    "/add",
    methods=["POST"]
)
@require_auth
def add():

    data = request.get_json()

    response, status = add_numbers(data)

    return jsonify(response), status


# --------------------------------------------------
# AI Chat Route
# --------------------------------------------------

@greet_bp.route(
    "/ai/chat",
    methods=["POST"]
)
@require_auth
def ai_chat():

    data = request.get_json()

    if not data or "message" not in data:

        return jsonify({
            "success": False,
            "error": "Message is required"
        }), 400

    user_message = data["message"]

    response, status = generate_ai_response(
        user_message
    )

    return jsonify(response), status


# --------------------------------------------------
# Chat History Route
# --------------------------------------------------

@greet_bp.route(
    "/chat-history",
    methods=["GET"]
)
@require_auth
def chat_history():

    try:

        page = int(
            request.args.get("page", 1)
        )

        limit = int(
            request.args.get("limit", 10)
        )

        if page < 1 or limit < 1:

            return jsonify({
                "success": False,
                "error":
                "Page and limit must be positive integers"
            }), 400

    except ValueError:

        return jsonify({
            "success": False,
            "error":
            "Page and limit must be integers"
        }), 400


    try:

        offset = (
            page - 1
        ) * limit

        history = get_chat_history(
            limit,
            offset
        )

        return jsonify({
            "success": True,
            "data": history
        }), 200

    except Exception:

        return jsonify({
            "success": False,
            "error":
            "Failed to fetch chat history"
        }), 500


# --------------------------------------------------
# Create Background AI Job
# --------------------------------------------------

@greet_bp.route(
    "/ai/analyze",
    methods=["POST"]
)
@require_auth
def analyze():

    data = request.get_json()

    if not data or "message" not in data:

        return jsonify({
            "success": False,
            "error": "Message required"
        }), 400

    job_id = create_job(
        data["message"]
    )

    return jsonify({
        "success": True,
        "job_id": job_id,
        "status": "pending"
    }), 202


# --------------------------------------------------
# Check Background Job
# --------------------------------------------------

@greet_bp.route(
    "/jobs/<int:job_id>",
    methods=["GET"]
)
@require_auth
def check_job(job_id):

    job = get_job(job_id)

    if not job:

        return jsonify({
            "success": False,
            "error": "Job not found"
        }), 404

    return jsonify({
        "success": True,
        "data": job
    }), 200