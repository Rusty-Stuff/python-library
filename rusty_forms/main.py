import requests
import json
from nostr.key import PrivateKey, PublicKey
from nostr.event import Event
from .helper import make_form, make_message, make_form_recipient, make_default_headers
from .config import RustyAPIConfig


class RustyAPI:
    base_url = "https://api.rusty-forms.com/v1"
    private_key = PrivateKey
    public_key = PublicKey
    timeout = 5

    is_logged_in = False
    access_token = None

    def __init__(self, cfg: RustyAPIConfig):
        self.base_url = cfg.base_url
        self.private_key = cfg.private_key
        self.public_key = cfg.public_key
        self.timeout = cfg.timeout

    def login_request(self):
        """Send login request; Expect 200"""
        res = requests.post(
            self.base_url + "/login",
            headers=make_default_headers(),
            data=json.dumps({"public_key": self.public_key.hex()}),
            timeout=5,
        )

        res.raise_for_status()
        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return res.json()

    def solve_login_challenge(
        self,
        login_response,
    ):
        """Solve login challenge; Expect 200
        - provides access_token
        """
        challenge = login_response["challenge"]

        challenge_event = Event(
            public_key=self.public_key.hex(),
            content="",
            kind=22242,
            tags=[["relay", self.base_url], ["challenge", challenge]],
        )

        self.private_key.sign_event(challenge_event)

        response_data = {
            "NOSTR": {
                "id": login_response["id"],
                "response": {
                    "id": challenge_event.id,
                    "pubkey": challenge_event.public_key,
                    "created_at": challenge_event.created_at,
                    "kind": challenge_event.kind,
                    "tags": challenge_event.tags,
                    "content": challenge_event.content,
                    "sig": challenge_event.signature,
                },
            }
        }

        response_json = json.dumps(response_data)

        res = requests.post(
            self.base_url + "/login/challenge",
            headers={"Content-Type": "application/json"},
            data=response_json,
            timeout=5,
        )

        res.raise_for_status()
        if res.status_code != 200:
            raise Exception("Unexpected status code")

        data = res.json()
        if "access_token" not in data:
            raise Exception("Missing access token")
        else:
            self.access_token = data["access_token"]
            self.is_logged_in = True

        return data

    def login(self):
        """Login; Expect 200"""
        login_response = self.login_request()
        return self.solve_login_challenge(login_response)

    def logout(self):
        """Send logout request; Expect 200"""
        res = requests.post(
            self.base_url + "/a/logout",
            headers=make_default_headers(self.access_token),
            timeout=5,
        )

        res.raise_for_status()
        if res.status_code != 200:
            raise Exception("Unexpected status code")

        self.access_token = None
        self.is_logged_in = False

        return res.json()

    def create_form(self, new_form: dict = make_form()):
        """Create a new form; Expect 201
        - title
        """

        res = requests.post(
            self.base_url + "/a/forms",
            headers=make_default_headers(self.access_token),
            data=json.dumps(new_form),
            timeout=5,
        )

        res.raise_for_status()
        if res.status_code != 201:
            raise Exception("Unexpected status code")

        return res.json()

    def get_forms(self):
        """Get all forms; Expect 200"""
        res = requests.get(
            self.base_url + "/a/forms",
            headers=make_default_headers(self.access_token),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return res.json()

    def update_form(
        self,
        form_id: str,
        data: dict,
    ):
        """Update a form; Expect 200
        - title
        - filter_spam
        - check_specs
        - specs
        - redirect_url
        """
        res = requests.patch(
            self.base_url + f"/a/forms/{form_id}",
            headers=make_default_headers(self.access_token),
            data=json.dumps(data),
            timeout=self.timeout,
        )

        if res.status_code == 400:
            print(res.text)

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return None

    def delete_form(self, form_id: str):
        """Delete a form; Expect 200"""
        res = requests.delete(
            self.base_url + f"/a/forms/{form_id}",
            headers=make_default_headers(self.access_token),
            timeout=self.timeout,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return None

    def new_message(self, form_id: str, new_message: dict = make_message()):
        """Create a new message json; Expect 201
        - title
        - body
        - email
        """
        res = requests.post(
            self.base_url + f"/digest/{form_id}",
            headers=make_default_headers(),
            data=json.dumps(new_message),
            timeout=self.timeout,
        )

        res.raise_for_status()

        if res.status_code != 201:
            raise Exception("Unexpected status code")

        return None

    def new_message_form(self, form_id: str, new_message: dict = make_message()):
        """Create a new message urlencoded; Expect 201"""
        res = requests.post(
            self.base_url + f"/digest/{form_id}",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data=new_message,
            timeout=self.timeout,
        )

        res.raise_for_status()

        if res.status_code != 201:
            raise Exception("Unexpected status code")

        return None

    def new_message_multipart(self, form_id: str, new_message: dict = make_message()):
        """Create a new message multipart; Expect 201"""

        res = requests.post(
            self.base_url + f"/digest/{form_id}",
            headers={
                "Content-Type": "multipart/form-data",
            },
            data=new_message,
            timeout=self.timeout,
        )

        res.raise_for_status()

        if res.status_code != 201:
            raise Exception("Unexpected status code")

        return None

    def get_messages(self):
        """Get all messages; Expect 200"""
        res = requests.get(
            self.base_url + "/a/messages",
            headers=make_default_headers(self.access_token),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return res.json()

    def get_messages_by_form(self, form_id: str):
        """Get all messages by form; Expect 200"""
        res = requests.get(
            self.base_url + f"/a/messages?form_id={form_id}",
            headers=make_default_headers(self.access_token),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return res.json()

    def delete_message(self, message_id: str):
        """Delete a message; Expect 200"""
        res = requests.delete(
            self.base_url + f"/a/messages/{message_id}",
            headers=make_default_headers(self.access_token),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return None

    def verify_email(self, email: str):
        """Verify an email; Expect 200"""
        res = requests.post(
            self.base_url + f"/a/emails/verify",
            headers=make_default_headers(self.access_token),
            data=json.dumps({"email": email}),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return res.json()

    def verify_email_confirm(self, verify_email_token: str):
        """Confirm an email; Expect 200"""
        res = requests.get(
            self.base_url + f"/emails/verify/{verify_email_token}",
            headers=make_default_headers(),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return res.text

    def get_emails(self):
        """Get all emails; Expect 200"""
        res = requests.get(
            self.base_url + "/a/emails",
            headers=make_default_headers(self.access_token),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return res.json()

    def delete_email(self, email_id: str):
        """Delete an email; Expect 200"""
        res = requests.delete(
            self.base_url + f"/a/emails/{email_id}",
            headers=make_default_headers(self.access_token),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return res.json()

    def create_form_recipient(self, form_id: str, email_id: str):
        """Create a new form recipient; Expect 201"""
        form_recipient = make_form_recipient(form_id, email_id)

        res = requests.post(
            self.base_url + f"/a/forms/recipients",
            headers=make_default_headers(self.access_token),
            data=json.dumps(form_recipient),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 201:
            raise Exception("Unexpected status code")

        return res.json()

    def get_form_recipients(
        self,
        form_id: str,
    ):
        """Get all form recipients; Expect 200"""
        res = requests.get(
            self.base_url + f"/a/forms/{form_id}/recipients",
            headers=make_default_headers(self.access_token),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return res.json()

    def delete_form_recipient(self, form_id: str, recipient_id: str):
        """Delete a form recipient; Expect 200"""
        res = requests.delete(
            self.base_url + f"/a/forms/{form_id}/recipients/{recipient_id}",
            headers=make_default_headers(self.access_token),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return None

    def account_balance(self):
        """Get account balance; Expect 200"""
        res = requests.get(
            self.base_url + "/a/balance",
            headers=make_default_headers(self.access_token),
            timeout=5,
        )

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception("Unexpected status code")

        return res.json()
