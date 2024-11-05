import React, { useState, useEffect } from 'react';
import './FilterPopup.css';

const FilterPopup = ({ onClose, onFilter }) => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);
  const [predefinedTags, setPredefinedTags] = useState([]);

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await fetch('http://localhost:8000/tags');
        const tags = await response.json();
        setPredefinedTags(tags.map(tag => tag.tag_name));
      } catch (error) {
        console.error('Erro ao buscar tags:', error);
      }
    };

    fetchTags();
  }, []);

  const handleTagClick = (tag) => {
    setSelectedTags((prevTags) =>
      prevTags.includes(tag)
        ? prevTags.filter((t) => t !== tag)
        : [...prevTags, tag]
    );
  };

  const handleFilter = () => {
    const filters = {
      startDate,
      endDate,
      tags: selectedTags,
    };
    onFilter(filters); 
    onClose();
  };

  return (
    <>
      <div className="overlay" onClick={onClose} role="button" aria-label="Fechar popup" />
      <div className="filter-popup">
        <h2 className='popup-title'>Opções de Filtragem</h2>
        <div className="date-container">
          <div>
            <label htmlFor="start-date">Data Inicial:</label>
            <input 
              id="start-date"
              type="date" 
              value={startDate} 
              onChange={(e) => setStartDate(e.target.value)} 
            />
          </div>
          <div>
            <label htmlFor="end-date">Data Final:</label>
            <input 
              id="end-date"
              type="date" 
              value={endDate} 
              onChange={(e) => setEndDate(e.target.value)} 
            />
          </div>
        </div>
        <div>
          <label>Tags:</label>
          <div className="tags-container">
            {predefinedTags.map((tag) => (
              <div 
                key={tag} 
                className={`tag ${selectedTags.includes(tag) ? 'selected' : ''}`}
                onClick={() => handleTagClick(tag)}
              >
                {tag}
              </div>
            ))}
          </div>
        </div>
        <button className="button-apply" onClick={handleFilter}>Ver Resultados</button>
      </div>
    </>
  );
};

export default FilterPopup;
