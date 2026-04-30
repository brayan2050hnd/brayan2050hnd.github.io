import cloudscraper
import re
import json

def actualizar_json():
    # Creamos el scraper para simular una visita real
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    
    # ¡NUEVA FUENTE!
    fuente = "https://www.xtremo-stereo.com/distrito-comedia-en-vivo/"
    print(f"Iniciando rastreo en nueva fuente: {fuente}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com/'
        }
        
        # 1. Extraer el código fuente de la página
        response = scraper.get(fuente, headers=headers, timeout=15).text
        
        # 2. Buscar links .m3u8 en la página principal
        links = re.findall(r'(https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*)', response)
        
        # 3. Si no está a simple vista, buscar en los iframes (reproductores)
        if not links:
            print("Buscando en reproductores internos...")
            iframes = re.findall(r'src=["\'](https?://[^\s<>"\']+?)["\']', response)
            for f_url in iframes:
                # Ignorar publicidad y basura
                if any(x in f_url.lower() for x in ['.jpg', '.png', '.js', '.css', 'google', 'facebook', 'twitter']):
                    continue
                
                print(f"Revisando: {f_url}")
                try:
                    f_res = scraper.get(f_url, headers={'Referer': fuente}, timeout=10).text
                    links.extend(re.findall(r'(https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*)', f_res))
                    if links: break
                except:
                    continue

        # 4. Verificar si logramos cazar algo
        if not links:
            print("No se encontró ningún link .m3u8 en esta página.")
            return

        # Limpiar el link de caracteres extraños que a veces se cuelan
        nuevo_link = links[0].replace('\\/', '/').replace('\\', '')
        print(f"¡BINGO! Nuevo link encontrado: {nuevo_link}")

        # 5. Guardarlo en el archivo mexico.json
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
            print("¡Éxito! Archivo mexico.json actualizado correctamente con el link de xtremo-stereo.")
        else:
            print("El link ya es el correcto en el archivo json. No se hicieron cambios.")

    except Exception as e:
        print(f"Ocurrió un error en la ejecución: {e}")

if __name__ == "__main__":
    actualizar_json()
