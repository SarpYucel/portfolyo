import pyodbc
import datetime
from typing import Optional, List, Dict, Any, Tuple
import hashlib


class DatabaseError(Exception):
    """Veritabanı ile ilgili sorunlar için özel istisna sınıfı."""


class Database:
    """Beslenme uygulaması için veritabanı etkileşimlerini yönetir."""

    def __init__(
        self,
        driver: str = "{ODBC Driver 17 for SQL Server}",
        server: str = "localhost",
        database: str = "NutritionApp",
        username: Optional[str] = None,
        password: Optional[str] = None,
        trusted_connection: bool = True,
    ) -> None:
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.trusted_connection = trusted_connection
        self._conn: Optional[pyodbc.Connection] = None


    def connect(self) -> None:
        if self._conn is not None:
            return

        try:
            if self.trusted_connection:
                conn_str = (
                    f"DRIVER={self.driver};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    "Trusted_Connection=yes;"
                )
            else:
                if not self.username or not self.password:
                    raise DatabaseError("SQL kimlik doğrulaması için kullanıcı adı ve şifre sağlanmalıdır.")
                conn_str = (
                    f"DRIVER={self.driver};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"UID={self.username};PWD={self.password};"
                )
            self._conn = pyodbc.connect(conn_str)
        except pyodbc.Error as e:
            raise DatabaseError(f"Veritabanına bağlanılamadı: {e}") from e

    @property
    def conn(self) -> pyodbc.Connection:
        if self._conn is None:
            self.connect()
        assert self._conn is not None
        return self._conn


    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()


    def register_user(
        self,
        username: str,
        password: str,
        age: int,
        height_cm: float,
        weight_kg: float,
        gender: str,
        goal: str,
        activity_level: str,
    ) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID FROM Users WHERE Username = ?", (username,))
            if cursor.fetchone():
                return False

            cursor.execute(
                """
                INSERT INTO Users (Username, PasswordHash, Age, Height_cm, Weight_kg, Gender, Goal, ActivityLevel)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    username,
                    self._hash_password(password),
                    age,
                    height_cm,
                    weight_kg,
                    gender,
                    goal,
                    activity_level,
                ),
            )
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            raise DatabaseError(f"Kullanıcı kaydedilemedi: {e}") from e

    def authenticate_user(self, username: str, password: str) -> Optional[int]:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID, PasswordHash FROM Users WHERE Username = ?", (username,))
            row = cursor.fetchone()
            if not row:
                return None
            user_id, stored_hash = row
            if stored_hash == self._hash_password(password):
                return int(user_id)
            return None
        except pyodbc.Error as e:
            raise DatabaseError(f"Kullanıcı doğrulanamadı: {e}") from e

    def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT ID, Username, Age, Height_cm, Weight_kg, Gender, Goal, ActivityLevel
                FROM Users
                WHERE ID = ?
                """,
                (user_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "ID": row[0],
                "Username": row[1],
                "Age": row[2],
                "Height_cm": row[3],
                "Weight_kg": row[4],
                "Gender": row[5],
                "Goal": row[6],
                "ActivityLevel": row[7],
            }
        except pyodbc.Error as e:
            raise DatabaseError(f"Kullanıcı profili alınamadı: {e}") from e


    def get_meals_by_category(self, category: str) -> List[Dict[str, Any]]:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT ID, MealName, Protein_per_100g, Carbs_per_100g, Calories_per_100g, Category
                FROM Meals
                WHERE Category = ?
                """,
                (category,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "ID": r[0],
                    "MealName": r[1],
                    "Protein_per_100g": r[2],
                    "Carbs_per_100g": r[3],
                    "Calories_per_100g": r[4],
                    "Category": r[5],
                }
                for r in rows
            ]
        except pyodbc.Error as e:
            raise DatabaseError(f"Öğünler alınamadı: {e}") from e

    def log_meal(self, user_id: int, meal_id: int, grams: float) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO UserLogs (UserID, MealID, LogDate, ConsumedGram)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, meal_id, datetime.date.today(), grams),
            )
            self.conn.commit()
        except pyodbc.Error as e:
            self.conn.rollback()
            raise DatabaseError(f"Öğün kaydedilemedi: {e}") from e

    def get_daily_totals(self, user_id: int) -> Tuple[float, float, float]:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT
                    SUM(M.Calories_per_100g * UL.ConsumedGram / 100.0) AS TotalCalories,
                    SUM(M.Protein_per_100g * UL.ConsumedGram / 100.0) AS TotalProtein,
                    SUM(M.Carbs_per_100g * UL.ConsumedGram / 100.0) AS TotalCarbs
                FROM UserLogs UL
                JOIN Meals M ON UL.MealID = M.ID
                WHERE UL.UserID = ? AND UL.LogDate = ?
                """,
                (user_id, datetime.date.today()),
            )
            row = cursor.fetchone()
            if not row or row[0] is None:
                return 0.0, 0.0, 0.0
            return float(row[0] or 0.0), float(row[1] or 0.0), float(row[2] or 0.0)
        except pyodbc.Error as e:
            raise DatabaseError(f"Günlük toplamlar alınamadı: {e}") from e

    def get_today_meals(self, user_id: int) -> List[Dict[str, Any]]:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT 
                    UL.ID,
                    M.MealName,
                    UL.ConsumedGram,
                    M.Calories_per_100g * UL.ConsumedGram / 100.0 AS Calories,
                    M.Protein_per_100g * UL.ConsumedGram / 100.0 AS Protein,
                    M.Carbs_per_100g * UL.ConsumedGram / 100.0 AS Carbs
                FROM UserLogs UL
                JOIN Meals M ON UL.MealID = M.ID
                WHERE UL.UserID = ? AND UL.LogDate = ?
                ORDER BY UL.ID DESC
                """,
                (user_id, datetime.date.today()),
            )
            rows = cursor.fetchall()
            return [
                {
                    "ID": r[0],
                    "MealName": r[1],
                    "Grams": r[2],
                    "Calories": r[3],
                    "Protein": r[4],
                    "Carbs": r[5],
                }
                for r in rows
            ]
        except pyodbc.Error as e:
            raise DatabaseError(f"Bugünkü öğünler alınamadı: {e}") from e

    def delete_meal_log(self, log_id: int) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM UserLogs WHERE ID = ?", (log_id,))
            self.conn.commit()
        except pyodbc.Error as e:
            self.conn.rollback()
            raise DatabaseError(f"Öğün kaydı silinemedi: {e}") from e

    def clear_today_logs(self, user_id: int) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                DELETE FROM UserLogs
                WHERE UserID = ? AND LogDate = ?
                """,
                (user_id, datetime.date.today()),
            )
            self.conn.commit()
        except pyodbc.Error as e:
            self.conn.rollback()
            raise DatabaseError(f"Bugünkü kayıtlar silinemedi: {e}") from e


    def get_today_water(self, user_id: int) -> float:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT WaterAmount_ml
                FROM WaterLogs
                WHERE UserID = ? AND LogDate = ?
                """,
                (user_id, datetime.date.today()),
            )
            row = cursor.fetchone()
            return float(row[0]) if row and row[0] is not None else 0.0
        except pyodbc.Error as e:
            raise DatabaseError(f"Su miktarı alınamadı: {e}") from e

    def add_water(self, user_id: int, amount_ml: float) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT WaterAmount_ml FROM WaterLogs
                WHERE UserID = ? AND LogDate = ?
                """,
                (user_id, datetime.date.today()),
            )
            row = cursor.fetchone()
            
            if row:
                new_amount = float(row[0]) + amount_ml
                cursor.execute(
                    """
                    UPDATE WaterLogs
                    SET WaterAmount_ml = ?
                    WHERE UserID = ? AND LogDate = ?
                    """,
                    (new_amount, user_id, datetime.date.today()),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO WaterLogs (UserID, LogDate, WaterAmount_ml)
                    VALUES (?, ?, ?)
                    """,
                    (user_id, datetime.date.today(), amount_ml),
                )
            self.conn.commit()
        except pyodbc.Error as e:
            self.conn.rollback()
            raise DatabaseError(f"Su miktarı güncellenemedi: {e}") from e

    def subtract_water(self, user_id: int, amount_ml: float) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT WaterAmount_ml FROM WaterLogs
                WHERE UserID = ? AND LogDate = ?
                """,
                (user_id, datetime.date.today()),
            )
            row = cursor.fetchone()
            
            if row and row[0] is not None:
                current_amount = float(row[0])
                new_amount = max(0.0, current_amount - amount_ml)
                cursor.execute(
                    """
                    UPDATE WaterLogs
                    SET WaterAmount_ml = ?
                    WHERE UserID = ? AND LogDate = ?
                    """,
                    (new_amount, user_id, datetime.date.today()),
                )
                self.conn.commit()
        except pyodbc.Error as e:
            self.conn.rollback()
            raise DatabaseError(f"Su miktarı güncellenemedi: {e}") from e


