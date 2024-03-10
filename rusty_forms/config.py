from typing import Union
from platformdirs import user_data_dir
from nostr.key import PrivateKey, PublicKey

appname = "rusty-forms"
appauthor = "FG"
user_config_dir = user_data_dir(appname, appauthor)


def save_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class RustyAPIConfig:
    config_dir: str
    base_url: str
    timeout: int

    private_key_path: str

    private_key: Union[None, PrivateKey] = None
    public_key: Union[None, PublicKey] = None

    def __init__(
        self,
        config_dir: str = user_config_dir,
        timeout: int = 5,
        base_url: str = "https://api.rusty-forms.com/v1",
        private_key: Union[None, PrivateKey] = None,
    ):
        self.config_dir = config_dir
        self.private_key_path = config_dir + "/private_key.pem"
        self.timeout = timeout
        self.base_url = base_url
        self.private_key = private_key
        self.public_key = private_key.public_key if private_key is not None else None

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
