import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from datetime import datetime
import time
# Caso de prueba: Verificar coincidencia entre imágenes y resultado de dados
# Crear el árbol XML para los casos de prueba
test_cases = ET.Element("testcases")
test_case1 = ET.SubElement(test_cases, "testcase", name="Verificar coincidencia entre imágenes y resultado de dados")

# Descripción del caso de prueba
summary = ET.SubElement(test_case1, "summary")
summary.text = "Verificar que las imágenes de los dados coincidan con los números mostrados en el resultado del lanzamiento."

# Precondiciones
preconditions = ET.SubElement(test_case1, "preconditions")
preconditions.text = "1. El navegador debe estar abierto.\n2. La página de lanzamiento de dados debe estar cargada."

# Pasos del caso de prueba
steps = ET.SubElement(test_case1, "steps")

# Paso 1: Hacer clic en el botón 'Lanzar Dados'
step1 = ET.SubElement(steps, "step")
ET.SubElement(step1, "step_number").text = "1"
ET.SubElement(step1, "actions").text = "Hacer clic en el botón 'Lanzar Dados'."
ET.SubElement(step1, "expectedresults").text = "Los dados muestran un resultado aleatorio con números del 1 al 6 y las imágenes coinciden con el resultado."

# Crear el árbol XML para los resultados de las pruebas
results = ET.Element("results")

# Configuración del driver
driver = webdriver.Chrome()
driver.get("http://localhost/DecideYa/html/dice.html")

# Obtener la fecha y hora actual para el timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    # Hacer clic en el botón 'Lanzar Dados'
    roll_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Lanzar Dados']"))
    )
    roll_button.click()

    time.sleep(2)
    
    # Capturar la pantalla y guardar la imagen como PNG
    driver.save_screenshot("test_dice_results.png")
    
    # Esperar a que las imágenes de los dados cambien
    dice1_img = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dice1")))
    dice2_img = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dice2")))

    # Esperar al resultado final del texto
    dice_result_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "diceResult"))
    ).text
    
    # Extraer los números mostrados en el resultado
    match = re.search(r"RESULTADO: (\d) Y (\d)", dice_result_text)
    print(dice_result_text)
    die1_result = int(match.group(1)) if match else None
    die2_result = int(match.group(2)) if match else None

    # Verificar que las imágenes coincidan con los resultados
    dice1_value = int(re.search(r"dice(\d)\.png", dice1_img.get_attribute("src")).group(1))
    dice2_value = int(re.search(r"dice(\d)\.png", dice2_img.get_attribute("src")).group(1))

    result = "p" if die1_result == dice1_value and die2_result == dice2_value else "f"
    comment = (
        f"Las imágenes coinciden con el resultado: {dice1_value} y {dice2_value}" if result == "p"
        else f"Error: Las imágenes ({dice1_value}, {dice2_value}) no coinciden con los resultados ({die1_result}, {die2_result})."
    )

    # Crear el elemento XML para el resultado del caso de prueba
    testcase1_result = ET.SubElement(results, "testcase", external_id="CP-3")
    ET.SubElement(testcase1_result, "tester").text = "admin"
    ET.SubElement(testcase1_result, "timestamp").text = timestamp
    ET.SubElement(testcase1_result, "result").text = result
    ET.SubElement(testcase1_result, "notes").text = comment

    print(comment)

finally:
    driver.quit()

# Crear el archivo XML con los casos de prueba
tree_test_cases = ET.ElementTree(test_cases)
tree_test_cases.write("test_cases_dice.xml", encoding="UTF-8", xml_declaration=True)

# Crear el archivo XML con los resultados de las pruebas
tree_results = ET.ElementTree(results)
tree_results.write("test_results_dice.xml", encoding="UTF-8", xml_declaration=True)
