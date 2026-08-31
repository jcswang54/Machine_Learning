import json
from src.pipeline import research

with open("data/evaluation_questions.json", "r") as f:
    evaluation_questions = json.load(f)
for question in evaluation_questions:
    query = question["question"]
    answer, sources = research(query)

    print("\n\n===== QUESTION =====")
    print(query)
    
    print("\n\n===== ANSWER =====")
    print(answer)

    print("\n===== SOURCES =====")
    for source in sources:
        print(source)
