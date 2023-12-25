import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from utils.common_libraries import *
from utils.constants import *


def load_image_from_url(url: str, new_size: tuple = None):
    """
    Loads an image from a given URL and optionally resizes it.

    :param url: The URL of the image to load.
    :type url: str
    :param new_size: The new size of the image, if resizing is desired. Defaults to None.
    :type new_size: tuple, optional
    :return: The loaded image, possibly resized.
    :rtype: PIL.Image.Image
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Open the image from the response content
    image = Image.open(BytesIO(response.content))

    # Resize the image only if a new size is provided
    if new_size is not None:
        image = image.resize(new_size)

    return image


def authenticate_google_service_account_credentials():
    """
    Authenticate with Google using a service account.

    Reads the Google application credentials from an environment variable and creates a service account credential object.

    Returns:
        service_account.Credentials: The service account credentials.

    Raises:
        RuntimeError: If authentication or logging of the authentication fails.
    """
    credentials = GOOGLE_APPLICATION_CREDENTIALS
    if not credentials:
        raise RuntimeError(
            "Authentication failed: 'GOOGLE_APPLICATION_CREDENTIALS' environment variable is not set"
        )

    try:
        with open(credentials, "r") as source:
            info = json.load(source)
            service_account.Credentials.from_service_account_info(info)
            logging.info("Successfully authenticated with Google service account.")
            print("Successfully authenticated with Google service account.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Authentication failed: {e}")


def configure_google_ai_api():
    """
    Configures the Google AI API with the provided API key.

    Args:
        api_key (str): The API key for Google AI API.

    Returns:
        The configuration object for Google AI API.
    """
    try:
        configuration = genai.configure(api_key=GOOGLE_AI_STUDIO)
        ## Printing the models as part of successful authentication otherwise will throw error
        for m in genai.list_models():
            print(m.name)
            print(m.supported_generation_methods)
        logging.info("Successfully configured Google AI API.")
        print("Successfully configured Google AI API.")
        return configuration
    except Exception as e:
        logging.error(f"Failed to configure Google AI API: {e}")
        raise
