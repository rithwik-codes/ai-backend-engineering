import sqlite3
import os
import logging
import json


DB_NAME = os.getenv("DB_NAME", "app.db")


# --------------------------------------------------
# Initialize Database
# --------------------------------------------------

def init_db():
    conn = None

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Chat History Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Background Jobs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                status TEXT NOT NULL,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)

        # AI Cache Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT UNIQUE NOT NULL,
                ai_response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cache_key TEXT UNIQUE NOT NULL,
        resume_text TEXT NOT NULL,
        job_description TEXT NOT NULL,
        analysis_result TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

        logging.info("Database initialized successfully")

    except sqlite3.Error as e:

        logging.error(
            f"Database initialization error: {e}"
        )

        raise

    finally:

        if conn:
            conn.close()


# --------------------------------------------------
# Save Chat History
# --------------------------------------------------

def save_chat_history(user_message, ai_response):

    conn = None

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO chat_history (
                user_message,
                ai_response
            )
            VALUES (?, ?)
            """,
            (
                user_message,
                str(ai_response)
            )
        )

        conn.commit()

        logging.info(
            "Chat history saved successfully"
        )

    except sqlite3.Error as e:

        logging.error(
            f"Chat history save error: {e}"
        )

        raise

    finally:

        if conn:
            conn.close()


# --------------------------------------------------
# Fetch Chat History with Pagination
# --------------------------------------------------

def get_chat_history(limit=10, offset=0):

    conn = None

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                user_message,
                ai_response,
                created_at
            FROM chat_history
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            """,
            (
                limit,
                offset
            )
        )

        rows = cursor.fetchall()

        history = []

        for row in rows:

            history.append({
                "id": row[0],
                "user_message": row[1],
                "ai_response": row[2],
                "created_at": row[3]
            })

        return history

    except sqlite3.Error as e:

        logging.error(
            f"Database fetch error: {e}"
        )

        raise

    finally:

        if conn:
            conn.close()


# --------------------------------------------------
# Create Background Job
# --------------------------------------------------

def create_job(user_message):

    conn = None

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO jobs (
                user_message,
                status
            )
            VALUES (?, ?)
            """,
            (
                user_message,
                "pending"
            )
        )

        job_id = cursor.lastrowid

        conn.commit()

        return job_id

    except sqlite3.Error as e:

        logging.error(
            f"Job creation error: {e}"
        )

        raise

    finally:

        if conn:
            conn.close()


# --------------------------------------------------
# Get Background Job
# --------------------------------------------------

def get_job(job_id):

    conn = None

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                user_message,
                status,
                result
            FROM jobs
            WHERE id = ?
            """,
            (job_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "user_message": row[1],
            "status": row[2],
            "result": row[3]
        }

    except sqlite3.Error as e:

        logging.error(
            f"Job fetch error: {e}"
        )

        raise

    finally:

        if conn:
            conn.close()


# --------------------------------------------------
# Get Cached AI Response
# --------------------------------------------------

def get_cached_response(user_message):

    conn = None

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT ai_response
            FROM ai_cache
            WHERE user_message = ?
            """,
            (user_message,)
        )

        row = cursor.fetchone()

        if row:
            return row[0]

        return None

    except sqlite3.Error as e:

        logging.error(
            f"Cache fetch error: {e}"
        )

        raise

    finally:

        if conn:
            conn.close()


# --------------------------------------------------
# Save AI Response To Cache
# --------------------------------------------------

def save_cache(user_message, ai_response):

    conn = None

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO ai_cache (
                user_message,
                ai_response
            )
            VALUES (?, ?)
            """,
            (
                user_message,
                str(ai_response)
            )
        )

        conn.commit()

        logging.info(
            "AI response cached successfully"
        )

    except sqlite3.Error as e:

        logging.error(
            f"Cache save error: {e}"
        )

        raise

    finally:

        if conn:
            conn.close()


# --------------------------------------------------
# Career Analysis Cache / History
# --------------------------------------------------

def get_cached_career_analysis(cache_key):
    conn = None

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT analysis_result
            FROM resume_analyses
            WHERE cache_key = ?
            """,
            (cache_key,)
        )

        row = cursor.fetchone()

        if row:
            return json.loads(row[0])

        return None

    finally:
        if conn:
            conn.close()


def save_career_analysis(
    cache_key,
    resume_text,
    job_description,
    analysis_result
):
    conn = None

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO resume_analyses (
                cache_key,
                resume_text,
                job_description,
                analysis_result
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                cache_key,
                resume_text,
                job_description,
                json.dumps(analysis_result)
            )
        )

        conn.commit()

    finally:
        if conn:
            conn.close()


