import os
import streamlit as st
from langchain_community.document_loaders import HuggingFaceDatasetLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

DATASET = "databricks/databricks-dolly-15k"
EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-base"
INDEX_DIR = "faiss_index"

@st.cache_resource(show_spinner="Loading embedding model...")
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMB_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": False},
    )

@st.cache_resource(show_spinner="Loading or building the vector index...")
def get_vectorstore():
    documents_folder = "documents"

    if not os.path.exists(documents_folder):
        os.makedirs(documents_folder)
        raise FileNotFoundError(f"Please put your PDF/TXT files inside the '{documents_folder}' folder.")

    loader = DirectoryLoader(
        documents_folder,
        glob="**/*.pdf",
        show_progress=True,
        use_multithreading=True,
    )

    documents = loader.load()

    if not documents:
        raise ValueError("No PDF documents found in the 'documents' folder.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore
        
    data = HuggingFaceDatasetLoader(DATASET, "context").load()
    docs = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0
    ).split_documents(data)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(INDEX_DIR)
    return db

@st.cache_resource(show_spinner="Loading language model...")
def get_qa_chain():
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
    model = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL)
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        return_full_text=False,
    )
    
    llm = HuggingFacePipeline(pipeline=pipe)

    retriever = get_vectorstore().as_retriever(search_kwargs={"k": 3})
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
    
st.set_page_config(page_title="Industrial Q&A Chatbot")
st.title("Industrial Q&A Chatbot")
st.caption("Ask a question.")

question = st.text_input("Your question", placeholder="Hope you are doing well! How can I help you today?")

if st.button("Ask", type="primary") and question.strip():
    with st.spinner("Searching and generating an answer..."):
        result = get_qa_chain().invoke({"query": question})
       
        answer = result["result"].strip()
        for junk in [
            "Use the following pieces of context",
            "Answer only using the information",
            "If you don't know the answer",
            "Context:",
            "Question:",
            "Helpful Answer:",
            "Answer:"
        ]:
            if junk in answer:
                answer = answer.split(junk)[-1].strip()
    st.subheader("Answer:")
    st.write(result["result"])
    
    with st.expander("Retrieved context"):
        for i, doc in enumerate(result["source_documents"], 1):
            st.markdown(f"**Chunk {i}**")
            st.write(doc.page_content)
            st.divider()
