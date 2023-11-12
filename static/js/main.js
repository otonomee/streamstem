document.addEventListener("DOMContentLoaded", () => {
  let submitBtn = document.querySelector("#submitBtn");
  let songTitle = document.querySelector("#songTitle");

  let filetype = document.querySelector("#fileType").value.split("-")[1];
  let numStems;

  let loadingGif = document.querySelector("#loadingGif");
  console.log(loadingGif);

  submitBtn.addEventListener("click", (e) => {
    loadingGif.setAttribute("style", "display:flex;flex-direction:row");
    resetUi();

    let elInputs = document.querySelectorAll("input");
    elInputs.forEach(function (el) {
      if (el.hasAttribute("checked")) {
        numStems = el.nextElementSibling.innerText[0];
      }
    });

    e.preventDefault();
    let url = document.querySelector("#url").value;

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

          console.log("filetype", filetype);
          console.log("filename", filename);
          console.log("num stems", numStems);

          updateUi(filename);
          fetch("/process_audio", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              filename: filename,
              filetype: filetype,
              numStems: numStems,
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
      });
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
