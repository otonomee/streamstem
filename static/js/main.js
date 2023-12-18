document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.querySelector("#submitBtn");
  const songTitle = document.querySelector("#songTitle");
  const loadingGif = document.querySelector("#loadingGif");
  const urlInput = document.querySelector(".my-form-control");
  const formEntry = document.querySelector("form");
  const statusMessageMainContainer = document.querySelector(".status-message-container");
  const cancelBtn = document.querySelector("#cancelBtn");
  cancelBtn.style.display = "none";
  urlInput.focus();
  urlInput.click();

  let radioLabels = document.querySelectorAll('label[class*="radio-label"]');
  radioLabels.forEach((label) => {
    label.addEventListener("click", () => {
      let radio = label.previousElementSibling;
      radio.checked = true;
      addChangeEventListener(radio);
    });
  });

  formEntry.addEventListener("submit", (e) => {
    e.preventDefault();
  });

  submitBtn.addEventListener("click", (e) => {
    e.preventDefault();
    const filetype = document.querySelector("#fileType").value.split("-")[1];
    const numStems = document.querySelector("input:checked").nextElementSibling.innerText[0];
    const url = document.querySelector("#url").value;

    // Validate URL format
    const youtubeUrlRegex = /^(https?:\/\/)?(www\.)?youtube\.com\/watch\?v=[\w-]{10,12}(&[\w-]+=([\w-]*))*$/;
    const youtubeUrlRegex2 = /^(https?:\/\/)?(www\.)?youtu\.be\/[\w-]{11}(&[\w-]+=([\w-]*))*$/;
    const spotifyUrlRegex = /^(https?:\/\/)?(www\.)?open\.spotify\.com\/track\/[\w-]{22}(\?[\w-]+=([\w-]*))*$/;

    https: if (!youtubeUrlRegex.test(url) && !spotifyUrlRegex.test(url) && !youtubeUrlRegex2.test(url)) {
      console.error("Unsupported URL:", url);
      alert("Invalid URL format. Please enter a valid YouTube or Spotify URL.");
      return;
    }

    formEntry.style.animation = "fadeOut 0.35s ease-in-out forwards";
    formEntry.style.display = "none";
    statusMessageMainContainer.style.animation = "fadeIn 0.35s ease-in-out forwards";
    statusMessageMainContainer.style.display = "block";
    cancelBtn.style.display = "block";
    cancelBtn.style.animation = "fadeIn 0.35s ease-in-out forwards";

    cancelBtn.addEventListener("click", () => {
      location.reload();
    });

    addMessage("Gathering song information");
    setTimeout(() => {
      addMessage("Analyzing audio");
    }, 5000);

    //const numStems = Array.from(elInputs).find((el) => el.hasAttribute("checked")).nextElementSibling.innerText[0];
    let songName;
    console.log(numStems);

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
          addMessage("Separating stems");

          songName = filename.substring(0, filename.lastIndexOf("."));
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
                showStepCompletion();
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
            var stemIcon = document.createElement("img");
            if (filename.includes("vocals")) {
              stemIcon.className = "stem-icon";
              stemIcon.src = "/static/vocal.svg";
            } else if (filename.includes("drums")) {
              stemIcon.className = "stem-icon";
              stemIcon.src = "/static/drums.svg";
            } else if (filename.includes("bass")) {
              stemIcon.className = "stem-icon";
              stemIcon.src = "/static/bass.svg";
            } else if (filename.includes("piano")) {
              stemIcon.className = "stem-icon";
              stemIcon.src = "/static/piano.svg";
            } else if (filename.includes("guitar")) {
              stemIcon.className = "stem-icon";
              stemIcon.src = "/static/guitar.svg";
            } else if (filename.includes("other")) {
              stemIcon.className = "stem-icon";
              stemIcon.src = "/static/other.svg";
            }

            audio.className = "stem-player";
            audioContainer.className = "stem-container";
            audioLabel.className = "stem-label";
            audio.src = "/tracks/" + directory + "/" + encodeURIComponent(songName) + "/" + encodeURIComponent(filename);
            audio.controls = true;
            audioLabel.innerHTML = `<img class="stem-icon" src="/static/${filename.substring(
              0,
              filename.lastIndexOf(".")
            )}.svg"></i>${filename.substring(0, filename.lastIndexOf("."))}`;

            let playerDiv = document.createElement("div");
            playerDiv.className = "player-div";

            playerDiv.appendChild(audio);
            playerDiv.innerHTML += `
            <button class="btn btn-primary btn-download-stem" id="download-stem-${filename}">
            <i id="download-icon-${filename}" class="download-icon fa fa-download" aria-hidden="true"></i>Download</button>
            `;
            audioContainer.appendChild(audioLabel);
            audioContainer.appendChild(playerDiv);

            container.appendChild(audioContainer);
          });

          let duoBtnDiv = document.createElement("div");
          duoBtnDiv.className = "duo-btn-div";

          let newSong = document.createElement("button");
          newSong.className = "btn btn-primary btn-new-song";
          newSong.innerHTML = `<i class="fa-solid fa-rotate-right"></i> New Song`;
          newSong.addEventListener("click", () => {
            location.reload();
          });

          let btnDownloadZip = document.createElement("button");
          btnDownloadZip.className = "btn btn-primary btn-download-zip";
          btnDownloadZip.innerHTML = `<i class="download-all-icon fa fa-download" aria-hidden="true"></i> Download All`;
          btnDownloadZip.addEventListener("click", () => {
            downloadZip(songName);
          });

          duoBtnDiv.appendChild(newSong);
          duoBtnDiv.appendChild(btnDownloadZip);
          container.appendChild(duoBtnDiv);

          let downloadBtns = document.querySelectorAll(".btn.btn-primary.btn-download-stem");
          downloadBtns.forEach((btn) => {
            // END: be15d9bcejpp
            btn.addEventListener("click", () => {
              let filename = btn.parentElement.firstChild.src.split("/").pop();

              downloadFile(filename, songName, directory);
              // window.location = "/download?filename=" + encodeURIComponent(filename);
            });
          });
        });
      document.querySelector(".begin-message").style.animation = "fadeOut 0.35s ease-in-out forwards";
      setTimeout(() => {
        document.querySelector(".begin-message").style.display = "none";
      }, 350);
      cancelBtn.style.animation = "fadeOut 0.35s ease-in-out forwards";
      setTimeout(() => {
        cancelBtn.style.display = "none";
      }, 350);
    }
  });

  function showStepCompletion() {
    let currentSpinney = document.querySelector(".spinnyGif");
    if (!currentSpinney) return;
    let message = currentSpinney.nextElementSibling;
    currentSpinney.src = "/static/success.svg"; // Update the src of the last spinney
    currentSpinney.className = "successGif";
    message.innerHTML = message.innerHTML.replace(/\.{1,3}/, "...Finished");

    // Clear the interval
    let currentMessageContainer = currentSpinney.parentElement;
    clearInterval(currentMessageContainer.intervalId);
  }

  function showSongName(filename) {
    songTitle.innerHTML = `Song title: <span style="font-weight:600;">${filename}</span>`;
    songTitle.style.display = "block";
  }

  function addMessage(message) {
    showStepCompletion();

    let messageContainer = document.createElement("div");
    messageContainer.className = "single-message-container";
    let elSpinney = document.createElement("img");
    elSpinney.src = "/static/spinny.gif";
    elSpinney.className = "spinnyGif";
    let elMessage = document.createElement("span");
    elMessage.className = "status-message";
    elMessage.innerHTML = message;
    messageContainer.appendChild(elSpinney);
    messageContainer.appendChild(elMessage);
    statusMessageMainContainer.appendChild(messageContainer);

    let dots = "";
    let intervalId = setInterval(() => {
      dots = dots.length < 3 ? dots + "." : "";
      elMessage.innerHTML = message + dots;
    }, 500);

    // Store the intervalId on the messageContainer so it can be cleared later
    messageContainer.intervalId = intervalId;
  }

  function downloadZip(data) {
    window.location = "/download?filename=STEMS-" + encodeURIComponent(data);
  }

  function downloadFile(filename, songName, stemType) {
    songName = document.querySelector("#songTitle").innerText.split(": ")[1];
    let a = document.createElement("a");
    //let stemType = numStems === 6 ? "htdemucs_6s" : "htdemucs";
    a.href = `/tracks/${stemType}/${encodeURIComponent(songName)}/${encodeURIComponent(filename)}`;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
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
  queueMicrotask;
  function showModal(message) {
    // Create the modal elements
    let modal = document.createElement("div");
    let modalContent = document.createElement("div");
    let modalText = document.createElement("p");

    // Set the content of the modal
    modalText.textContent = mesdsdddddDDDdsage;

    // Set the classes for styling
    modal.className = "modal";
    modalContent.className = "modal-content";
    modalText.className = "modal-text";

    // Append the elements
    modalContent.appendChild(modalText);
    modal.appendChild(modalContent);
    document.body.appendChild(modal);

    // Add a click event to close the modal
    modal.addEventListener("click", function () {
      modal.remove();
    });
  }

  // function addChangeListeners() {
  //   const radios = document.querySelectorAll('input[type=radio][name="flexRadioDefault"]');

  //   radios.forEach(addChangeEventListener);
  // }

  // addChangeListeners();
});
