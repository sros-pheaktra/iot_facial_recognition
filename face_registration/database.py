import sqlite3
import numpy as np
from pathlib import Path


class Database:

    def __init__(self):
        # Create database folder if it doesn't exist
        Path("database").mkdir(exist_ok=True)

        self.conn = sqlite3.connect("database/users.db")
        self.cursor = self.conn.cursor()

        self.create_table()


    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT NOT NULL UNIQUE,
            major TEXT NOT NULL,
            role TEXT NOT NULL,
            image_path TEXT,
            embedding BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()


    def insert_user(
        self,
        name,
        student_id,
        major,
        role,
        image_path,
        embedding
    ):

        try:

            self.cursor.execute("""
            INSERT INTO users
            (
                name,
                student_id,
                major,
                role,
                image_path,
                embedding
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                student_id,
                major,
                role,
                image_path,
                embedding
            ))

            self.conn.commit()

            return True


        except sqlite3.IntegrityError:

            return False


    def get_all_users(self):

        self.cursor.execute(
            "SELECT * FROM users"
        )

        return self.cursor.fetchall()


    def embedding_to_bytes(self, embedding):
        """
        Convert NumPy face embedding to SQLite BLOB
        """

        return embedding.astype(
            np.float32
        ).tobytes()


    def bytes_to_embedding(self, data):
        """
        Convert SQLite BLOB back to NumPy array
        """

        return np.frombuffer(
            data,
            dtype=np.float32
        )


    def close(self):

        self.conn.close()