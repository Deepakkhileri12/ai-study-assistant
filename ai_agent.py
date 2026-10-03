import os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from dotenv import load_dotenv

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_community.document_load")

load_dotenv() 

UPLOAD_DIR = "uploaded_pdfs"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def get_rag_chain():
    """Initializes and returns the RAG chain."""
    loader = DirectoryLoader(UPLOAD_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()

    if not docs:
        docs = [
            Document(
                page_content="No PDF documents are currently available in the system.", 
                metadata={"source": "empty_folder_fallback"}
            )
        ]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    splits = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorStore = FAISS.from_documents(splits, embeddings)
    retriever = vectorStore.as_retriever(search_kwargs={"k": 4})

    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0,  
    )

    prompt = ChatPromptTemplate.from_template("""
        Read the context provided below and answer the question.

        1. If the answer depends on the context, then provide the answer based on that context.
        2. If the answer does not depend on the context, then use your general knowledge to provide the answer and at the end state:
        "This information was not in the provided document; I stated it based on general knowledge."

        Context:
        {context}

        Question: {question}
        Answer:""")

    def format_docs_for_llm(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    retrieval_step = RunnableParallel(
        {"raw_docs": retriever, "question": RunnablePassthrough()}
    )

    rag_chain = retrieval_step | {
        "answer": (
            {
                "context": lambda x: format_docs_for_llm(x["raw_docs"]),
                "question": lambda x: x["question"],
            }
            | prompt
            | llm
            | StrOutputParser()
        ),
        "contexts": lambda x: [doc.page_content for doc in x["raw_docs"]],
        "question": lambda x: x["question"],
    }
    
    return rag_chain

def get_answer_from_rag_chain(query, rag_chain):
    result = rag_chain.invoke(query)
    return result["answer"]