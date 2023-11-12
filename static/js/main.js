document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.querySelector("#submitBtn");
  const songTitle = document.querySelector("#songTitle");
  const loadingGif = document.querySelector("#loadingGif");

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

  function addChangeEventListener(radio) {
    radio.addEventListener("change", () => {
      const radios = document.querySelectorAll(
        'input[type=radio][name="flexRadioDefault"]'
      );

      radios.forEach((r) => {
        r.removeAttribute("checked");
      });

      radio.setAttribute("checked", "");
    });
  }

  function addChangeListeners() {
    const radios = document.querySelectorAll(
      'input[type=radio][name="flexRadioDefault"]'
    );

    radios.forEach(addChangeEventListener);
  }

  addChangeListeners();
});
