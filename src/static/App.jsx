const { useState, useEffect, useRef } = React;

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(Date.now().toString());
  const [step, setStep] = useState("symptom");
  const [audioEnabled, setAudioEnabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]); // New state for storing chat history
  const [showHistory, setShowHistory] = useState(false); // State to toggle history view
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, showHistory]);

  useEffect(() => {
    const startInitialChat = async () => {
      setIsLoading(true);
      try {
        const response = await fetch("/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: sessionId,
            name: "",
            audio: false,
          }),
        });
        const data = await response.json();
        setMessages([{ text: data.message, sender: "bot" }]);
        setStep(data.step || "symptom");
      } catch {
        setMessages([{ text: "Error starting chat.", sender: "bot" }]);
      } finally {
        setIsLoading(false);
      }
    };
    startInitialChat();
  }, []);

  const sendMessage = async (userInput) => {
    if (!userInput.trim()) return;

    setMessages([...messages, { text: userInput, sender: "user" }]);
    setInput("");
    setIsLoading(true);

    let response;
    try {
      response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          input: userInput,
          audio: audioEnabled,
        }),
      });

      const data = await response.json();
      const newMsgs = [{ text: userInput, sender: "user" }];

      let ack = "";
      let responseText = data.message || data.error || "";
      if (
        responseText.startsWith("Got it, you’re not experiencing") ||
        responseText.startsWith("Okay, I’ll note that you are experiencing")
      ) {
        ack = responseText.split(". ")[0] + ".";
        responseText = responseText.substring(ack.length + 1).trim();
      }

      if (ack) {
        newMsgs.push({ text: ack, sender: "bot" });
      }

      if (responseText) {
        const predictionMatch = responseText.match(/You may have ([^\.]+)/);
        const prediction = predictionMatch ? predictionMatch[1] : "";
        const description = responseText
          .split("Take following measures:")[0]
          .replace(prediction, "")
          .trim();
        const precautions = responseText.includes("Take following measures:")
          ? responseText
              .split("Take following measures:")[1]
              .split(/[\d]\)/)
              .filter((p) => p.trim())
              .map((p) => p.trim())
          : [];

        if (prediction) {
          newMsgs.push({
            text: "",
            sender: "bot",
            prediction,
            description,
            precautions,
          });
        } else {
          newMsgs.push({ text: responseText, sender: "bot" });
        }
      }

      setMessages([...messages, ...newMsgs]);
      setStep(data.step || step);
    } catch {
      setMessages([
        ...messages,
        { text: userInput, sender: "user" },
        { text: "Error communicating with server.", sender: "bot" },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage(input);
  };

  const getPlaceholder = () => {
    const map = {
      symptom: "Enter your symptom...",
      select_symptom: "Enter the number of your symptom...",
      days: "Number of days?",
      follow_up: "Answer yes or no...",
    };
    return map[step] || "Type your message...";
  };

  const startNewChat = async () => {
    // Store current chat in history if there are messages
    if (messages.length > 0) {
      setChatHistory([
        ...chatHistory,
        {
          id: sessionId,
          messages: [...messages],
          timestamp: new Date().toLocaleString(),
        },
      ]);
    }

    // Reset current chat
    setMessages([]);
    setInput("");
    const newSessionId = Date.now().toString();
    setSessionId(newSessionId);
    setStep("symptom");
    setIsLoading(true);
    setAudioEnabled(false);
    setShowHistory(false); // Hide history view when starting new chat

    try {
      const response = await fetch("/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: newSessionId,
          name: "",
          audio: false,
        }),
      });
      const data = await response.json();
      setMessages([{ text: data.message, sender: "bot" }]);
      setStep(data.step || "symptom");
    } catch {
      setMessages([{ text: "Error starting new chat.", sender: "bot" }]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleHistory = () => {
    setShowHistory(!showHistory);
  };

  return (
    <>
      <header className="chat-header">
        <div className="header-title">
          <span className="header-emoji">🩺</span>
          <h1>Healthcare Assistant</h1>
        </div>
      </header>
      <div className="app-layout">
        <aside className="sidebar">
          <h2>🩺 Menu</h2>
          <ul>
            <li onClick={startNewChat}>
              <span>🆕</span> New Chat
            </li>
            <li onClick={toggleHistory}>
              <span>⏱️</span> History
            </li>
          </ul>
        </aside>

        <main className="main-chat">
          <div className="chat-messages">
            {showHistory ? (
              chatHistory.length > 0 ? (
                chatHistory.map((chat, index) => (
                  <div key={index} className="history-session">
                    <h3>
                      Chat Session {index + 1} - {chat.timestamp}
                    </h3>
                    {chat.messages.map((msg, msgIndex) => (
                      <div
                        key={msgIndex}
                        className={`message ${
                          msg.sender === "user" ? "user" : "bot"
                        }`}
                      >
                        {msg.prediction ? (
                          <div className="response-card">
                            <h3>Bot: {msg.prediction}</h3>
                            <p className="description">{msg.description}</p>
                            {msg.precautions.length > 0 && (
                              <div className="precautions">
                                <h4>Precautions:</h4>
                                <ul>
                                  {msg.precautions.map((p, i) => (
                                    <li key={i}>{p}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </div>
                        ) : (
                          <div className="bubble">{msg.text}</div>
                        )}
                      </div>
                    ))}
                  </div>
                ))
              ) : (
                <div className="no-history">No chat history available.</div>
              )
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  className={`message ${
                    msg.sender === "user" ? "user" : "bot"
                  }`}
                >
                  {msg.prediction ? (
                    <div className="response-card">
                      <h3>Bot: {msg.prediction}</h3>
                      <p className="description">{msg.description}</p>
                      {msg.precautions.length > 0 && (
                        <div className="precautions">
                          <h4>Precautions:</h4>
                          <ul>
                            {msg.precautions.map((p, i) => (
                              <li key={i}>{p}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="bubble">{msg.text}</div>
                  )}
                </div>
              ))
            )}
            {isLoading && !showHistory && (
              <div className="message bot">
                <div className="bubble loading">
                  <span className="dot"></span>
                  <span className="dot"></span>
                  <span className="dot"></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-area">
            <div className="input-row">
              <div className="input-container">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={getPlaceholder()}
                  disabled={showHistory} // Disable input when viewing history
                />
                <button
                  onClick={() => sendMessage(input)}
                  disabled={showHistory}
                >
                  <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path d="M2 21l21-9L2 3v7l15 2-15 2v7z" />
                  </svg>
                </button>
              </div>
            </div>
            <div className="audio-toggle">
              <input
                type="checkbox"
                id="audio-toggle"
                checked={audioEnabled}
                onChange={() => setAudioEnabled(!audioEnabled)}
                disabled={showHistory}
              />
              <label htmlFor="audio-toggle">
                {audioEnabled ? "🔊 Audio Enabled" : "🔇 Audio Disabled"}
              </label>
            </div>
          </div>
        </main>
      </div>
    </>
  );
};

ReactDOM.render(<App />, document.getElementById("root"));
