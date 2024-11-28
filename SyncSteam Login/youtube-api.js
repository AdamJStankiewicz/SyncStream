// Configuration: API Key and Video ID
const youtubeConfig = {
    apiKey: "AIzaSyApjUYQS3sh6wITTjYZuACIa7or7T9Vdok", // Your YouTube API key for making API calls
    videoId: null // This will hold the parsed video ID from the URL
};

// Function to extract video ID from a YouTube URL
function extractVideoId(url) {
    const urlPattern = /(?:https?:\/\/)?(?:www\.)?youtube\.com\/.*[?&]v=([^&\s]*)|youtu\.be\/([^?&\s]*)/; // Regex to match YouTube URLs and extract video IDs
    const match = url.match(urlPattern); // Check if the URL matches the regex pattern
    return match ? match[1] || match[2] : null; // Return the first matching group (standard URL) or second group (shortened URL), or null if no match
}

// Event listener for Submit URL button
document.getElementById('submit-url').addEventListener('click', () => {
    const urlInput = document.getElementById('youtube-url').value; // Get the value from the Paste YouTube URL input field
    const videoId = extractVideoId(urlInput); // Extract the video ID from the provided URL

    if (videoId) { // Check if a valid video ID was extracted
        // Updates the video ID in the config
        youtubeConfig.videoId = videoId; // Save the extracted video ID in the config object

        // Displays the updated video ID
        document.getElementById('video-id-display').textContent = `Video ID: ${videoId}`; // Update the Video ID display element with the extracted ID

        // Embed the video player
        embedVideoPlayer(videoId); // Call the function to embed the video player using the extracted ID
    } else {
        alert("Invalid YouTube URL. Please enter a valid URL."); // Alert the user if the URL is invalid
    }
});

// Function to embed the YouTube video player
function embedVideoPlayer(videoId) {
    const playerContainer = document.getElementById('video-player-container'); // Get the container for the embedded video player
    playerContainer.innerHTML = ` 
        <iframe
            width="300" 
            height="315" 
            src="https://www.youtube.com/embed/${videoId}?autoplay=1" 
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen> 
        </iframe>
    `;
}
