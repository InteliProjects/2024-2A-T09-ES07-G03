import React, { useState, useEffect } from 'react';
import { UilSearch, UilFilter, UilMicrophone } from '@iconscout/react-unicons';
import FilterPopup from '../FilterPopup/FilterPopup';
import './Header.css';

const Header = ({ onSearch, onFilter }) => {
  const [query, setQuery] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [debouncedQuery, setDebouncedQuery] = useState(query);

  // Função para debouncing
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(query);
      console.log("Debounced query:", query);
    }, 100);

    return () => {
      clearTimeout(handler); // Limpar o timeout se o usuário continuar digitando
    };
  }, [query]);

  // Acionar a busca sempre que o debouncedQuery mudar
  useEffect(() => {
    if (debouncedQuery !== undefined) {
      if (debouncedQuery === '') {
        console.log("No query, retrieving all results.");
        onSearch('');
      } else if (onSearch) {
        console.log("Searching for:", debouncedQuery);
        onSearch(debouncedQuery);
      }
    }
  }, [debouncedQuery, onSearch]);

  const handleChange = (e) => {
    setQuery(e.target.value);
    console.log("Input changed:", e.target.value);
  };

  const handleSearch = () => {
    console.log("Search triggered for:", query);
    if (onSearch) {
      onSearch(query);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      console.log("Enter key pressed, searching for:", query);
      handleSearch();
    }
  };

  const handleMicrophoneClick = async () => {
    if (!isRecording) {
      console.log("Starting audio recording...");
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);

      recorder.ondataavailable = event => {
        if (event.data.size > 0) {
          setAudioChunks(prev => [...prev, event.data]);
        }
        console.log("Audio chunk received:", event.data); 
      };

      recorder.onstop = () => {
        console.log("Recording stopped, processing audio...");
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        sendAudio(audioBlob);
      };

      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
    } else {
      console.log("Stopping audio recording...");
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  const sendAudio = async (audioBlob) => {
    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.wav');

    try {
      console.log("Sending audio to server...");
      const response = await fetch('http://localhost:8000/record-and-transcribe-audio', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Audio sent successfully! Transcription:", data.transcription);
        alert('Áudio enviado com sucesso! Transcrição: ${data.transcription}');
        setQuery(data.transcription);
        onSearch(data.transcription);
      } else {
        const errorDetail = await response.json();
        console.error("Error sending audio:", errorDetail);
      }
    } catch (error) {
      console.error('Erro ao enviar áudio:', error);
    }
  };

  const handleFilterToggle = () => {
    setIsPopupOpen(!isPopupOpen);
    console.log("Filter popup toggled:", !isPopupOpen);
  };

  const handleVoiceRecognitionClick = () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'pt-BR';
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    recognition.start();
    console.log("Voice recognition started...");

    recognition.onresult = (event) => {
      let speechToText = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        speechToText += event.results[i][0].transcript;
      }
      console.log("Voice recognition result:", speechToText); 
      setQuery(speechToText); // Atualiza o estado da query em tempo real
    };

    recognition.onend = () => {
      console.log("Voice recognition ended...");
      onSearch(query); // Chama a função de busca após o reconhecimento
    };

    recognition.onerror = (event) => {
      console.error('Erro de reconhecimento de fala:', event.error);
      alert('Erro ao reconhecer a fala. Tente novamente.');
    };
  };

  return (
    <div className="header-container">
      <div className="search-bar">
        <UilSearch className="icon-search" onClick={handleSearch} />
        <input
          type="text"
          placeholder="Pesquisar por regulamentações..."
          value={query}
          onChange={handleChange}
          onKeyPress={handleKeyPress}
        />
        <UilMicrophone className="icon-microphone" 
          onClick={isRecording ? handleMicrophoneClick : handleVoiceRecognitionClick} />
        <UilFilter className="icon-filter" onClick={handleFilterToggle} />
      </div>
      {isPopupOpen && (
        <FilterPopup onClose={handleFilterToggle} onFilter={onFilter} />
      )}
    </div>
  );
};

export default Header;