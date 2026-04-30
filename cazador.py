import cloudscraper
import re
import json

def actualizar_json():
    # Usamos cloudscraper para saltar la protección de Deporflix
    scraper = cloudscraper.create_scraper()
    url_fuente = "https://deporflix.net/canales/distrito-comedia/"
    
    try:
        print("Buscando link nuevo en Deporflix...")
        # 1. Obtenemos el HTML de la página
        response = scraper.get(url_fuente).text
        
        # 2. Buscamos el link .m3u8 que contiene el token
        links = re.findall(r'https?://[^\s<>"]+?\.m3u8[^\s<>"]*', response)
        
        if not links:
            print("No se encontró ningún link m3u8. Es posible que la web haya cambiado.")
            return

        nuevo_link = links[0]
        print(f"¡Link capturado!: {nuevo_link}")

        # 3. Abrimos tu archivo mexico.json para leerlo
        with open('mexico.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 4. Buscamos el canal exacto y actualizamos su URL
        # Usamos 'nombre' y 'DISTRITO COMEDIA' tal como están en tu captura
        encontrado = False
        for canal in data:
            if "DISTRITO COMEDIA" in canal['nombre']:
                canal['url'] = nuevo_link
                encontrado = True
                print("URL de DISTRITO COMEDIA actualizada en el JSON con éxito.")

        if not encontrado:
            print("No se encontró el canal 'DISTRITO COMEDIA' en el archivo JSON.")
            return

        # 5. Guardamos los cambios de vuelta en el archivo mexico.json
        with open('mexico.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Archivo guardado correctamente.")

    except Exception as e:
        print(f"Error durante la ejecución: {e}")

if __name__ == "__main__":
    actualizar_json()
