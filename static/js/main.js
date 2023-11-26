document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.querySelector("#submitBtn");
  const songTitle = document.querySelector("#songTitle");
  const loadingGif = document.querySelector("#loadingGif");
  const urlInput = document.querySelector(".my-form-control");

  // JavaScript
  submitBtn.addEventListener("mouseover", function () {
    document.querySelector(".hoverLine").style.width = "55%";
  });

  submitBtn.addEventListener("mouseout", function () {
    document.querySelector(".hoverLine").style.width = "0";
  });

  urlInput.focus();
  urlInput.click();

  let radioBtns = document.querySelectorAll(".form-check");
  radioBtns.forEach((btn) => {
    btn.addEventListener("hover", () => {
      // Display a popup tooltip explaining the number of stems
      console.log(btn);
    });
  });

  let numStems;

  submitBtn.addEventListener("click", (e) => {
    loadingGif.style.display = "flex";
    resetUi();

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
              console.log(data.message);

              updateUi("Video title:", data.filename.replace(/\.[^/.]+$/, ""));
              if (data.message === "Finished") {
                loadingGif.style.display = "none";

                displayAudioFiles(data.filename);
                // window.location =
                //   "/download?filename=STEMS-" +
                //   encodeURIComponent(data.filename.replace(/\.[^/.]+$/, ""));
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

  function updateUi(filename) {
    songTitle.innerHTML = `Song name: ${filename}`;
    songTitle.style.display = "block";
  }

  function resetUi() {
    songTitle.innerHTML = "";
    songTitle.style.display = "none";
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

  function addChangeListeners() {
    const radios = document.querySelectorAll('input[type=radio][name="flexRadioDefault"]');

    radios.forEach(addChangeEventListener);
  }

  addChangeListeners();
});
