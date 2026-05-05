import cloudscraper
import re
import json
import requests
import os
import asyncio
from playwright.async_api import async_playwright

# ============================================================
# FUNCIÓN AUXILIAR CON PLAYWRIGHT
# ============================================================
async def extraer_m3u8_con_playwright(fuente_web):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        link_valido = None

        async def interceptar(request):
            nonlocal link_valido
            if ".m3u8" in request.url:
                link_valido = request.url

        page.on("request", interceptar)
        await page.goto(fuente_web, wait_until="networkidle")
        await asyncio.sleep(5)  # esperar a que el reproductor cargue
        await browser.close()
        return link_valido


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
# CANAL CHOLUVISION — ACTUALIZA EL ARCHIVO choluvision.html
# ============================================================
def actualizar_choluvision():
    API_KEY = os.environ.get('YOUTUBE_API_KEY')
    VIDEO_ID_REFERENCIA = "TEqTZ34X-_Q"

    if not API_KEY:
        print("❌ Error: No se encontró la clave de API de YouTube en los secretos.")
        return

    print("\nObteniendo ID del canal de CHOLUVISION...")
    video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={VIDEO_ID_REFERENCIA}&key={API_KEY}"

    try:
        video_resp = requests.get(video_url).json()
        items = video_resp.get("items", [])
        if not items:
            print("❌ No se pudo obtener información del video.")
            return
        channel_id = items[0]["snippet"]["channelId"]
        print(f"ℹ️ ID del canal obtenido: {channel_id}")
    except Exception as e:
        print(f"❌ Error al obtener ID del canal: {e}")
        return

    print("Verificando si CHOLUVISION está en vivo...")
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"

    try:
        respuesta = requests.get(search_url).json()
        items = respuesta.get("items", [])

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
            html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CHOLUVISION</title>
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
            import re
            nuevo_html = re.sub(r'(embed/)[^"?]+', r'\1' + video_id, html)

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
            import re
            nuevo_html = re.sub(r'(embed/)[^"?]+', r'\1' + video_id, html)

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
# CANAL TELEMUNDO MIAMI — extrae m3u8 de cxtvenvivo
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
# CANAL TELEMUNDO ACCIÓN — extrae m3u8 de cxtvenvivo (con Playwright)
# ============================================================
def actualizar_telemundo_accion():
    fuente_web = "https://www.cxtvenvivo.com/tv-en-vivo/telemundo-accion"
    print(f"Buscando señal de Telemundo Acción en: {fuente_web}")

    try:
        link_valido = asyncio.run(extraer_m3u8_con_playwright(fuente_web))

        if link_valido:
            print(f"¡LOGRADO! Link de Telemundo Acción encontrado: {link_valido}")

            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for canal in data:
                if "TELEMUNDO ACCION" in canal.get('nombre', '').upper():
                    canal['url'] = link_valido
                    print("URL de Telemundo Acción actualizada en el JSON.")
                    break
            else:
                print("⚠️ No se encontró 'TELEMUNDO ACCION' en usa.json. Agregando entrada nueva.")
                data.append({
                    "nombre": "TELEMUNDO ACCION",
                    "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Telemundo_logo_2018.svg/640px-Telemundo_logo_2018.svg.png",
                    "url": link_valido,
                    "pais": "USA"
                })

            with open('usa.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("No se encontró ningún link .m3u8 válido para Telemundo Acción.")

    except Exception as e:
        print(f"Error en la captura: {e}")


# ============================================================
# CANAL TELEMUNDO CALIFORNIA — extrae m3u8 de cxtvenvivo (con Playwright)
# ============================================================
def actualizar_telemundo_california():
    fuente_web = "https://www.cxtvenvivo.com/tv-en-vivo/telemundo-california"
    print(f"Buscando señal de Telemundo California en: {fuente_web}")

    try:
        link_valido = asyncio.run(extraer_m3u8_con_playwright(fuente_web))

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
    actualizar_choluvision()
    actualizar_telemundo_florida()
    actualizar_telemundo_miami()
    actualizar_telemundo_accion()
    actualizar_telemundo_california()
