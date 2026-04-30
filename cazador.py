import cloudscraper
import re
import json
import os

def actualizar_json():
    scraper = cloudscraper.create_scraper()
    url_fuente = "https://deporflix.net/canales/distrito-comedia/"
    
    try:
        # 1. Obtenemos el link nuevo
        response = scraper.get(url_fuente).text
        links = re.findall(r'https?://[^\s<>"]+?\.m3u8[^\s<>"]*', response)
        
        if not links:
            print("No se encontró el link m3u8")
            return

        nuevo_link = links[0]
        print(f"Link capturado: {nuevo_link}")

        # 2. Leemos tu archivo mexico.json
        with open('mexico.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 3. Buscamos 'Distrito Comedia' y actualizamos su URL
        # Ajusta 'name' o 'url' según como tengas escrito tu JSON
        for canal in data:
            if "Distrito Comedia" in canal['name']:
                canal['url'] = nuevo_link
                print("URL actualizada en el JSON")

        # 4. Guardamos los cambios
        with open('mexico.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    actualizar_json()

