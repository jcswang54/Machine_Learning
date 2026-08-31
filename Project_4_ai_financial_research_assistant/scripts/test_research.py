from src.pipeline import research

answer, sources = research(
   "What will NVIDIA's stock price be in 2030?" 
)

print("\n===== An Example Question: =====")
print("What will NVIDIA's stock price be in 2030?")
print("\n===== Answer: =====")
print(answer)
print("\n===== Sources: =====")
print(sources)