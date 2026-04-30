import cloudscraper
import re
import json

def actualizar_json():
    scraper = cloudscraper.create_scraper()
    url_fuente = "https://deporflix.net/canales/distrito-comedia/"
    
    try:
        # 1. Capturamos el link m3u8
        response = scraper.get(url_fuente).text
        links = re.findall(r'https?://[^\s<>"]+?\.m3u8[^\s<>"]*', response)
        
        if not links:
            print("No se encontró el link en la web")
            return

        nuevo_link = links[0]
        print(f"Link nuevo hallado: {nuevo_link}")

        # 2. Leemos el archivo mexico.json
        with open('mexico.json', 'r', encoding='utf-8') as f:
            canales = json.load(f)

        # 3. Buscamos y actualizamos
        actualizado = False
        for canal in canales:
            # Esto busca "DISTRITO COMEDIA" sin importar si hay espacios extra
            if "DISTRITO COMEDIA" in canal.get('nombre', '').upper():
                canal['url'] = nuevo_link
                actualizado = True
                print("¡Se encontró el canal y se cambió la URL!")

        # 4. Solo guardamos si realmente hubo un cambio
        if actualizado:
            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(canales, f, indent=4, ensure_ascii=False)
            print("Cambios guardados en mexico.json")
        else:
            print("OJO: No se encontró ningún canal con el nombre DISTRITO COMEDIA")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    actualizar_json()
