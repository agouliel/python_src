from llama_index.core import VectorStoreIndex # https://github.com/run-llama/llama_index/issues/7113
from llama_index.core import SimpleDirectoryReader # https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader/

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


DATA_DIR = './data_simple'
documents = SimpleDirectoryReader(DATA_DIR).load_data()

my_llm = Ollama(model="llama3", request_timeout=300.0) # timeout is important
my_embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5") # this downloads stuff to ~/Library/Caches/llama_index (see notes)
#my_embed_model = HuggingFaceEmbedding(model_name='hkunlp/instructor-xl') # too slow
index = VectorStoreIndex.from_documents(documents, llm=my_llm, embed_model=my_embed_model)

query_engine = index.as_query_engine(llm=my_llm, embed_model=my_embed_model)

obs_definition = 'Each observation has an answer, which contains three parts: a root cause, corrective actions and preventive actions.'
obs_str = 'Faulty radar' # change here
prompt_last_part = f'give a full answer (including root cause, corrective actions with bullets and preventive actions with bullets) for the following new observation: "{obs_str}"'
query_for_simple = f'{obs_definition} Based on the history of observations and their answers, {prompt_last_part}'

print(query_engine.query(query_for_simple))
