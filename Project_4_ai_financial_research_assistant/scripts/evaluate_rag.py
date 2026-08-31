import json
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.retrieval import (
    expand_query,
    retrieve_documents,
    deduplicate_chunks,
)

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

llm = ChatOpenAI(
    model="gpt-5.6",
    temperature=0
)

def select_top_chunks(unique_chunks, n=5):
    sorted_chunks = sorted(
        unique_chunks.values(),
        key=lambda x: x[1]
    )
    return sorted_chunks[:n]

correct = 0
total_relevant_retrieved = 0
total_retrieved = 0

for question in evaluation_questions:
    expanded_queries = expand_query(question["question"], llm)
    all_results = retrieve_documents(expanded_queries, vectorstore, k=3)
    unique_chunks = deduplicate_chunks(all_results)
    top_chunks = select_top_chunks(unique_chunks)
    retrieved_pages = [
        int(result.metadata.get("page_label"))
        for result, score in top_chunks
    ]

    expected_pages = question["expected_pages"]
    relevant_retrieved = 0
    relevant_retrieved = sum(
        page in expected_pages
        for page in retrieved_pages
        )
    question_precision = relevant_retrieved / len(retrieved_pages)
    
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
    print("Question precision:", f"{question_precision:.1%}")

recall = correct / len(evaluation_questions)
precision = total_relevant_retrieved / total_retrieved

print("\n===== QUERY EXPANSION RESULTS =====")
print(f"Retrieval Recall: {recall:.1%}")
print(f"Retrieval Precision: {precision:.1%}") 