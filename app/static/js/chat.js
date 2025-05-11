const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const responseDiv = document.getElementById("response");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userMessage = input.value.trim();
  if (!userMessage) return;

  addMessage(userMessage, "user-msg");
  input.value = "";

  // Adiciona indicador de digitação
  const typingIndicator = addTypingIndicator();

  // Envia a mensagem ao backend
  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userMessage }),
  });

  // Remove o indicador de digitação
  responseDiv.removeChild(typingIndicator);

  const data = await res.json();
  const botReply = data.response || "Algo deu errado.";
  addMessage(botReply, "bot-msg");
});

function addMessage(text, className) {
  const msg = document.createElement("div");
  msg.className = className;
  msg.textContent = text;
  responseDiv.appendChild(msg);
  responseDiv.scrollTop = responseDiv.scrollHeight;
}

function addTypingIndicator() {
  const typingDiv = document.createElement("div");
  typingDiv.className = "typing-indicator";
  typingDiv.innerHTML = `
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
    <span class="typing-text">Digitando...</span>
  `;
  responseDiv.appendChild(typingDiv);
  responseDiv.scrollTop = responseDiv.scrollHeight;
  return typingDiv;
}

// Exibir/ocultar dúvidas frequentes
document.getElementById('toggle-faq').onclick = () => {
    document.getElementById('faq-section').classList.toggle('hidden');
};

// Inserir texto de dúvida no campo de mensagem
function insertFAQ(texto) {
    document.getElementById('message').value = texto;
    document.getElementById('message').focus();
}

// Voltar à tela inicial
document.getElementById('go-home').onclick = () => {
    window.location.href = "/";
};


// Envia a mensagem de duvidas frequentes automaticamente
/*document.querySelectorAll(".faq li").forEach((item) => {
  item.addEventListener("click", () => {
    const faqQuestion = item.textContent.trim();
    input.value = faqQuestion;
    form.dispatchEvent(new Event("submit")); // Envia como se fosse uma mensagem
  });
});
*/
