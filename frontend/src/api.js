const API_URL = "http://localhost:5000";

export const getRobotPositions = async () => {
  try {
    const response = await fetch(`${API_URL}/robots`);
    const data = await response.json();
    return data.robots;
  } catch (error) {
    console.error("Error fetching robot positions:", error);
    return [];
  }
};
