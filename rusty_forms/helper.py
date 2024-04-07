from typing import Union


def make_form():
    return {
        "title": "Test Form",
    }


def make_message():
    return {
        "title": "Test Message",
        "body": "This is a test message",
        "email": "mike@gmail.com",
    }


def make_form_recipient(form_id: str, email_id: str):
    return {
        "form_id": form_id,
        "verified_email_id": email_id,
    }


def make_default_headers(access_token: Union[None, str] = None):
    headers = {
        "Content-Type": "application/json",
    }

    if access_token is not None:
        headers["Authorization"] = f"Bearer {access_token}"

    return headers


def save_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
