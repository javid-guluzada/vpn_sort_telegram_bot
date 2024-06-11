import sqlite3


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    """admins table columns: user_id"""

    def create_admins_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY
            )
        """
        )
        self.connection.commit()

    def add_admin(self, user_id: int):
        self.cursor.execute(
            """
            INSERT INTO admins (user_id) VALUES (?)
        """,
            (user_id,),
        )
        self.connection.commit()

    def remove_admin(self, user_id: int):
        self.cursor.execute(
            """
            DELETE FROM admins WHERE user_id = ?
        """,
            (user_id,),
        )
        self.connection.commit()

    def get_admins(self):
        self.cursor.execute(
            """
            SELECT user_id FROM admins
        """
        )
        return self.cursor.fetchall()

    def create_auth_chats_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS auth_chats (
                auth_chat INTEGER PRIMARY KEY,
                is_auth INTEGER NOT NULL
            )
        """
        )
        self.connection.commit()

    def add_auth_chat(self, auth_chat: int):
        self.cursor.execute(
            """
            INSERT INTO auth_chats (auth_chat, is_auth) VALUES (?, ?)
        """,
            (auth_chat, 1),
        )
        self.connection.commit()

    def remove_auth_chat(self, auth_chat: int):
        # dont remove just make is_auth 0
        self.cursor.execute(
            """
            UPDATE auth_chats SET is_auth = 0 WHERE auth_chat = ?
        """,
            (auth_chat,),
        )

    def get_auth_chats(self):
        self.cursor.execute(
            """
            SELECT auth_chat FROM auth_chats WHERE is_auth = 1
        """
        )
        return self.cursor.fetchall()
