from pypdf import PdfReader

pdf_path = "data/nvidia_10k.pdf"

reader = PdfReader(pdf_path)

print("Number of pages:", len(reader.pages))

first_page = reader.pages[0]
text = first_page.extract_text()

print("\n--- FIRST PAGE ---\n")
print(text)
