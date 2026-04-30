import cloudscraper
import re
import json

def actualizar_json():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    url_web = "https://elnovelerovariadito.com/2024/07/distrito-comedia-en-vivo/"
    url_iframe = "https://embed.ksdjugfsddeports.com/embed2/distritocomedia.html"

    print(f"Buscando señal real en: {url_web}")

    try:
        headers = {
            'Referer': url_web,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'
        }
        
        response = scraper.get(url_iframe, headers=headers, timeout=15).text
        
        # 1. Buscamos todos los links posibles
        todos_los_links = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', response)
        
        link_real = None

        # 2. Filtramos la basura
        for link in todos_los_links:
            # Limpiamos el link de caracteres residuales
            link_limpio = link.replace('\\/', '/').split('"')[0].split("'")[0]
            
            # LISTA NEGRA: Si el link tiene estas palabras, es un anuncio.
            if any(x in link_limpio.lower() for x in ['wcpkckormoghp', 'ads', 'pop', 'click', 'doubleclick']):
                continue
            
            # PRIORIDAD: Si tiene el servidor que vimos en Web Video Caster, este es el bueno.
            if 'saohgdasregions' in link_limpio:
                link_real = link_limpio
                break
            
            # Si no encontramos el prioritario, nos quedamos con el primero que no sea anuncio
            if not link_real:
                link_real = link_limpio

        if link_real:
            print(f"¡SEÑAL CAPTURADA SIN ANUNCIOS!: {link_real}")

            with open('mexico.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for canal in data:
                if "DISTRITO COMEDIA" in canal.get('nombre', '').upper():
                    canal['url'] = link_real

            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("mexico.json actualizado con la señal correcta.")
        else:
            print("No se encontró un link de video válido que no sea publicidad.")

    except Exception as e:
        print(f"Error en el rastreo: {e}")

if __name__ == "__main__":
    actualizar_json()
