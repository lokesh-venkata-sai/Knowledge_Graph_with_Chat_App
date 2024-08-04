import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [responses, setResponses] = useState([]);

  const handleSubmit = async (e) => {
    console.log("In button handling");
    e.preventDefault();
    const response = await axios.post('http://localhost:5000/chatbot', { message });
    const botResponse = response.data.response || "Couldn't understand. Please give more info?";
    setResponses([...responses, { user: message, bot: botResponse }]);
    setMessage('');
  };

  return (
    <div className="App">
      <h1>Chatbot</h1>
      <div className="chat-container">
        {responses.map((res, index) => (
          <div key={index} className="chat-message">
            <p><strong>You:</strong> {res.user}</p>
            <p><strong>Bot:</strong> {res.bot}</p>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default App;