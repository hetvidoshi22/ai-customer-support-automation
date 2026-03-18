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
            console.log("Fetching dashboard data...");
            const response = await fetch(`${API_BASE_URL}/dashboard`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log("Dashboard data received:", data);

            if(data.success) {
                // Update summary stats
                totalQueriesEl.textContent = data.summary.total_queries;
                uniqueCategoriesEl.textContent = data.summary.unique_categories;
                // Format the date range nicely
                const startDate = new Date(data.summary.date_range.start).toLocaleDateString();
                const endDate = new Date(data.summary.date_range.end).toLocaleDateString();
                dataPeriodEl.textContent = `${startDate} to ${endDate}`;

                // Prepare data for Chart.js
                const categories = data.distribution.map(item => item.category);
                const counts = data.distribution.map(item => item.count);
                const percentages = data => item.percentage);

                // Destroy existing chart if it exists to prevent duplication
                if (distributionChart) {
                    distributionChart.destroy();
                }

                // Create the chart
                distributionChart = new Chart(distributionChartCtx, {
                    type: 'bar', // You can change this to 'pie' or 'doughnut'
                    data: {
                        labels: categories,
                        datasets: [{
                            label: 'Number of Queries',
                            data: counts,
                            backgroundColor: [
                                'rgba(52, 152, 219, 0.7)', // Blue
                                'rgba(231, 76, 60, 0.7)',  // Red
                                'rgba(46, 204, 113, 0.7)', // Green
                                'rgba(155, 89, 182, 0.7)', // Purple
                                'rgba(241, 196, 15, 0.7)', // Yellow
                                'rgba(230, 126, 34, 0.7)', // Orange
                                'rgba(149, 165, 166, 0.7)', // Grey
                                'rgba(127, 140, 141, 0.7)'  // Dark Grey
                            ],
                            borderColor: [
                                'rgba(52, 152, 219, 1)',
                                'rgba(231, 76, 60, 1)',
                                'rgba(46, 204, 113, 1)',
                                'rgba(155, 89, 182, 1)',
                                'rgba(241, 196, 15, 1)',
                                'rgba(230, 126, 34, 1)',
                                'rgba(149, 165, 166, 1)',
                                'rgba(127, 140, 141, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'top',
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        const dataset = context.dataset;
                                        const index = context.dataIndex;
                                        const percentage = percentages[index];
                                        return `${dataset.label}: ${dataset.data[index]} (${percentage}%)`;
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Number of Queries'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Category'
                                }
                            }
                        }
                    }
                });
            } else {
                alert(`Error loading dashboard: ${data.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            alert(`Failed to load dashboard data: ${error.message}`);
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