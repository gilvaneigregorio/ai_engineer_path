from ai.agents.recipe_retriever import RecipeRetrieverAgent
from ai.models.diffusals import DiffusalModel
from ai.tools.base import BaseTool


class RecipeTool(BaseTool):
    def __init__(self, diffusal_model: DiffusalModel):
        self.diffusal_model = diffusal_model

    def get_function_definition(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": "recipe_tool",
                "description": "Get a recipe based on the input and ingredient preferences. All ingredients must be specified in English.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ingredients_to_use": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of ingredients that should be included in the recipe (the result have to be in English). e.g. ['chicken', 'tomato']",
                        },
                        "ingredients_to_avoid": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of ingredients that should not be included in the recipe (the result have to be in English). e.g. ['beef', 'pork']",
                        },
                    },
                    "required": ["ingredients_to_use", "ingredients_to_avoid"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }

    def call(
        self, ingredients_to_use: list[str] = [], ingredients_to_avoid: list[str] = []
    ) -> tuple[str, str]:
        recipe_retriever = RecipeRetrieverAgent()
        recipe, url = recipe_retriever.call(
            self.diffusal_model, ingredients_to_use, ingredients_to_avoid
        )
        return recipe, url
