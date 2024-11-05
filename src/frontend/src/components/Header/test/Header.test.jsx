import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import Header from "../Header";
import FilterPopup from "../../FilterPopup/FilterPopup";
import { UilSearch, UilFilter, UilMicrophone } from "@iconscout/react-unicons";

// Mock dos ícones para evitar erros de renderização nos testes
jest.mock("@iconscout/react-unicons", () => ({
  UilSearch: (props) => <div data-testid="icon-search" {...props}></div>,
  UilFilter: (props) => <div data-testid="icon-filter" {...props}></div>,
  UilMicrophone: (props) => (
    <div data-testid="icon-microphone" {...props}></div>
  ),
}));

// Mock para o componente de FilterPopup
jest.mock("../../FilterPopup/FilterPopup", () => ({ onClose, onFilter }) => (
  <div data-testid="filter-popup">
    <button onClick={onClose} data-testid="close-filter-popup">
      Close
    </button>
  </div>
));

describe("Header Component", () => {
  const mockOnSearch = jest.fn();
  const mockOnFilter = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks(); // Limpa todos os mocks antes de cada teste
  });

  test("renders the component with search bar and icons", () => {
    render(<Header onSearch={mockOnSearch} onFilter={mockOnFilter} />);

    // Verifica se os ícones e a barra de pesquisa estão presentes
    expect(
      screen.getByPlaceholderText("Pesquisar por regulamentações...")
    ).toBeInTheDocument();
    expect(screen.getByTestId("icon-search")).toBeInTheDocument();
    expect(screen.getByTestId("icon-filter")).toBeInTheDocument();
    expect(screen.getByTestId("icon-microphone")).toBeInTheDocument();
  });

  test("calls onSearch when the search icon is clicked", () => {
    render(<Header onSearch={mockOnSearch} onFilter={mockOnFilter} />);

    // Digita uma query na barra de pesquisa
    const searchInput = screen.getByPlaceholderText(
      "Pesquisar por regulamentações..."
    );
    fireEvent.change(searchInput, { target: { value: "test query" } });

    // Clica no ícone de busca
    fireEvent.click(screen.getByTestId("icon-search"));

    // Verifica se `onSearch` foi chamado com a query correta
    expect(mockOnSearch).toHaveBeenCalledWith("test query");
  });

  test("calls onSearch when Enter key is pressed in the search input", () => {
    render(<Header onSearch={mockOnSearch} onFilter={mockOnFilter} />);

    // Digita uma query e pressiona Enter
    const searchInput = screen.getByPlaceholderText(
      "Pesquisar por regulamentações..."
    );
    fireEvent.change(searchInput, { target: { value: "another query" } });
    fireEvent.keyPress(searchInput, {
      key: "Enter",
      code: "Enter",
      charCode: 13,
    });

    // Verifica se `onSearch` foi chamado com a query correta
    expect(mockOnSearch).toHaveBeenCalledWith("another query");
  });

  test("opens and closes the filter popup when the filter icon is clicked", () => {
    render(<Header onSearch={mockOnSearch} onFilter={mockOnFilter} />);

    // Clica no ícone de filtro para abrir o popup
    fireEvent.click(screen.getByTestId("icon-filter"));
    expect(screen.getByTestId("filter-popup")).toBeInTheDocument();

    // Clica no botão de fechar dentro do popup
    fireEvent.click(screen.getByTestId("close-filter-popup"));
    expect(screen.queryByTestId("filter-popup")).not.toBeInTheDocument();
  });
});
