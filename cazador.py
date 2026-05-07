import cloudscraper
import re
import json
import requests
import os

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
# CANAL CHOLUVISION — desde YouTube @choluvisioncanal27hd
# (si no hay directo, mantiene el video de referencia)
# ============================================================
def actualizar_choluvision():
    API_KEY = os.environ.get('YOUTUBE_API_KEY')
    CHANNEL_HANDLE = "@choluvisioncanal27hd"
    VIDEO_ID_REFERENCIA = "TEqTZ34X-_Q"  # Video base por defecto

    if not API_KEY:
        print("❌ Error: No se encontró la clave de API de YouTube en los secretos.")
        return

    print("\nObteniendo ID del canal de CHOLUVISION...")
    channels_url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
    try:
        ch_resp = requests.get(channels_url).json()
        items = ch_resp.get("items", [])
        if not items:
            print("❌ No se encontró el canal con el handle especificado.")
            return
        channel_id = items[0]["id"]
        print(f"ℹ️ ID del canal: {channel_id}")
    except Exception as e:
        print(f"❌ Error al obtener ID del canal: {e}")
        return

    print("Verificando si CHOLUVISION está en vivo...")
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"

    try:
        respuesta = requests.get(search_url).json()
        items = respuesta.get("items", [])

        # Si no hay directo, NO tocamos el HTML, mantenemos el que exista (con video de referencia)
        if not items:
            print("ℹ️ CHOLUVISION no está transmitiendo en este momento. No se actualiza el HTML.")
            return

        video_id = items[0]["id"]["videoId"]
        print(f"✅ Nuevo directo detectado: {video_id}")

        html_path = "choluvision.html"
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()
        except FileNotFoundError:
            # Si el archivo no existe, lo creamos con el video de referencia
            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CHOLUVISION</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ width: 100%; height: 100%; overflow: hidden; background: #000; }}
        iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }}
    </style>
</head>
<body>
    <iframe src="https://www.youtube.com/embed/{VIDEO_ID_REFERENCIA}?autoplay=1&rel=0&modestbranding=1&playsinline=1"
            allow="autoplay; encrypted-media"
            allowfullscreen>
    </iframe>
</body>
</html>"""
            # Para que el reemplazo funcione correctamente con el placeholder
            video_id = VIDEO_ID_REFERENCIA

        # Reemplazar el placeholder "VIDEO_ID" por el ID real
        if "VIDEO_ID" in html:
            nuevo_html = html.replace("VIDEO_ID", video_id)
        else:
            nuevo_html = re.sub(r'embed/[^"?]+', f'embed/{video_id}', html)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(nuevo_html)
        print("✅ Archivo choluvision.html actualizado con el nuevo directo.")

        url_html = "https://brayan2050hnd.github.io/choluvision.html"
        try:
            with open('honduras.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        encontrado = False
        for canal in data:
            if "CHOLUVISION" in canal.get('nombre', '').upper():
                canal['url'] = url_html
                encontrado = True
                print("URL de CHOLUVISION en honduras.json actualizada a la página HTML fija.")
                break

        if not encontrado:
            print("⚠️ No se encontró 'CHOLUVISION' en honduras.json. Agregando entrada nueva.")
            data.append({
                "nombre": "CHOLUVISION",
                "imagen": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Golden_TV_Logo.png",
                "url": url_html,
                "pais": "HONDURAS"
            })

        with open('honduras.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"❌ Error al verificar el directo: {e}")
# ============================================================
# CANAL TELEMUNDO FLORIDA — desde YouTube @TelemundoSeries
# ============================================================
def actualizar_telemundo_florida():
    API_KEY = os.environ.get('YOUTUBE_API_KEY')
    CHANNEL_HANDLE = "@TelemundoSeries"

    if not API_KEY:
        print("❌ Error: No se encontró la clave de API de YouTube en los secretos.")
        return

    print("\nObteniendo ID del canal de Telemundo Florida...")
    channels_url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
    try:
        ch_resp = requests.get(channels_url).json()
        items = ch_resp.get("items", [])
        if not items:
            print("❌ No se encontró el canal con el handle especificado.")
            return
        channel_id = items[0]["id"]
        print(f"ℹ️ ID del canal: {channel_id}")
    except Exception as e:
        print(f"❌ Error al obtener ID del canal: {e}")
        return

    print("Verificando si Telemundo Florida está en vivo...")
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"

    try:
        respuesta = requests.get(search_url).json()
        items = respuesta.get("items", [])

        if not items:
            print("ℹ️ Telemundo Florida no está transmitiendo en este momento. No se actualiza el HTML.")
            return

        video_id = items[0]["id"]["videoId"]
        print(f"✅ Nuevo directo detectado: {video_id}")

        html_path = "telemundo_florida.html"
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()
        except FileNotFoundError:
            html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TELEMUNDO FLORIDA</title>
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

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(nuevo_html)
        print("✅ Archivo telemundo_florida.html actualizado con el nuevo directo.")

        url_html = "https://brayan2050hnd.github.io/telemundo_florida.html"
        try:
            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        encontrado = False
        for canal in data:
            if "TELEMUNDO FLORIDA" in canal.get('nombre', '').upper():
                canal['url'] = url_html
                encontrado = True
                print("URL de Telemundo Florida en usa.json actualizada a la página HTML fija.")
                break

        if not encontrado:
            print("⚠️ No se encontró 'TELEMUNDO FLORIDA' en usa.json. Agregando entrada nueva.")
            data.append({
                "nombre": "TELEMUNDO FLORIDA",
                "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Telemundo_logo_2018.svg/640px-Telemundo_logo_2018.svg.png",
                "url": url_html,
                "pais": "USA"
            })

        with open('usa.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"❌ Error al verificar el directo: {e}")


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
# CANAL USA — desde YouTube (con filtro anti-estreno y anti-anuncios)
# ============================================================
def actualizar_usa():
    API_KEY = os.environ.get('YOUTUBE_API_KEY')
    VIDEO_ID_REFERENCIA = "Ck1H1OQRPPk"

    if not API_KEY:
        print("❌ Error: No se encontró la clave de API de YouTube en los secretos.")
        return

    print("\nObteniendo ID del canal de USA...")
    video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={VIDEO_ID_REFERENCIA}&key={API_KEY}"

    try:
        video_resp = requests.get(video_url).json()
        items = video_resp.get("items", [])
        if not items:
            print("❌ No se pudo obtener información del video.")
            return
        channel_id = items[0]["snippet"]["channelId"]
        print(f"ℹ️ ID del canal: {channel_id}")
    except Exception as e:
        print(f"❌ Error al obtener ID del canal: {e}")
        return

    print("Verificando si USA está en vivo...")
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"

    try:
        respuesta = requests.get(search_url).json()
        items = respuesta.get("items", [])

        if not items:
            print("ℹ️ USA no está transmitiendo en este momento. No se actualiza el HTML.")
            return

        video_id_candidato = items[0]["id"]["videoId"]
        detalles_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id_candidato}&key={API_KEY}"
        detalles_resp = requests.get(detalles_url).json()
        detalles_items = detalles_resp.get("items", [])

        if not detalles_items:
            print("⚠️ No se pudieron obtener detalles del video. Se omite la actualización.")
            return

        broadcast_content = detalles_items[0]["snippet"]["liveBroadcastContent"]
        print(f"   Tipo de emisión detectado: '{broadcast_content}'")

        if broadcast_content != "live":
            print(f"ℹ️ El video encontrado no es una transmisión en vivo real (es '{broadcast_content}'). No se actualiza el HTML.")
            return

        video_id_final = video_id_candidato
        print(f"✅ Nuevo directo detectado: {video_id_final}")

        html_path = "usa.html"
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()
        except FileNotFoundError:
            html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>USA</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { width: 100%; height: 100%; overflow: hidden; background: #000; }
        iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <iframe id="player" src="https://www.youtube-nocookie.com/embed/VIDEO_ID?autoplay=1&mute=1&controls=0&rel=0&modestbranding=1&playsinline=1"
            allow="autoplay; encrypted-media"
            allowfullscreen>
    </iframe>
    <script>
        setTimeout(() => {
            const iframe = document.getElementById('player');
            if (iframe) {
                iframe.contentWindow.postMessage('{"event":"command","func":"unMute","args":""}', '*');
            }
        }, 3000);

        setInterval(() => {
            try {
                const iframe = document.getElementById('player');
                if (iframe && iframe.contentWindow) {
                    iframe.contentWindow.postMessage('{"event":"command","func":"skipVideoAd","args":""}', '*');
                    const adElements = iframe.contentDocument.querySelectorAll('.ytp-ad-module, .ytp-ad-image-overlay, .ytp-ad-player-overlay');
                    adElements.forEach(el => el.remove());
                }
            } catch (e) {}
        }, 1000);
    </script>
</body>
</html>"""

        if "VIDEO_ID" in html:
            nuevo_html = html.replace("VIDEO_ID", video_id_final)
        else:
            nuevo_html = re.sub(r'embed/[^"?]+', f'embed/{video_id_final}', html)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(nuevo_html)
        print("✅ Archivo usa.html actualizado con el nuevo directo.")

        url_html = "https://brayan2050hnd.github.io/usa.html"
        try:
            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        encontrado = False
        for canal in data:
            if "USA" == canal.get('nombre', '').strip().upper():
                canal['url'] = url_html
                encontrado = True
                print("URL de USA en usa.json actualizada a la página HTML fija.")
                break

        if not encontrado:
            print("⚠️ No se encontró 'USA' en usa.json. Agregando entrada nueva.")
            data.append({
                "nombre": "USA",
                "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/USA_Network_logo.svg/640px-USA_Network_logo.svg.png",
                "url": url_html,
                "pais": "USA"
            })

        with open('usa.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"❌ Error al verificar el directo: {e}")


# ============================================================
# CANAL DISNEY CHANNEL — búsqueda en YouTube con selección aleatoria
# ============================================================
def actualizar_disney_channel():
    import random
    API_KEY = os.environ.get('YOUTUBE_API_KEY')
    CHANNEL_ID = "UCayRpbmAiiuU50OpDPVSjwA"

    if not API_KEY:
        print("❌ Error: No se encontró la clave de API de YouTube en los secretos.")
        return

    print("\nVerificando si Disney Channel España está en vivo...")
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&eventType=live&type=video&key={API_KEY}"

    try:
        respuesta = requests.get(search_url).json()
        items = respuesta.get("items", [])

        if not items:
            print("ℹ️ Disney Channel no está transmitiendo en este momento. No se actualiza el HTML.")
            return

        if len(items) > 1:
            print(f"⚠️ Se encontraron {len(items)} transmisiones en vivo. Seleccionando una aleatoriamente...")
            elegido = random.choice(items)
        else:
            elegido = items[0]

        video_id = elegido["id"]["videoId"]
        titulo = elegido["snippet"]["title"]
        print(f"✅ Transmisión seleccionada: '{titulo}' (ID: {video_id})")

        html_path = "disney.html"
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()
        except FileNotFoundError:
            html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>DISNEY CHANNEL</title>
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

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(nuevo_html)
        print("✅ Archivo disney.html actualizado.")

        url_html = "https://brayan2050hnd.github.io/disney.html"
        try:
            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        encontrado = False
        for canal in data:
            if "DISNEY CHANNEL" in canal.get('nombre', '').upper():
                canal['url'] = url_html
                encontrado = True
                print("URL de Disney Channel en usa.json actualizada.")
                break

        if not encontrado:
            print("⚠️ No se encontró 'DISNEY CHANNEL' en usa.json. Agregando entrada nueva.")
            data.append({
                "nombre": "DISNEY CHANNEL",
                "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Disney_Channel_logo.svg/640px-Disney_Channel_logo.svg.png",
                "url": url_html,
                "pais": "USA"
            })

        with open('usa.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"❌ Error al verificar el directo: {e}")


# ============================================================
# CANAL UNIVERSAL KIDS — desde YouTube (si no hay directo, mantiene el video de referencia)
# ============================================================
def actualizar_universal_kids():
    API_KEY = os.environ.get('YOUTUBE_API_KEY')
    VIDEO_ID_REFERENCIA = "XAYgvRwSFKA"

    if not API_KEY:
        print("❌ Error: No se encontró la clave de API de YouTube en los secretos.")
        return

    print("\nObteniendo ID del canal de Universal Kids...")
    # Obtener channelId a partir del video de referencia
    video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={VIDEO_ID_REFERENCIA}&key={API_KEY}"
    try:
        video_resp = requests.get(video_url).json()
        items = video_resp.get("items", [])
        if not items:
            print("❌ No se pudo obtener información del video de referencia.")
            return
        channel_id = items[0]["snippet"]["channelId"]
        print(f"ℹ️ ID del canal: {channel_id}")
    except Exception as e:
        print(f"❌ Error al obtener ID del canal: {e}")
        return

    print("Verificando si Universal Kids está en vivo...")
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"

    try:
        respuesta = requests.get(search_url).json()
        items = respuesta.get("items", [])

        # Si no hay directo, mantenemos el HTML existente (no se modifica)
        if not items:
            print("ℹ️ Universal Kids no está transmitiendo en este momento. No se actualiza el HTML.")
            return

        video_id = items[0]["id"]["videoId"]
        print(f"✅ Nuevo directo detectado: {video_id}")

        html_path = "universal_kids.html"
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()
        except FileNotFoundError:
            # Si no existe el archivo, lo creamos con el video de referencia
            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>UNIVERSAL KIDS</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ width: 100%; height: 100%; overflow: hidden; background: #000; }}
        iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }}
    </style>
</head>
<body>
    <iframe src="https://www.youtube.com/embed/{VIDEO_ID_REFERENCIA}?autoplay=1&rel=0&modestbranding=1&playsinline=1"
            allow="autoplay; encrypted-media"
            allowfullscreen>
    </iframe>
</body>
</html>"""
            video_id = VIDEO_ID_REFERENCIA  # Para que el placeholder funcione

        # Reemplazar el placeholder "VIDEO_ID" por el ID real
        if "VIDEO_ID" in html:
            nuevo_html = html.replace("VIDEO_ID", video_id)
        else:
            nuevo_html = re.sub(r'embed/[^"?]+', f'embed/{video_id}', html)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(nuevo_html)
        print("✅ Archivo universal_kids.html actualizado con el nuevo directo.")

        url_html = "https://brayan2050hnd.github.io/universal_kids.html"
        try:
            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        encontrado = False
        for canal in data:
            if "UNIVERSAL KIDS" in canal.get('nombre', '').upper():
                canal['url'] = url_html
                encontrado = True
                print("URL de Universal Kids en usa.json actualizada a la página HTML fija.")
                break

        if not encontrado:
            print("⚠️ No se encontró 'UNIVERSAL KIDS' en usa.json. Agregando entrada nueva.")
            data.append({
                "nombre": "UNIVERSAL KIDS",
                "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Universal_Kids_logo.svg/640px-Universal_Kids_logo.svg.png",
                "url": url_html,
                "pais": "USA"
            })

        with open('usa.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"❌ Error al verificar el directo: {e}")


# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    actualizar_zaz()
    actualizar_choluvision()
    actualizar_telemundo_florida()
    actualizar_telemundo_miami()
    actualizar_telemundo_california()
    actualizar_usa()
    actualizar_disney_channel()
    actualizar_universal_kids()
