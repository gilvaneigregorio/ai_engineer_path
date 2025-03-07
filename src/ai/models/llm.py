from typing import Dict, List, Optional

from openai import OpenAI

MODEL_NAME = "gpt-4o-mini"


class LargeLanguageModel:
    _instance = None

    def __new__(cls, api_key: str = None):
        if cls._instance is None and api_key:
            cls._instance = super().__new__(cls)
            cls._instance.client = OpenAI(api_key=api_key)
            cls._instance.model_name = MODEL_NAME
        return cls._instance

    def call(
        self,
        messages: List[Dict[str, str]],
        tools_definitions: Optional[Dict[str, str]] = None,
        max_tokens: int = 8000,
        temperature: float = 0.5,
    ) -> any:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools_definitions,
            )

            return response.choices[0].message
        except Exception as e:
            raise Exception(f"Error in API call: {str(e)}")
