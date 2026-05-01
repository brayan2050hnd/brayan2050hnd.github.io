import cloudscraper
import yt_dlp
import re
import json

def obtener_link_youtube(url_yt):
    # Configuramos cabeceras de navegador para evitar el bloqueo de bot en YouTube
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url_yt, download=False)
            return info.get('url')
        except Exception as e:
            print(f"Error en YouTube: {e}")
            return None

def actualizar_zaz(scraper):
    fuente_zaz = "https://www.cxtvenvivo.com/tv-en-vivo/zaz-tv"
    try:
        res = scraper.get(fuente_zaz, timeout=15).text
        # Buscamos el link m3u8 en la página de ZAZ
        links = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', res)
        if links:
            link_v = links[0].replace('\\/', '/')
            with open('mexico.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            for canal in data:
                if canal.get('nombre') == "ZAZ":
                    canal['url'] = link_v
            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("¡LOGRADO!: ZAZ actualizado en mexico.json")
    except Exception as e:
        print(f"Error en ZAZ: {e}")

def actualizar_animal_planet():
    # URL del en vivo de Animal Planet
    url_yt = "https://www.youtube.com/live/2LSgooEZPsc"
    link_directo = obtener_link_youtube(url_yt)
    
    if link_directo:
        try:
            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            for canal in data:
                # Buscamos el canal en usa.json
                if "ANIMAL PLANET" in canal.get('nombre', '').upper():
                    canal['url'] = link_directo
            with open('usa.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("¡LOGRADO!: ANIMAL PLANET actualizado en usa.json")
        except Exception as e:
            print(f"Error al guardar Animal Planet: {e}")
    else:
        print("No se pudo obtener el link de YouTube para Animal Planet.")

def main():
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'android','desktop': False})
    print("Iniciando actualización de canales...")
    
    # Procesamos ambos canales sin borrar el progreso del otro
    actualizar_zaz(scraper)
    actualizar_animal_planet()
    
    print("Proceso multicanal finalizado.")

if __name__ == "__main__":
    main()
