import logging

from services.clients.ai_client import call_ai_api

from database import (
    get_cached_response,
    save_cache,
    save_chat_history
)


def generate_ai_response(user_message):

    logging.info("AI request received")

    # ------------------------------------------
    # Step 0: Validate Input
    # ------------------------------------------

    if not user_message:

        logging.warning(
            "Empty message received"
        )

        return {
            "success": False,
            "error": "Message is required"
        }, 400

    try:

        # ------------------------------------------
        # Step 1: Check Cache
        # ------------------------------------------

        cached_response = get_cached_response(
            user_message
        )

        if cached_response:

            logging.info(
                "Cache hit - AI call skipped"
            )

            return {
                "success": True,
                "data": cached_response,
                "source": "cache"
            }, 200

        # ------------------------------------------
        # Step 2: Cache Miss
        # ------------------------------------------

        logging.info(
            "Cache miss - calling AI"
        )

        # ------------------------------------------
        # Step 3: Call AI Client
        # ------------------------------------------

        ai_response = call_ai_api(
            user_message
        )

        # IMPORTANT:
        # If call_ai_api() raises an exception,
        # execution jumps directly to except.
        #
        # Therefore the following database/cache
        # operations WILL NOT execute.

        # ------------------------------------------
        # Step 4: Save Successful Response
        # ------------------------------------------

        save_chat_history(
            user_message,
            ai_response
        )

        # ------------------------------------------
        # Step 5: Cache Successful Response
        # ------------------------------------------

        save_cache(
            user_message,
            ai_response
        )

        logging.info(
            "AI processing completed successfully"
        )

        # ------------------------------------------
        # Step 6: Return Successful Response
        # ------------------------------------------

        return {
            "success": True,
            "data": ai_response,
            "source": "ai"
        }, 200

    except Exception as e:

        logging.error(
            f"AI processing failed: {e}"
        )

        return {
            "success": False,
            "error": "AI processing failed"
        }, 500