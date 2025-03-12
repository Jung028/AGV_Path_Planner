import React, { useState } from "react";
import "./App.css"; // Import styles

const GRID_SIZE = 20; // Adjust grid size as needed

const App = () => {
  const [zoom, setZoom] = useState(1); // Zoom level
  const [objects, setObjects] = useState({}); // Store objects by "row,col"

  // Handle zoom in/out
  const handleZoom = (factor) => {
    setZoom((prevZoom) => Math.max(0.5, Math.min(2, prevZoom * factor))); // Limit zoom
  };

  // Handle placing objects (QR, Robot, Charging Station)
  const handleClick = (row, col) => {
    const key = `${row},${col}`;
    const objectTypes = ["QR", "Robot", "Charging"]; // Cycle through objects
    const currentType = objects[key] || null;
    const nextType = objectTypes[(objectTypes.indexOf(currentType) + 1) % objectTypes.length];

    setObjects({ ...objects, [key]: nextType });
  };

  return (
    <div className="container">
      <div className="controls">
        <button onClick={() => handleZoom(1.2)}>Zoom In</button>
        <button onClick={() => handleZoom(0.8)}>Zoom Out</button>
      </div>

      <div className="grid-container" style={{ transform: `scale(${zoom})` }}>
        {[...Array(GRID_SIZE)].map((_, row) =>
          [...Array(GRID_SIZE)].map((_, col) => {
            const key = `${row},${col}`;
            return (
              <div key={key} className="cell" onClick={() => handleClick(row, col)}>
                {objects[key] && <span className="object">{objects[key]}</span>}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default App;
