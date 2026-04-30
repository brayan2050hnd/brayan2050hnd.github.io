import cloudscraper
import re
import json

def actualizar_json():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    # Lista de posibles fuentes para el mismo canal
    fuentes = [
        "https://deporflix.net/canales/distrito-comedia/",
        "https://deporflix.net/canal.php?id=distrito-comedia"
    ]
    
    link_final = None

    for url in fuentes:
        print(f"Probando suerte en: {url}")
        try:
            # Forzamos cabeceras de un celular real
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36',
                'Referer': 'https://deporflix.net/',
                'Accept': '*/*'
            }
            response = scraper.get(url, headers=headers, timeout=15).text
            
            # Buscamos cualquier cosa que parezca un m3u8, incluso si está roto o codificado
            encontrados = re.findall(r'(https?%3A%2F%2F%[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', response) # Links encodeados
            if not encontrados:
                encontrados = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', response) # Links normales

            if encontrados:
                link_final = encontrados[0].replace('%3A', ':').replace('%2F', '/')
                break
        except:
            continue

    if not link_final:
        print("EL TOKEN ES INVISIBLE: La web genera el link mediante una función privada de JS.")
        return

    print(f"¡LINK CAPTURADO!: {link_final}")

    # Actualizar el JSON
    with open('mexico.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for canal in data:
        if "DISTRITO COMEDIA" in canal.get('nombre', '').upper():
            canal['url'] = link_final

    with open('mexico.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("mexico.json actualizado.")

if __name__ == "__main__":
    actualizar_json()
