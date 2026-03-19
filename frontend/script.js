document.addEventListener('DOMContentLoaded', function () {
    const API_BASE_URL = 'http://127.0.0.1:5000/api'; // Flask backend address

    // DOM Elements
    const totalQueriesEl = document.getElementById('total-queries-count');
    const uniqueCategoriesEl = document.getElementById('unique-categories-count');
    const dataPeriodEl = document.getElementById('data-period');
    const distributionChartCtx = document.getElementById('distributionChart').getContext('2d');
    const queryForm = document.getElementById('query-form');
    const newQueryInput = document.getElementById('new-query');
    const classificationResultDiv = document.getElementById('classification-result');
    const resultQueryEl = document.getElementById('result-query');
    const resultCategoryEl = document.getElementById('result-category');
    const resultConfidenceEl = document.getElementById('result-confidence');
    const resultReasoningEl = document.getElementById('result-reasoning');

    let distributionChart = null; // Variable to hold the chart instance

    // --- Function to Load and Display Dashboard Data ---
    async function loadDashboardData() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard`);
        const data = await response.json();

        if (data.success) {
            const dashboard = data.data;

            totalQueriesEl.textContent = dashboard.summary.total_queries;
            uniqueCategoriesEl.textContent = dashboard.summary.unique_categories;
            dataPeriodEl.textContent =
                dashboard.summary.date_range.start + " → " +
                dashboard.summary.date_range.end;

            const labels = dashboard.distribution.map(d => d.category);
            const values = dashboard.distribution.map(d => d.count);

            if (distributionChart) distributionChart.destroy();

            distributionChart = new Chart(distributionChartCtx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values
                    }]
                }
            });

        } else {
            alert("Dashboard error");
        }

    } catch (error) {
        console.error(error);
        alert("Failed to load dashboard");
    }
}


    // --- Function to Handle Query Classification ---
    async function classifyQuery(event) {
        event.preventDefault(); // Prevent the form from submitting traditionally

        const queryText = newQueryInput.value.trim();
        if (!queryText) {
            alert('Please enter a query to classify.');
            return;
        }

        try {
            console.log("Sending query for classification:", queryText);
            const response = await fetch(`${API_BASE_URL}/classify`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: queryText }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Classification result received:", data);

            if(data.success) {
                // Populate the result div with the response
                resultQueryEl.textContent = data.original_query;
                resultCategoryEl.textContent = data.predicted_category;
                resultConfidenceEl.textContent = `${(data.confidence * 100).toFixed(2)}%`;
                resultReasoningEl.textContent = data.reasoning;

                // Show the result div
                classificationResultDiv.classList.remove('hidden');
            } else {
                alert(`Classification error: ${data.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Classification failed:', error);
            alert(`Classification failed: ${error.message}`);
        }
    }


    // --- Event Listeners ---
    queryForm.addEventListener('submit', classifyQuery);

    // --- Initial Load ---
    loadDashboardData();

});