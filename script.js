// static/js/script.js
document.getElementById("investment-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const riskLevel = document.getElementById("risk-level").value;
    const budget = document.getElementById("budget").value;

    if (budget <= 0) {
        alert("Please enter a valid budget.");
        return;
    }

    // Send data to Flask API for investment recommendations
    fetch("/investment_recommendation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            risk_level: riskLevel,
            budget: parseFloat(budget),
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            const recommendationsDiv = document.getElementById("recommendations");
            recommendationsDiv.innerHTML = "";

            if (data.recommendations) {
                const ul = document.createElement("ul");
                data.recommendations.forEach((recommendation) => {
                    const li = document.createElement("li");
                    li.textContent = `${recommendation.crypto}: $${recommendation.allocation.toFixed(2)}`;
                    ul.appendChild(li);
                });
                recommendationsDiv.appendChild(ul);
            } else {
                recommendationsDiv.textContent = data.error || "No recommendations available.";
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Something went wrong. Please try again later.");
        });
});
