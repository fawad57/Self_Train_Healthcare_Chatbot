# Healthcare Chatbot

## Overview
This is a web-based healthcare chatbot application built using React and Flask. The chatbot assists users by collecting symptoms, asking follow-up questions, and providing potential health condition predictions along with precautions. It includes features like chat history storage, audio toggle, and a responsive design.

## Features
- Interactive symptom-based conversation with the user.
- Prediction of possible health conditions based on user input.
- Display of precautions for diagnosed conditions.
- Storage and retrieval of chat history.
- Audio-enabled responses (optional).
- Responsive design for desktop and mobile devices.

## Technologies Used
- **Frontend**: React, HTML, CSS
- **Backend**: Flask (Python)
- **Styling**: Custom CSS with Poppins font
- **Dependencies**: React, ReactDOM, Babel (via CDN), Flask

## Prerequisites
- **Node.js and npm**: For frontend development and testing (download from [nodejs.org](https://nodejs.org)).
- **Python 3.x**: For running the Flask backend (download from [python.org](https://www.python.org)).
- **Git**: For cloning the repository (download from [git-scm.com](https://git-scm.com)).

## Installation

### Clone the Repository
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/fawad57/Self_Train_Healthcare_Chatbot.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Self_Train_Healthcare_Chatbot
   ```

### Backend Setup
1. Ensure Python 3.x is installed. Verify with:
   ```bash
   python --version
   ```
   or
   ```bash
   python3 --version
   ```
2. Install the required Python package:
   ```bash
   pip install flask
   ```
3. (Optional) Create a virtual environment for isolation:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install flask
   ```

### Frontend Setup
1. Ensure Node.js and npm are installed. Verify with:
   ```bash
   node -v
   npm -v
   ```
2. No additional npm packages are required since the frontend uses CDN-hosted React, ReactDOM, and Babel. However, for local development, you can use a simple server like `live-server`:
   - Install `live-server` globally:
     ```bash
     npm install -g live-server
     ```
   - This step is optional; the project can run directly with the Flask server serving static files.

## Running the Project

### Start the Backend
1. Ensure you are in the project directory.
2. Run the Flask server:
   ```bash
   python app.py
   ```
   or
   ```bash
   python3 app.py
   ```
3. The server will start on `http://localhost:5000`. Keep this terminal open.

### Start the Frontend
1. The frontend is served by the Flask backend. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```
2. Alternatively, if using `live-server` for local testing:
   - Run:
     ```bash
     live-server
     ```
   - Open the URL provided (e.g., `http://localhost:8080`).

## Usage
1. Open your browser and go to `http://localhost:5000`.
2. Start a new chat by entering a symptom (e.g., "fever", "chills").
3. Answer the follow-up questions with "yes" or "no".
4. View the predicted condition and precautions once the chatbot completes the diagnosis.
5. Use the sidebar to:
   - Start a "New Chat" to reset the conversation (history is saved).
   - View "History" to see past chat sessions with timestamps.
   - Access "Settings" (currently placeholder).
6. Toggle audio on/off using the checkbox below the input field.

## Project Structure
- `index.html`: Main HTML file with CDN links for React and Babel.
- `App.jsx`: React component containing the chatbot logic.
- `App.css`: Stylesheet for the application layout and components.
- `app.py`: Flask backend server handling chat logic.
- `README.md`: Project documentation.
- `LICENSE.md`: MIT License file.

## Contributing
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- Inspired by healthcare assistant concepts.
- Uses Poppins font from Google Fonts.
- Built with guidance from xAI's Grok 3.

## Troubleshooting
- **Backend not running**: Ensure Flask is installed and the port 5000 is not in use.
- **Frontend not loading**: Verify the Flask server is running and serving static files correctly, or use `live-server` with the correct directory.
- **Errors in console**: Check the browser developer tools (F12) for JavaScript errors and the terminal for Python errors.