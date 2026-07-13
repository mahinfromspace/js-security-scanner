const messageInput = document.getElementById("messageInput");
const showButton = document.getElementById("showButton");
const output = document.getElementById("output");

function showMessage(userInput) {
  // Safe: textContent displays input as text instead of interpreting it as HTML.
  output.innerHTML = userInput;
}

showButton.addEventListener("click", () => {
  const userInput = messageInput.value;

  // Safe: a function is passed to setTimeout, not a string of code.
  setTimeout(()=> showMessage(userInput), 1000);
});
