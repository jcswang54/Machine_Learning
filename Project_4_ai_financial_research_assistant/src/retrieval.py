def expand_query(query, llm, n=5):
    expansion_prompt = f"""
Generate {n} different search queries that could help retrieve relevant passages from NVIDIA's 10-K for the following question.
The queries should use different terminology and perspectives, while preserving the meaning of the original question.
Original question:
{query}

Return ONLY the {n} queries, one per line.
"""
    expansion_response = llm.invoke(expansion_prompt)

    return [
        q.strip()
        for q in expansion_response.content.split("\n")
        if q.strip()
    ]

def retrieve_documents(expanded_queries, vectorstore, k=3):
    all_results = []

    for expanded_query in expanded_queries:
        results = vectorstore.similarity_search_with_score(
            expanded_query,
            k=k
        )

        for result, score in results:
            all_results.append(
                (result, score, expanded_query)
            )

    return all_results

def deduplicate_chunks(all_results):
    unique_chunks = {}

    for result, score, expanded_query in all_results:
        chunk_text = result.page_content.strip()

        if chunk_text not in unique_chunks:
            unique_chunks[chunk_text] = (result, score)

    return unique_chunks

def baseline_search(query, vectorstore, k=5):
    return vectorstore.similarity_search_with_score(
        query,
        k=k
    )

def expanded_search(query, vectorstore, llm, n=5, k=3):
    expanded_queries = expand_query(
        query,
        llm,
        n=n
    )

    all_results = retrieve_documents(
        expanded_queries,
        vectorstore,
        k=k
    )

    unique_chunks = deduplicate_chunks(all_results)

    return unique_chunks

def targeted_search(subquestion, vectorstore, k=3):
    results = vectorstore.similarity_search_with_score(
        subquestion,
        k=k
    )

    return results