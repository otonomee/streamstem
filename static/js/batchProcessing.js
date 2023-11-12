// Function to add a new URL input field
function addUrlInput() {
  var container = document.getElementById("urlInputsContainer");
  var index = container.childElementCount + 1;

  var inputField = document.createElement("div");
  inputField.className = "url-input";
  inputField.innerHTML = `
        <input type="text" name="url${index}" placeholder="Enter URL" />
        <button type="button" class="remove-btn" onclick="removeUrlInput(this)">Remove</button>
    `;

  container.appendChild(inputField);
}

// Function to remove a URL input field
function removeUrlInput(button) {
  var container = document.getElementById("urlInputsContainer");
  container.removeChild(button.parentElement);
}

// Function to submit the form (replace with your actual submission logic)
function submitForm() {
  var form = document.getElementById("urlForm");
  // Add your logic to submit the form data (e.g., AJAX request)
  // ...

  // For demonstration purposes, log the form data to the console
  console.log(new FormData(form));
}
