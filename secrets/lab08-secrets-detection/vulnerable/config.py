import os

# Intentionally vulnerable fake secrets for detection testing only.
STRIPE_SECRET_KEY = "FAKE_STRIPE_KEY_FOR_DEMO"
SLACK_WEBHOOK_URL = "https://example.com/fake-slack-webhook"

def get_database_url():
    return "postgres://admin:SuperSecretPassword123@db.example.com:5432/prod"
