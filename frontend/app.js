let currentMode = "text";

function selectMode(mode) {

    currentMode = mode;

    document.getElementById("textMode").style.display =
        mode === "text" ? "block" : "none";

    document.getElementById("urlMode").style.display =
        mode === "url" ? "block" : "none";

    document.querySelectorAll(".tab").forEach(tab => {
        tab.classList.remove("active");
    });

    event.target.classList.add("active");
}


async function analyze() {

    const resultBox = document.getElementById("result");

    let endpoint;
    let body;

    if (currentMode === "text") {

        const text = document.getElementById("messageInput").value.trim();

        if (!text) {
            alert("Please enter a message.");
            return;
        }

        endpoint = "https://cyberrakshak-6ntn.onrender.com/analyze/text";

        body = {
            text: text
        };

    } else {

        const url = document.getElementById("urlInput").value.trim();

        if (!url) {
            alert("Please enter a URL.");
            return;
        }

        endpoint = "https://cyberrakshak-6ntn.onrender.com/analyze/url";

        body = {
            url: url
        };
    }


    try {

        const response = await fetch(endpoint, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(body)

        });


        if (!response.ok) {
            throw new Error("API request failed");
        }


        const data = await response.json();

        showResult(data);


    } catch (error) {

        console.error(error);

        alert(
            "Cannot connect to CyberRakshak backend.\n\n" +
            "Make sure Uvicorn is running on port 8000."
        );
    }
}


function showResult(data) {

    const resultBox = document.getElementById("result");

    resultBox.classList.remove("hidden");

    document.getElementById("riskScore").textContent =
        data.risk_score;

    document.getElementById("riskLevel").textContent =
        data.risk_level;

    document.getElementById("verdict").textContent =
        data.verdict || "Suspicious activity detected";

    document.getElementById("progressBar").style.width =
        data.risk_score + "%";


    const signalsBox = document.getElementById("signals");

    signalsBox.innerHTML = "";


    if (data.signals && data.signals.length > 0) {

        data.signals.forEach(signal => {

            const element = document.createElement("div");

            element.className = "signal";

            element.textContent = "⚠ " + signal;

            signalsBox.appendChild(element);

        });

    } else {

        signalsBox.innerHTML =
            '<div class="signal">✓ No suspicious signals</div>';
    }


    resultBox.scrollIntoView({
        behavior: "smooth"
    });
}