# Rusty Forms Python Library

This is a super-early release of our python library. Initially we were using these to write tests, but I decided to release it stand-alone so everyone can benefit. If you have a look under the hood, you'll probably find it's very verbose (for ex. checking for specific response codes) - I'll clean this up in the next iterations.

## Installation

This works everywhere, python works:

```bash
pip install https://github.com/Rusty-Stuff/python-library
```

## Usage

Login:

```python
from rusty-forms import RustyAPI

api = make_api()
req = api.login_request()
api.solve_login_challenge(req)
```

Create a new form:

```python
new_form = api.create_form({
    "title": "My Form",
})
```

Get form messages:

```python
messages = api.get_form_messages(new_form["id"])
```