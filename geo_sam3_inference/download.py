import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import login, snapshot_download

logger = logging.getLogger(__name__)


def setup_hf_token() -> None:
    load_dotenv()
    token = os.getenv("HF_TOKEN")
    if not token:
        raise EnvironmentError("HF_TOKEN not set in .env or environment")
    login(token=token)
    logger.info("HuggingFace login successful")


def download_model(model_id: str = "facebook/sam3") -> Path:
    logger.info("Downloading model: %s", model_id)
    path = snapshot_download(repo_id=model_id)
    logger.info("Model available at: %s", path)
    return Path(path)
