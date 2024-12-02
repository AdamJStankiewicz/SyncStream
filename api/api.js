var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
var userId = '9dd02531-af61-11ef-8b66-086ac515207e';
var isHost = true;
var timerInterval;
var isTimerRunning = false;
var lobbyCode = '123';

/*
const userSession = JSON.parse(localStorage.getItem('userSession'));
if (userSession) {
  userId = userSession.userID;
  console.log("Current User ID from localStorage:", userId);
} else {
  console.error("No user session found in localStorage");
}

const lobbyCode = localStorage.getItem('lobbyCode');
if (lobbyCode) {
  console.log("Lobby Code from LocalStorage:", lobbyCode);
}
*/

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

// Youtube API Miniplayer
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: 'M7lc1UVf-VE',
    playerVars: {
      'playsinline': 1
    },
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

// Calls startTimer when the video gets played
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
