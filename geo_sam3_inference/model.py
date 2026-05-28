import logging

import numpy as np
import torch
from PIL import Image
from transformers import Sam3Model, Sam3Processor

logger = logging.getLogger(__name__)


class Sam3InferenceEngine:
    def __init__(self, model_id: str = "facebook/sam3"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.processor = None
        logger.info("Loading SAM3 on %s", self.device)
        try:
            self.model = Sam3Model.from_pretrained(model_id).to(self.device)
            self.processor = Sam3Processor.from_pretrained(model_id)
            logger.info("SAM3 loaded successfully")
        except Exception as e:
            logger.error("Error loading SAM3: %s", e)

    def predict_masks(
        self, image: Image.Image, prompt: str, threshold: float = 0.4
    ) -> list[Image.Image]:
        if self.model is None:
            return []
        inputs = self.processor(
            images=image, text=prompt, return_tensors="pt"
        ).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        results = self.processor.post_process_instance_segmentation(
            outputs,
            threshold=threshold,
            mask_threshold=0.5,
            target_sizes=inputs["original_sizes"].tolist(),
        )[0]
        masks = []
        if "masks" in results:
            for mask_tensor in results["masks"]:
                mask_np = (mask_tensor.cpu().numpy() * 255).astype(np.uint8)
                masks.append(Image.fromarray(mask_np))
        logger.debug("predict_masks: %d mask(s) detected", len(masks))
        return masks
