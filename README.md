# AGV Path Planner

## Overview
This project is an AGV (Automated Guided Vehicle) path planning simulator using **Pygame**. Users can click on a location to set different path types (Turning, Idle, Normal, Charging), place an AGV, and move it along selected paths. The simulation runs on a clean map instead of a grid.

## Features
- Click anywhere on the map to create waypoints.
- Select different types of waypoints via a dropdown menu.
- Place an AGV anywhere on the map.
- Click on the AGV to select it, choose a destination, and press Enter to move it.
- Object-Oriented Design for scalability.

## Installation
### Prerequisites
Make sure you have **Python 3.8+** installed.

### Clone the Repository
```bash
git clone https://github.com/your-username/agv-path-planner.git
cd agv-path-planner
```

### Install Dependencies
```bash
pip install pygame
```

### Run the Simulation
```bash
python main.py
```

## Git Workflow
### Creating a New Branch
Before making any changes, create a separate branch:
```bash
git checkout -b feature/ui-improvements
```
This ensures that the `main` branch remains stable.

### Making Changes & Committing
After modifying the code, check your changes:
```bash
git status
```
Then, stage and commit them:
```bash
git add .
git commit -m "Improved dropdown UI and removed grid for a clean map"
```

### Pushing the Branch to GitHub
```bash
git push origin feature/ui-improvements
```

### Creating a Pull Request
1. Go to your GitHub repository.
2. Click **"Compare & pull request"** for `feature/ui-improvements`.
3. Add a description of your changes.
4. Click **"Create pull request"** to submit for review.

### Merging the Branch
Once approved, merge it into `main`:
```bash
git checkout main
git pull origin main
git merge feature/ui-improvements
git push origin main
```

### Deleting the Branch
After merging, clean up old branches:
```bash
git branch -d feature/ui-improvements
git push origin --delete feature/ui-improvements
```

## Future Improvements
- Add smooth animations for AGV movement.
- Implement pathfinding algorithms (e.g., A*).
- Improve UI with interactive controls.

## License
MIT License

