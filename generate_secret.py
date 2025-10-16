#!/usr/bin/env python3
"""
Generate a secure secret key for Flask sessions
Run this script to generate a new secret key for production
"""

import secrets

def generate_secret_key():
    """Generate a secure random secret key"""
    return secrets.token_hex(32)

if __name__ == "__main__":
    secret = generate_secret_key()
    print("Generated Secret Key:")
    print(secret)
    print("\nAdd this to your Railway environment variables as 'SECRET_KEY'")
    print("You can also set it in your local environment:")
    print(f"export SECRET_KEY='{secret}'")
