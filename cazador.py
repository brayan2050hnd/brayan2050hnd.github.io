import cloudscraper
import re
import json

def buscar_m3u8(url, scraper):
    try:
        html = scraper.get(url).text
        # Busca el link .m3u8
        links = re.findall(r'https?://[^\s<>"]+?\.m3u8[^\s<>"]*', html)
        if links:
            return links[0]
        
        # Si no hay link, busca si hay una ventana interna (iframe)
        iframes = re.findall(r'<iframe.*?src=["\'](.*?)["\']', html)
        for frame_url in iframes:
            if "http" not in frame_url: continue # Saltar links relativos
            print(f"Probando ventana interna: {frame_url}")
            link_interno = buscar_m3u8(frame_url, scraper)
            if link_interno:
                return link_interno
        return None
    except:
        return None

def actualizar_json():
    scraper = cloudscraper.create_scraper()
    fuente = "https://deporflix.net/canales/distrito-comedia/"
    
    print(f"Buscando en: {fuente}")
    nuevo_link = buscar_m3u8(fuente, scraper)
    
    if not nuevo_link:
        print("ERROR: Sigo sin encontrar el link. Puede que la web use protección avanzada.")
        return

    print(f"¡Link encontrado!: {nuevo_link}")

    try:
        with open('mexico.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        actualizado = False
        for canal in data:
            if "DISTRITO COMEDIA" in canal.get('nombre', '').upper():
                if canal['url'] != nuevo_link:
                    canal['url'] = nuevo_link
                    actualizado = True
                    print("URL actualizada en el archivo.")
                else:
                    print("El link ya estaba actualizado.")

        if actualizado:
            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("Cambios guardados con éxito.")
            
    except Exception as e:
        print(f"Error procesando el JSON: {e}")

if __name__ == "__main__":
    actualizar_json()
