# Rusty Forms Python Library

This is a super-early release of our python library. Initially we were using these to write tests, but I decided to release it stand-alone so everyone can benefit. If you have a look under the hood, you'll probably find it's very verbose (for ex. checking for specific response codes) - I'll clean this up in the next iterations.

## Installation

This works everywhere, python works:

```bash
pip install https://github.com/Rusty-Stuff/python-library
```

## Usage

#### Login (& Signup)

```python
from rusty-forms import RustyAPI, NostrAuthApiConfig

auth = NostrAuthApiConfig()
auth.generate_keys()
auth.save()

api = RustyAPI(auth)
api.login()
```

#### Create a new form

```python
new_form = api.create_form({
    "title": "My Form",
})
```

#### Get form messages

```python
messages = api.get_form_messages(new_form["id"])
```

#### Update form

```python
title = "My Form with Specs"
specs = r"""
    [first_name]
    name = "first_name"
    field = "text"
    required = true

    [last_name]
    name = "last_name"
    field = "text"
    required = true

    [message]
    name = "message"
    field = "textarea"
    required = true
    check_spam = true

    [settings]
    discard_additional_fields = true
"""
check_specs = True
filter_spam = True
redirect_url = "https://rusty-stuff.com"

api.update_form(new_form["id"], {
    "title": title,
    "specs": specs,
    "check_specs": check_specs,
    "filter_spam": filter_spam,
    "redirect_url": redirect_url,
})
```

The forms URL looks like this:

```python
f"https://api.rusty-forms.com/v1/digest/{new_form["id"]}"
```

It accepts:

- JSON
- URL Encoded
- Multipart

#### Check Balance

```python
balance = api.account_balance()
```

## API

- `login()`: Login
- `logout()`: Logout
- `create_form(new_form)`: Create a new form
- `get_forms()`: Get all forms
- `update_form(form_id, data)`: Update a form
- `delete_form(form_id)`: Delete a form
- `new_message(form_id, new_message)`: Create a new message json
- `new_message_form(form_id, new_message)`: Create a new message urlencoded
- `new_message_multipart(form_id, new_message)`: Create a new message multipart
- `get_messages()`: Get all messages
- `get_messages_by_form(form_id)`: Get all messages by form
- `delete_message(message_id)`: Delete a message
- `verify_email(email)`: Verify an email
- `verify_email_confirm(verify_email_token)`: Confirm an email
- `get_emails()`: Get all emails
- `delete_email(email_id)`: Delete an email
- `create_form_recipient(form_id, email_id)`: Create a new form recipient
- `get_form_recipients(form_id)`: Get all form recipients
- `delete_form_recipient(form_id, recipient_id)`: Delete a form recipient
- `account_balance()`: Get account balance

## Caution

This library will save your private key in a file. Feel free to supplement a more secure storage option such as your keychain, and pass the key to the library:

```python
from nostr.key import PrivateKey
from rusty_forms import NostrAuthApiConfig

# your own method to get the key
private_key = PrivateKey(key)
auth = NostrAuthApiConfig(private_key=private_key)
```