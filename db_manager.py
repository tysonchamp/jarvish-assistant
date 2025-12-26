
import mysql.connector
from datetime import datetime
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class DBManager:
    def __init__(self):
        self.config = {
            "host": DB_HOST,
            "user": DB_USER,
            "password": DB_PASSWORD,
            "database": DB_NAME
        }

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return None

    def create_tables(self):
        """Creates necessary tables if they don't exist."""
        conn = self.get_connection()
        if not conn:
            # If DB doesn't exist, try connecting without DB name to create it
            try:
                temp_config = self.config.copy()
                del temp_config["database"]
                conn = mysql.connector.connect(**temp_config)
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
                conn.close()
                # Reconnect with DB name
                conn = self.get_connection()
            except Exception as e:
                print(f"Failed to create database: {e}")
                return

        if conn:
            cursor = conn.cursor()
            
            # Conversations Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Messages Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    conversation_id INT,
                    role VARCHAR(50),
                    content TEXT,
                    audio_path VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()

    def create_conversation(self, title="New Chat"):
        conn = self.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO conversations (title) VALUES (%s)", (title,))
            conn.commit()
            cid = cursor.lastrowid
            cursor.close()
            conn.close()
            return cid
        return None

    def add_message(self, conversation_id, role, content, audio_path=None):
        conn = self.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO messages (conversation_id, role, content, audio_path)
                VALUES (%s, %s, %s, %s)
            """, (conversation_id, role, content, audio_path))
            conn.commit()
            cursor.close()
            conn.close()

    def get_conversations(self):
        conn = self.get_connection()
        conversations = []
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM conversations ORDER BY created_at DESC")
            conversations = cursor.fetchall()
            cursor.close()
            conn.close()
        return conversations

    def get_messages(self, conversation_id):
        conn = self.get_connection()
        messages = []
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM messages WHERE conversation_id = %s ORDER BY created_at ASC", (conversation_id,))
            messages = cursor.fetchall()
            cursor.close()
            conn.close()
        return messages

    def delete_conversation(self, conversation_id):
        conn = self.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversations WHERE id = %s", (conversation_id,))
            conn.commit()
            cursor.close()
            conn.close()
