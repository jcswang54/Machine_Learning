# Machine Learning Portfolio — JinCheng Wang

Mathematics PhD building machine learning and AI systems.

This repository contains end-to-end machine learning projects spanning
- Data Analysis
- Classical Machine Learning
- Scientific Machine Learning
- Neural ODEs
- Retrieval-Augmented Generation (RAG)
- Agentic AI Systems

using Python, PyTorch, scikit-learn, SciPy, SQL, and modern LLM-based tools.

Each project includes source code, documentation, visualizations, and reproducible experiments.
## Featured Projects

* **Project 4:** [Agentic Financial Research Assistant](./Project_4_ai_financial_research_assistant/README.md)
    * Built an agentic RAG system that answers questions about NVIDIA's 10-K with page-level, citation-grounded answers based *ONLY* on the filing. The agent explicitly controls when sufficient evidence has been gathered, rather than leaving that decision implicit in the LLM
    * Research agent adaptively selects retrieval strategy (baseline search, query expansion, or targeted subquestions) based on question structure, with iterative research bounded by an explicit evidence-sufficiency check
    * Evaluated at three levels: retrieval quality, agent behavior, and claim-level answer grounding, which goes beyond demo-only evaluation typical of RAG portfolio projects
    * **Skills:** Python, RAG, LLMs, Agentic AI, Chroma, FastAPI, Semantic Search, Evaluation
* **Project 3:** [Neural ODE Learning Geodesic Flow](./Project_3_geodesic_neural_ode/README.md)
    * Trained a Neural ODE to learn continuous geodesic dynamics from trajectory data
    * **Skills:** PyTorch, torchdiffeq, SciPy, Neural ODE, Differential Equations
* **Project 2:** [Machine Learning for University Ranking Prediction](./Project_2_university_rankings/README.md)
    * Predicted Top-100 universities using supervised and unsupervised machine learning on the Times Higher Education rankings dataset
    * **Skills:** scikit-learn, Logistic Regression, Random Forest, PCA, K-Means
* **Project 1:** [Data Analysis for University Rankings](./Project_1_university_rankings/README.md)
	* Data analysis of the Times Higher Education rankings dataset (2,603 universities, 2011–2016)
    * Demonstrated that the correlation matrix is a Gram matrix, revealing a low-dimensional structure in the ranking data
	* **Skills:** pandas, NumPy, SQL
  
## Tech Stack
**AI / LLM**
- Retrieval-Augmented Generation (RAG) • Agentic AI • LLMs • Semantic Search • Vector Databases

**Machine Learning**

- PyTorch • scikit-learn • torchdiffeq

**Data**

- NumPy • SciPy • pandas • Matplotlib

**Languages**
- Python • SQL


**Tools**

- FastAPI • Chroma • Git • GitHub • SQLite • Jupyter

## Repository Structure

```text
Machine_Learning/
├── Project_4_ai_financial_research_assistant
│   └── RAG + Agentic AI
├── Project_3_geodesic_neural_ode
│   └── Scientific Machine Learning
├── Project_2_university_rankings
│   └── Machine Learning
├── Project_1_university_rankings
│   └── Data Analysis
└── README.md
```

Additional machine learning projects will be added as the portfolio continues to grow.