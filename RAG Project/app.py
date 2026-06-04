import os
import shutil
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# LangChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

st.set_page_config(
    page_title="PDF RAG System",
    layout="wide"
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY missing in .env")
    st.stop()


st.markdown("""
<style>

.stApp{
background:#0E1117;
}

[data-testid="stSidebar"]{
background:#161B22;
}

.stButton>button{
width:100%;
background:#00FFA3;
color:black;
font-weight:bold;
border:none;
}

.stChatMessage{
background:#1C2128;
padding:10px;
border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_embedding_model():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# ==========================
# DOCUMENT PROCESSING
# ==========================

def process_document(uploaded_file):

    temp_file = Path("temp.pdf")

    with open(temp_file, "wb") as f:
        f.write(uploaded_file.getbuffer())

    loader = PyPDFLoader(
        str(temp_file)
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=250
    )

    chunks = splitter.split_documents(
        documents
    )

    if os.path.exists("chroma-db"):
        shutil.rmtree(
            "chroma-db"
        )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embedding_model(),
        persist_directory="chroma-db"
    )

    os.remove(
        temp_file
    )

    return vectorstore


# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    st.title(
        "RAG SYSTEM"
    )

    st.caption(
        "Upload PDF → Build Vector DB → Ask Questions"
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    if st.button(
        "INITIALIZE DATABASE"
    ):

        if uploaded_file:

            with st.spinner(
                "Creating vector database..."
            ):

                st.session_state.vs = process_document(
                    uploaded_file
                )

                st.success(
                    "Database Ready"
                )

        else:

            st.error(
                "Upload PDF first"
            )



if "messages" not in st.session_state:

    st.session_state.messages = []



st.title(
    "Chat With Document"
)

st.divider()


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )



question = st.chat_input(
    "Ask your document..."
)

if question:

    st.session_state.messages.append({

        "role": "user",

        "content": question

    })

    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )

    if "vs" not in st.session_state:

        st.warning(
            "Upload and initialize a PDF first"
        )

    else:

        try:

            retriever = (
                st.session_state.vs
                .as_retriever(

                    search_type="similarity",

                    search_kwargs={
                        "k": 4
                    }

                )
            )

            docs = retriever.invoke(
                question
            )

            if not docs:

                answer = (
                    "No relevant information found."
                )

            else:

                context = "\n\n".join(

                    doc.page_content

                    for doc in docs

                )

                context = context[:5000]

                with st.expander(
                    "Retrieved Context"
                ):

                    st.write(
                        context
                    )

                llm = ChatGroq(

                    groq_api_key=GROQ_API_KEY,

                    model="llama-3.1-8b-instant",

                    temperature=0.2

                )

                prompt = (
                    ChatPromptTemplate
                    .from_messages([

                        (

                            "system",

                            """
You are a helpful PDF assistant.

Answer ONLY using context.

If context partially answers,
provide best answer.

Say INFORMATION UNAVAILABLE only if
the information truly does not exist.
"""

                        ),

                        (

                            "human",

                            """
Context:

{context}

Question:

{question}
"""

                        )

                    ])
                )

                chain = prompt | llm

                result = chain.invoke({

                    "context": context,

                    "question": question

                })

                answer = (
                    result.content
                )

            with st.chat_message(
                "assistant"
            ):

                st.markdown(
                    answer
                )

            st.session_state.messages.append({

                "role": "assistant",

                "content": answer

            })

        except Exception as e:

            st.error(
                str(e)
            )