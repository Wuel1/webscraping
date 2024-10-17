from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Caminho correto para o ChromeDriver
url = os.path.abspath('chromedriver_win32/chromedriver.exe')

try:
    # Inicializando o WebDriver
    driver = webdriver.Chrome(executable_path=url)
    
    # Abrindo a página do Mercado Livre
    driver.get("https://www.mercadolivre.com.br/")
    
    # Usando WebDriverWait para esperar até que o campo de pesquisa esteja interagível
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='cb1-edit']"))
    )
    
    # Interagindo com o campo de pesquisa
    search_box.send_keys("Gaveteiro")  # Digita 'Gaveteiro'
    search_box.send_keys(Keys.RETURN)  # Pressiona 'Enter'

    # Espera até que os resultados carreguem
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class,"ui-search-layout__item")]'))
    )

    items = driver.find_elements(By.XPATH, '//li[contains(@class,"ui-search-layout__item")]')

    print(f"{len(items)} itens encontrados") 
    
    item_prices = [] 

    for item in items:
        try:
            # Aguarda a presença do preço antes de tentar capturá-lo
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, './/span[contains(@class, "andes-money-amount")]'))
            )

            # Obtendo o elemento que contém o preço
            price = item.find_element(By.XPATH, './/span[contains(@class, "andes-money-amount")]')
            price_limpo = price.text.replace('\n', '').replace('R$', '').replace(',', '.').strip()  # Limpa o preço
            
            # Converte o preço para um número float
            item_prices.append(float(price_limpo))  # Adiciona o preço convertido à lista
        except Exception as e:
            print(f'Erro ao extrair o item: {e}')

    print("Preços coletados:")
    print(item_prices)

    contagem = 0

    for item in item_prices:
        contagem += item

    print(f'Montante:',{contagem})    
    print(f'Média dos preços:',contagem/len(item_prices))

except Exception as e:
    print(f'Error: {e}')

finally:
    driver.quit()