const API_URL = "http://127.0.0.1:5000/api";

/* ---------------- CLASSIFY ---------------- */
document.getElementById("classifyBtn").addEventListener("click", async () => {

    const query = document.getElementById("queryInput").value;

    if (!query) {
        alert("Please enter a query");
        return;
    }

    try {
        const res = await fetch(`${API_URL}/classify`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
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
            <p><b>Category:</b> ${data.predicted_category}</p>
            <p><b>Confidence:</b> ${(data.confidence * 100).toFixed(1)}%</p>
            <p><b>Reason:</b> ${data.reasoning}</p>
            <p><b>Response:</b> ${data.auto_response}</p>
            <p><b>Escalation:</b> ${data.escalation}</p>
        `;

    } catch (err) {
        alert("Backend not running or CORS issue");
    }
});


/* ---------------- DASHBOARD ---------------- */

async function loadDashboard() {
    try {
        const res = await fetch(`${API_URL}/dashboard`);
        const result = await res.json();

        const data = result.data;

        /* Cards */
        document.getElementById("totalQueries").innerText = data.summary.total_queries;
        document.getElementById("totalCategories").innerText = data.summary.unique_categories;
        document.getElementById("topIssue").innerText = data.insights.most_common_issue;

        /* PIE CHART (with %) */
        const labels = data.distribution.map(d => `${d.category} (${d.percentage}%)`);
        const values = data.distribution.map(d => d.count);

        new Chart(document.getElementById("pieChart"), {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{ data: values }]
            }
        });

        /* LINE CHART (daily trend) */
        const trendMap = {};

        data.trend.forEach(item => {
            if (!trendMap[item.date]) trendMap[item.date] = 0;
            trendMap[item.date] += item.count;
        });

        new Chart(document.getElementById("lineChart"), {
            type: "line",
            data: {
                labels: Object.keys(trendMap),
                datasets: [{
                    label: "Daily Queries",
                    data: Object.values(trendMap),
                    fill: false
                }]
            }
        });

    } catch (err) {
        console.error("Dashboard error:", err);
    }
}

loadDashboard();