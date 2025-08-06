const socket = new WebSocket("ws://192.168.1.100:8080"); // IP del server WebSocket

socket.onopen = () => {
  console.log("WebSocket connesso");
};

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Messaggio ricevuto:", data);
};

export function sendMessage(obj) {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(obj));
  } else {
    console.warn("WebSocket non connesso");
  }
}
