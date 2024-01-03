
const cpuDataPoints = [];
const cpuChart = new CanvasJS.Chart("cpuChart", {
    title: {
        text: " "
    },
    axisX: {
        title: "",
        valueFormatString: " "
    },
    axisY: {
        title: "CPU Usage (%)",
        valueFormatString: "0.0%",
        minimum: 0,
        maximum: 1
    },
    data: [{
        type: "line",
        dataPoints: cpuDataPoints
    }]
});

function updateCpu() {
    fetch('/api/cpu')
        .then(response => response.json())
        .then(data => {
            const now = new Date();
            cpuDataPoints.push({ x: now, y: (data.cpu / 100 ) });
            if (cpuDataPoints.length > 10) {
                cpuDataPoints.shift();
            }
            cpuChart.render();
        })
        .catch(error => console.error('Error fetching data:', error));
}

setInterval(updateCpu, 1000);