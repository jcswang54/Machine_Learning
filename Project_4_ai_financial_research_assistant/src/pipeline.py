from src.config import vectorstore, llm

from src.retrieval import (
    expand_query,
    retrieve_documents,
    deduplicate_chunks,
)

from src.generation import (
    build_context,
    generate_answer,
    build_source_list,
    convert_citations,
)

def research(query):
    expanded_queries = expand_query(query, llm)

    all_results = retrieve_documents(
        expanded_queries,
        vectorstore,
        k=3
    )

    unique_chunks = deduplicate_chunks(all_results)

    context, source_map = build_context(unique_chunks)

    answer = generate_answer(
        query,
        context,
        llm
    )

    sources = build_source_list(
        answer,
        source_map
    )

    answer = convert_citations(
        answer,
        source_map
    )

    return answer, sources