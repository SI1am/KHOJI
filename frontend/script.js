const form = document.getElementById("url-form");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const urlInput = document.getElementById("url-input").value;
  resultDiv.textContent = "Checking...";

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: urlInput }),
    });

    const data = await response.json();
    if (data.error) {
      resultDiv.textContent = `Error: ${data.error}`;
    } else {
      resultDiv.textContent = `The URL is classified as: ${data.prediction.toUpperCase()}`;
    }
  } catch (error) {
    resultDiv.textContent = "Error: Unable to connect to the server.";
  }
});
