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
- **Dependencies**: React, ReactDOM, Babel

## Prerequisites
- Node.js and npm (for frontend)
- Python 3.x (for backend)
- Git (for version control and GitHub)

## Installation

### Backend Setup
1. Navigate to the project directory containing `app.py`.
2. Install the required Python packages:
   ```bash
   pip install flask
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
   The server will run on `http://localhost:5000` by default.

### Frontend Setup
1. Ensure you have Node.js and npm installed.
2. Navigate to the project directory containing `index.html`, `App.jsx`, and `App.css`.
3. The frontend relies on CDN-hosted React and Babel scripts, so no additional installation is needed beyond serving the files via a web server or locally with a tool like `live-server`.

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