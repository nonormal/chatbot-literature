import os
import gradio as gr
from dotenv import load_dotenv
from pymongo import MongoClient

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["chatbot"]
history_collection = db["chat_history"]

# Embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load vectorstore
db_vector = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)

# OpenRouter LLM
llm = ChatOpenAI(
    model="deepseek/deepseek-prover-v2:free",
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1"
)


# Build RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db_vector.as_retriever()
)

# Chatbot logic
def chatbot_response(message, history):
    result = qa_chain.invoke({"query": message})
    response = result["result"]

    # Save to MongoDB
    history_collection.insert_one({
        "user_message": message,
        "bot_response": response
    })

    history.append((message, response))
    return history, history
# --- Load History Function ---
def load_history():
    docs = history_collection.find({}, {"_id": 0})
    chat = [(doc["user_message"], doc["bot_response"]) for doc in docs]
    return chat, chat

# Gradio Interface
# --- Gradio Interface ---
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    state = gr.State([])
    msg = gr.Textbox(label="Enter your message")

    with gr.Row():
        send_btn = gr.Button("Send")
        load_btn = gr.Button("History")

    send_btn.click(fn=chatbot_response, inputs=[msg, state], outputs=[chatbot, state])
    load_btn.click(fn=load_history, inputs=[], outputs=[chatbot, state])

demo.launch(share=True)

iface = gr.Interface(
    fn=chatbot_response,
    inputs=["text", "state"],
    outputs=["chatbot", "state"],
    title="ChatBot Vietnamese Literature",
    description="ChatBot Vietnamese Literature User Interface",
)

iface.launch(share=True)
