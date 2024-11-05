import React, { useState } from "react";
import './Popup.css';

// Mapeamento de cores para tags
const tagColors = {
    sustentabilidade: '#8FBC8F', 
    saúde: '#C1FFC1',
    economia: '#EED5D2',
    educação: '#EEE8AA', 
    segurança: '#778899'
};

const Popup = ({ content, onClose }) => {
    const { title, description, tags, data, moreInfo } = content;

    return (
        <div className="popup-overlay">
            <div className="popup-content">
                <div className="popup-header">
                    <h2 className="popup-title">{title}</h2>
                    <button className="button-close" onClick={onClose}>✖</button>
                </div>
                <div className="popup-body">
                    <div className="popup-meta">
                        <span className="popup-data">{data}</span>
                        <div className="popup-tags">
                            {tags && tags.length > 0 ? (
                                tags.map((tag, index) => {
                                    const normalizedTag = tag.trim().toLowerCase();
                                    return (
                                        <span
                                            key={index}
                                            className="popup-tag"
                                            style={{ backgroundColor: tagColors[normalizedTag] || '#e0e0e0' }}
                                        >
                                            {tag}
                                        </span>
                                    );
                                })
                            ) : (
                                <span>Nenhuma tag disponível</span>
                            )}
                        </div>
                    </div>
                    <p>{description}</p>
                    {moreInfo && <p><strong>Mais informações:</strong> {moreInfo}</p>}
                    <button className="button-download">Baixar PDF</button>
                </div>
            </div>
        </div>
    );
};

export default Popup;
