from typing import Union
from nostr.key import PrivateKey, PublicKey
from nostr.event import Event

from platformdirs import user_data_dir

from .helper import save_file, load_file

appname = "rusty-forms"
appauthor = "FG"

user_config_dir = user_data_dir(appname, appauthor)


class NostrAuthApiConfig:
    config_dir: str
    private_key_path: str
    private_key: Union[None, PrivateKey] = None
    public_key: Union[None, PublicKey] = None

    def __init__(
        self,
        config_dir: str = user_config_dir,
        private_key: Union[None, PrivateKey] = None,
    ):
        self.config_dir = config_dir
        self.private_key_path = config_dir + "/private_key.pem"
        self.private_key = private_key
        self.public_key = private_key.public_key if private_key is not None else None

    def make_login_request(self):
        return {
            "NOSTR": {
                "public_key": self.public_key.hex(),
            }
        }

    def make_login_challenge_response(self, base_url: str, login_response):
        challenge = login_response["challenge"]

        challenge_event = Event(
            public_key=self.public_key.hex(),
            content="",
            kind=22242,
            tags=[["relay", base_url], ["challenge", challenge]],
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

        return response_data

    def generate_keys(self):
        print("Generating new keys. Don't forget to save them!")
        self.private_key = PrivateKey()
        self.public_key = self.private_key.public_key

    def save(self):
        if self.private_key is not None:
            print("Saving private key to", self.private_key_path)
            save_file(self.private_key_path, self.private_key.hex())

    def load(self):
        if self.private_key_path.exists():
            self.private_key = PrivateKey(load_file(self.private_key_path))
            self.public_key = self.private_key.public_key
        else:
            print("No private key found in", self.private_key_path)


class EmailAuthApiConfig:
    email: str

    def make_login_request(self):
        return {
            "EMAIL": {
                "email": self.email,
            }
        }

    def make_login_challenge_response(self, base_url: str, login_response):
        """
        This login response here actually comes from the user's email.
        Two approaches:
        - Keep browser window open (with id, email) and only prompt for challenge
        - Embed all details in email link
        """

        return {
            "EMAIL": {
                "id": login_response["id"],
                "response": {
                    "email": self.email,
                    "challenge": login_response["challenge"],
                },
            }
        }
