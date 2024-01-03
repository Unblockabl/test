function updateUptime() {
    fetch('/api/uptime')
        .then(response => response.json())
        .then(data => {
            const uptimeTimestamp = data.uptime;
            const now = new Date();
            const uptimeDate = new Date(uptimeTimestamp * 1000); // Convert seconds to milliseconds

            const uptimeDifference = now - uptimeDate;
            const days = Math.floor(uptimeDifference / (1000 * 60 * 60 * 24));
            const hours = Math.floor((uptimeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((uptimeDifference % (1000 * 60 * 60)) / (1000 * 60));

            const formattedUptime = `${days} days, ${hours} hours, ${minutes} minutes`;

            document.getElementById("uptimeChart").innerHTML = formattedUptime;
       })
        .catch(error => console.error('Error fetching data:', error));
}

setInterval(updateUptime, 10000);
