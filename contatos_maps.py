from selenium import webdriver  # Importa o Selenium para automatizar o navegador
from selenium.webdriver.common.by import By  # Permite localizar elementos no DOM
from selenium.webdriver.common.keys import Keys  # Permite interagir com o teclado
from selenium.webdriver.chrome.service import Service  # Configura o serviço do ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager  # Gerencia a instalação do ChromeDriver
from selenium.webdriver.support.ui import WebDriverWait  # Aguarda elementos aparecerem na página
from selenium.webdriver.support import expected_conditions as EC  # Define condições esperadas para interações
import time  # Permite adicionar atrasos para garantir carregamento adequado

# Configura e inicializa o WebDriver
servico = Service(ChromeDriverManager().install())  # Instala e configura o ChromeDriver
navegador = webdriver.Chrome(service=servico)  # Inicializa o navegador Chrome
navegador.get("https://www.google.com.br/maps")  # Acessa o site do Google Maps

# Solicita dados ao usuário para pesquisa
cidade = input("Digite o nome da CIDADE em que você deseja prospectar os técnicos: ")  # Recebe a cidade
estado = input("Muito bem! Agora digite a sigla do ESTADO: ")  # Recebe a sigla do estado
pesquisa = f"{cidade} - {estado}, informática"  # Formata a string de pesquisa

# Localiza a barra de pesquisa e insere o texto
search_box = WebDriverWait(navegador, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="searchboxinput"]'))  # Aguarda a presença da caixa de pesquisa
)
search_box.send_keys(pesquisa)  # Insere o termo de pesquisa
navegador.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').click()  # Clica no botão de pesquisa

# Aguarda o carregamento dos resultados
WebDriverWait(navegador, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "Nv2PK"))  # Aguarda a presença dos resultados
)

def extrair_telefone():
    """Extrai o telefone da página atual."""
    try:
        telefone_element = WebDriverWait(navegador, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Telefone')]")  # Localiza o botão de telefone
        ))
        telefone = telefone_element.text  # Obtém o texto do telefone
        return telefone  # Retorna o telefone extraído
    except:
        return "Telefone não encontrado"  # Retorna mensagem caso não encontre telefone

# Inicializa a lista de telefones coletados
telefones = []

# Captura a lista de locais encontrados na pesquisa
locais = navegador.find_elements(By.CLASS_NAME, "Nv2PK")  # Obtém os locais da pesquisa

# Itera sobre cada local para extrair o telefone
for i in range(len(locais)):
    try:
        # Atualiza a lista de locais pois pode mudar após interações
        locais = navegador.find_elements(By.CLASS_NAME, "Nv2PK")  # Obtém novamente os locais
        locais[i].click()  # Clica no local atual
        time.sleep(3)  # Aguarda o carregamento da página
        
        # Extrai o telefone do local
        telefone = extrair_telefone()  # Chama a função para obter telefone
        telefones.append(telefone)  # Adiciona o telefone à lista
        print(f"{i+1}. Telefone coletado: {telefone}")  # Exibe o telefone coletado
        
        # Voltar para a lista de locais para processar o próximo
        navegador.find_element(By.XPATH, "//button[@aria-label='Voltar']").click()  # Clica no botão de voltar
        time.sleep(3)  # Aguarda o recarregamento da lista
        
    except Exception as e:
        print(f"Erro ao processar item {i+1}: {e}")  # Exibe erro caso algo dê errado

# Exibe a lista final de telefones coletados
print("Coleta finalizada. Telefones extraídos:", telefones)
navegador.quit()  # Fecha o navegador e encerra a execução
