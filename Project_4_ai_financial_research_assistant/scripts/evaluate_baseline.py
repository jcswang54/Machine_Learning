import json
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

with open("data/evaluation_questions.json", "r") as f:
    evaluation_questions = json.load(f)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embeddings,
)

def retrieve_baseline(question, vectorstore, k=5):
    results = vectorstore.similarity_search_with_score(
        question,
        k=k
    )
    return results

correct = 0
total_relevant_retrieved = 0
total_retrieved = 0

for question in evaluation_questions:
    results = retrieve_baseline(
        question["question"],
        vectorstore
    )

    retrieved_pages = [
        int(result.metadata.get("page_label"))
        for result, score in results
    ]

    expected_pages = question["expected_pages"]

    relevant_retrieved = sum(
        page in expected_pages
        for page in retrieved_pages
        )
    
    total_relevant_retrieved += relevant_retrieved
    total_retrieved += len(retrieved_pages)
    
    hit = any(
        page in retrieved_pages
        for page in expected_pages
    )

    if hit:
        correct += 1

    print("\nQuestion:")
    print(question["question"])
    print("Expected pages:", expected_pages)
    print("Retrieved pages:", retrieved_pages)
    print("Ground-truth hit:", hit)
    for result, score in results:
            page = result.metadata.get("page_label")
            print(f"Page {page} | Score {score:.4f}")

recall = correct / len(evaluation_questions)
precision = total_relevant_retrieved / total_retrieved

print("\n===== BASELINE RESULTS =====")
print(f"Retrieval Recall: {recall:.1%}")
print(f"Retrieval Precision: {precision:.1%}") 