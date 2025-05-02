document.getElementById("chat-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = document.getElementById("message").value;
    const responseDiv = document.getElementById("chat-response");
  
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
  
    const data = await res.json();
    responseDiv.textContent = data.response;
  });
  