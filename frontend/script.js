const API_URL = "http://127.0.0.1:5000/api";

let pieChart = null;
let lineChart = null;

/* ---------------- CLASSIFY ---------------- */
document.getElementById("classifyBtn").addEventListener("click", async () => {

    const query = document.getElementById("queryInput").value.trim();
    const source = document.getElementById("sourceSelect").value;

    if (!query) {
        alert("Please enter a query");
        return;
    }

    try {
        const res = await fetch(`${API_URL}/classify`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, source })
        });

        const data = await res.json();

        if (!data.success) {
            alert("Error in classification");
            return;
        }

        document.getElementById("resultBox").classList.remove("hidden");

        document.getElementById("resultBox").innerHTML = `
            <h3>🔍 Classification Result</h3>
            <p><b>Query:</b> ${data.original_query}</p>
            <p><b>Source:</b> ${data.source}</p>
            <p><b>Category:</b> ${data.predicted_category}</p>
            <p><b>Confidence:</b> ${(data.confidence * 100).toFixed(1)}%</p>
            <p><b>Response:</b> ${data.auto_response}</p>
            <p><b>Automation:</b> ${data.automation_action}</p>
            <p><b>Escalation:</b> ${data.escalation}</p>
            <p><b>Time:</b> ${new Date(data.timestamp).toLocaleString()}</p>
        `;

    } catch (err) {
        console.error(err);
        alert("Backend not running or CORS issue");
    }
});


/* ---------------- DASHBOARD ---------------- */

async function loadDashboard() {
    try {
        const res = await fetch(`${API_URL}/dashboard`);
        const result = await res.json();

        if (!result.success) {
            console.error(result.error);
            return;
        }

        const data = result.data;

        /* -------- CARDS -------- */
        document.getElementById("totalQueries").innerText = data.summary.total_queries || 0;
        document.getElementById("totalCategories").innerText = data.summary.unique_categories || 0;
        document.getElementById("topIssue").innerText = data.insights.most_common_issue || "-";

        /* -------- PIE CHART -------- */
        const labels = data.distribution.map(d => `${d.category} (${d.percentage}%)`);
        const values = data.distribution.map(d => d.count);

        if (pieChart) pieChart.destroy();

        pieChart = new Chart(document.getElementById("pieChart"), {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: values
                }]
            },
            options: {
                responsive: true
            }
        });

        /* -------- LINE CHART -------- */
        const labelsTrend = data.trend.map(d => d.date);
        const valuesTrend = data.trend.map(d => d.count);

        if (lineChart) lineChart.destroy();

        lineChart = new Chart(document.getElementById("lineChart"), {
            type: "line",
            data: {
                labels: labelsTrend,
                datasets: [{
                    label: "Daily Queries",
                    data: valuesTrend,
                    fill: false,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true
            }
        });

    } catch (err) {
        console.error("Dashboard error:", err);
    }
}

/* Load dashboard on page load */
window.onload = loadDashboard;