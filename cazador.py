import cloudscraper
import re
import json

def actualizar_json():
    scraper = cloudscraper.create_scraper()
    url_fuente = "https://deporflix.net/canales/distrito-comedia/"
    try:
        response = scraper.get(url_fuente).text
        links = re.findall(r'https?://[^\s<>"]+?\.m3u8[^\s<>"]*', response)
        if not links:
            print("No se encontró link m3u8 en la web")
            return
        nuevo_link = links[0]
        
        with open('mexico.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        encontrado = False
        for canal in data:
            # Buscamos 'DISTRITO COMEDIA' exactamente como está en tu foto
            if "DISTRITO COMEDIA" in canal.get('nombre', ''):
                canal['url'] = nuevo_link
                encontrado = True
                print(f"¡Canal encontrado! Nueva URL: {nuevo_link}")

        if encontrado:
            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("Archivo mexico.json guardado con éxito localmente")
        else:
            print("ERROR: No se encontró el nombre 'DISTRITO COMEDIA' en el JSON")
            # Imprime los nombres que sí encuentra para ver el error
            nombres = [c.get('nombre') for c in data[:3]]
            print(f"Nombres encontrados en el archivo: {nombres}")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    actualizar_json()
