# https://www.photondesigner.com/articles/english-database-query

from time import sleep
from openai import OpenAI
import os, sys
from dotenv import load_dotenv

load_dotenv()

if len(sys.argv) > 1:
    query = sys.argv[1]
else:
   query = 'What is your expertise?'

client = OpenAI(api_key=os.environ['OPENAI_KEY'])
instructions = f"You are a personal data analyst."
assistant = client.beta.assistants.create(
        instructions=instructions,
        name="Data analyst",
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo-16k",
)
thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role='user',
            content=query
)
run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
)

while run.completed_at is None:
  sleep(1)
  run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

messages = client.beta.threads.messages.list(thread_id=thread.id)
text_messages = reversed([message.content[0].text.value for message in messages.data])

for text_message in text_messages:
    print(text_message)
