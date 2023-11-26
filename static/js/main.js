document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.querySelector("#submitBtn");
  const songTitle = document.querySelector("#songTitle");
  const loadingGif = document.querySelector("#loadingGif");
  const urlInput = document.querySelector(".my-form-control");
  const statusMsgCotainer = document.querySelector(".status-message-container");

  // JavaScript
  submitBtn.addEventListener("mouseover", function () {
    document.querySelector(".hoverLine").style.width = "55%";
  });

  submitBtn.addEventListener("mouseout", function () {
    document.querySelector(".hoverLine").style.width = "0";
  });

  urlInput.focus();
  urlInput.click();

  submitBtn.addEventListener("click", (e) => {
    statusMsgCotainer.style.display = "block";

    addMessage("Gathering song information...");

    const filetype = document.querySelector("#fileType").value.split("-")[1];
    const elInputs = document.querySelectorAll("input");

    elInputs.forEach((el) => {
      if (el.hasAttribute("checked")) {
        numStems = el.nextElementSibling.innerText[0];
      }
    });

    e.preventDefault();
    const url = document.querySelector("#url").value;

    fetch("/download_video", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: url,
        filetype: filetype,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          const filename = data.filename;
          showStepCompletion();
          addMessage("Separating stems...");
          showSongName(filename);

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
              if (data.message === "Finished") {
                displayAudioFiles(data.filename);
              }
            })
            .catch((error) => console.error("Error:", error));
        }
      });

    function displayAudioFiles(songName) {
      let directory = numStems == 6 ? "htdemucs_6s" : "htdemucs";
      // Fetch the list of audio files from the server
      fetch("/tracks/" + directory + "/" + encodeURIComponent(songName))
        .then((response) => response.json())
        .then((files) => {
          let container = document.createElement("div");
          let centerContent = document.querySelector(".center-content");
          container.className = "stems-container";
          centerContent.appendChild(container);
          files.forEach((filename) => {
            var audioContainer = document.createElement("div");
            var audio = document.createElement("audio");
            var audioLabel = document.createElement("label");
            audio.className = "stem-player";
            audioContainer.className = "stem-container";
            audioLabel.className = "stem-label";
            audio.src =
              "/tracks/" + directory + "/" + encodeURIComponent(songName) + "/" + encodeURIComponent(filename);
            audio.controls = true;
            audioLabel.innerHTML = filename.substring(0, filename.lastIndexOf("."));
            audioContainer.appendChild(audioLabel);
            audioContainer.appendChild(audio);
            audioContainer.innerHTML += `<i id="download-icon" class="download-icon fa fa-download" aria-hidden="true"></i>`;
            container.appendChild(audioContainer);

            let btnDownloadZip = document.createElement("button");
            btnDownloadZip.className = "btn btn-primary btn-download-zip";
            btnDownloadZip.innerHTML = "Download all stems";
            btnDownloadZip.addEventListener("click", downloadZip);
          });
          let downloadIcons = document.querySelectorAll("#download-icon");
          downloadIcons.forEach((icon) => {
            icon.addEventListener("click", () => {
              let filename = icon.parentElement.children[1].src.split("/").pop();
              window.location = "/download?filename=" + encodeURIComponent(filename);
            });
          });
        });
    }
  });

  function showStepCompletion() {
    let currentSpinney = document.querySelector(".spinnyGif:last-of-type");
    currentSpinney.src = "/static/success.svg"; // Update the src of the last spinney
    currentSpinney.nextElementSibling.innerHTML += "DONE";
  }

  function showSongName(filename) {
    songTitle.innerHTML = filename;
    songTitle.style.display = "block";
  }

  function addMessage(message) {
    let elSpinney = document.createElement("img");
    elSpinney.src = "/static/spinny.gif";
    elSpinney.className = "spinnyGif";
    let elMessage = document.createElement("span");
    elMessage.className = "status-message";
    elMessage.innerHTML = message;
    statusMsgCotainer.appendChild(elSpinney);
    statusMsgCotainer.appendChild(elMessage);
  }

  function downloadZip() {
    window.location = "/download?filename=STEMS-" + encodeURIComponent(data.filename.replace(/\.[^/.]+$/, ""));
  }

  function addChangeEventListener(radio) {
    radio.addEventListener("change", () => {
      const radios = document.querySelectorAll('input[type=radio][name="flexRadioDefault"]');

      radios.forEach((r) => {
        r.removeAttribute("checked");
      });

      radio.setAttribute("checked", "");
    });
  }

  // function addChangeListeners() {
  //   const radios = document.querySelectorAll('input[type=radio][name="flexRadioDefault"]');

  //   radios.forEach(addChangeEventListener);
  // }

  // addChangeListeners();
});
