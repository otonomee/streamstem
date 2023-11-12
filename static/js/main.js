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

document.addEventListener("DOMContentLoaded", () => {
  let submitBtn = document.querySelector("#submitBtn");
  let songTitle = document.querySelector("#songTitle");
  submitBtn.addEventListener("click", (e) => {
    e.preventDefault();
    let url = document.querySelector("#url").value;
    resetUi();

    console.log("button clicked");
    console.log(url);
    fetch("/download_video", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: url,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status == "success") {
          console.log(data);
          let filename = data.filename;
          updateUi(filename);
          fetch("/process_audio", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ filename: filename }),
          })
            .then((response) => response.json())
            .then((data) => {
              console.log(data.message); // Should print 'Processing started'
              // Initiate file download after processing

              updateUi("Video title:", data.filename.replace(".mp3", ""));
              if (data.message == "Finished") {
                window.location =
                  "/download?filename=STEMS: " +
                  encodeURIComponent(data.filename.replace(".mp3", ""));
              }

              // fetch("/download", {
              //   method: "POST",
              //   headers: { "Content-Type": "application/json" },
              //   body: JSON.stringify({ filename: data.filename }),
              // })
              //   .then((response) => response.blob())
              //   .then((blob) => {
              //     // Create a new object URL for the blob
              //     const url = window.URL.createObjectURL(blob);

              //     // Create a link and programmatically click it to initiate download
              //     const link = document.createElement("a");
              //     link.href = url;
              //     link.download = `${data.filename}.zip`;
              //     link.click();

              //     // // Release the reference to the object URL after the download starts
              //     // setTimeout(() => window.URL.revokeObjectURL(url), 100);
              //   });
            })
            .catch((error) => console.error("Error:", error));
        }
      })
      .catch((error) => console.error("Error:", error));
  });

  function updateUi(filename) {
    songTitle.innerHTML = filename;
    songTitle.style.display = "block";
  }

  function resetUi() {
    songTitle.innerHTML = "";
    songTitle.style.display = "none";
  }
  //     .then((response) => response.json())
  //     .then((data) => {
  //       console.log(data.message); // Should print 'Processing started'
  //       // Initiate file download after processing
  //       fetch("/download")
  //         .then((response) => response.blob())
  //         .then((blob) => {
  //           // Create a new object URL for the blob
  //           const url = window.URL.createObjectURL(blob);

  //           // Create a link and programmatically click it to initiate download
  //           const link = document.createElement("a");
  //           link.href = url;
  //           link.download = "separated.zip";
  //           link.click();

  //           // Release the reference to the object URL after the download starts
  //           setTimeout(() => window.URL.revokeObjectURL(url), 100);
  //         });
  //     })
  //     .catch((error) => console.error("Error:", error));
  // });
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
});
