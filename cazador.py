import cloudscraper
import re
import json

def actualizar_json():
    # Usamos cloudscraper para saltar protecciones básicas
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    fuente_web = "https://www.cxtvenvivo.com/tv-en-vivo/zaz-tv"
    print(f"Buscando señal de ZAZ en: {fuente_web}")

    try:
        # 1. Obtenemos el contenido de la página principal
        response = scraper.get(fuente_web, timeout=15).text
        
        # 2. Buscamos el link .m3u8
        # Buscamos patrones comunes y también el específico de playback.studio que tienes en tu JSON
        links = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', response)
        
        # Si no aparece, buscamos dentro de iframes
        if not links:
            iframes = re.findall(r'src=["\'](https?://[^\s<>"\']+?)["\']', response)
            for frame_url in iframes:
                if 'google' in frame_url or 'facebook' in frame_url: continue
                try:
                    f_res = scraper.get(frame_url, headers={'Referer': fuente_web}, timeout=10).text
                    links.extend(re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', f_res))
                except:
                    continue

        link_valido = None
        for l in links:
            l_limpio = l.replace('\\/', '/').split('"')[0].split("'")[0]
            # Evitamos anuncios
            if any(x in l_limpio.lower() for x in ['ads', 'click', 'pop', 'wcpkck']):
                continue
            link_valido = l_limpio
            break

        if link_valido:
            print(f"¡LOGRADO! Link de ZAZ encontrado: {link_valido}")

            # 3. Actualizamos mexico.json
            with open('mexico.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for canal in data:
                # Buscamos exactamente el nombre "ZAZ"
                if canal.get('nombre') == "ZAZ":
                    canal['url'] = link_valido
                    print("URL de ZAZ actualizada en el JSON.")

            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("No se encontró ningún link .m3u8 válido para ZAZ.")

    except Exception as e:
        print(f"Error en la captura: {e}")

if __name__ == "__main__":
    actualizar_json()
