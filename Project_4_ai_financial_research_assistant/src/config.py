from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma

load_dotenv()


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embeddings,
)

llm = ChatOpenAI(
    model="gpt-5.6",
    temperature=0,
    reasoning_effort="none"
)