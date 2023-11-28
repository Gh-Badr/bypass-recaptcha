from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def bypassing_google_captcha(driver, size, index_imgs):

    images_indexes = [int(i) for i in index_imgs]
    # Initialiser le navigateur Chrome
    # driver = webdriver.Chrome()

    # Accéder au site web contenant le reCAPTCHA
    # driver.get("https://mouadfiali.github.io/recaptcha-example/")

    # Configurer l'attente explicite pour les éléments
    wait = WebDriverWait(driver, 10)

    try:
        # Basculer vers l'iframe du reCAPTCHA
        # wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')))
        
        # Cliquer sur le checkbox du reCAPTCHA
        # checkbox = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border")))
        # checkbox.click()

        # Revenir au document principal
        driver.switch_to.default_content()

        # Titres possibles pour l'iframe secondaire
        titres_iframe = ["Le test reCAPTCHA expire dans deux minutes", "recaptcha challenge expires in two minutes"]

        # Variable pour suivre si l'iframe a été trouvé
        iframe_trouve = False

        # Essayer de basculer vers l'un des iframes
        for titre in titres_iframe:
            try:
                # Attendre et basculer vers l'iframe si disponible
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f'iframe[title="{titre}"]')))
                iframe_trouve = True
                break  
            except:
                # Continuer à essayer avec le prochain titre 
                continue

        # Vérifier si l'iframe a été trouvé
        if not iframe_trouve:
            raise Exception("L'iframe requis n'a pas été trouvé.")
            
        # Attendre la présence des éléments <tr>
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))

        # Trouver les éléments <tr> et les stocker
        rows = driver.find_elements(By.TAG_NAME, "tr")

        # Cliquer sur les images correspondantes
        for index in images_indexes:
            index = index - 1  # Ajustement de l'index (base 0)
            row = rows[index // size]  # Sélection de la ligne
            image = row.find_elements(By.TAG_NAME, "td")[index % size]  # Sélection de l'image
            image.click()

        # Cliquer sur le bouton de vérification
        verify = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "rc-button-default")))
        verify.click()

        # Attendre une action de l'utilisateur pour continuer
        input("Appuyez sur une touche pour continuer...")

    except Exception as e:
        print("Une erreur est survenue :", e)

    finally:
        # Garder la session du navigateur ouverte
        print("FIN")
        # driver.quit()  # Décommenter pour fermer le navigateur

# Exécuter la fonction
bypassing_google_captcha()