import xml.etree.ElementTree as ET 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
#Caso de prueba: Verificar opcion Lanzar Moneda

# Crear el árbol XML para los casos de prueba
test_cases = ET.Element("testcases")
test_case1 = ET.SubElement(test_cases, "testcase", name="Verificar opcion Lanzar Moneda")

# Descripción del caso de prueba
summary = ET.SubElement(test_case1, "summary")
summary.text = "Verificar que al seleccionar la opción 'Lanzar Moneda' en el menú desplegable, se redirige correctamente a la URL correspondiente."

# Precondiciones
preconditions = ET.SubElement(test_case1, "preconditions")
preconditions.text = "1. El navegador debe estar abierto.\n2. La página de inicio debe estar cargada."

# Pasos del caso de prueba
steps = ET.SubElement(test_case1, "steps")

# Paso 1: Abrir el menú desplegable
step1 = ET.SubElement(steps, "step")
ET.SubElement(step1, "step_number").text = "1"
ET.SubElement(step1, "actions").text = "Abrir el menú desplegable."
ET.SubElement(step1, "expectedresults").text = "El menú desplegable se muestra correctamente."

# Paso 2: Seleccionar la opción "Lanzar Moneda"
step2 = ET.SubElement(steps, "step")
ET.SubElement(step2, "step_number").text = "2"
ET.SubElement(step2, "actions").text = "Seleccionar la opción 'Lanzar Moneda' del menú."
ET.SubElement(step2, "expectedresults").text = "Debería redirigir a la página 'coinflip.html'."

# Crear el árbol XML para los resultados de las pruebas
results = ET.Element("results")

# Configuración del driver
driver = webdriver.Chrome()
driver.get("http://localhost/DecideYa/index.html") 

# Obtener la fecha y hora actual para el timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    # Verificar menú desplegable
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dropdown-btn"))
    )
    dropdown_button.click()

    # Caso de prueba a realizar: verificar redirección para la opción "Lanzar Moneda"
    option_text = "Lanzar Moneda"
    expected_url = "coinflip.html"
    
    # Localizar el enlace
    menu_option = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//a[normalize-space()="{option_text}"]'))
    )
    print(f"Opción encontrada: {option_text}")
    
    # Hacer clic y verificar URL
    menu_option.click()
    
     # Esperar 1 segundo para asegurarse de que los resultados se carguen
    time.sleep(1)

    # Capturar la pantalla y guardar la imagen como PNG
    driver.save_screenshot("test_menu_results_coinflip.png")
    
    current_url = driver.current_url
    result = "p" if expected_url in current_url else "f"
    comment = f"Redirigido correctamente a {current_url}" if result == "p" else f"Error: {option_text} no redirige a {expected_url}"

    # Crear el elemento XML para el resultado del caso de prueba
    testcase1_result = ET.SubElement(results, "testcase", external_id="CP-1")
    ET.SubElement(testcase1_result, "tester").text = "admin"
    ET.SubElement(testcase1_result, "timestamp").text = timestamp
    ET.SubElement(testcase1_result, "result").text = result
    ET.SubElement(testcase1_result, "notes").text = comment

    print(comment)

finally:
    driver.quit()

# Crear el archivo XML con el caso de prueba
tree_test_cases = ET.ElementTree(test_cases)
tree_test_cases.write("test_cases_menu_coinflip.xml", encoding="UTF-8", xml_declaration=True)

# Crear el archivo XML con los resultados de las pruebas
tree_results = ET.ElementTree(results)
tree_results.write("test_results_menu_coinflip.xml", encoding="UTF-8", xml_declaration=True)
