import cloudscraper
import re
import json

def actualizar_json():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    fuente = "https://deporflix.net/canales/distrito-comedia/"
    print(f"Buscando en: {fuente}")

    try:
        response = scraper.get(fuente, timeout=10).text
        
        # 1. Buscar link m3u8 directo (si existe)
        links = re.findall(r'(https?://[^\s<>"]+?\.m3u8[^\s<>"]*)', response)
        
        # 2. Si no hay directo, buscar solo en IFRAMES que no sean basura
        if not links:
            iframes = re.findall(r'src=["\'](https?://.*?)["\']', response)
            for f_url in iframes:
                # IGNORAR imágenes, scripts y cosas que no son reproductores
                if any(x in f_url.lower() for x in ['.jpg', '.png', '.js', '.css', 'google', 'analytics']):
                    continue
                
                print(f"Probando reproductor: {f_url}")
                try:
                    f_html = scraper.get(f_url, timeout=5).text
                    links = re.findall(r'(https?://[^\s<>"]+?\.m3u8[^\s<>"]*)', f_html)
                    if links: break
                except:
                    continue

        if not links:
            print("ERROR: No se encontró el video. La web podría estar usando un reproductor encriptado.")
            return

        # Limpiar el link encontrado
        nuevo_link = links[0].replace('\\', '').replace('"', '').replace("'", "")
        print(f"¡Cazado!: {nuevo_link}")

        # 3. Guardar en el archivo
        with open('mexico.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        actualizado = False
        for canal in data:
            if "DISTRITO COMEDIA" in canal.get('nombre', '').upper():
                if canal['url'] != nuevo_link:
                    canal['url'] = nuevo_link
                    actualizado = True
                    print("URL actualizada en memoria.")

        if actualizado:
            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("¡EXITO: Archivo mexico.json guardado!")
        else:
            print("El link ya es el actual. No hubo cambios.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    actualizar_json()
