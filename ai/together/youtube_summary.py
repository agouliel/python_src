# https://www.freecodecamp.org/news/how-to-start-building-projects-with-llms

from langchain_together import ChatTogether
from langchain_community.document_loaders import YoutubeLoader
from langchain.prompts import PromptTemplate
from langchain import LLMChain
from dotenv import load_dotenv
import os

load_dotenv()

prompt = """Read through the entire transcript carefully.
           Provide a concise summary of the video's main topic and purpose.
           Extract and list the five most interesting or important points from the transcript.
           For each point: State the key idea in a clear and concise manner.

        - Ensure your summary and key points capture the essence of the video without including unnecessary details.
        - Use clear, engaging language that is accessible to a general audience.
        - If the transcript includes any statistical data, expert opinions, or unique insights, prioritize including these in your summary or key points."""

llm = ChatTogether(
  together_api_key = os.environ['TOGETHER_API_KEY'], # https://python.langchain.com/docs/integrations/llms/together
  model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
)

video_url = 'https://www.youtube.com/watch?v=XEgX04mAwK8' # Making a game like it's 1993
loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False)
data = loader.load()
messages = [
    ("system", prompt,),
    ("human", data[0].page_content),
]
ai_msg = llm.invoke(messages)

product_description_template = PromptTemplate(
    input_variables=["video_transcript"],
    template = prompt + "\n Video transcript: {video_transcript}"
)

chain = LLMChain(llm=llm, prompt=product_description_template)

summary = chain.invoke({
    "video_transcript": data[0].page_content
})

#UserWarning: Importing LLMChain from langchain root module is no longer supported. Please use langchain.chains.LLMChain instead.
#<python-input-11>:1: LangChainDeprecationWarning: The class `LLMChain` was deprecated in LangChain 0.1.17 and will be removed in 1.0. Use :meth:`~RunnableSequence, e.g., `prompt | llm`` instead.
#chain = LLMChain(llm=llm, prompt=product_description_template)

print(summary['text'])

"**Summary:**\nThe video is about creating a game like it's 1993, using old tools and techniques. The creator decides to make a maze-like game with a bouncing character that shoots things, and uses various libraries and tools to create the game. They discuss their process, from choosing a development environment to implementing features like collision detection, mouse support, and keyboard input.\n\n**Five Most Interesting or Important Points:**\n\n1. **Key Idea:** The creator chooses to write their own game engine in C, using Borland Turbo C++ as their development environment, to have more control over the graphics and performance.\n2. **Key Idea:** The creator uses a public domain library called Xlib to handle graphics operations, including setting up screen resolutions, hardware scrolling, and double buffering.\n3. **Key Idea:** The creator implements a major optimization by using hardware scrolling, which allows them to only re-draw the tiles that have a sprite over them, improving performance.\n4. **Key Idea:** The creator uses a shareware utility called 256paint to create graphics, and a conversion utility to convert the raw image data into tile sets that can be loaded into the game.\n5. **Key Idea:** The creator implements a state machine to deal with level transitions and other game logic, and uses a look-up table to calculate the velocity of bullets, which helps to improve performance and fix issues with the game."
