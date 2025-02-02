const video = document.getElementById('video');
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
document.body.appendChild(canvas);

// Mediapipe Pose initialization
async function initializePose() {
    return new Promise((resolve, reject) => {
        const pose = new Pose({
            locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
        });

        pose.setOptions({
            modelComplexity: 1,
            smoothLandmarks: true,
            enableSegmentation: false,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        pose.onResults((results) => {
            if (!results.poseLandmarks) {
                console.warn("⚠️ No Pose Detected.");
                return;
            }

            // Clear the canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Ensure the canvas size matches the video
            canvas.width = video.videoWidth || 640;
            canvas.height = video.videoHeight || 480;

            // Draw pose landmarks
            drawConnectors(ctx, results.poseLandmarks, POSE_CONNECTIONS, { color: 'blue', lineWidth: 4 });
            drawLandmarks(ctx, results.poseLandmarks, { color: 'red', radius: 5 });

            // Get the landmarks
            const lmList = results.poseLandmarks;

            // Check if landmarks are detected
            if (lmList.length > 0) {
                // Draw lines specifically between points 12, 14, 16 (Shoulder, Elbow, Wrist)
                const x1 = lmList[12].x * canvas.width;
                const y1 = lmList[12].y * canvas.height;
                const x2 = lmList[14].x * canvas.width;
                const y2 = lmList[14].y * canvas.height;
                const x3 = lmList[16].x * canvas.width;
                const y3 = lmList[16].y * canvas.height;

                // Draw the lines between shoulder (12), elbow (14), and wrist (16)
                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.lineTo(x3, y3);
                ctx.lineWidth = 4;
                ctx.strokeStyle = 'blue';  // Line color
                ctx.stroke();

                // Detect angle for curls
                const angle = findAngle(lmList, 12, 14, 16); // Shoulder (12), Elbow (14), Wrist (16)
                detectCurls(angle); // Detect curls based on the angle
            }
        });

        resolve(pose);
    });
}

// Calculate angle between three points (p1, p2, p3)
function findAngle(lmList, p1, p2, p3) {
    const x1 = lmList[p1].x * canvas.width;
    const y1 = lmList[p1].y * canvas.height;
    const x2 = lmList[p2].x * canvas.width;
    const y2 = lmList[p2].y * canvas.height;
    const x3 = lmList[p3].x * canvas.width;
    const y3 = lmList[p3].y * canvas.height;

    // Calculate angle using the atan2 function
    let angle = Math.atan2(y3 - y2, x3 - x2) - Math.atan2(y1 - y2, x1 - x2);
    angle = Math.abs(angle * 180 / Math.PI); // Convert radians to degrees
    if (angle > 180) {
        angle = 360 - angle; // Ensure angle is within 0-180 degrees
    }

    return angle;
}

// Curls logic
let curlsCount = 0;
let direction = 0;  // 0 = waiting, 1 = going down, 2 = going up

function detectCurls(angle) {
    // Check for downward movement (full extension of the arm)
    if (angle > 160) {
        if (direction === 2) {  // Was moving up before
            curlsCount++;  // Count curl only when full motion is completed
            direction = 0;  // Reset to waiting state
        }
        direction = 1;  // Now moving down
    }
    // Check for upward movement (bent arm)
    else if (angle < 70) {
        direction = 2;  // Now moving up
    }

    // Display the curl count and angle on the screen in black color
    ctx.font = '30px Arial';
    ctx.fillStyle = 'black';  // Change text color to black
    ctx.fillText(`Curls: ${curlsCount}`, 30, 50);
    ctx.fillText(`Angle: ${Math.round(angle)}°`, 30, 90);
}

// Main function to start pose detection
async function main() {
    try {
        const poseDetector = await initializePose();
        console.log("✅ Pose Model Initialized!");

        if (!video) {
            console.error("❌ Video element not found!");
            return;
        }

        video.src = "video2.mp4"; // Replace with actual video path
        video.load();
        video.play();

        video.onloadedmetadata = () => {
            console.log("✅ Video Metadata Loaded!");

            // Adjust the canvas size according to the video size
            canvas.width = video.videoWidth || 640;
            canvas.height = video.videoHeight || 480;

            function processFrame() {
                if (!video.paused && !video.ended) {
                    poseDetector.send({ image: video }).then(() => {
                        requestAnimationFrame(processFrame);
                    });
                }
            }

            requestAnimationFrame(processFrame);

            // setTimeout(() => {
            //     console.log("⏹ Stopping Video after 10 seconds.");
            //     video.pause();
            // }, 10000);
        };
    } catch (error) {
        console.error('❌ Pose detection error:', error);
    }
}

// Start the process
main();