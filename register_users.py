import requests
import json

API_URL = "http://localhost:8000"

def register_user(username, email, password):
    """Register a new user"""
    data = {
        "username": username,
        "email": email,
        "password": password
    }
    
    response = requests.post(f"{API_URL}/auth/register", json=data)
    
    if response.status_code == 200:
        print(f"✅ User '{username}' registered successfully!")
        return response.json()
    else:
        print(f"❌ Registration failed: {response.text}")
        return None

if __name__ == "__main__":
    # Register test user
    register_user("admin", "admin@example.com", "admin123")
    register_user("testuser", "test@example.com", "password123")