
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "data" / "assistant_memory.db"


class MemoryManager:

    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize_database()

    # --------------------------------------------------
    # DATABASE CONNECTION
    # --------------------------------------------------

    def get_connection(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize_database(self):
        with self.get_connection() as connection:

            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT,
                    preferences TEXT DEFAULT '{}',
                    created_at TEXT,
                    updated_at TEXT
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS liked_cars (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    make TEXT,
                    model TEXT,
                    year INTEGER,
                    price_aed REAL,
                    mileage_km REAL,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS conversation_state (
                    user_id TEXT PRIMARY KEY,
                    last_search_results TEXT DEFAULT '[]',
                    updated_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

    # --------------------------------------------------
    # UTILITIES
    # --------------------------------------------------

    @staticmethod
    def current_time():
        return datetime.now(timezone.utc).isoformat()

    # --------------------------------------------------
    # USER PROFILE / LONG-TERM MEMORY
    # --------------------------------------------------

    def get_profile(self, user_id):
        with self.get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM users WHERE user_id = ?",
                (user_id,)
            ).fetchone()

        if not row:
            return None

        profile = dict(row)
        profile["preferences"] = json.loads(
            profile["preferences"] or "{}"
        )

        return profile

    def update_profile(self, user_id, name=None, preferences=None):
        existing = self.get_profile(user_id)
        now = self.current_time()

        if existing:
            saved_preferences = existing["preferences"]
            saved_preferences.update(preferences or {})

            updated_name = (
                name if name is not None else existing["name"]
            )

            with self.get_connection() as connection:
                connection.execute("""
                    UPDATE users
                    SET name = ?, preferences = ?, updated_at = ?
                    WHERE user_id = ?
                """, (
                    updated_name,
                    json.dumps(saved_preferences),
                    now,
                    user_id
                ))

        else:
            with self.get_connection() as connection:
                connection.execute("""
                    INSERT INTO users
                    (user_id, name, preferences, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id,
                    name,
                    json.dumps(preferences or {}),
                    now,
                    now
                ))

        return self.get_profile(user_id)

    # --------------------------------------------------
    # LIKED CARS / USER PREFERENCES
    # --------------------------------------------------

    def add_liked_car(self, user_id, car):

        if not self.get_profile(user_id):
            self.update_profile(user_id)

        with self.get_connection() as connection:

            existing = connection.execute("""
                SELECT id
                FROM liked_cars
                WHERE user_id = ?
                  AND make = ?
                  AND model = ?
                  AND year = ?
                  AND price_aed IS ?
                LIMIT 1
            """, (
                user_id,
                car.get("make"),
                car.get("model"),
                car.get("year"),
                car.get("price_aed")
            )).fetchone()

            if existing:
                return False

            connection.execute("""
                INSERT INTO liked_cars
                (
                    user_id,
                    make,
                    model,
                    year,
                    price_aed,
                    mileage_km,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                car.get("make"),
                car.get("model"),
                car.get("year"),
                car.get("price_aed"),
                car.get("mileage_km"),
                self.current_time()
            ))

        return True

    def get_liked_cars(self, user_id):
        with self.get_connection() as connection:
            rows = connection.execute("""
                SELECT
                    make,
                    model,
                    year,
                    price_aed,
                    mileage_km,
                    created_at
                FROM liked_cars
                WHERE user_id = ?
                ORDER BY id DESC
            """, (user_id,)).fetchall()

        return [dict(row) for row in rows]

    # --------------------------------------------------
    # CONVERSATION MEMORY / SHORT-TERM HISTORY
    # --------------------------------------------------

    def save_message(self, user_id, role, content):

        if not self.get_profile(user_id):
            self.update_profile(user_id)

        with self.get_connection() as connection:
            connection.execute("""
                INSERT INTO messages
                (user_id, role, content, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                user_id,
                role,
                content,
                self.current_time()
            ))

    def get_recent_messages(self, user_id, limit=10):

        with self.get_connection() as connection:
            rows = connection.execute("""
                SELECT role, content, created_at
                FROM messages
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
            """, (
                user_id,
                limit
            )).fetchall()

        return [
            dict(row)
            for row in reversed(rows)
        ]

    # --------------------------------------------------
    # LAST SEARCH RESULTS / CONTEXT
    # --------------------------------------------------

    def save_search_results(self, user_id, cars):

        if not self.get_profile(user_id):
            self.update_profile(user_id)

        with self.get_connection() as connection:
            connection.execute("""
                INSERT INTO conversation_state
                (user_id, last_search_results, updated_at)
                VALUES (?, ?, ?)

                ON CONFLICT(user_id) DO UPDATE SET
                    last_search_results = excluded.last_search_results,
                    updated_at = excluded.updated_at
            """, (
                user_id,
                json.dumps(cars),
                self.current_time()
            ))

    def get_last_search_results(self, user_id):

        with self.get_connection() as connection:
            row = connection.execute("""
                SELECT last_search_results
                FROM conversation_state
                WHERE user_id = ?
            """, (user_id,)).fetchone()

        if not row:
            return []

        return json.loads(
            row["last_search_results"] or "[]"
        )
