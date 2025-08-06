function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("predictionResult").innerHTML = "Error: " + data.error;
        } else {
            document.getElementById("predictionResult").innerHTML = "Predicted Temperature: " + data.predicted_temperature + "°C";
        }
    })
    .catch(error => {
        document.getElementById("predictionResult").innerHTML = "Error processing request.";
    });
}
// Load Vanta.js Clouds Background
VANTA.CLOUDS({
    el: "body",
    skyColor: 0x87ceeb, // Sky blue
    cloudColor: 0xffffff, // White clouds
    cloudShadowColor: 0xb0c4de, // Light steel blue
    sunColor: 0xffd700, // Golden sun
    sunlightIntensity: 0.6, // Slightly stronger sunlight
    speed: 0.3, // Slower clouds for realism
    scale: 1.1, // Moderate cloud density
    backgroundAlpha: 0 // Make the sky blend better
});

// Create and Animate the Sun
const sun = document.createElement("div");
sun.style.position = "absolute";
sun.style.top = "10%";
sun.style.left = "10%";
sun.style.width = "80px";
sun.style.height = "80px";
sun.style.borderRadius = "50%";
sun.style.background = "radial-gradient(circle, #FFD700, #FFA500)";
document.body.appendChild(sun);

let sunAngle = 0;
function animateSun() {
    sunAngle += 0.005;
    sun.style.transform = `translateY(${Math.sin(sunAngle) * 10}px)`;
    requestAnimationFrame(animateSun);
}
animateSun();

// Create and Animate Floating Clouds
function createCloud(leftPosition, animationDuration) {
    const cloud = document.createElement("div");
    cloud.style.position = "absolute";
    cloud.style.top = "20%";
    cloud.style.left = leftPosition;
    cloud.style.width = "200px";
    cloud.style.height = "100px";
    cloud.style.background = "rgba(255, 255, 255, 0.8)";
    cloud.style.borderRadius = "100px";
    cloud.style.boxShadow = "10px 10px 30px rgba(0, 0, 0, 0.1)";
    document.body.appendChild(cloud);

    let cloudDirection = 1;
    function animateCloud() {
        cloud.style.left = `${parseInt(cloud.style.left) + cloudDirection}px`;
        if (parseInt(cloud.style.left) > window.innerWidth - 200 || parseInt(cloud.style.left) < 0) {
            cloudDirection *= -1;
        }
        setTimeout(animateCloud, animationDuration);
    }
    animateCloud();
}

createCloud("30%", 50);
createCloud("60%", 60);
createCloud("80%", 70);

// Create a Soft Ground Effect
const ground = document.createElement("div");
ground.style.position = "absolute";
ground.style.bottom = "0";
ground.style.width = "100%";
ground.style.height = "150px";
ground.style.background = "linear-gradient(to top, #6B8E23, transparent)";
document.body.appendChild(ground);
