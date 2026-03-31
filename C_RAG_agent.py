import os
from typing import TypedDict, List 
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document 
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("Groq_API")
os.environ["TAVILY_API_KEY"] = os.getenv("Tavily_API")

class AgentState(TypedDict):
    question: str
    context: str
    relevance: str
    answer: str

sample_docs = [
    Document(page_content="LangGraph is a library for building stateful, multi-actor applications with LLMs. It extends LangChain with cyclic graph support, enabling robust agent and multi-step RAG pipelines.", metadata={"source": "langgraph_intro"}),
    Document(page_content="Groq provides ultra-fast LLM inference using LPU hardware. It supports models like LLaMA-3, Mixtral and Whisper for speech transcription.", metadata={"source": "groq_intro"}),
    Document(page_content="Retrieval-Augmented Generation (RAG) enhances LLM responses by retrieving relevant documents from a vector store before generating an answer, reducing hallucinations.", metadata={"source": "rag_intro"}),
    Document(page_content="FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors, widely used for building vector databases.", metadata={"source": "faiss_intro"}),
    Document(page_content="Text-to-Speech (TTS) converts written text into spoken audio. gTTS uses Google's TTS API to generate natural-sounding speech from any text string.", metadata={"source": "tts_intro"}),
    Document(page_content="Speech-to-Text (STT) transcribes spoken audio to written text. Groq's Whisper endpoint provides fast and accurate transcription from audio files.", metadata={"source": "stt_intro"}),
    Document(page_content="FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard type hints. It auto-generates OpenAPI docs.", metadata={"source": "fastapi_intro"}),
    Document(page_content="Image analysis with vision LLMs can describe, classify, and answer questions about images. LLaMA 4 Scout on Groq supports vision tasks with image+text prompts.", metadata={"source": "vision_intro"}),
]


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(sample_docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
search_tool = TavilySearchResults(max_results=2)


def retrieve(state: AgentState):
    print("\n--- [NODE] RETRIEVING LOCAL DATA ---")
    docs = retriever.invoke(state["question"])
    context = "\n".join([doc.page_content for doc in docs])
    return {"context": context}

def grade(state: AgentState):
    print("--- [NODE] GRADING RELEVANCE ---")
    prompt = f"Is this context relevant to '{state['question']}'? Context: {state['context']}. Answer ONLY 'yes' or 'no'."
    score = llm.invoke(prompt).content.lower()
    return {"relevance": "yes" if "yes" in score else "no"}

def web_search(state: AgentState):
    print("--- [NODE] FALLBACK TO WEB SEARCH ---")
    results = search_tool.invoke(state["question"])
    return {"context": str(results)}

def generate(state: AgentState):
    print("--- [NODE] GENERATING FINAL ANSWER ---")
    prompt = f"Answer the question: {state['question']} using this context: {state['context']}"
    response = llm.invoke(prompt).content
    return {"answer": response}


workflow = StateGraph(AgentState)
workflow.add_node("retrieve_node", retrieve)
workflow.add_node("grade_node", grade)
workflow.add_node("web_search_node", web_search)
workflow.add_node("generate_node", generate)

workflow.add_edge(START, "retrieve_node")
workflow.add_edge("retrieve_node", "grade_node")

workflow.add_conditional_edges(
    "grade_node",
    lambda x: x["relevance"],
    {"yes": "generate_node", "no": "web_search_node"}
)

workflow.add_edge("web_search_node", "generate_node")
workflow.add_edge("generate_node", END)

app = workflow.compile()

print("TEST 1: Local Knowledge")
res1 = app.invoke({"question": "What is LangGraph?"})
print("Result:", res1["answer"])

print("\n" + "="*30 + "\n")

print("TEST 2: Web Knowledge")
res2 = app.invoke({"question": "What is the price of Gold today?"})
print("Result:", res2["answer"])