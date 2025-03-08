from ai.models.diffusals import DiffusalModel


class RecipeImageAgent:
    def __init__(self, diffusal_model: DiffusalModel):
        self.diffusal_model = diffusal_model

    def call(self, promp: str) -> str:
        prompt = f"""
            Given the following recipe title, generate an image of the dish: {promp}
            e.g. "Spaghetti Carbonara", "Beef Stroganoff", "Chicken Alfredo"
            """
        return self.diffusal_model.call(prompt)[0]
