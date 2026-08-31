from langchain_community.document_loaders import PyPDFLoader

pdf_path = "data/nvidia_10k.pdf"

loader = PyPDFLoader(pdf_path)

documents = loader.load()

print("Number of documents:", len(documents))

print("\n--- FIRST DOCUMENT ---\n")
print(documents[0].page_content)

print("\n--- METADATA ---\n")
print(documents[0].metadata)
