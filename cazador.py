import cloudscraper
import re
import json
import requests
import os
import random

# ============================================================
# MOTOR DE BÚSQUEDA DE DIRECTOS DE YOUTUBE (VERSIÓN DEFINITIVA)
# ============================================================
def obtener_directo_youtube(channel_id, random_select=False):
    """
    Busca de la forma más efectiva posible si un canal está en vivo.
    Retorna el ID del video si hay directo, o None si no hay.
    """
    video_ids = []
    API_KEY = os.environ.get('YOUTUBE_API_KEY')

    # --- MÉTODO 1: API de YouTube (Sin el filtro bugueado) ---
    # Pedimos los 5 videos más recientes y revisamos nosotros mismos cuál es el directo
    if API_KEY:
        try:
            search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&order=date&type=video&maxResults=5&key={API_KEY}"
            resp = requests.get(search_url).json()
            
            for item in resp.get("items", []):
                # Revisamos si alguno de esos videos recientes está transmitiendo en este instante
                if item.get("snippet", {}).get("liveBroadcastContent") == "live":
                    vid = item["id"]["videoId"]
                    if vid not in video_ids:
                        video_ids.append(vid)
        except Exception as e:
            print(f"  [Info] Fallo en la API de YouTube: {e}")

    # --- MÉTODO 2: Extracción Web Directa (Por si la API llega a fallar) ---
    # Usamos cloudscraper en lugar de requests para evadir los bloqueos de GitHub Actions
    if not video_ids:
        try:
            url_live = f"https://www.youtube.com/channel/{channel_id}/live"
            scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})
            r = scraper.get(url_live, timeout=10)
            
            match = re.search(r'rel="canonical" href="https://www.youtube.com/watch\?v=([^"]+)"', r.text)
            if match:
                vid = match.group(1)
                # Si encuentra un ID canónico en la ruta /live, lo tomamos como válido
                video_ids.append(vid)
        except Exception as e:
            print(f"  [Info] Método Web no resolvió: {e}")

    # --- RESOLUCIÓN FINAL ---
    if not video_ids:
        return None
    
    if random_select and len(video_ids) > 1:
        return random.choice(video_ids)
    else:
        return video_ids[0]


# ============================================================
# FUNCIÓN PRINCIPAL DE YOUTUBE (HTML Y JSON)
# ============================================================
def actualizar_canal_youtube(
    canal_nombre,
    html_file,
    json_file,
    pais,
    imagen_url,
    channel_id,
    filter_live=False, 
    random_select=False
):
    print(f"\n📡 Analizando señal de {canal_nombre}...")
    
    video_id = obtener_directo_youtube(channel_id, random_select)

    if not video_id:
        print(f"❌ {canal_nombre} no está transmitiendo en este momento.")
        return

    print(f"✅ ¡Señal de {canal_nombre} capturada! Video ID: {video_id}")

    # 1. ACTUALIZAR O CREAR ARCHIVO HTML
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        # Plantilla limpia desde cero
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{canal_nombre}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ width: 100%; height: 100%; overflow: hidden; background: #000; }}
        iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }}
    </style>
</head>
<body>
    <iframe src="https://www.youtube.com/embed/VIDEO_ID?autoplay=1&rel=0&modestbranding=1&playsinline=1"
            allow="autoplay; encrypted-media"
            allowfullscreen>
    </iframe>
</body>
</html>"""

    # Reemplazo seguro del ID en el HTML
    if "VIDEO_ID" in html:
        nuevo_html = html.replace("VIDEO_ID", video_id)
    else:
        nuevo_html = re.sub(r'embed/[^"?]+', f'embed/{video_id}', html)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(nuevo_html)
    print(f"   --> Archivo {html_file} guardado correctamente.")

    # 2. ACTUALIZAR ARCHIVO JSON
    url_html_github = f"https://brayan2050hnd.github.io/{html_file}"
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    canal_existe = False
    for canal in data:
        if canal.get("nombre", "").strip().upper() == canal_nombre.strip().upper():
            canal["url"] = url_html_github
            canal_existe = True
            break

    if not canal_existe:
        data.append({
            "nombre": canal_nombre,
            "imagen": imagen_url,
            "url": url_html_github,
            "pais": pais
        })
        print(f"   --> Nuevo canal '{canal_nombre}' añadido a {json_file}.")
    else:
        print(f"   --> Ruta de '{canal_nombre}' actualizada en {json_file}.")

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ============================================================
# CANAL ZAZ — NO SE TOCA, FUNCIONA PERFECTO
# ============================================================
def actualizar_zaz():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    fuente_web = "https://www.cxtvenvivo.com/tv-en-vivo/zaz-tv"
    print(f"\nBuscando señal de ZAZ en: {fuente_web}")

    try:
        response = scraper.get(fuente_web, timeout=15).text
        
        links = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', response)
        
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
            if any(x in l_limpio.lower() for x in ['ads', 'click', 'pop', 'wcpkck']):
                continue
            link_valido = l_limpio
            break

        if link_valido:
            print(f"¡LOGRADO! Link de ZAZ encontrado: {link_valido}")

            with open('mexico.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for canal in data:
                if canal.get('nombre') == "ZAZ":
                    canal['url'] = link_valido
                    print("URL de ZAZ actualizada en el JSON.")

            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("No se encontró ningún link .m3u8 válido para ZAZ.")

    except Exception as e:
        print(f"Error en la captura: {e}")


# ============================================================
# CANAL TELEMUNDO MIAMI — extrae m3u8 de cxtvenvivo (cloudscraper)
# ============================================================
def actualizar_telemundo_miami():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    fuente_web = "https://www.cxtvenvivo.com/tv-en-vivo/telemundo-51-miami"
    print(f"\nBuscando señal de Telemundo Miami en: {fuente_web}")

    try:
        response = scraper.get(fuente_web, timeout=15).text
        
        links = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', response)
        
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
            if any(x in l_limpio.lower() for x in ['ads', 'click', 'pop', 'wcpkck']):
                continue
            link_valido = l_limpio
            break

        if link_valido:
            print(f"¡LOGRADO! Link de Telemundo Miami encontrado: {link_valido}")

            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for canal in data:
                if "TELEMUNDO MIAMI" in canal.get('nombre', '').upper():
                    canal['url'] = link_valido
                    print("URL de Telemundo Miami actualizada en el JSON.")
                    break
            else:
                print("⚠️ No se encontró 'TELEMUNDO MIAMI' en usa.json. Agregando entrada nueva.")
                data.append({
                    "nombre": "TELEMUNDO MIAMI",
                    "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Telemundo_logo_2018.svg/640px-Telemundo_logo_2018.svg.png",
                    "url": link_valido,
                    "pais": "USA"
                })

            with open('usa.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("No se encontró ningún link .m3u8 válido para Telemundo Miami.")

    except Exception as e:
        print(f"Error en la captura: {e}")


# ============================================================
# CANAL TELEMUNDO CALIFORNIA — cloudscraper (mismo método que ZAZ)
# ============================================================
def actualizar_telemundo_california():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    fuente_web = "https://www.cxtvenvivo.com/tv-en-vivo/telemundo-california"
    print(f"\nBuscando señal de Telemundo California en: {fuente_web}")

    try:
        response = scraper.get(fuente_web, timeout=15).text
        
        links = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', response)
        
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
            if any(x in l_limpio.lower() for x in ['ads', 'click', 'pop', 'wcpkck']):
                continue
            link_valido = l_limpio
            break

        if link_valido:
            print(f"¡LOGRADO! Link de Telemundo California encontrado: {link_valido}")

            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for canal in data:
                if "TELEMUNDO CALIFORNIA" in canal.get('nombre', '').upper():
                    canal['url'] = link_valido
                    print("URL de Telemundo California actualizada en el JSON.")
                    break
            else:
                print("⚠️ No se encontró 'TELEMUNDO CALIFORNIA' en usa.json. Agregando entrada nueva.")
                data.append({
                    "nombre": "TELEMUNDO CALIFORNIA",
                    "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Telemundo_logo_2018.svg/640px-Telemundo_logo_2018.svg.png",
                    "url": link_valido,
                    "pais": "USA"
                })

            with open('usa.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("No se encontró ningún link .m3u8 válido para Telemundo California.")

    except Exception as e:
        print(f"Error en la captura: {e}")


# ============================================================
# EJECUCIÓN DEL SCRIPT
# ============================================================
if __name__ == "__main__":
    print("Iniciando cacería de enlaces...")
    
    # 1. Los que no son de YouTube (Funcionan con m3u8)
    actualizar_zaz()
    actualizar_telemundo_miami()
    actualizar_telemundo_california()

    # 2. Los canales de YouTube
    actualizar_canal_youtube(
        canal_nombre="CHOLUVISION",
        html_file="choluvision.html",
        json_file="honduras.json",
        pais="HONDURAS",
        imagen_url="https://upload.wikimedia.org/wikipedia/commons/d/d6/Golden_TV_Logo.png",
        channel_id="UCdEAEJ8Sdyn0kIQ3wbcX5ow",
        filter_live=True
    )

    actualizar_canal_youtube(
        canal_nombre="TELEMUNDO FLORIDA",
        html_file="telemundo_florida.html",
        json_file="usa.json",
        pais="USA",
        imagen_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Telemundo_logo_2018.svg/640px-Telemundo_logo_2018.svg.png",
        channel_id="UCsDG_lFhRcvC14XRYVLeIfA"
    )

    actualizar_canal_youtube(
        canal_nombre="USA",
        html_file="usa.html",
        json_file="usa.json",
        pais="USA",
        imagen_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/USA_Network_logo.svg/640px-USA_Network_logo.svg.png",
        channel_id="UCAAxhCE6iHfINacI4FCx_8A",
        filter_live=True
    )

    actualizar_canal_youtube(
        canal_nombre="DISNEY CHANNEL",
        html_file="disney.html",
        json_file="usa.json",
        pais="USA",
        imagen_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Disney_Channel_logo.svg/640px-Disney_Channel_logo.svg.png",
        channel_id="UCayRpbmAiiuU50OpDPVSjwA",
        random_select=True
    )

    actualizar_canal_youtube(
        canal_nombre="UNIVERSAL KIDS",
        html_file="universal_kids.html",
        json_file="usa.json",
        pais="USA",
        imagen_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Universal_Kids_logo.svg/640px-Universal_Kids_logo.svg.png",
        channel_id="UCY26xU0-avwTJ6F6TzUZVEw"
    )
    
    print("\n✅ ¡Actualización completada!")
