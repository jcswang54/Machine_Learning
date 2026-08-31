from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

from src.config import llm, vectorstore

from src.retrieval import (
    baseline_search,
    expanded_search,
    targeted_search
)

from src.generation import (
    generate_answer,
    convert_citations,
    build_agent_context
)


@tool
def search_with_baseline(query: str):
    """
    Search NVIDIA's 10-K using direct vector retrieval.
    Use this for straightforward questions where direct retrieval is appropriate.
    """
    results = baseline_search(
        query,
        vectorstore,
        k=5
    )

    return [
        {
            "content": result.page_content,
            "page": result.metadata.get("page_label"),
            "source": result.metadata.get("source"),
            "score": score,
        }
        for result, score in results
    ]


@tool
def search_with_query_expansion(query: str):
    """
    Search NVIDIA's 10-K using multiple alternative formulations of the question.
    Use this when the question is broad, ambiguous, or difficult to retrieve directly.
    """
    unique_chunks = expanded_search(
        query,
        vectorstore,
        llm,
        n=5,
        k=3
    )

    return [
        {
            "content": result.page_content,
            "page": result.metadata.get("page_label"),
            "source": result.metadata.get("source"),
            "score": score,
        }
        for result, score in unique_chunks.values()
    ]


@tool
def search_targeted_subquestion(subquestion: str):
    """
    Search NVIDIA's 10-K for a specific subquestion created from a larger
    research question.
    """
    results = targeted_search(
        subquestion,
        vectorstore,
        k=5
    )

    return [
        {
            "content": result.page_content,
            "page": result.metadata.get("page_label"),
            "source": result.metadata.get("source"),
            "score": score,
        }
        for result, score in results
    ]


@tool
def finish_research():
    """
    End the research process when the retrieved evidence is sufficient
    to answer the user's question.
    """
    return "Research complete. The retrieved evidence is sufficient."


tools = [
    search_with_baseline,
    search_with_query_expansion,
    search_targeted_subquestion,
    finish_research,
]


tool_map = {
    tool.name: tool
    for tool in tools
}


llm_with_tools = llm.bind_tools(
    tools,
    tool_choice="required"
)


def run_agent(query):
    messages = [
        HumanMessage(
            content=f"""
You are a financial research agent specializing in NVIDIA's 10-K.

Your job is to decide WHAT research to perform and WHEN you have enough
evidence to answer the user's question.

You MUST use at least one research tool.
Your first action must be a tool call.
Do not answer from general knowledge.

RESEARCH STRATEGY:

1. search_with_baseline

Use for a focused factual question that can likely be answered by
direct retrieval from the 10-K.

2. search_with_query_expansion

Use when the question is broad, ambiguous, conceptual, or likely to
require multiple formulations to retrieve the relevant evidence.

3. search_targeted_subquestion

Use when the question contains multiple distinct research components.

Break the question into meaningful subquestions and search them separately.

RESEARCH CONTROL:

After EVERY retrieval result, inspect the evidence and decide whether it is
sufficient to answer the user's question.

If the evidence is sufficient:
- Call finish_research.
- Do not perform another retrieval search.
- After finish_research is called, the research phase is complete.

If the evidence is insufficient:
- Identify what information is missing.
- Choose the most appropriate next research strategy.
- Search only for the missing information.

finish_research is NOT a retrieval tool.
Use it only when you have enough evidence to answer the question.

Do NOT repeat a search merely to obtain additional supporting passages
when the existing evidence is already sufficient.

For straightforward factual questions, prefer stopping after one successful
retrieval.

For multi-part questions, ensure that each meaningful component is supported
before stopping.

Do not use more than 3 research rounds.

ONLY provide the final answer after obtaining evidence from the NVIDIA 10-K.
Base the final answer only on the retrieved evidence.

User question:
{query}
"""
        )
    ]

    tool_results = []

    for _ in range(3):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            break

        finish_called = False

        for tool_call in response.tool_calls:

            tool = tool_map[tool_call["name"]]

            result = tool.invoke(tool_call["args"])

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )

            # Keep retrieval results for final answer generation.
            if tool_call["name"] != "finish_research":
                tool_results.extend(result)

            if tool_call["name"] == "finish_research":
                finish_called = True

        if finish_called:
            break

    # Build the final evidence context from actual retrieval results.
    context, source_map = build_agent_context(tool_results)

    # Generate the final answer separately from the research agent.
    answer = generate_answer(
        query,
        context,
        llm
    )

    # Replace SOURCE_ID citations with document/page citations.
    answer = convert_citations(
        answer,
        source_map
    )

    return answer, messages, source_map