let mediaRecorder;
let audioChunks = [];
let conversationHistory = [];

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  audioChunks = [];
  mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
  mediaRecorder.start();
  document.getElementById("status").textContent = "🔴 Recording...";
}

async function stopRecording() {
  mediaRecorder.stop();
  document.getElementById("status").textContent = "Processing...";
  document.getElementById("btn").disabled = true;

  mediaRecorder.onstop = async () => {
    const blob = new Blob(audioChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio", blob, "audio.webm");

    // Step 1: transcribe
    const transcribeRes = await fetch("/transcribe", { method: "POST", body: formData });
    const { text } = await transcribeRes.json();
    if (!text || text.trim() === "") {
      document.getElementById("status").textContent = "Didn't catch that. Try again.";
      document.getElementById("btn").disabled = false;
      return;
    }
    document.getElementById("transcript").textContent = text;

    // Step 2: chat
    const chatRes = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history: conversationHistory })
    });
    const { reply } = await chatRes.json();
    document.getElementById("response").textContent = reply;

    // Step 3: speak
    const utterance = new SpeechSynthesisUtterance(reply);
    utterance.lang = "en-US";
    speechSynthesis.speak(utterance);

    // Update history
    conversationHistory.push({ role: "user", content: text });
    conversationHistory.push({ role: "assistant", content: reply });
    renderHistory();

    document.getElementById("status").textContent = "Press and hold to speak";
    document.getElementById("btn").disabled = false;
  };
}

function clearHistory() {
  conversationHistory = [];
  document.getElementById("history-box").innerHTML = "";
  document.getElementById("transcript").textContent = "–";
  document.getElementById("response").textContent = "–";
}

function renderHistory() {
  const box = document.getElementById("history-box");
  box.innerHTML = "<strong>Conversation so far:</strong><br>" +
    conversationHistory.map(m => `<b>${m.role}:</b> ${m.content}`).join("<br>");
}