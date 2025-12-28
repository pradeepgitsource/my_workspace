from app.core.auth import get_password_hash
from app.core.user_models import User

# Default test user credentials
DEFAULT_USER = {
    "username": "admin",
    "email": "admin@example.com", 
    "password": "admin123"
}

def create_test_user():
    """Create a default test user"""
    hashed_password = get_password_hash(DEFAULT_USER["password"])
    user = User(
        id=1,
        username=DEFAULT_USER["username"],
        email=DEFAULT_USER["email"],
        hashed_password=hashed_password
    )
    print(f"Test user created:")
    print(f"Username: {DEFAULT_USER['username']}")
    print(f"Password: {DEFAULT_USER['password']}")
    return user

if __name__ == "__main__":
    create_test_user()