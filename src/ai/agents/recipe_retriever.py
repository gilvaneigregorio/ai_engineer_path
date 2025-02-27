import ast

from ai.vectordb import DEFAULT_COLLECTION, VectorDB


class RecipeRetrieverAgent:
    def __init__(self):
        self.vector_db = VectorDB()

    def call(
        self, ingredients_to_use: list[str], ingredients_to_avoid: list[str]
    ) -> str:
        collection = self.vector_db.get_or_create_collection(DEFAULT_COLLECTION)
        # Search for recipes that contain the ingredients to use
        results = self.vector_db.search(
            collection=collection, query="".join(ingredients_to_use), top_k=10
        )

        # Filter out recipes that contain ingredients to avoid
        results["metadatas"][0] = [
            result
            for result in results["metadatas"][0]
            if not any(
                ingredient in ast.literal_eval(result["NER"])
                for ingredient in ingredients_to_avoid
            )
        ]

        # Top result is the most relevant
        if len(results["metadatas"][0]) == 0:
            return "No recipes found. Try again with different ingredients."

        result = results["metadatas"][0][0]
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
