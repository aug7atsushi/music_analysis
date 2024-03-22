from openai import OpenAI

from music_analysis.utils.log import get_module_logger

logger = get_module_logger(__name__)


class DalleImageGenerator:
    def __init__(self) -> None:
        self.client = OpenAI()

    def get_generated_images_as_b64(
        self,
        prompt: str,
        model: str = "dall-e-2",
        width: int = 256,
        height: int = 256,
        quality: str = "standard",
        n: int = 1,
    ):
        logger.info("Generating images...")
        response = self.client.images.generate(
            prompt=prompt,
            model=model,
            size=f"{width}x{height}",
            quality=quality,
            n=n,
            response_format="b64_json",
        )
        logger.info("Done Generating images!")
        return [img.b64_json for img in response.data]
