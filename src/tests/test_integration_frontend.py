from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

# Iniciar o WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
print("WebDriver iniciado.")

# Abrir o Frontend (React) que está rodando localmente
driver.get("http://localhost:3000")
print("Frontend aberto.")

# Esperar o carregamento da página
time.sleep(2)

# Localizar o campo de busca no Header e enviar um termo de pesquisa
search_input = driver.find_element(By.XPATH, "//input[@placeholder='Pesquisar por regulamentações...']")
search_input.send_keys("Regulamentação")
print("Termo de pesquisa enviado.")

# Submeter a busca
search_input.send_keys(Keys.RETURN)
print("Busca submetida.")

# Esperar o resultado
time.sleep(5)

# Verificar se os resultados estão sendo exibidos
results = driver.find_elements(By.CLASS_NAME, 'card-container')
assert len(results) > 0, "Nenhum resultado encontrado"
print("Resultados encontrados.")

# Testar o filtro (abrir o modal)
filter_button = driver.find_element(By.CLASS_NAME, 'icon-filter')
filter_button.click()
print("Modal de filtro aberto.")

# Espera explícita para garantir que o modal foi carregado
wait = WebDriverWait(driver, 10)

# Localizar uma tag para filtragem
tag_to_select = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Economia']")))
tag_to_select.click()
print("Tag 'Economia' selecionada.")

time.sleep(5)

# Aplicar o filtro clicando no botão "Ver Resultados"
apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Ver Resultados']")))
apply_button.click()
print("Filtro aplicado, resultados sendo carregados.")

# Esperar os resultados filtrados
time.sleep(3)

# Validar se os resultados filtrados estão sendo exibidos
filtered_results = driver.find_elements(By.CLASS_NAME, 'card-container')
assert len(filtered_results) > 0, "Filtro não retornou resultados"
print(f"{len(filtered_results)} resultados filtrados encontrados.")

# Clicar no primeiro card e verificar se o popup é exibido
first_card = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'card')))
first_card.click()
print("Primeiro card clicado.")

# Verificar se o popup foi exibido
popup = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'popup-overlay')))
assert popup.is_displayed(), "O Popup não foi exibido."
print("Popup exibido.")

# Verificar se o título do popup está correto
popup_title = driver.find_element(By.CLASS_NAME, 'popup-title')
assert popup_title.text == "Regulamentação de criptomoedas.", "Título do popup está incorreto."
print("Título do popup verificado.")

# Fechar o popup
close_button = driver.find_element(By.CLASS_NAME, 'button-close')
close_button.click()
print("Popup fechado.")

# Tentar encontrar o popup e verificar se ele foi removido
try:
    popup = driver.find_element(By.CLASS_NAME, 'popup-overlay')
    assert not popup.is_displayed(), "O Popup não foi fechado corretamente."
    print("Popup não foi fechado corretamente.")
except NoSuchElementException:
    print("O Popup foi fechado com sucesso.")

# Fechar o navegador após o teste
driver.quit()
print("Navegador fechado.")