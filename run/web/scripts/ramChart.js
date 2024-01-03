
const ramDataPoints = [];
const ramChart = new CanvasJS.Chart("ramChart", {
    title: {
        text: " "
    },
    axisX: {
        title: "",
        valueFormatString: " "
    },
    axisY: {
        title: "RAM Usage (%)",
        valueFormatString: "0.0%",
        minimum: 0,
        maximum: 1
    },
    data: [{
        type: "line",
        dataPoints: ramDataPoints
    }]
});

function updateRam() {
    fetch('/api/ram')
        .then(response => response.json())
        .then(data => {
            const now = new Date();
            ramDataPoints.push({ x: now, y: (data.ram / 100 ) });
            if (ramDataPoints.length > 10) {
                ramDataPoints.shift();
            }
            ramChart.render();
        })
        .catch(error => console.error('Error fetching data:', error));
}

setInterval(updateRam, 1000);