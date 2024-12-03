import xml.etree.ElementTree as ET 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from datetime import datetime
import time
## Caso de prrueba: Verificar coincidencia entre imagen de la moneda y el resultado

# Crear el árbol XML para los casos de prueba
test_cases = ET.Element("testcases")
test_case1 = ET.SubElement(test_cases, "testcase", name="Verificar coincidencia entre imagen de la moneda y el resultado")

# Descripción del caso de prueba
summary = ET.SubElement(test_case1, "summary")
summary.text = "Verificar que la imagen de la moneda coincida con el resultado (cara o sello) mostrado en el texto."

# Precondiciones
preconditions = ET.SubElement(test_case1, "preconditions")
preconditions.text = "1. El navegador debe estar abierto.\n2. La página de lanzamiento de moneda debe estar cargada."

# Pasos del caso de prueba
steps = ET.SubElement(test_case1, "steps")

# Paso 1: Hacer clic en el botón 'Lanzar'
step1 = ET.SubElement(steps, "step")
ET.SubElement(step1, "step_number").text = "1"
ET.SubElement(step1, "actions").text = "Hacer clic en el botón 'Lanzar'."
ET.SubElement(step1, "expectedresults").text = "La imagen de la moneda (cara o sello) debe coincidir con el texto del resultado."

# Crear el árbol XML para los resultados de las pruebas
results = ET.Element("results")

# Configuración del driver
driver = webdriver.Chrome()
driver.get("http://localhost/DecideYa/html/coinflip.html")

# Obtener la fecha y hora actual para el timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Variables para almacenar si ambos resultados fueron obtenidos
got_heads = False
got_tails = False

try:
    # Continuar lanzando hasta obtener ambos resultados
    while not (got_heads and got_tails):
        # Hacer clic en el botón 'Lanzar'
        flip_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Lanzar']"))
        )
        flip_button.click()

        # Esperar a que la animación de la moneda termine
        time.sleep(5)  # Tiempo ajustado para dar tiempo suficiente al giro de la moneda


        # Capturar la pantalla y guardar la imagen como PNG
        driver.save_screenshot("test_coinflip_results.png")
        
        # Esperar que la imagen de la moneda cambie
        coin_image = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "coin")))

        # Obtener el texto del resultado de la moneda
        coin_result_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "coinResult"))
        ).text
        
        # Extraer el resultado (Cara o Sello) del texto
        match = re.search(r"RESULTADO: (\w+)", coin_result_text)
        print(coin_result_text)
        coin_result = match.group(1) if match else None

        # Verificar que la imagen de la moneda coincida con el resultado
        coin_face = driver.find_element(By.ID, "coinCara")
        coin_tail = driver.find_element(By.ID, "coinSello")

        # Determinar cuál imagen está visible
        if "rotateY(0deg)" in coin_face.get_attribute("style"):
            visible_coin = "CARA"
        else:
            visible_coin = "SELLO"

        # Comprobar si el resultado y la imagen coinciden
        if coin_result == visible_coin:
            result = "p"
            comment = f"La imagen de la moneda coincide con el resultado: {visible_coin}"
        else:
            result = "f"
            comment = f"Error: La imagen ({visible_coin}) no coincide con el resultado ({coin_result})."

        # Crear el elemento XML para el resultado del caso de prueba
        testcase1_result = ET.SubElement(results, "testcase", external_id="CP-4")
        ET.SubElement(testcase1_result, "tester").text = "admin"
        ET.SubElement(testcase1_result, "timestamp").text = timestamp
        ET.SubElement(testcase1_result, "result").text = result
        ET.SubElement(testcase1_result, "notes").text = comment

        print(comment)

        # Marcar si se obtuvo 'Cara' o 'Sello'
        if coin_result == "CARA":
            got_heads = True
        elif coin_result == "SELLO":
            got_tails = True
finally:
    driver.quit()

# Crear el archivo XML con los casos de prueba
tree_test_cases = ET.ElementTree(test_cases)
tree_test_cases.write("test_cases_coinflip.xml", encoding="UTF-8", xml_declaration=True)

# Crear el archivo XML con los resultados de las pruebas
tree_results = ET.ElementTree(results)
tree_results.write("test_results_coinflip.xml", encoding="UTF-8", xml_declaration=True)
