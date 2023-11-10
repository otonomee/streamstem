// document.getElementById('myForm').addEventListener('submit', function(e) {
//     e.preventDefault();

//     var youtube_url = document.getElementById('url').value;
//     // document.querySelector('h3').innerHTML = youtube_url;

//     fetch('/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             url: youtube_url
//         })
//     })
//     .then(response => response.text())
//     .then(data => {
//         // Handle the response from the server here
//     });
// });
let submitBtn = document.querySelector("#submitBtn");

submitBtn.addEventListener("click", (e) => {
  e.preventDefault();
  console.log("button clicked");

  const source = new EventSource("/process_audio");
  source.onmessage = function (event) {
    console.log(event.data);
  };

  fetch("/process_audio", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      audio_filename: "video-name.mp3",
    }),
  });
});

// Start processing the audio file
// fetch('/process_audio', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ audio_filename: 'video-name' })
// })
// .then(response => response.json())
// .then(data => {
//     console.log(data.message);  // Should print 'Processing started'

//     // Poll the server at regular intervals to check if processing is complete
//     const intervalId = setInterval(() => {
//         fetch('/check_process')
//             .then(response => response.json())
//             .then(data => {
//                 if (data.status === 'finished') {
//                     clearInterval(intervalId);
//                     window.location.href = '/download';
//                 }
//             })
//             .catch(error => console.error('Error:', error));
//     }, 5000);  // Check every 5 seconds
// })
// .catch(error => console.error('Error:', error));
// })
