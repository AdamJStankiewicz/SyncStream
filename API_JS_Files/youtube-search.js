// Load the YouTube API client
function loadClient() {
    gapi.client.setApiKey("AIzaSyApjUYQS3sh6wITTjYZuACIa7or7T9Vdok"); // API key
    return gapi.client.load("https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest") // Load the YouTube API client library
        .then(() => console.log("GAPI client loaded for API"), // Log success when the client loads
              err => console.error("Error loading GAPI client for API", err)); // Log error if the client fails to load
}

// Execute the YouTube API search
function executeSearch() {
    const query = document.getElementById('search-query').value; // Get the user's search term from the input field

    if (!query) {
        alert("Please enter a search term."); // Alert the user if the search term is empty
        return; // Stop execution if no search term is provided
    }

    gapi.client.youtube.search.list({
        "part": "snippet", // Specify the part of the resource to retrieve (e.g., title, description)
        "maxResults": 3, // Limit the number of search results to 3
        "type": "video", // Restrict the search to video type only
    // NEXT LINE IS VERY IMPORTANT, SOME VIDEOS CANNOT BE EMBEDDED 
        "videoEmbeddable": "true", // Ensure only embeddable videos are returned
        "order": "viewCount" // Sort results by the number of views
    }).then(response => {
        console.log("Search Results:", response); // Log the response from the API

        // Get the search results placeholder in the test container
        const searchResults = document.getElementById('search-results'); // Get the container for displaying search results
        searchResults.innerHTML = ''; // Clear previous results

        const videos = response.result.items; // Get the array of video results

        if (videos && videos.length > 0) { // Check if there are any videos in the response
            videos.forEach(video => { // Loop through each video
                const videoId = video.id.videoId; // Extract the video ID
                const title = video.snippet.title; // Extract the video title
                const thumbnailUrl = video.snippet.thumbnails.default.url; // Extract the video thumbnail URL
                const videoUrl = `https://www.youtube.com/watch?v=${videoId}`; // Construct the full video URL

                // Create a container for the video
                const videoItem = document.createElement('div'); // Create a div element to hold the video information
                videoItem.style.marginBottom = '15px'; // Add spacing below each video
                videoItem.style.display = 'flex'; // Use flex display for layout
                videoItem.style.flexDirection = 'column'; // Arrange elements in a column

                // Create the thumbnail
                const thumbnail = document.createElement('img'); // Create an img element for the thumbnail
                thumbnail.src = thumbnailUrl; // Set the thumbnail image source
                thumbnail.alt = title; // Set the alt text for accessibility
                thumbnail.style.width = '120px'; // Set the thumbnail width
                thumbnail.style.height = '90px'; // Set the thumbnail height
                thumbnail.style.marginBottom = '5px'; // Add spacing below the thumbnail

                // Create the clickable URL
                const videoLink = document.createElement('a'); // Create an anchor element for the video URL
                videoLink.href = "#"; // Prevent default navigation behavior
                videoLink.textContent = videoUrl; // Set the text content to the video URL
                videoLink.style.color = 'white'; // Style the link color
                videoLink.style.cursor = 'pointer'; // Change the cursor to pointer when hovering

                // Add click event to populate the URL submit bar
                videoLink.addEventListener('click', (event) => {
                    event.preventDefault(); // Prevent navigation when clicking the link
                    const youtubeUrlInput = document.getElementById('youtube-url'); // Get the YouTube URL input field
                    youtubeUrlInput.value = videoUrl; // Populate the URL into the submit bar
                    searchResults.innerHTML = ''; // Clear previous results after clicking
                });

                // Append thumbnail and URL to the video item
                videoItem.appendChild(thumbnail); // Add the thumbnail to the video container
                videoItem.appendChild(videoLink); // Add the clickable URL to the video container

                // Append the video item to the search results
                searchResults.appendChild(videoItem); // Add the video container to the results section
            });
        } else {
            searchResults.textContent = "No results found."; // Display a message if no videos are found
        }
    }).catch(err => {
        console.error("Error executing search:", err); // Log any errors that occur during the API call
    });
}

// Attach search functionality to the button
document.getElementById('search-button').addEventListener('click', executeSearch); // Add a click event listener to the search button

// Initialize the GAPI client on page load
gapi.load("client", loadClient); // Load the GAPI client library when the page loads
