import ast

from ai.vectordb.base import DEFAULT_COLLECTION
from ai.vectordb.pgvector.pgvector import PGVector
from utils.relational_database import get_session


class RecipeRetrieverAgent:
    def __init__(self):
        db_session = next(get_session())
        self.vector_db = PGVector(db_session)

    def call(
        self, ingredients_to_use: list[str], ingredients_to_avoid: list[str]
    ) -> str:
        # Search for recipes that contain the ingredients to use
        results = self.vector_db.search(
            collection_name=DEFAULT_COLLECTION,
            query="".join(ingredients_to_use),
            top_k=10,
        )

        # Filter out recipes that contain ingredients to avoid
        results = [
            result
            for result in results
            if not any(
                ingredient in ast.literal_eval(result.metadata["NER"])
                for ingredient in ingredients_to_avoid
            )
        ]

        # Top result is the most relevant
        if len(results) == 0:
            return "No recipes found. Try again with different ingredients."

        result = results[0].metadata
        return f"""
            {result["title"]}
            Ingredients:
            {result["ingredients"]}
            Instructions:
            {result["directions"]}

            Use:
            {ingredients_to_use}
            Avoid:
            {ingredients_to_avoid}

        """
