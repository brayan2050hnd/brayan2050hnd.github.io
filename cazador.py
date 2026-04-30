import cloudscraper
import re
import json

def actualizar_json():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    url_web = "https://elnovelerovariadito.com/2024/07/distrito-comedia-en-vivo/"
    url_iframe = "https://embed.ksdjugfsddeports.com/embed2/distritocomedia.html"

    try:
        # Usamos el Referer de la web para que nos deje entrar al iframe
        headers = {'Referer': url_web}
        response = scraper.get(url_iframe, headers=headers, timeout=15).text
        
        # 1. Buscamos TODOS los posibles links m3u8
        # Esta vez usamos un patrón más amplio para no perder nada
        links_sucios = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', response)
        
        link_ganador = None

        # 2. Analizamos los links uno por uno
        for l in links_sucios:
            # Limpieza básica
            l_limpio = l.replace('\\/', '/').split('"')[0].split("'")[0]
            
            # REGLA DE ORO: Si tiene 'regionales', es el link que viste en Web Video Caster.
            # Este es el que nos interesa sí o sí.
            if 'regionales' in l_limpio.lower():
                link_ganador = l_limpio
                break
            
            # Si no hay 'regionales', aceptamos cualquier m3u8 que NO sea el anuncio wcpkck
            if not link_ganador and 'wcpkckormoghp' not in l_limpio:
                link_ganador = l_limpio

        if link_ganador:
            print(f"¡SEÑAL LOCALIZADA!: {link_ganador}")
            
            with open('mexico.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for canal in data:
                if "DISTRITO COMEDIA" in canal.get('nombre', '').upper():
                    canal['url'] = link_ganador

            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("Archivo mexico.json actualizado correctamente.")
        else:
            print("ERROR: El servidor escondió el link de 'regionales'.")

    except Exception as e:
        print(f"Fallo en el sistema: {e}")

if __name__ == "__main__":
    actualizar_json()
