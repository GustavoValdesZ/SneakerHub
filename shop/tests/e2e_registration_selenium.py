import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def human_delay(min_sec=0.5, max_sec=2.0):
    time.sleep(random.uniform(min_sec, max_sec))

def type_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))

def run_e2e_test():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1200,1000")
    # chrome_options.add_argument("--headless") # Comment out to see if needed, but for agentic use headless is usually better unless capturing recording

    # Initialize driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print("Obteniendo la página de registro...")
        driver.get("http://127.0.0.1:8000/register/")
        human_delay(1, 2)

        # Fill: Nombre
        print("Escribiendo Nombre...")
        first_name = driver.find_element(By.NAME, "first_name")
        type_human(first_name, "Juan")
        human_delay()

        # Fill: Apellido
        print("Escribiendo Apellido...")
        last_name = driver.find_element(By.NAME, "last_name")
        type_human(last_name, "Perez")
        human_delay()

        # Fill: Correo
        print("Escribiendo Correo...")
        email = driver.find_element(By.NAME, "email")
        type_human(email, f"juan.perez.{random.randint(1000, 9999)}@example.com")
        human_delay()

        # Fill: Contraseña
        print("Escribiendo Contraseña...")
        password = driver.find_element(By.NAME, "password")
        type_human(password, "Password123!")
        human_delay()

        # Fill: Confirmar Contraseña
        print("Confirmando Contraseña...")
        confirm_password = driver.find_element(By.NAME, "confirm_password")
        type_human(confirm_password, "Password123!")
        human_delay(1, 3)

        # Submit
        print("Haciendo clic en Registrarse...")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        human_delay(2, 4)
        
        # Verify redirect
        print("Verificando redirección...")
        if "Tu Tienda de Zapatillas" in driver.page_source or "Bienvenido" in driver.page_source or "Hola, Juan" in driver.page_source:
            print("¡Prueba E2E Exitosa! Usuario registrado y redirigido al inicio.")
        else:
            print("La redirección falló o no se encontró el mensaje esperado.")
            print(f"URL actual: {driver.current_url}")

    except Exception as e:
        print(f"Ocurrió un error durante la prueba: {e}")
    finally:
        human_delay(3, 5)
        driver.quit()

if __name__ == "__main__":
    run_e2e_test()
