from typing import List

from ai.constants import ROLE_SYSTEM
from ai.models.llm import LargeLanguageModel
from ai.tools.base import BaseTool


class ConversationalAgent:
    def __init__(
        self,
        llm_model: LargeLanguageModel,
        tools: List[BaseTool] = [],
    ):
        self.llm_model = llm_model
        self.tools = tools

        self.tools_definitions = [tool.get_function_definition() for tool in tools]

    def get_system_message(self) -> dict:
        return {
            "role": ROLE_SYSTEM,
            "content": """You are an AI culinary assistant powered by a sophisticated recipe recommendation system. Your primary function is to help users discover personalized meal suggestions from our curated recipe database. Here's how you operate:

            1. Recipe Search & Recommendations:
            - Process natural language queries to find relevant recipes from the database
            - Consider dietary preferences and restrictions when suggesting meals
            - Provide semantically similar alternatives when exact matches aren't found
            - Focus on recipes that are actually available in our database

            2. Recipe Information Delivery:
            - Present structured recipes with clear ingredients and instructions
            - Mention any dietary categories (vegetarian, vegan, gluten-free, etc.)

            3. Communication Guidelines:
            - Use a friendly, helpful tone
            - Reply on the same language as the user
            - If a specific recipe isn't found, suggest similar alternatives
            - Always stay within the scope of available recipes
            - Be transparent about limitations

            Remember that you can only recommend recipes that exist in our database. Don't invent or generate new recipes. If you're unsure about specific details, acknowledge this and stick to the information available in our database.
            """,
        }

    def call(self, messages: List[dict]) -> str:
        message = self.llm_model.call(
            messages=messages, tools_definitions=self.tools_definitions
        )
        if message.tool_calls:
            return self._execute_tool(message.tool_calls[0])

        return message.content

    def _execute_tool(self, tool_call: any) -> str:
        tool = self._get_tool(tool_call.function.name)
        parameters = tool_call.function.arguments
        if isinstance(parameters, str):
            import json

            parameters = json.loads(parameters)
        return tool.call(**parameters)

    def _get_tool(self, tool_name: str) -> BaseTool:
        for tool in self.tools:
            if tool.get_function_definition()["function"]["name"] == tool_name:
                return tool

        return None
