const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const responseDiv = document.getElementById("response");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userMessage = input.value.trim();
  if (!userMessage) return;

  addMessage(userMessage, "user-msg");

  input.value = "";

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userMessage }),
  });

  const data = await res.json();
  const botReply = data.response || "Something went wrong.";

  addMessage(botReply, "bot-msg");
});

function addMessage(text, className) {
  const msg = document.createElement("div");
  msg.className = className;
  msg.textContent = text;
  responseDiv.appendChild(msg);
  responseDiv.scrollTop = responseDiv.scrollHeight;
}
