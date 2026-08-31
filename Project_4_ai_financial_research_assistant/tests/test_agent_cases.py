TEST_CASES = [
    {
        "name": "simple_retrieval",
        "question": "What was NVIDIA's revenue in fiscal 2026?",
        "expected_tools": ["search_with_baseline", "finish_research"],
        "max_research_rounds": 2,
    },
    {
        "name": "broad_question",
        "question": "What are the major risks to NVIDIA's future growth?",
        "expected_tools": [
            "search_with_query_expansion",
            "finish_research",
        ],
        "max_research_rounds": 3,
    },
    {
        "name": "multi_part_question",
        "question": (
            "How did NVIDIA's revenue and operating income change "
            "from fiscal 2025 to fiscal 2026, and what factors drove "
            "those changes?"
        ),
        "expected_tools": [
            "search_targeted_subquestion",
            "finish_research",
        ],
        "max_research_rounds": 3,
    },
]