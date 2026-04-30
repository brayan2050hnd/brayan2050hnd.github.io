import cloudscraper
import re
import json

def actualizar_json():
    # Usamos un scraper que simula un navegador real para evitar bloqueos
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    fuente = "https://deporflix.net/canales/distrito-comedia/"
    print(f"Iniciando búsqueda profunda en: {fuente}")

    try:
        # 1. Obtener la página principal
        headers = {'Referer': 'https://deporflix.net/'}
        response = scraper.get(fuente, headers=headers, timeout=15).text
        
        # 2. Buscar todos los links posibles (m3u8, directos o en variables JS)
        # Este patrón atrapa links incluso si están dentro de código JavaScript
        patrones = [
            r'["\'](https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*?)["\']',
            r'source\s*:\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
            r'file\s*:\s*["\']([^"\']+\.m3u8[^"\']*)["\']'
        ]
        
        links_encontrados = []
        for p in patrones:
            links_encontrados.extend(re.findall(p, response))

        # 3. Si no hay links, buscar dentro de los IFRAMES de video
        if not links_encontrados:
            iframes = re.findall(r'src=["\'](https?://[^\s<>"\']+?)["\']', response)
            for f_url in iframes:
                if any(x in f_url.lower() for x in ['.jpg', '.png', '.js', '.css', 'google', 'analytics', 'facebook']):
                    continue
                
                print(f"Explorando reproductor interno: {f_url}")
                try:
                    f_res = scraper.get(f_url, headers={'Referer': fuente}, timeout=10).text
                    for p in patrones:
                        links_encontrados.extend(re.findall(p, f_res))
                    if links_encontrados: break
                except:
                    continue

        if not links_encontrados:
            print("AVISO: El video está protegido o encriptado. No se detectó URL pública.")
            return

        # Limpiar el link (quitar barras inclinadas de escape si existen)
        nuevo_link = links_encontrados[0].replace('\\/', '/')
        print(f"¡LOGRADO!: {nuevo_link}")

        # 4. Actualizar mexico.json
        with open('mexico.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        cambio = False
        for canal in data:
            if "DISTRITO COMEDIA" in canal.get('nombre', '').upper():
                if canal['url'] != nuevo_link:
                    canal['url'] = nuevo_link
                    cambio = True
                    print(f"Actualizando {canal['nombre']}...")

        if cambio:
            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("Cambios guardados en mexico.json.")
        else:
            print("El link ya es el más reciente.")

    except Exception as e:
        print(f"Error durante la ejecución: {e}")

if __name__ == "__main__":
    actualizar_json()
