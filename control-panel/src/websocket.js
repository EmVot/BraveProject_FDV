let socket = null;
let isConnected = false;
const messageQueue = [];

function connectWebSocket() {
  socket = new WebSocket("ws://localhost:8080");

  socket.onopen = () => {
    console.log("WebSocket connesso");
    isConnected = true;

    while (messageQueue.length > 0) {
      const msg = messageQueue.shift();
      console.log("Invio messaggio in coda:", msg);
      socket.send(msg);
    }
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Messaggio ricevuto:", data);
  };

  socket.onerror = (error) => {
    console.error("Errore WebSocket:", error);
  };

  socket.onclose = () => {
    console.warn("WebSocket chiuso. Riconnessione tra 2 secondi...");
    isConnected = false;
    setTimeout(connectWebSocket, 2000); // Riprova la connessione
  };
}

// Avvia la connessione subito
connectWebSocket();

// Funzione di invio messaggi
export function sendMessage(obj) {
  const msg = JSON.stringify(obj);

  if (isConnected && socket.readyState === WebSocket.OPEN) {
    console.log("Invio messaggio:", msg);
    socket.send(msg);
  } else {
    console.warn("WebSocket non ancora connesso, accodo:", msg);
    messageQueue.push(msg);
  }
}