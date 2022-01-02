import os
import jwt
from configparser import ConfigParser

def set_up():
    env = os.getenv("ENV")

    if env == "dev":
        config = ConfigParser()
        config.read(".config")
        config = config["AUTH0"]
    else:
        config = {
            "DOMAIN": os.getenv("DOMAIN", "your.domain.com"),
            "API_AUDIENCE": os.getenv("API_AUDIENCE", "your.audience.com"),
            "ISSUER": os.getenv("ISSUER", "https://your.domain.com/"),
            "ALGORITHMS": os.getenv("ALGORITHMS", "RS256")
        }

    return config

class VerifyToken:

    def __init__(self, token):
        self.token = token
        self.config = set_up()

        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as err:
            return {"status": "error", "type": "PyJWKClientError", "msg": str(err)}
        except jwt.exceptions.DecodeError as err:
            return {"status": "error", "type": "DecodeError", "msg": str(err)}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"]
            )
        except Exception as e:
            return {"status": "error", "type": "JWTError", "msg": str(e)}

        return payload
