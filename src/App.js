import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const initialPoints = [
  { id: 1, type: "QR Code", position: [51.505, -0.09] },
  { id: 2, type: "Charging Station", position: [51.51, -0.1] },
  { id: 3, type: "Robot", position: [51.52, -0.12] },
];

const AddPoint = ({ onAdd }) => {
  useMapEvents({
    click(e) {
      const type = prompt("Enter point type (QR Code / Charging Station / Robot):");
      if (type) {
        onAdd({ id: Date.now(), type, position: [e.latlng.lat, e.latlng.lng] });
      }
    },
  });
  return null;
};

const WarehouseMap = () => {
  const [points, setPoints] = useState(initialPoints);

  const addPoint = (newPoint) => {
    setPoints([...points, newPoint]);
  };

  return (
    <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: "80vh", width: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <AddPoint onAdd={addPoint} />
      {points.map((point) => (
        <Marker key={point.id} position={point.position}>
          <Popup>{point.type}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

const App = () => {
  return (
    <div>
      <h1>Warehouse Simulation</h1>
      <WarehouseMap />
    </div>
  );
};

export default App;
