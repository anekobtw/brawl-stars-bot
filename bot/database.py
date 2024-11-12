import sqlite3


class DBManager:
    def __init__(self, db_name: str, table_schema: str) -> None:
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        self.cursor.execute(table_schema)
        self.connection.commit()

    def execute_query(self, query: str, params: tuple = ()) -> None:
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query: str, params: tuple = ()) -> list:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query: str, params: tuple = ()) -> list:
        self.cursor.execute(query, params)
        return self.cursor.fetchone()


class UsersManager(DBManager):
    def __init__(self) -> None:
        table_schema = """CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER,
            tag TEXT
        )"""
        super().__init__("assets/users.db", table_schema)

    def create_user(self, user_id: str, tag: str) -> None:
        if self.get_user_tag(user_id) is None:
            self.execute_query("INSERT INTO users VALUES (?, ?)", (user_id, tag))

    def delete_user(self, user_id: int) -> None:
        if self.get_user_tag(user_id) is not None:
            self.execute_query("DELETE FROM users WHERE user_id = ?", (user_id,))

    def get_user_tag(self, user_id: int) -> str | None:
        try:
            return self.fetch_one("SELECT tag FROM users WHERE user_id = ? LIMIT 1", (user_id,))[0]
        except TypeError:
            return None
