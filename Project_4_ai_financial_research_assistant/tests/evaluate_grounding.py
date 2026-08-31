import json
from pathlib import Path


GROUNDING_FILE = Path("data/grounding_evaluation.json")


def load_evaluation():
    with open(GROUNDING_FILE, "r") as f:
        return json.load(f)


def main():
    evaluations = load_evaluation()

    total_claims = 0
    passed_citation_correctness = 0
    passed_citation_completeness = 0
    grounded_answers = 0

    for case in evaluations:
        claims = case["claims"]

        total_claims += len(claims)

        passed_citation_correctness += sum(
            claim["citation_correct"] for claim in claims
        )

        passed_citation_completeness += sum(
            claim["citation_complete"] for claim in claims
        )

        if all(claim["grounded"] for claim in claims):
            grounded_answers += 1

    citation_correctness = (
        passed_citation_correctness / total_claims
        if total_claims
        else 0
    )

    citation_completeness = (
        passed_citation_completeness / total_claims
        if total_claims
        else 0
    )

    total_answers = len(evaluations)

    groundedness = (
        grounded_answers / total_answers
        if total_answers
        else 0
    )

    print("=" * 60)
    print("Citation and Grounding Evaluation")
    print("=" * 60)

    print(
        f"Citation correctness:  "
        f"{passed_citation_correctness}/{total_claims} "
        f"({citation_correctness:.1%})"
    )

    print(
        f"Citation completeness: "
        f"{passed_citation_completeness}/{total_claims} "
        f"({citation_completeness:.1%})"
    )

    print(
        f"Groundedness:           "
        f"{grounded_answers}/{total_answers} "
        f"({groundedness:.1%})"
    )


if __name__ == "__main__":
    main()