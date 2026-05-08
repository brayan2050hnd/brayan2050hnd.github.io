import cloudscraper
import re
import json
import requests
import os
import random

# ============================================================
# FUNCIÓN UNIFICADA PARA TODOS LOS CANALES DE YOUTUBE (CORREGIDA)
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
    print(f"\nBuscando si {canal_nombre} está en vivo...")
    video_id = None

    # ----------------------------------------------------
    # ESTRATEGIA 1: Scraping del enlace /live (Infalible para streams 24/7)
    # ----------------------------------------------------
    if not random_select:
        try:
            url_live = f"https://www.youtube.com/channel/{channel_id}/live"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            # Se usan cookies para saltar el molesto aviso de consentimiento de Google
            res = requests.get(url_live, headers=headers, cookies={'CONSENT': 'YES+1'}, timeout=10)
            
            # Buscar la URL canónica del directo en el código fuente de la página
            match = re.search(r'rel="canonical" href="https://www.youtube.com/watch\?v=([^"]+)"', res.text)
            if match:
                vid = match.group(1)
                # Confirmar que es un directo activo y no un video normal
                if '"isLive":true' in res.text or 'isLiveNow' in res.text or '"isLiveBroadcast":true' in res.text:
                    video_id = vid
                    print(f"✅ [Método Web] Directo detectado: {video_id}")
        except Exception as e:
            print(f"⚠️ Error en Método Web: {e}")

    # ----------------------------------------------------
    # ESTRATEGIA 2: API de YouTube (Si falla el web o si random_select es True)
    # ----------------------------------------------------
    if not video_id:
        API_KEY = os.environ.get('YOUTUBE_API_KEY')
        if not API_KEY:
            print("❌ Error: No se encontró la clave de API de YouTube y el Método Web falló.")
            return

        print(f"Intentando con API de YouTube para {canal_nombre}...")
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"
        
        try:
            resp = requests.get(search_url).json()
            items = resp.get("items", [])
            
            if items:
                candidatos = []
                # Extraemos IDs y consultamos su estado real con el endpoint de videos
                vids = [item["id"]["videoId"] for item in items]
                ids_str = ",".join(vids)
                
                det_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ids_str}&key={API_KEY}"
                det_resp = requests.get(det_url).json()
                det_items = det_resp.get("items", [])
                
                for det in det_items:
                    # Validar estrictamente que esté en vivo en este instante
                    if det.get("snippet", {}).get("liveBroadcastContent") == "live":
                        titulo = det.get("snippet", {}).get("title", "Directo")
                        candidatos.append({"id": {"videoId": det["id"]}, "snippet": {"title": titulo}})
                
                if candidatos:
                    if random_select and len(candidatos) > 1:
                        elegido = random.choice(candidatos)
                        print(f"⚠️ [API] {len(candidatos)} directos. Selección aleatoria: {elegido['snippet']['title']}")
                    else:
                        elegido = candidatos[0]
                    video_id = elegido["id"]["videoId"]
                    print(f"✅ [API] Nuevo directo detectado: {video_id}")
        except Exception as e:
            print(f"❌ Error al buscar directos con API: {e}")

    # Si ninguna de las dos estrategias encuentra directo, abortamos actualización
    if not video_id:
        print(f"ℹ️ {canal_nombre} no está transmitiendo. No se actualiza el HTML.")
        return

    # ============================================================
    # CREACIÓN DEL HTML Y ACTUALIZACIÓN DEL JSON
    # ============================================================
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>""" + canal_nombre + """</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { width: 100%; height: 100%; overflow: hidden; background: #000; }
        iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <iframe src="https://www.youtube.com/embed/VIDEO_ID?autoplay=1&rel=0&modestbranding=1&playsinline=1"
            allow="autoplay; encrypted-media"
            allowfullscreen>
    </iframe>
</body>
</html>"""

    if "VIDEO_ID" in html:
        nuevo_html = html.replace("VIDEO_ID", video_id)
    else:
        nuevo_html = re.sub(r'embed/[^"?]+', f'embed/{video_id}', html)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(nuevo_html)
    print(f"✅ Archivo {html_file} actualizado.")

    # Actualizar JSON
    url_html = f"https://brayan2050hnd.github.io/{html_file}"
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    encontrado = False
    for canal in data:
        if canal.get("nombre", "").upper() == canal_nombre.upper():
            canal["url"] = url_html
            encontrado = True
            print(f"URL de {canal_nombre} actualizada en {json_file}.")
            break

    if not encontrado:
        print(f"⚠️ No se encontró '{canal_nombre}' en {json_file}. Agregando entrada nueva.")
        data.append({
            "nombre": canal_nombre,
            "imagen": imagen_url,
            "url": url_html,
            "pais": pais
        })

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
    print(f"Buscando señal de ZAZ en: {fuente_web}")

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
    print(f"Buscando señal de Telemundo Miami en: {fuente_web}")

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
    print(f"Buscando señal de Telemundo California en: {fuente_web}")

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
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    actualizar_zaz()
    actualizar_telemundo_miami()
    actualizar_telemundo_california()

    actualizar_canal_youtube(
        canal_nombre="CHOLUVISION",
        html_file="choluvision.html",
        json_file="honduras.json",
        pais="HONDURAS",
        imagen_url="https://upload.wikimedia.org/wikipedia/commons/d/d6/Golden_TV_Logo.png",
        channel_id="UCdEAEJ8Sdyn0kIQ3wbcX5ow",
        filter_live=True          # solo transmisiones en vivo reales
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
