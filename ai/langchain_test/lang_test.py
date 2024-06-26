# https://python.langchain.com/v0.1/docs/get_started/quickstart/

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
#from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
#from langchain_community.document_loaders import WebBaseLoader # pip install beautifulsoup4
from langchain_community.document_loaders import DirectoryLoader # pip install unstructured
from langchain_openai import OpenAIEmbeddings
#from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS # pip install faiss-cpu
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')

llm = ChatOpenAI(api_key=openai_api_key)
#llm = Ollama(model="llama2") # ollama pull llama2

# Prompt templates convert raw user input to better input to the LLM.
prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a world class technical documentation writer.'),
    ('user', '{input}')
])

#question = 'how can langsmith help with testing?'
question = 'Faulty radar'

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

#response = chain.invoke({'input': question})
#print('Answer without context:', response)
#print('-------------')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

loader = DirectoryLoader('/Users/agou/Desktop/_progr/python/llamaindex/data_obs_simple') #WebBaseLoader('https://docs.smith.langchain.com/user_guide')
docs = loader.load() # for DirectoryLoader, this downloads averaged_perceptron_tagger to ~/nltk_data (needs certifi)

embeddings = OpenAIEmbeddings()
#embeddings = OllamaEmbeddings()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template('''Each observation has an answer, which contains three parts: a root cause, corrective actions and preventive actions.
Based on the below history of observations and their answers:
<context>
{context}
</context>
give a full answer (including root cause, corrective actions with bullets and preventive actions with bullets) for the following new observation: {input}''')

# chain that takes a question and the retrieved documents and generates an answer.
document_chain = create_stuff_documents_chain(llm, prompt)
#response = document_chain.invoke({'input': question, 'context': docs}) # manual list: [Document(page_content="text")]
# the above fails for large context
#print('Answer with all context:', response)
#print('-------------')

# use the retriever to dynamically select the most relevant documents
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)
response = retrieval_chain.invoke({'input': question})
print('Answer with relevant context:', response['answer'])
print('-------------')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name='chat_history'),
    ('user', '{input}'),
    ('user', 'Given the above conversation, generate a search query to look up to get information relevant to the conversation')
])
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Answer the user questions based on the below context:\n\n{context}'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('user', '{input}'),
])
document_chain = create_stuff_documents_chain(llm, prompt)

retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

chat_history = [HumanMessage(content='Can LangSmith help test my LLM applications?'),
                AIMessage(content='Yes!')]
#response = retrieval_chain.invoke({'chat_history': chat_history, 'input': 'Tell me how'})
#print('Answer with history:', response['answer'])
