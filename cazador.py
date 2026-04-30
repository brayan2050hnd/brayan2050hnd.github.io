import cloudscraper
import re
import json
import base64

def decodificar_base64(texto):
    try:
        # Intenta traducir textos ocultos que podrían ser el link
        if len(texto) > 20:
            decode = base64.b64decode(texto).decode('utf-8')
            if ".m3u8" in decode:
                return decode
    except:
        return None
    return None

def actualizar_json():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    fuente = "https://deporflix.net/canales/distrito-comedia/"
    print(f"Iniciando búsqueda de links ocultos en: {fuente}")

    try:
        headers = {'Referer': 'https://deporflix.net/'}
        html = scraper.get(fuente, headers=headers, timeout=15).text
        
        # 1. Buscar links normales
        links = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', html)
        
        # 2. Buscar dentro de textos sospechosos (Base64)
        if not links:
            print("Buscando links encriptados...")
            sospechosos = re.findall(r'["\']([A-Za-z0-9+/]{40,})={0,2}["\']', html)
            for texto in sospechosos:
                descifrado = decodificar_base64(texto)
                if descifrado:
                    links.append(descifrado)
                    break

        # 3. Revisar reproductores internos (iframes)
        if not links:
            iframes = re.findall(r'src=["\'](https?://[^\s<>"\']+?)["\']', html)
            for f_url in iframes:
                if any(x in f_url.lower() for x in ['.jpg', '.js', 'google', 'analytics']): continue
                try:
                    f_html = scraper.get(f_url, headers={'Referer': fuente}, timeout=10).text
                    links.extend(re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', f_html))
                    if links: break
                except: continue

        if not links:
            print("LA WEB ES IMPENETRABLE: El link está protegido por tokens dinámicos.")
            return

        nuevo_link = links[0].replace('\\/', '/').split('"')[0]
        print(f"¡LO TENGO!: {nuevo_link}")

        # 4. Guardar en mexico.json
        with open('mexico.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        actualizado = False
        for canal in data:
            if "DISTRITO COMEDIA" in canal.get('nombre', '').upper():
                if canal['url'] != nuevo_link:
                    canal['url'] = nuevo_link
                    actualizado = True

        if actualizado:
            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("Archivo mexico.json actualizado correctamente.")
        else:
            print("No hubo cambios, el link ya es el correcto.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    actualizar_json()
