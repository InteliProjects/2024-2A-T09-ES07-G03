import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import FilterPopup from "../FilterPopup";

// Mock para `fetch`
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve([
        { tag_name: "sustentabilidade" },
        { tag_name: "educação" },
      ]),
  })
);

describe("FilterPopup Component", () => {
  const mockOnClose = jest.fn();
  const mockOnFilter = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders the component correctly", async () => {
    render(<FilterPopup onClose={mockOnClose} onFilter={mockOnFilter} />);

    // Verifica se o título e os campos de data estão renderizados
    expect(screen.getByText("Opções de Filtragem")).toBeInTheDocument();
    expect(screen.getByLabelText("Data Inicial:")).toBeInTheDocument();
    expect(screen.getByLabelText("Data Final:")).toBeInTheDocument();

    // Espera pela renderização das tags mockadas
    await waitFor(() => {
      expect(screen.getByText("sustentabilidade")).toBeInTheDocument();
      expect(screen.getByText("educação")).toBeInTheDocument();
    });
  });

  test("handles start date and end date changes correctly", () => {
    render(<FilterPopup onClose={mockOnClose} onFilter={mockOnFilter} />);

    // Verifica a interação com o campo de Data Inicial
    const startDateInput = screen.getByLabelText("Data Inicial:");
    fireEvent.change(startDateInput, { target: { value: "2023-09-01" } });
    expect(startDateInput.value).toBe("2023-09-01");

    // Verifica a interação com o campo de Data Final
    const endDateInput = screen.getByLabelText("Data Final:");
    fireEvent.change(endDateInput, { target: { value: "2023-09-30" } });
    expect(endDateInput.value).toBe("2023-09-30");
  });

  test("calls onClose when the overlay is clicked", () => {
    render(<FilterPopup onClose={mockOnClose} onFilter={mockOnFilter} />);

    // Clica no overlay para fechar o popup
    const overlay = screen.getByRole("button", { name: "Fechar popup" });
    fireEvent.click(overlay);

    // Verifica se `onClose` foi chamado
    expect(mockOnClose).toHaveBeenCalled();
  });
});
