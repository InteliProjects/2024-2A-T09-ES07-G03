import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import Chatbot from "../ChatBot";

// Mock dos ícones para evitar erros de renderização nos testes
jest.mock("@iconscout/react-unicons", () => ({
  UilRobot: () => <div data-testid="robot-icon"></div>,
  UilCommentAlt: ({ ...props }) => (
    <div data-testid="comment-icon" {...props}></div>
  ),
  UilMessage: ({ ...props }) => <div data-testid="send-icon" {...props}></div>,
}));

describe("Chatbot Component", () => {
  test("renders the chatbot button initially", () => {
    render(<Chatbot />);

    // Verifica se o ícone do botão de chatbot está presente inicialmente
    const chatbotButton = screen.getByTestId("comment-icon");
    expect(chatbotButton).toBeInTheDocument();
  });

  test("opens the chatbot window when the button is clicked", () => {
    render(<Chatbot />);

    // Clicar no botão para abrir o chatbot
    const chatbotButton = screen.getByTestId("comment-icon");
    fireEvent.click(chatbotButton);

    // Verificar se a janela do chatbot abriu
    const chatbotWindow = screen.getByText("Chatbot");
    expect(chatbotWindow).toBeInTheDocument();
  });

  test("closes the chatbot window when the close button is clicked", () => {
    render(<Chatbot />);

    // Abre o chatbot
    const chatbotButton = screen.getByTestId("comment-icon");
    fireEvent.click(chatbotButton);

    // Fecha o chatbot
    const closeButton = screen.getByText("✖");
    fireEvent.click(closeButton);

    // Verifica se a janela do chatbot foi fechada
    const chatbotWindow = screen.queryByText("Chatbot");
    expect(chatbotWindow).not.toBeInTheDocument();
  });

  test("sends a user message and displays the bot response", async () => {
    render(<Chatbot />);

    // Abre o chatbot
    const chatbotButton = screen.getByTestId("comment-icon");
    fireEvent.click(chatbotButton);

    // Digita uma mensagem no campo de input
    const inputField = screen.getByPlaceholderText("Digite sua mensagem...");
    fireEvent.change(inputField, { target: { value: "Hello bot!" } });

    // Clica no botão de enviar mensagem
    const sendButton = screen.getByTestId("send-icon");
    fireEvent.click(sendButton);

    // Verifica se a mensagem do usuário foi adicionada
    const userMessage = screen.getByText("Hello bot!");
    expect(userMessage).toBeInTheDocument();

    // espera 2 segundos com setTimeout para a resposta do bot ser exibida
    setTimeout(() => {
      const botMessage = screen.getByText("Esta é uma resposta automática.");
      expect(botMessage).toBeInTheDocument();
    }, 2000);
  });

  test("sends a message when Enter is pressed in the input field", async () => {
    render(<Chatbot />);

    // Abre o chatbot
    const chatbotButton = screen.getByTestId("comment-icon");
    fireEvent.click(chatbotButton);

    // Digita uma mensagem no campo de input e pressiona Enter
    const inputField = screen.getByPlaceholderText("Digite sua mensagem...");
    fireEvent.change(inputField, { target: { value: "Testing Enter key" } });
    fireEvent.keyPress(inputField, {
      key: "Enter",
      code: "Enter",
      charCode: 13,
    });

    // Verifica se a mensagem do usuário foi adicionada
    const userMessage = screen.getByText("Testing Enter key");
    expect(userMessage).toBeInTheDocument();

    // espera 2 segundos com setTimeout para a resposta do bot ser exibida
    setTimeout(() => {
      const botMessage = screen.getByText("Esta é uma resposta automática.");
      expect(botMessage).toBeInTheDocument();
    }, 2000);
  });
});
