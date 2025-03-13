import React, { useEffect } from "react";

const App = () => {
  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:5001");

    const handleKeyDown = (event) => {
      let action = null;
      if (event.key === "ArrowUp") action = "UP";
      else if (event.key === "ArrowDown") action = "DOWN";
      else if (event.key === "ArrowLeft") action = "LEFT";
      else if (event.key === "ArrowRight") action = "RIGHT";

      if (action) {
        ws.send(JSON.stringify({ action }));
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      ws.close();
    };
  }, []);

  return (
    <div>
      <h1>Robot Simulation</h1>
      <iframe src="http://127.0.0.1:5000" width="600" height="600" />
    </div>
  );
};

export default App;
