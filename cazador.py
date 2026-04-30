import cloudscraper
import re
import json

def actualizar_json():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    # URL de la página y el iframe que detectamos en el log anterior
    url_web = "https://elnovelerovariadito.com/2024/07/distrito-comedia-en-vivo/"
    url_iframe = "https://embed.ksdjugfsddeports.com/embed2/distritocomedia.html"

    print(f"Atacando fuente: {url_web}")

    try:
        # 1. Engañamos al servidor diciendo que venimos de la web oficial
        headers = {
            'Referer': url_web,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'
        }
        
        # 2. Entramos directo al reproductor
        response = scraper.get(url_iframe, headers=headers, timeout=15).text
        
        # 3. Buscamos el patrón del link que viste en Web Video Caster
        # Buscamos cualquier cosa que empiece por http y termine en .m3u8
        links = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', response)

        if not links:
            # Intento 2: Buscar links que estén "escapados" con barras (/)
            links = re.findall(r'https?:\\/\\/[^\s<>"\']+?\.m3u8', response)

        if not links:
            print("Página muy protegida. Intentando método de emergencia...")
            # Si no hay m3u8, buscamos el servidor 'saohgdasregions' que viste en tu captura
            links = re.findall(r'https?://[^\s<>"\']+?saohgdasregions[^\s<>"\']*', response)

        if links:
            nuevo_link = links[0].replace('\\/', '/').split('"')[0].split("'")[0]
            print(f"¡LO CAPTURÉ!: {nuevo_link}")

            # Actualizar el JSON
            with open('mexico.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for canal in data:
                if "DISTRITO COMEDIA" in canal.get('nombre', '').upper():
                    canal['url'] = nuevo_link

            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("mexico.json actualizado con éxito.")
        else:
            print("No se pudo extraer el link automáticamente. El servidor requiere una sesión activa.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    actualizar_json()
