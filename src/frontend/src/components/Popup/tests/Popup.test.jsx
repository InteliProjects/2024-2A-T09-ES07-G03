import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Popup from '../Popup';

describe('Popup Component', () => {
  const mockOnClose = jest.fn();

  const defaultProps = {
    content: {
      title: 'Exemplo de Título',
      description: 'Esta é uma descrição de exemplo para o popup.',
      tag: 'educação',
      data: '2024-09-26',
      moreInfo: 'Aqui estão mais informações sobre o item.',
    },
    onClose: mockOnClose,
  };

  beforeEach(() => {
    jest.clearAllMocks(); // Limpa os mocks antes de cada teste
  });

  test('renders the popup with correct content', () => {
    render(<Popup {...defaultProps} />);

    // Verifica se o título está presente
    expect(screen.getByText('Exemplo de Título')).toBeInTheDocument();

    // Verifica se a descrição está presente
    expect(screen.getByText('Esta é uma descrição de exemplo para o popup.')).toBeInTheDocument();

    // Verifica se a tag e a data estão presentes
    expect(screen.getByText('educação')).toBeInTheDocument();
    expect(screen.getByText('2024-09-26')).toBeInTheDocument();

    // Verifica se as informações adicionais estão presentes
    expect(screen.getByText('Mais informações:')).toBeInTheDocument();
    expect(screen.getByText('Aqui estão mais informações sobre o item.')).toBeInTheDocument();
  });

  test('does not render "Mais informações" when moreInfo is not provided', () => {
    const noMoreInfoProps = { ...defaultProps, content: { ...defaultProps.content, moreInfo: '' } };
    render(<Popup {...noMoreInfoProps} />);

    // Verifica se "Mais informações" não está presente
    expect(screen.queryByText('Mais informações:')).not.toBeInTheDocument();
  });

  test('calls onClose when the close button is clicked', () => {
    render(<Popup {...defaultProps} />);

    // Clica no botão de fechar
    const closeButton = screen.getByText('✖');
    fireEvent.click(closeButton);

    // Verifica se `onClose` foi chamado
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  test('renders the download button and handles click', () => {
    render(<Popup {...defaultProps} />);

    // Verifica se o botão de download está presente
    const downloadButton = screen.getByText('Baixar PDF');
    expect(downloadButton).toBeInTheDocument();

    // Simula um clique no botão de download
    fireEvent.click(downloadButton);
    
    // Como a funcionalidade de download não está implementada, apenas garantimos que o botão é renderizado
    expect(downloadButton).toBeInTheDocument();
  });
});
