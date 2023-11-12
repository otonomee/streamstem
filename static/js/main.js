document.addEventListener("DOMContentLoaded", () => {
  let submitBtn = document.querySelector("#submitBtn");
  let songTitle = document.querySelector("#songTitle");

  let filetype = document.querySelector("#fileType");
  let numStems = document.querySelector("#numberOfStems");

  let loadingGif = document.querySelector("#loadingGif");

  submitBtn.addEventListener("click", (e) => {
    e.preventDefault();
    let url = document.querySelector("#url").value;
    resetUi();

    loadingGif.style.display = "block";

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
            body: JSON.stringify({
              filename: filename,
              filetype: filetype.value,
              numStems: numStems.value[0],
            }),
          })
            .then((response) => response.json())
            .then((data) => {
              console.log(data.message); // Should print 'Processing started'
              // Initiate file download after processing

              updateUi("Video title:", data.filename.replace(/\.[^/.]+$/, ""));
              if (data.message == "Finished") {
                loadingGif.style.display = "none";
                window.location =
                  "/download?filename=STEMS-" +
                  encodeURIComponent(data.filename.replace(/\.[^/.]+$/, ""));
              }
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
});
