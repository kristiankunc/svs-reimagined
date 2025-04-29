import os
import secrets
from dotenv import load_dotenv
from .base_dir import BASE_DIR

ENV_VARS = {
    "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY": None,
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET": None,
    "SECRET_KEY": None,
    "DEBUG": False,
    "ALLOWED_HOSTS": ["localhost", "127.0.0.1"],
}


def load_env() -> dict:
    variables = {}
    if os.path.exists(os.path.join(BASE_DIR, ".env")):
        load_dotenv(os.path.join(BASE_DIR, ".env"))

    secret_key_path = os.path.join(BASE_DIR, "data", "secret_key.txt")

    if os.path.exists(secret_key_path):
        with open(secret_key_path, "r") as f:
            secret_key = f.read().strip()
            os.environ["SECRET_KEY"] = secret_key
    else:
        with open(secret_key_path, "w") as f:
            secret_key = secrets.token_urlsafe(32)
            f.write(secret_key)
            os.environ["SECRET_KEY"] = secret_key

    for key, default_value in ENV_VARS.items():
        if key in os.environ:
            value = os.environ[key]

        else:
            if default_value is None:
                raise ValueError(f"Environment variable {key} is not set and has no default value.")

            value = default_value

            if key == "SECRET_KEY":
                with open(os.path.join(BASE_DIR, "data", "secret_key.txt"), "w") as f:
                    f.write(os.environ.get(key, default_value))
                    print(f"Generated new secret key, saved to {f.name}")

        variables[key] = value

    return variables
