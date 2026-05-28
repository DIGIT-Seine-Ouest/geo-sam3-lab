import logging
import os

from dotenv import load_dotenv
from huggingface_hub import login

logger = logging.getLogger(__name__)


def setup_hf_token() -> None:
    load_dotenv()
    token = os.getenv("HF_TOKEN")
    if not token:
        raise EnvironmentError("HF_TOKEN not set in .env or environment")
    login(token=token)
    logger.info("HuggingFace login successful")
