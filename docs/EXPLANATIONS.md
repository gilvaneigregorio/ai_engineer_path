# The Path to Become an AI Engineer

## Models Used

### Large Language Models
- ** all-MiniLM-L6-v2 ** - Used to create the embeddings
- ** gpt-4o-mini ** - Used for text generation
- ** dall-e-3 ** - Used for image generation\

### Vector Database
- ** ChromaDB ** - Dropped
- ** PG Vector ** - Used for storing the embeddings

### Chat
- ** Streamlit ** - Used for the chat interface

# Reasoning

## Load recipes
The file with the recipes is quit bit, more them 2gb, so I read the CSV file in chunks in order to load the recipes into the database.
I started trying to use ChromaDB, but it was taking too long to load the recipes. I switched to PG Vector and it was much faster and supported the size of the file.

It takes around 2 hour to load all the recipes into the database but it is a one time process.

## Conversional AI
I wanted something simple and easy to use, so I used Streamlit to create the chat interface.
For the text generation I used GPT-4o-mini, it is a small model but it is enough for the purpose of this project.
The user will be free to ask any question he wants, leeting the conversation flow naturally.

Once the user asks for a recipe, the tool I created will search for the most similar recipe in the database and return it to the user.
This is a nice way to let the llm decide when he needs to ask for more information or for a recipe in this case.
The goal of this tool is identify the ingredients the user wants to use or avoid and return a recipe that fits the user's needs.
My first ideal was use some multi language modal to translate it to english, but gpt-4o covers a lot of languages, so I decided to use it.

With the ingredients identified, it need to be embedded and a search on the database is made to find the most similar recipe.
The recipe is then returned to the user.

If the user wants the recipe in a specific language, the tool will use the gpt-4o to translate it to the desired language.

## Image Generation
I used DALL-E-3 to generate the images of the recipes.
The image is generated based on the ingredients of the recipe, so the user can have a visual idea of the recipe he is going to cook.
