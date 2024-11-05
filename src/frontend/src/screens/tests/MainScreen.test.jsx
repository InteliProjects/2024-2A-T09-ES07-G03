import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import axios from "axios";
import MainScreen from "../MainScreen";

// Corrige o mock do axios, garantindo que seja declarado antes de seu uso
jest.mock("axios", () => ({
  __esModule: true, // Permite que o Jest reconheça o `axios` como módulo ES6
  default: {
    get: jest.fn(),
  },
}));

describe("MainScreen Component", () => {
  const mockRegulations = [
    {
      lrr_explanation: "Regulamentação de Teste 1",
      regulator: "Regulador A",
      lrr_type: "Tipo 1",
      effective_date: "2024-09-25",
      tag_names: "educação, saúde",
    },
    {
      lrr_explanation: "Regulamentação de Teste 2",
      regulator: "Regulador B",
      lrr_type: "Tipo 2",
      effective_date: "2024-09-26",
      tag_names: "economia",
    },
  ];

  beforeEach(() => {
    // Define o mock de resposta para o axios
    axios.get.mockResolvedValue({ data: mockRegulations });
  });

  afterEach(() => {
    jest.clearAllMocks(); // Limpa todos os mocks após cada teste
  });

  test("renders loading state initially", async () => {
    render(<MainScreen />);

    // Verifica se a mensagem de carregamento é exibida
    expect(screen.getByText("Carregando...")).toBeInTheDocument();

    // Espera a resposta da requisição
    await waitFor(() =>
      expect(screen.queryByText("Carregando...")).not.toBeInTheDocument()
    );
  });

  test("renders error message when there is a fetch error", async () => {
    axios.get.mockRejectedValue(new Error("Erro ao buscar dados"));
    render(<MainScreen />);

    // Espera a mensagem de erro
    await waitFor(() =>
      expect(screen.getByText("Erro ao buscar dados")).toBeInTheDocument()
    );
  });

  test("renders regulations correctly after data fetch", async () => {
    render(<MainScreen />);

    // Espera a requisição e verifica se os cards são renderizados corretamente
    await waitFor(() => {
      expect(screen.getByText("Regulamentação de Teste 1")).toBeInTheDocument();
      expect(screen.getByText("Regulador A Tipo 1")).toBeInTheDocument();
      expect(screen.getByText("Regulamentação de Teste 2")).toBeInTheDocument();
      expect(screen.getByText("Regulador B Tipo 2")).toBeInTheDocument();
    });
  });

  test("applies search term and filters regulations correctly", async () => {
    render(<MainScreen />);

    // Espera os dados serem carregados
    await waitFor(() =>
      expect(screen.getByText("Regulamentação de Teste 1")).toBeInTheDocument()
    );

    // Simula a entrada de um termo de busca no Header
    const searchInput = screen.getByPlaceholderText(
      "Pesquisar por regulamentações..."
    );
    fireEvent.change(searchInput, { target: { value: "Teste 1" } });

    // Espera o termo de busca ser aplicado e verifica se apenas a regulamentação correspondente é exibida
    await waitFor(() => {
      expect(screen.getByText("Regulamentação de Teste 1")).toBeInTheDocument();
      expect(
        screen.queryByText("Regulamentação de Teste 2")
      ).not.toBeInTheDocument();
    });
  });
});
