import os

import streamlit as st
from dotenv import load_dotenv

from ai.agents.conversational import ConversationalAgent
from ai.constants import ROLE_ASSISTANT, ROLE_SYSTEM, ROLE_USER
from ai.llms import OpenAILLM
from ai.tools.recipes import RecipeTool

load_dotenv()


class ChatbotUI:
    def __init__(self):
        self.conversational_agent = None

        self.initialize_session_state()
        self.initialize_llm()

    def initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []

        os_openai_api_key = os.getenv("OPENAI_API_KEY")
        if "openai_api_key" not in st.session_state:
            st.session_state.openai_api_key = os_openai_api_key or ""

    def initialize_llm(self):
        api_key = st.session_state.openai_api_key
        if api_key:
            llm_model = OpenAILLM(api_key=api_key)
            self.conversational_agent = ConversationalAgent(
                llm_model=llm_model, tools=[RecipeTool()]
            )
            if st.session_state.messages == []:
                st.session_state.messages = [
                    self.conversational_agent.get_system_message()
                ]

        else:
            self.conversational_agent = None

    def setup_sidebar(self):
        with st.sidebar:
            st.session_state.openai_api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                key="api_key_input",
                value=st.session_state.openai_api_key,
            )
            if st.session_state.openai_api_key:
                self.initialize_llm()

    def display_header(self):
        st.title("🍝 TastyAI")
        st.caption("""
            AI-powered  meal  recommendation  platform  that 
            provides users with personalized meal suggestions based on their dietary preferences and 
            constraints.  Instead  of  flipping through static magazine pages, users can describe what 
            they  want  to  eat  in  natural  language,  and  the  system  will  generate  tailored  meal 
            recommendations,  complete  with  structured  recipes,  translation  options,  and 
            AI-generated images of the dish.
            """)

    def display_chat_history(self):
        for message in st.session_state.messages:
            if message["role"] != ROLE_SYSTEM:  # Skip system messages
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    def handle_user_input(self):
        if prompt := st.chat_input("What would you like to know?"):
            if not st.session_state.openai_api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()

            st.session_state.messages.append({"role": ROLE_USER, "content": prompt})
            with st.chat_message(ROLE_USER):
                st.markdown(prompt)

            with st.chat_message(ROLE_ASSISTANT):
                response = self.conversational_agent.call(st.session_state.messages)
                st.markdown(response)

            st.session_state.messages.append(
                {"role": ROLE_ASSISTANT, "content": response}
            )

    def run(self):
        self.setup_sidebar()
        self.display_header()
        self.display_chat_history()
        self.handle_user_input()


chatbot_ui = ChatbotUI()
