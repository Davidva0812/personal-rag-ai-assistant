import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

function App() {
  const [messages, setMessages] = useState([
    { text: "Hi! I'm David. Feel free to ask me anything about my professional background or projects!", sender: 'ai' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Auto-scroll to the latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { text: input, sender: 'user' };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      // API call to the Python (FastAPI) backend
      const response = await axios.post('http://localhost:10000/chat', {
        message: input
      });

      setMessages(prev => [...prev, { text: response.data.response, sender: 'ai' }]);
    } catch (error) {
      console.error("Hiba:", error);
      setMessages(prev => [...prev, { text: "I'm having trouble connecting to the server. Please make sure the backend is running!", sender: 'ai' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '50px auto', fontFamily: 'Arial', border: '1px solid #ccc', borderRadius: '10px', overflow: 'hidden', backgroundColor: '#272332' }}>
      <div style={{ bg: '#63BCD3', background: '#63BCD3', color: '#f1f1f1', padding: '15px', textAlign: 'center' }}>
        <strong>Personal AI Assistant</strong>
      </div>
      
      <div style={{ height: '450px', overflowY: 'auto', padding: '15px', background: '#f9f9f9' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left', marginBottom: '10px' }}>
            <div style={{ 
              display: 'inline-block', 
              padding: '10px', 
              borderRadius: '10px', 
              background: msg.sender === 'user' ? '#63BCD3' : '#e9e9eb',
              color: msg.sender === 'user' ? 'white' : 'black',
              maxWidth: '80%'
            }}>
              {msg.text}
            </div>
          </div>
        ))}
        {loading && <p style={{ fontSize: '12px', color: '#666' }}>Thinking...</p>}
        <div ref={chatEndRef} />
      </div>

      <form onSubmit={sendMessage} style={{ display: 'flex', padding: '10px', borderTop: '1px solid #ccc' }}>
        <input 
          style={{ flex: 1, padding: '10px', border: '1px solid #ccc', borderRadius: '5px' }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me something..."
        />
        <button type="submit" style={{ marginLeft: '10px', padding: '10px 20px', background: '#63BCD3', color: '#f1f1f1', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
          Send
        </button>
      </form>
    </div>
  );
}

export default App;