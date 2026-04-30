import cloudscraper
import re
import json
import base64

def decodificar_base64(texto):
    try:
        if len(texto) > 20:
            decode = base64.b64decode(texto).decode('utf-8')
            if ".m3u8" in decode:
                return decode
    except:
        pass
    return None

def actualizar_json():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    
    fuente = "https://elnovelerovariadito.com/2024/07/distrito-comedia-en-vivo/"
    print(f"Rastreando nueva página: {fuente}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com/'
        }
        
        response = scraper.get(fuente, headers=headers, timeout=15).text
        
        # 1. Buscar de forma normal
        links = re.findall(r'(https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*)', response)
        
        # 2. Si no está a simple vista, buscar en reproductores (iframes)
        if not links:
            print("Buscando en reproductores internos (iframes)...")
            iframes = re.findall(r'src=["\'](https?://[^\s<>"\']+?)["\']', response)
            
            for f_url in iframes:
                if any(x in f_url.lower() for x in ['.jpg', '.png', '.js', '.css', 'google', 'facebook', 'twitter', 'youtube']):
                    continue
                
                print(f"Revisando iframe: {f_url}")
                try:
                    f_res = scraper.get(f_url, headers={'Referer': fuente}, timeout=10).text
                    # Buscar m3u8 directo
                    links.extend(re.findall(r'(https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*)', f_res))
                    
                    # Buscar en base64 por si está encriptado
                    sospechosos = re.findall(r'["\']([A-Za-z0-9+/]{40,})={0,2}["\']', f_res)
                    for texto in sospechosos:
                        descifrado = decodificar_base64(texto)
                        if descifrado:
                            links.append(descifrado)
                            
                    if links: break
                except:
                    continue

        if not links:
            print("ERROR: No encontré el .m3u8. El código fuente oculta el link en peticiones de red.")
            return

        # Limpiar el link
        nuevo_link = links[0].replace('\\/', '/').replace('\\', '')
        print(f"¡BINGO, LO ENCONTRÉ!: {nuevo_link}")

        # Guardar en mexico.json
        with open('mexico.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        cambio = False
        for canal in data:
            if "DISTRITO COMEDIA" in canal.get('nombre', '').upper():
                if canal['url'] != nuevo_link:
                    canal['url'] = nuevo_link
                    cambio = True

        if cambio:
            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("¡Éxito! Archivo mexico.json actualizado.")
        else:
            print("El link ya está actualizado en tu JSON.")

    except Exception as e:
        print(f"Error durante el rastreo: {e}")

if __name__ == "__main__":
    actualizar_json()
