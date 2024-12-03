import os
import xml.etree.ElementTree as ET

def unify_test_cases_and_results(base_path):
    # Crear un árbol XML vacío para los casos de prueba unificados
    unified_test_cases = ET.Element("testcases")
    unified_test_results = ET.Element("results")

    # Recorrer todas las carpetas y archivos dentro del directorio base
    for root_dir, dirs, files in os.walk(base_path):
        for file in files:
            # Asegurarse de que 'file' sea una cadena (nombre de archivo)
            if isinstance(file, str):
                # Filtrar archivos de casos de prueba
                if file.startswith("test_cases_") and file.endswith(".xml"):
                    file_path = os.path.join(root_dir, file)
                    if os.path.getsize(file_path) > 0:  # Verificar si el archivo no está vacío
                        try:
                            tree = ET.parse(file_path)
                            root = tree.getroot()
                            for testcase in root.findall("testcase"):
                                unified_test_cases.append(testcase)  # Agregar al XML unificado de casos de prueba
                        except ET.ParseError:
                            print(f"Error al parsear el archivo: {file_path}")
                
                # Filtrar archivos de resultados de prueba
                elif file.startswith("test_results_") and file.endswith(".xml"):
                    file_path = os.path.join(root_dir, file)
                    if os.path.getsize(file_path) > 0:  # Verificar si el archivo no está vacío
                        try:
                            tree = ET.parse(file_path)
                            root = tree.getroot()
                            for testcase in root.findall("testcase"):
                                unified_test_results.append(testcase)  # Agregar al XML unificado de resultados
                        except ET.ParseError:
                            print(f"Error al parsear el archivo: {file_path}")

    # Guardar los XML unificados en el mismo directorio donde se ejecuta el script
    ET.ElementTree(unified_test_cases).write("unified_test_cases.xml", encoding="UTF-8", xml_declaration=True)
    ET.ElementTree(unified_test_results).write("unified_test_results.xml", encoding="UTF-8", xml_declaration=True)

# Obtener el directorio donde se ejecuta el script
current_directory = os.getcwd()

# Llamar a la función usando el directorio actual
unify_test_cases_and_results(current_directory)
