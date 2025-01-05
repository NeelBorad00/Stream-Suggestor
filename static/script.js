document.addEventListener('DOMContentLoaded', function() {
    let currentStep = 1;
    const form = document.getElementById('careerForm');
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const downloadBtn = document.getElementById('downloadPDF');

    // Chart configuration
    // Update the chart configuration colors
const chartConfig = {
    plugins: {
        legend: {
            labels: {
                color: '#EEEEEE'  // text-primary
            }
        }
    },
    scales: {
        r: {
            grid: {
                color: '#31363F'  // bg-secondary
            },
            pointLabels: {
                color: '#EEEEEE'  // text-primary
            }
        },
        x: {
            grid: {
                color: '#31363F'  // bg-secondary
            },
            ticks: {
                color: '#EEEEEE'  // text-primary
            }
        },
        y: {
            grid: {
                color: '#31363F'  // bg-secondary
            },
            ticks: {
                color: '#EEEEEE'  // text-primary
            }
        }
    }
};

// Update chart colors in createCharts function
function createCharts(data) {
    // ... existing code ...
    datasets: [{
        label: 'Career Progress',
        data: [0, 25, 50, 75, 100],
        borderColor: '#76ABAE',  // accent-primary
        backgroundColor: 'rgba(118, 171, 174, 0.2)',  // accent-primary with opacity
        tension: 0.4
    }]
}

    function updateProgressBar(step) {
        const steps = document.querySelectorAll('.step');
        steps.forEach((stepElement, index) => {
            if (index + 1 < step) {
                stepElement.classList.add('completed');
                stepElement.classList.remove('active');
            } else if (index + 1 === step) {
                stepElement.classList.add('active');
                stepElement.classList.remove('completed');
            } else {
                stepElement.classList.remove('active', 'completed');
            }
        });
    }

    function showStep(step) {
        document.querySelectorAll('.step-content').forEach(el => el.classList.add('hidden'));
        document.getElementById(`step${step}`).classList.remove('hidden');
        
        prevBtn.classList.toggle('hidden', step === 1);
        nextBtn.textContent = step === 2 ? 'Analyze' : 'Next';
        
        updateProgressBar(step);
    }


    nextBtn.addEventListener('click', async () => {
        if (currentStep === 2) {
            // Simulate API call
            setTimeout(() => {
                displayResults({
                    professions: [
                        {
                            name: 'Software Developer',
                            requiredSkills: ['JavaScript', 'Python', 'Problem Solving'],
                            careerPath: ['Junior Developer', 'Senior Developer', 'Tech Lead'],
                            salaryRange: '$60,000 - $150,000',
                            marketStats: 'High demand, growing industry'
                        }
                    ]
                });
                currentStep++;
                showStep(currentStep);
                createCharts();
            }, 1000);
        } else if (currentStep < 3) {
            currentStep++;
            showStep(currentStep);
        }
    });

    prevBtn.addEventListener('click', () => {
        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    });

    downloadBtn.addEventListener('click', () => {
        const element = document.getElementById('results');
        html2pdf().from(element).save('career-recommendations.pdf');
    });

    function displayResults(data) {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = data.professions.map(profession => `
            <div class="result-card">
                <h3 class="text-xl font-bold mb-2">${profession.name}</h3>
                <p><strong>Required Skills:</strong> ${profession.requiredSkills.join(', ')}</p>
                <p><strong>Career Path:</strong> ${profession.careerPath.join(' → ')}</p>
                <p><strong>Salary Range:</strong> ${profession.salaryRange}</p>
                <p><strong>Market Statistics:</strong> ${profession.marketStats}</p>
            </div>
        `).join('');
    }
});