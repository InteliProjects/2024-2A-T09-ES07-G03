import React, { useState, useEffect } from "react";
import { UilAngleLeft, UilAngleRight } from '@iconscout/react-unicons';
import Header from "../components/Header/Header";
import Card from "../components/Card/Card";
import Chatbot from "../components/ChatBot/ChatBot";
import '../screens/MainScreen.css';
import axios from 'axios';

const MainScreen = () => {
    const [searchTerm, setSearchTerm] = useState("");
    const [regulations, setRegulations] = useState([]);
    const [filteredRegulations, setFilteredRegulations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const cardsPerPage = 10;

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://ec2-3-84-35-40.compute-1.amazonaws.com:8000/lrr');
                // const response = await axios.get('http://localhost:8000/lrr');
                setRegulations(response.data);
                setFilteredRegulations(response.data); // Inicializa as regulamentações filtradas
                setLoading(false);
            } catch (error) {
                setError("Erro ao buscar dados");
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        // Filtrar automaticamente com base no termo de pesquisa sempre que ele mudar
        handleSearch({ tags: [], startDate: '', endDate: '' });
    }, [searchTerm, regulations]); // Trigger filtering when regulations or searchTerm changes

    const handleSearch = (filters) => {
        const { startDate, endDate, tags } = filters;

        let filtered = regulations.slice();

        // Filtrar pelo termo de pesquisa
        if (searchTerm) {
            filtered = filtered.filter(item =>
                item.lrr_explanation && item.lrr_explanation.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }

        // Filtrar pelas datas
        if (startDate) {
            filtered = filtered.filter(item => new Date(item.effective_date) >= new Date(startDate));
        }
        if (endDate) {
            filtered = filtered.filter(item => new Date(item.effective_date) <= new Date(endDate));
        }

        // Filtrar pelas tags
        if (tags.length > 0) {
            filtered = filtered.filter(item =>
                item.tag_names && tags.some(tag => item.tag_names.split(', ').includes(tag))
            );
        }

        // Atualiza o estado das regulamentações filtradas
        setFilteredRegulations(filtered); 

    };

    const totalPages = Math.ceil(filteredRegulations.length / cardsPerPage);
    const currentRegulations = filteredRegulations.slice((currentPage - 1) * cardsPerPage, currentPage * cardsPerPage);

    return (
        <div>
            <Header onSearch={(term) => {
                setSearchTerm(term); // Define o termo de pesquisa
            }} onFilter={handleSearch} /> {/* Passa a função handleSearch para o Header */}

            <div className="card-container">
                {loading ? (
                    <p>Carregando...</p>
                ) : error ? (
                    <p>{error}</p>
                ) : currentRegulations.length > 0 ? (
                    currentRegulations.map((item, index) => (
                        <Card
                            key={index}
                            title={item.lrr_explanation}
                            description={`${item.regulator} ${item.lrr_type}`} 
                            data={item.effective_date}
                            tags={item.tag_names ? item.tag_names.split(', ') : []}
                        />
                    ))
                ) : (
                    <p>Nenhum resultado encontrado.</p>
                )}

                <div className="pagination">
                    <button 
                        onClick={() => setCurrentPage(currentPage - 1)} 
                        disabled={currentPage === 1}
                    >
                        <UilAngleLeft />
                    </button>
                    <span>{currentPage} / {totalPages}</span>
                    <button 
                        onClick={() => setCurrentPage(currentPage + 1)} 
                        disabled={currentPage === totalPages}
                    >
                        <UilAngleRight />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default MainScreen;