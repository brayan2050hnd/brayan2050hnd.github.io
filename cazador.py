import cloudscraper
import re
import json

def actualizar_json():
    # Simulamos ser un celular Android para que no nos bloqueen
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'android',
            'desktop': False
        }
    )
    
    url_fuente = "https://deporflix.net/canales/distrito-comedia/"
    print(f"Intentando entrar a: {url_fuente}")

    try:
        # 1. Obtenemos el contenido de la web
        response = scraper.get(url_fuente, timeout=15)
        html = response.text

        # 2. Buscador ultra-sensible de links .m3u8
        # Busca links directos, entre comillas, o en código oculto
        patron = r'(https?://[\w\.\/\-\%\?\&\=\#\:]+\.m3u8[\w\.\/\-\%\?\&\=\#\:]*)'
        links = re.findall(patron, html)

        if not links:
            # Si falla, intentamos buscar dentro de los "iframes" (ventanas internas)
            frames = re.findall(r'src=["\'](https?://.*?)["\']', html)
            for f_url in frames:
                if "m3u8" not in f_url: 
                    print(f"Buscando dentro de ventana: {f_url}")
                    html_f = scraper.get(f_url).text
                    links = re.findall(patron, html_f)
                    if links: break

        if not links:
            print("ERROR: La web bloqueó al bot o cambió su estructura.")
            return

        nuevo_link = links[0].split('\\')[0].replace('"', '').replace("'", "")
        print(f"¡LO ENCONTRÉ!: {nuevo_link}")

        # 3. Actualizar el archivo JSON
        with open('mexico.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        modificado = False
        for canal in data:
            if "DISTRITO COMEDIA" in canal.get('nombre', '').upper():
                if canal['url'] != nuevo_link:
                    print(f"Cambiando link viejo por el nuevo...")
                    canal['url'] = nuevo_link
                    modificado = True

        if modificado:
            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("ARCHIVO ACTUALIZADO CON ÉXITO.")
        else:
            print("El link ya es el más reciente, no hubo cambios.")

    except Exception as e:
        print(f"FALLO CRÍTICO: {e}")

if __name__ == "__main__":
    actualizar_json()
