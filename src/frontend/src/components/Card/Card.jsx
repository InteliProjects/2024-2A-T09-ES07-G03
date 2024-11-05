import React, { useState } from "react";
import '../Card/Card.css';
import Popup from "../Popup/Popup";

// Mapeamento de cores para tags
const tagColors = {
    sustentabilidade: '#8FBC8F', 
    saúde: '#C1FFC1',
    economia: '#EED5D2',
    educação: '#EEE8AA', 
    segurança: '#778899'
};

const Card = ({ title, description, tags, data, image, moreInfo }) => {
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    const handleCardClick = () => {
        setIsPopupOpen(true);
    };

    const handleClosePopup = () => {
        setIsPopupOpen(false);
    };

    return (
        <>
            <div className="card" onClick={handleCardClick} role="button">
                {image && <img src={image} alt={title} className="card-image" />}
                <div className="card-content">
                    <h1 className="card-title">{title}</h1>
                    <p className="card-description">{description}</p>
                    <div className="card-meta">
                        <div className="tag-container">
                            {tags && tags.length > 0 ? (
                                tags.map((tag, index) => {
                                    const normalizedTag = tag.trim().toLowerCase();
                                    return (
                                        <span 
                                            key={index} 
                                            className="card-tag" 
                                            style={{ backgroundColor: tagColors[normalizedTag] || '#e0e0e0' }} // Cor da tag
                                        >
                                            {tag}
                                        </span>
                                    );
                                })
                            ) : (
                                <span>Nenhuma tag disponível</span>
                            )}
                        </div>
                        <span className="card-data">{data}</span>
                    </div>
                </div>
            </div>

            {isPopupOpen && (
                <Popup
                    onClose={handleClosePopup}
                    content={{ title, description, tags, data, moreInfo }}
                />
            )}
        </>
    );
};

export default Card;
