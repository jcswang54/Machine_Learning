from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

pdf_path = "data/nvidia_10k.pdf"

loader = PyPDFLoader(pdf_path)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="data/chroma_db",
)

print(f"Stored {len(chunks)} chunks in Chroma.")



query = "What are NVIDIA's major competitive risks?"

results = vectorstore.similarity_search(query, k=3)

for i, result in enumerate(results):
    print(f"\n--- RESULT {i+1} ---")
    print(result.page_content)
    print("\nMetadata:", result.metadata)

