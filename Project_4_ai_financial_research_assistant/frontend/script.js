const button = document.getElementById("ask-button");
const questionInput = document.getElementById("question");
const answerDiv = document.getElementById("answer");
const sourcesDiv = document.getElementById("sources");
const loadingDiv = document.getElementById("loading");

function formatAnswer(text) {
    return text
        // Convert Markdown section headings to HTML headings.
        .replace(/^## (.*)$/gm, "<h3>$1</h3>")

        // Convert Markdown bold text.
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")

        // Remove the line break immediately following a section heading.
        .replace(/<\/h3>\s*<br>/g, "</h3>")

        // Convert remaining line breaks to HTML line breaks.
        .replace(/\n/g, "<br>");
}

button.addEventListener("click", async () => {

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    loadingDiv.textContent = "Researching...";
    answerDiv.textContent = "";
    sourcesDiv.textContent = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/research", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: question
            })
        });

        const data = await response.json();

        answerDiv.innerHTML = formatAnswer(data.answer);

        sourcesDiv.textContent = data.sources.join("\n");

    } catch (error) {
        answerDiv.textContent =
            "Something went wrong. Please check that the backend is running.";
    }

    loadingDiv.textContent = "";
});