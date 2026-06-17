document.addEventListener('DOMContentLoaded', function() {
    const sensorA = document.getElementById('sensorA');
    const sensorB = document.getElementById('sensorB');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const validationMsg = document.getElementById('validationMsg');
    const form = document.getElementById('crossCorrelationForm');
    
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');
    const errorMsg = document.getElementById('errorMsg');
    const resultsSection = document.getElementById('resultsSection');
    const warningState = document.getElementById('warningState');
    const warningMsg = document.getElementById('warningMsg');
    const generateVisBtn = document.getElementById('generateVisBtn');
    
    let graphGenerated = false;
    
    function updateGenerateVisButton() {
        if (graphGenerated) {
            generateVisBtn.disabled = false;
            generateVisBtn.title = "";
            generateVisBtn.className = "btn btn-outline-primary flex-grow-1";
            generateVisBtn.style.cssText = "background-color: transparent; border: 1px solid var(--sel-primary-main, #1A365D); color: var(--sel-primary-main, #1A365D); transition: all 0.2s;";
            generateVisBtn.setAttribute('onmouseover', "this.style.backgroundColor='var(--sel-primary-main, #1A365D)'; this.style.color='white';");
            generateVisBtn.setAttribute('onmouseout', "this.style.backgroundColor='transparent'; this.style.color='var(--sel-primary-main, #1A365D)';");
            generateVisBtn.setAttribute('onclick', "window.location.href=homeUrl");
        } else {
            generateVisBtn.disabled = true;
            generateVisBtn.title = "Please generate and view the cross-correlation graph before creating a visualization.";
            generateVisBtn.className = "btn btn-secondary flex-grow-1";
            generateVisBtn.style.cssText = "opacity: 0.5; cursor: not-allowed; pointer-events: none;";
            generateVisBtn.removeAttribute('onmouseover');
            generateVisBtn.removeAttribute('onmouseout');
            generateVisBtn.removeAttribute('onclick');
        }
    }
    
    const metricValue = document.getElementById('metricValue');
    const metricInterpretation = document.getElementById('metricInterpretation');
    const graphTitle = document.getElementById('graphTitle');

    // Validation logic
    function validateSelection() {
        if (!sensorA || !sensorB || !analyzeBtn) return;
        
        const valA = sensorA.value;
        const valB = sensorB.value;
        
        if (valA && valB) {
            if (valA === valB) {
                validationMsg.style.display = 'block';
                analyzeBtn.disabled = true;
            } else {
                validationMsg.style.display = 'none';
                analyzeBtn.disabled = false;
            }
        } else {
            validationMsg.style.display = 'none';
            analyzeBtn.disabled = true;
        }
    }

    if (sensorA) sensorA.addEventListener('change', validateSelection);
    if (sensorB) sensorB.addEventListener('change', validateSelection);

    // Form submission
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Reset state
            graphGenerated = false;
            updateGenerateVisButton();
            
            const valA = sensorA.value;
            const valB = sensorB.value;
            
            const nameA = sensorA.options[sensorA.selectedIndex].text.split('(')[0].trim();
            const nameB = sensorB.options[sensorB.selectedIndex].text.split('(')[0].trim();
            
            // Show loading
            resultsSection.style.display = 'none';
            errorState.style.display = 'none';
            loadingState.style.display = 'block';
            analyzeBtn.disabled = true;
            
            // Perform AJAX request
            fetch(analyzeUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    sensor_a: valA,
                    sensor_b: valB
                })
            })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(result => {
                loadingState.style.display = 'none';
                analyzeBtn.disabled = false;
                
                if (result.status !== 200 || result.body.error) {
                    errorMsg.textContent = result.body.error || 'An unexpected error occurred.';
                    errorState.style.display = 'block';
                    return;
                }
                
                // Success, render chart and metrics
                renderResults(result.body, nameA, nameB);
            })
            .catch(error => {
                console.error("Error during analysis:", error);
                loadingState.style.display = 'none';
                analyzeBtn.disabled = false;
                errorMsg.textContent = 'Failed to connect to the server.';
                errorState.style.display = 'block';
            });
        });
    }

    function renderResults(data, nameA, nameB) {
        resultsSection.style.display = 'block';
        
        // Show Warning if applicable
        if (data.correlation_warning) {
            warningMsg.textContent = data.correlation_warning;
            warningState.style.display = 'block';
        } else {
            warningState.style.display = 'none';
        }
        
        // Update Metrics
        metricInterpretation.textContent = data.interpretation;
        
        if (data.correlation === null || isNaN(parseFloat(data.correlation))) {
            metricValue.textContent = 'N/A';
            metricValue.style.color = '#6c757d';
            metricInterpretation.style.backgroundColor = 'rgba(108, 117, 125, 0.1)';
            metricInterpretation.style.color = '#6c757d';
        } else {
            const corr = parseFloat(data.correlation);
            metricValue.textContent = corr.toFixed(3);
            
            // Color coding for metrics
            if (Math.abs(corr) >= 0.8) {
                metricValue.style.color = '#2E8B57'; // Strong - Green
                metricInterpretation.style.backgroundColor = 'rgba(46, 139, 87, 0.1)';
                metricInterpretation.style.color = '#2E8B57';
            } else if (Math.abs(corr) >= 0.5) {
                metricValue.style.color = '#FF8C00'; // Moderate - Orange
                metricInterpretation.style.backgroundColor = 'rgba(255, 140, 0, 0.1)';
                metricInterpretation.style.color = '#FF8C00';
            } else if (Math.abs(corr) >= 0.2) {
                metricValue.style.color = '#6c757d'; // Weak - Gray
                metricInterpretation.style.backgroundColor = 'rgba(108, 117, 125, 0.1)';
                metricInterpretation.style.color = '#6c757d';
            } else {
                metricValue.style.color = '#dc3545'; // No sig - Red
                metricInterpretation.style.backgroundColor = 'rgba(220, 53, 69, 0.1)';
                metricInterpretation.style.color = '#dc3545';
            }
        }
        
        graphTitle.textContent = `Cross-Correlation: ${nameA} vs ${nameB}`;

        // Prepare Plotly Traces
        const traceA = {
            x: data.times,
            y: data.values_a,
            mode: 'lines',
            name: nameA,
            line: {color: '#1f77b4', width: 2, shape: 'spline'},
            yaxis: 'y1',
            hovertemplate: '<b>%{x}</b><br>' + nameA + ': %{y:.2f}<extra></extra>'
        };
        
        const traceB = {
            x: data.times,
            y: data.values_b,
            mode: 'lines',
            name: nameB,
            line: {color: '#ff7f0e', width: 2, shape: 'spline'},
            yaxis: 'y2',
            hovertemplate: '<b>%{x}</b><br>' + nameB + ': %{y:.2f}<extra></extra>'
        };
        
        const layout = {
            title: '',
            margin: {l: 60, r: 60, t: 30, b: 60},
            xaxis: {
                title: '<b>Time</b>',
                gridcolor: '#f0f0f0',
                tickangle: -45
            },
            yaxis: {
                title: `<b>${nameA}</b>`,
                titlefont: {color: '#1f77b4'},
                tickfont: {color: '#1f77b4'},
                gridcolor: '#f0f0f0'
            },
            yaxis2: {
                title: `<b>${nameB}</b>`,
                titlefont: {color: '#ff7f0e'},
                tickfont: {color: '#ff7f0e'},
                overlaying: 'y',
                side: 'right',
                gridcolor: 'transparent'
            },
            showlegend: true,
            legend: {x: 0.5, y: 1.15, xanchor: 'center', orientation: 'h'},
            plot_bgcolor: 'white',
            paper_bgcolor: 'white',
            hovermode: 'x unified'
        };
        
        const config = {responsive: true, displayModeBar: false};
        Plotly.newPlot('ccChart', [traceA, traceB], layout, config);
        
        // Immediately enable the Generate Visualization button since graph data is present and rendering
        graphGenerated = true;
        updateGenerateVisButton();
        
        // Scroll to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }
});
