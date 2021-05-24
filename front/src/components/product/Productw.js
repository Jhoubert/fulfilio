import React, { useState, useEffect } from "react";


const ENDPOINT = "http://127.0.0.1:5000/global";

function App() {
  const [response, setResponse] = useState("");
  const [onlineUsers, setOnlineUsers] = useState("");

  useEffect(() => {    

    const socket = socketIOClient(ENDPOINT);

    window.addEventListener("beforeunload", (ev) => {  
        socket.emit("disconnect_request");
    });


    socket.on("messages", data => {
      console.log(data);
      setResponse(data.data);
    });

    socket.on("people", data => {
      console.log(data);
      setOnlineUsers(data);
    });

    
    socket.on("event", data => {
      console.log(data);
    });


  }, []);

  return (
    <p>
      Users online: {onlineUsers.length}<br /><br />
      Message received: {response}
    </p>
  );
}

export default App;