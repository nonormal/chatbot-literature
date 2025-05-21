import os
import gradio as gr
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load vectorstore
db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)

# OpenRouter LLM
llm = ChatOpenAI(
    model="deepseek/deepseek-prover-v2:free",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)


# Build RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
    return_source_documents=False
)

# Chatbot logic
def chatbot_response(message, history=[]):
    result = qa_chain.invoke({"query": message})
    history.append((message, result["result"]))
    return history, history

# Gradio Interface
iface = gr.Interface(
    fn=chatbot_response,
    inputs=["text", "state"],
    outputs=["chatbot", "state"],
    title="ChatBot Vietnamese Literature",
    description="ChatBot Vietnamese Literature User Interface",
)

iface.launch(share=True)
