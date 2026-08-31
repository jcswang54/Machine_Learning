from src.agent import run_agent
from tests.test_agent_cases import TEST_CASES


def get_tool_trace(messages):
    tools = []

    for message in messages:
        if hasattr(message, "tool_calls"):
            for tool_call in message.tool_calls:
                tools.append(tool_call["name"])

    return tools


for case in TEST_CASES:

    print("\n" + "=" * 70)
    print(case["name"])
    print("=" * 70)

    answer, messages, sources = run_agent(case["question"])

    tool_trace = get_tool_trace(messages)

    retrieval_tools = [
        tool
        for tool in tool_trace
        if tool != "finish_research"
    ]

    research_rounds = len(retrieval_tools)

    print("Question:")
    print(case["question"])

    print("\nTool trace:")
    print(" → ".join(tool_trace))

    print("\nResearch rounds:")
    print(research_rounds)

    print("\nFinal answer:")
    print(answer)

    print("\nSources:")
    print(sources)