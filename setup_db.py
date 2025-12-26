
from db_manager import DBManager
import time

def setup():
    print("⏳ Initializing Database...")
    try:
        db = DBManager()
        db.create_tables()
        print("✅ Database 'jarvish_db' and tables created successfully!")
    except Exception as e:
        print(f"❌ Error setting up database: {e}")

if __name__ == "__main__":
    setup()
