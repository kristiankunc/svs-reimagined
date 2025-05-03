import os
import secrets
from dotenv import load_dotenv
from .base_dir import BASE_DIR

# All required environment variables and their default values
ENV_VARS = {
    "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY": None,
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET": None,
    "SECRET_KEY": None,
    "DEBUG": False,
    "ALLOWED_HOSTS": ["localhost", "127.0.0.1"],
}


def load_env() -> dict:
    """
    Loads environment variables from a `.env` file and a `secret_key.txt` file,
    and ensures all required environment variables are set. If a secret key
    does not exist, it generates a new one and saves it to `secret_key.txt`.
    Additionally, all loaded values are added to the global environment variables
    using `os.environ`.

    Returns:
        dict: A dictionary containing the loaded environment variables and their values.

    Raises:
        ValueError: If a required environment variable is not set and has no default value.

    Notes:
        - The function checks for the existence of a `.env` file in the `BASE_DIR` directory
          and loads its contents into the environment using `load_dotenv`.
        - If the `secret_key.txt` file does not exist, a new secret key is generated, saved
          to the file, and added to the environment variables.
        - The `ENV_VARS` dictionary is expected to define the required environment variables
          and their default values.
        - All loaded or default values are added to the global environment variables (`os.environ`),
          arrays are converted to comma-separated strings.
    """
    variables = {}
    if os.path.exists(os.path.join(BASE_DIR, ".env")):
        load_dotenv(os.path.join(BASE_DIR, ".env"))

    secret_key_path = os.path.join(BASE_DIR, "data", "secret_key.txt")

    # Using already generated secret key, otherwise generating a new one
    if os.path.exists(secret_key_path):
        with open(secret_key_path, "r") as f:
            secret_key = f.read().strip()
            os.environ["SECRET_KEY"] = secret_key
    else:
        with open(secret_key_path, "w") as f:
            secret_key = secrets.token_urlsafe(32)
            f.write(secret_key)
            os.environ["SECRET_KEY"] = secret_key

    # Check if all vars are already defined, if not attempt to use the default values
    for key, default_value in ENV_VARS.items():
        if key in os.environ:
            value = os.environ[key]
            if isinstance(default_value, list):
                value = value.split(",")
        else:
            if default_value is None:
                raise ValueError(f"Environment variable {key} is not set and has no default value.")

            value = default_value

            if key == "SECRET_KEY":
                with open(os.path.join(BASE_DIR, "data", "secret_key.txt"), "w") as f:
                    f.write(value)
                    print(f"Generated new secret key, saved to {f.name}")

        variables[key] = value

        env_value = value
        if isinstance(value, list):
            env_value = ",".join(map(str, value))

        os.environ[key] = str(env_value)

    return variables
