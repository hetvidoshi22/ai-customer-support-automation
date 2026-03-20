async function classifyQuery() {
    const query = document.getElementById("queryInput").value;

    if (!query) {
        alert("Enter a query!");
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/classify", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query })
    });

    const data = await response.json();

    const resultBox = document.getElementById("resultBox");

    resultBox.classList.remove("hidden");

    resultBox.innerHTML = `
        <h3>🔍 Classification Result</h3>
        <p><b>Query:</b> ${data.query}</p>
        <p><b>Category:</b> ${data.category}</p>
        <p><b>Confidence:</b> ${data.confidence}</p>
        <p><b>Response:</b> ${data.response}</p>
        <p><b>Escalation:</b> ${data.escalation}</p>
    `;
}

/* Dummy Charts (replace later with backend data) */

const pieChart = new Chart(document.getElementById('pieChart'), {
    type: 'pie',
    data: {
        labels: ['Delivery Delay', 'Refund', 'Product Issue', 'Other'],
        datasets: [{
            data: [35, 25, 20, 20]
        }]
    }
});

const lineChart = new Chart(document.getElementById('lineChart'), {
    type: 'line',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        datasets: [{
            label: 'Queries',
            data: [10, 20, 15, 25, 18],
            fill: false
        }]
    }
});