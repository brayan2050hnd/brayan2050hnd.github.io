import cloudscraper
import re
import json

def actualizar_json():
    scraper = cloudscraper.create_scraper()
    url_fuente = "https://deporflix.net/canales/distrito-comedia/"
    try:
        response = scraper.get(url_fuente).text
        links = re.findall(r'https?://[^\s<>"]+?\.m3u8[^\s<>"]*', response)
        if not links: return

        nuevo_link = links[0]

        with open('mexico.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for canal in data:
            # Aquí está el truco: coincidir con tu mayúscula exacta
            if "DISTRITO COMEDIA" in canal['nombre']:
                canal['url'] = nuevo_link
                print("¡Actualizado!")

        with open('mexico.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    actualizar_json()
