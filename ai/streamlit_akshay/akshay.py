import uuid, gc, base64, os, tempfile
import streamlit as st
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, PromptTemplate #, Settings
#from llama_index.embeddings.huggingface import HuggingFaceEmbedding

if 'id' not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}

session_id = st.session_state.id
client = None

def reset_chat():
    st.session_state.messages = []
    st.session_state.context = None
    gc.collect()

def display_pdf(file):
    # Opening file from file path
    st.markdown('### PDF Preview')
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    # Embedding PDF in HTML
    pdf_display = f'''<iframe src="data:application/pdf;base64,{base64_pdf}" width="400"
    height="100%" type="application/pdf" style="height:100vh; width:100%">
    </iframe>'''
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

with st.sidebar:
    selected_model = st.selectbox('Select your LLM:', ('OpenAI','Llama-3','Phi-3','Qwen'), index=0, key='selected _model')
    st.header(f'Add your documents!')
    uploaded_file = st.file_uploader('Choose your `.pdf` file', type='pdf')

    if uploaded_file:
        #display_pdf(uploaded_file)
        try:
            file_key = f'{session_id}-{uploaded_file.name}'
            # Check if the model has changed or the cache needs refreshing
            if 'current_model' not in st.session_state or st.session_state.current_model != selected_model:
                st.session_state.current_model = selected_model
                # Clear cached data relevant to the previous model
                st.session_state.file_cache.pop(file_key, None)
                st.rerun() #experimental_rerun() # Optionally rerun to refresh

            # Continue with file processing and LLM instantiation
            # Instantiate the LLM model based on the current selection
            if st.session_state.current_model == 'OpenAI':
                pass # OpenAI is the default, so it does not need settings
            elif st.session_state.current_model == 'Llama-3':
                pass #llm = Ollama(model='llama3', request_timeout=120.0)
            elif st.session_state.current_model == 'Phi-3':
                pass #llm = Ollama(model='phi3', request_timeout=120.0)
            elif st.session_state.current_model == 'Qwen':
                pass #llm = Ollama(model='qwen:7b', request_timeout=120.0)

            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())

                st.write('Indexing your document...')

                if file_key not in st.session_state.get('file_cache', {}):
                    if os.path.exists(temp_dir):
                        loader = SimpleDirectoryReader(input_dir = temp_dir, required_exts=['.pdf'], recursive=True)
                    else:
                        st.error('Could not find the file you uploaded, please check')
                        st.stop()

                    docs = loader.load_data()

                    # setup embedding model (not needed if using OpenAI)
                    #embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-large-en-v1.5')
                    #Settings.embed_model = embed_model

                    index = VectorStoreIndex.from_documents(docs, show_progress=True)

                    # Create the query engine, where we use a cohere reranker
                    #Settings.llm = llm # (not needed if using OpenAI)

                    query_engine = index.as_chat_engine() # this doesn't work with response_synthesizer prompt
                    #query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)

                    qa_prompt_tmpl_str = (
                      'Context information is below.\n'
                      '----------\n'
                      '{context_str}\n'
                      '----------\n'
                      'Given the context information above, I want you to answer the query.'
                      'Query: {query_str}\n'
                      'Answer: '
                    )
                    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
                    #query_engine.update_prompts({'response_synthesizer:text_qa_template': qa_prompt_tmpl})

                    st.session_state.file_cache[file_key] = query_engine
                else:
                    query_engine = st.session_state.file_cache[file_key]

                st.success('Ready to Chat!')
                display_pdf(uploaded_file)
        except Exception as e:
            print(e)

col1, col2 = st.columns([6, 1])
with col1:
    st.header('Chat with your Docs!')
with col2:
    st.button('Clear', on_click=reset_chat)
# Initialize chat history
if 'messages' not in st.session_state:
    reset_chat()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'] )
# Accept user input
if prompt := st.chat_input('Whats up?'):
    # Add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ''

        chat_response = query_engine.chat(prompt)
        full_response = chat_response.response

        # Simulate stream of response with milliseconds delay
        #streaming_response = query_engine.query(prompt)
        #for chunk in streaming_response.response_gen:
            #full_response += chunk
            #message_placeholder.markdown(full_response + '| ')

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({'role': 'assistant', 'content': full_response})