import React, { useState } from 'react';
import { UilRobot, UilCommentAlt, UilMessage } from '@iconscout/react-unicons';
import '../ChatBot/ChatBot.css';

function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([{ text: 'Olá! Como posso te ajudar?', sender: 'bot' }]);
  const [input, setInput] = useState('');

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = () => {
    if (input.trim() !== '') {
      const newMessage = { text: input, sender: 'user' };
      setMessages([...messages, newMessage]);
      setInput('');

      // Simular resposta do bot
      setTimeout(() => {
        const botReply = { text: 'Esta é uma resposta automática.', sender: 'bot' };
        setMessages((prevMessages) => [...prevMessages, botReply]);
      }, 1000);
    }
  };

  return (
    <>
      {!isOpen && (
        <UilCommentAlt className="chatbot-button" onClick={toggleChatbot}></UilCommentAlt>
      )}
      
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <UilRobot className="icon-robot" ></UilRobot>
            Chatbot
            <button className="chatbot-close" onClick={toggleChatbot}>✖</button>
          </div>
          <div className="chatbot-body">
            {messages.map((message, index) => (
              <p key={index} className={`chatbot-message ${message.sender}`}>
                {message.text}
              </p>
            ))}
          </div>
          <div className="chatbot-input">
            <input 
              type="text" 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              placeholder="Digite sua mensagem..."
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()} 
            />
            <UilMessage className="icon-send" onClick={sendMessage}></UilMessage>
          </div>
        </div>
      )}
    </>
  );
}

export default Chatbot;
