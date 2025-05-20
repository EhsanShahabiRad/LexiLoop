from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User

# ensure all models are loaded
from app.db import base  # noqa: F401


def test_connection():
    try:
        db: Session = SessionLocal()
        # simple query to check if User table is accessible
        users = db.query(User).all()
        print(f"✅ Connected! Found {len(users)} users in DB.")
    except Exception as e:
        print("❌ Failed to connect to database:")
        print(e)
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
