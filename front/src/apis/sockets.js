import socketIOClient from "socket.io-client";
const socket = socketIOClient(ENDPOINT);

window.addEventListener("beforeunload", (ev) => {  
    socket.emit("disconnect_request");
});


socket.on("messages", data => {
    console.log(data);
    setResponse(data.data);
});


socket.on("event", data => {
    console.log(data);
});
