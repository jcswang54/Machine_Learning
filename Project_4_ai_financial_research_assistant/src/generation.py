def build_agent_context(tool_results):
    source_map = {}
    context_parts = []

    for i, item in enumerate(tool_results, start=1):
        source_id = f"SOURCE_{i}"

        page = item.get("page", "Unknown")
        source = item.get("source", "Unknown")
        content = item.get("content", "")

        source_map[source_id] = {
            "source": source,
            "page": page
        }

        context_parts.append(
            f"[{source_id} | Page {page} | Source: {source}]"
            f"{content}"
        )

    context = "\n\n".join(context_parts)

    return context, source_map

def build_context(unique_chunks):
    source_map = {}
    context_parts = []

    for i, (chunk_text, (result,score)) in enumerate(
        unique_chunks.items(),
        start=1
    ):
        source_id = f"SOURCE_{i}"
        page = result.metadata.get("page_label", "Unknown")
        source = result.metadata.get("source", "Unknown")

        source_map[source_id] = {
            "source": source,
            "page": page
        }

        context_parts.append(
            f"[{source_id} | Page {page} | Source: {source}]"
            f"{chunk_text}"
        )

    context = "\n\n".join(context_parts)

    return context, source_map


def get_document_name(source):
    if source.endswith("nvidia_10k.pdf"):
        return "NVIDIA 2026 10-K"

    return source


def generate_answer(query, context, llm):
    prompt = f"""
You are a financial research assistant.
Answer the question using ONLY the provided sources.

Answer the query following the instructions:
- Separate Fact / Risk / Implication when appropriate.
- For objective questions, it is fine to provide only the sections that are relevant.
- Clearly distinguish reported facts from analytical inference.
- FACT should describe what NVIDIA reports in the provided sources.
- RISK should identify a business or financial risk supported by those facts.
- IMPLICATION should explain why that risk or fact matters to NVIDIA's business, financial position, or outlook.
- Do not present analytical inferences as facts.

IMPORTANT CITATION RULES:
- Every substantive claim must have a citation.
- Cite the SOURCE_ID that supports each claim.
- Use this exact format: [SOURCE_1], [SOURCE_2], etc.
- Do NOT write page numbers yourself.
- Do NOT invent SOURCE_IDs.
- Only cite SOURCE_IDs that appear in the provided context.
- Place citations immediately after the claim they support.
- If the provided sources do not contain enough information to answer the question, say so.
- Be concise and focus only on information relevant to the question.

Example:
NVIDIA depends on third-party foundries to manufacture its semiconductor wafers [SOURCE_1].
NVIDIA also relies on independent subcontractors for assembly, testing, and packaging [SOURCE_2].

Provided sources:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)

    return response.content


def convert_citations(answer, source_map):
    """
    Convert SOURCE_ID citations into human-readable citations
    and remove duplicate citations referring to the same document/page.
    """

    import re

    citation_map = {}

    for source_id, metadata in source_map.items():
        source = get_document_name(metadata["source"])
        page = metadata["page"]
        citation_map[source_id] = f"[{source}, Page {page}]"

    # Convert SOURCE_ID -> human-readable citation
    pattern = r"\[(SOURCE_\d+)\]"

    def replace_citation(match):
        source_id = match.group(1)
        return citation_map.get(source_id, match.group(0))

    answer = re.sub(pattern, replace_citation, answer)

    # Deduplicate identical citations within each paragraph.
    paragraphs = answer.split("\n\n")
    cleaned_paragraphs = []

    citation_pattern = r"\[NVIDIA 2026 10-K, Page \d+\]"

    for paragraph in paragraphs:
        seen = set()

        def remove_duplicate(match):
            citation = match.group(0)

            if citation in seen:
                return ""

            seen.add(citation)
            return citation

        paragraph = re.sub(
            citation_pattern,
            remove_duplicate,
            paragraph
        )

        # Clean up extra whitespace created by removing citations
        paragraph = re.sub(r"\s+([.,;:])", r"\1", paragraph)

        cleaned_paragraphs.append(paragraph)

    return "\n\n".join(cleaned_paragraphs)


def build_source_list(answer, source_map):
    sources = []

    for source_id, metadata in source_map.items():
        citation = f"[{source_id}]"

        if citation in answer:
            source = get_document_name(metadata["source"])
            page = metadata["page"]

            source_entry = f"{source}, Page {page}"

            if source_entry not in sources:
                sources.append(source_entry)

    return sources