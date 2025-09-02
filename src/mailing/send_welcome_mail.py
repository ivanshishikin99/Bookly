from .send_mail import send_email


def send_welcome_email(username: str, email: str):
    return send_email(recipient=email,
                      subject="Welcome to Bookly!",
                      body=f"Welcome to our site, {username}!")