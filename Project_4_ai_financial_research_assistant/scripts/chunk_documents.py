from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

pdf_path = "data/nvidia_10k.pdf"

loader = PyPDFLoader(pdf_path)
documents = loader.load()

print("Pages:", len(documents))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(documents)

print("Chunks:", len(chunks))

print("\n--- FIRST CHUNK ---\n")
print(chunks[0].page_content)

print("\n--- METADATA ---\n")
print(chunks[0].metadata)

