import React from "react";
import { render, screen, fireEvent, within } from "@testing-library/react";
import '@testing-library/jest-dom';
import Card from "../Card";

// Mock para o componente de Popup
jest.mock("../../Popup/Popup", () => ({ onClose, content }) => (
  <div data-testid="popup">
    <h1>{content.title}</h1>
    <p>{content.description}</p>
    <button onClick={onClose} data-testid="close-popup">
      Close
    </button>
  </div>
));

describe("Componente Card", () => {
  const defaultProps = {
    title: "Card Title",
    description: "This is a description",
    tags: ["saúde", "economia"],
    data: "2023-09-26",
    image: "image-url.jpg",
    moreInfo: "More information about this card",
  };

  test("renderiza o componente Card corretamente com as props fornecidas", () => {
    render(<Card {...defaultProps} />);

    // Verifica se a imagem está presente
    const imageElement = screen.getByAltText("Card Title");
    expect(imageElement).toBeInTheDocument();
    expect(imageElement).toHaveAttribute("src", "image-url.jpg");

    // Verifica se o título e a descrição estão renderizados
    const titleElement = screen.getByText("Card Title");
    const descriptionElement = screen.getByText("This is a description");
    expect(titleElement).toBeInTheDocument();
    expect(descriptionElement).toBeInTheDocument();

    // Verifica se as tags estão sendo renderizadas com as cores corretas
    const tagElements = screen.getAllByText(/saúde|economia/);
    expect(tagElements.length).toBe(2);
    expect(tagElements[0]).toHaveStyle({ backgroundColor: "#C1FFC1" }); // Cor para "saúde"
    expect(tagElements[1]).toHaveStyle({ backgroundColor: "#EED5D2" }); // Cor para "economia"
  });

  test("exibe uma mensagem de placeholder quando nenhuma tag é fornecida", () => {
    const propsWithoutTags = { ...defaultProps, tags: [] };
    render(<Card {...propsWithoutTags} />);

    // Verifica se a mensagem de placeholder aparece
    const noTagsElement = screen.getByText("Nenhuma tag disponível");
    expect(noTagsElement).toBeInTheDocument();
  });

  test("abre o popup quando o card é clicado e passa o conteúdo correto", () => {
    render(<Card {...defaultProps} />);
  
    // Simula um clique no card para abrir o popup
    const cardElement = screen.getByRole("button");
    fireEvent.click(cardElement);
  
    // Verifica se o popup foi aberto
    const popupElement = screen.getByTestId("popup");
    expect(popupElement).toBeInTheDocument();
  
    // Usar `within` para verificar o conteúdo dentro do popup
    const popupTitle = within(popupElement).getByText("Card Title");
    const popupDescription = within(popupElement).getByText("This is a description");
    
    expect(popupTitle).toBeInTheDocument();
    expect(popupDescription).toBeInTheDocument();
  });

  test("fecha o popup quando o botão de fechar é clicado", () => {
    render(<Card {...defaultProps} />);

    // Abre o popup
    const cardElement = screen.getByRole("button");
    fireEvent.click(cardElement);
    const popupElement = screen.getByTestId("popup");
    expect(popupElement).toBeInTheDocument();

    // Fecha o popup
    const closeButton = screen.getByTestId("close-popup");
    fireEvent.click(closeButton);
    expect(popupElement).not.toBeInTheDocument(); // Popup não deve mais estar no DOM
  });
});
