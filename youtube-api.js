
var userId = '9dd02531-af61-11ef-8b66-086ac515207e';
var isHost = true;
var timerInterval;
var isTimerRunning = false;
var lobbyCode = '123';

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


fetch(`http://127.0.0.1:1477/lobby/${lobbyCode}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  })
    .then(response => response.json())
    .then(data => {
      console.log("Lobby state:", data);
      const currentUser = data.participants.find(participant => participant.userId === userId);
      
      if (currentUser) {
        isHost = currentUser.isHost || false;
        console.log('User ID:', userId);
        console.log('Is Host:', isHost);
      } else {
        console.error("User not found in lobby participants");
      }
    })
    .catch(error => {
      console.error("Error fetching lobby state:", error);
    });
  

function onPlayerReady(event) {
    event.target.playVideo();
    startTimer();
  }
  
  // Listens for changes in the player's state
  function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
      if (!isTimerRunning) {
        startTimer();
      }
    } else if (event.data == YT.PlayerState.PAUSED) {
      stopTimer();
    }
  }
  
  // Calls sendHostTime every 5 seconds
  function startTimer() {
    isTimerRunning = true;
    timerInterval = setInterval(sendHostTime, 5000);
  }
  
  // Stops the timer
  function stopTimer() {
    isTimerRunning = false;
    clearInterval(timerInterval);
  }
  
  /*
  If the user is the host, it sends their time to the server.
  Else the user gets the hosts time from the server. 
  It checks if the users current timestamp in the video is greater than 3 seconds.
  If the time difference is greater than 3 seconds, it syncs the video with the hosts time.
  */
  function sendHostTime() {
    if (isHost) {
      var hostTime = player.getCurrentTime();
      console.log(hostTime);
      fetch(`http://127.0.0.1:1477/lobby/${lobbyCode}/get_host_time`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: userId,
          hostTime: hostTime
        })
      })
        .then(response => response.json())
        .then(data => {
          console.log("Host time updated:", data);
        })
        .catch(error => {
          console.error('Error sending host time:', error);
        });
    } 
    else {
      fetch(`http://127.0.0.1:1477/lobby/${lobbyCode}/send_host_time`, {
        method: 'POST'
      })
        .then(response => response.json())
        .then(data => {
          console.log("Received host time:", data);
          const hostTime = data.hostTime;
  
          var currentUserTime = player.getCurrentTime();
          var timeDifference = Math.abs(currentUserTime - hostTime);
  
          if (timeDifference > 3) { 
            console.log("Syncing player time to host time.");
            player.seekTo(hostTime, true);
          }
        })
        .catch(error => {
          console.error('Error receiving host time:', error);
        });
    }
  }
  