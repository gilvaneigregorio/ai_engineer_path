from typing import List

from openai import OpenAI

MODEL_NAME = "dall-e-3"


class DiffusalModel:
    _instance = None

    def __new__(cls, api_key: str = None):
        if cls._instance is None and api_key:
            cls._instance = super().__new__(cls)
            cls._instance.client = OpenAI(api_key=api_key)
            cls._instance.model_name = MODEL_NAME
        return cls._instance

    def call(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1,
    ) -> List[str]:
        try:
            response = self.client.images.generate(
                model=self.model_name,
                prompt=prompt,
                size=size,
                quality=quality,
                n=n,
            )

            return [image.url for image in response.data]
        except Exception as e:
            raise Exception(f"Error generating image: {str(e)}")
