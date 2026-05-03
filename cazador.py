import cloudscraper
import re
import json
import asyncio
from playwright.async_api import async_playwright

# ============================================================
# CANAL ZAZ — sin cambios, funciona perfecto
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
# ANIMAL PLANET — ACCESO VÍA PÁGINA PRINCIPAL E IFRAME
# ============================================================
PAGINA_PRINCIPAL = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"

async def capturar_animal_planet():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process"
            ]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36",
            viewport={"width": 412, "height": 823},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
            locale="es-HN",
            timezone_id="America/Tegucigalpa",
            extra_http_headers={
                "Accept-Language": "es-HN,es;q=0.9,en;q=0.8",
                "Origin": "https://www.tvporinternet2.com"
            }
        )

        page = await context.new_page()
        m3u8_encontrado = None

        # Interceptar peticiones de red a nivel global (incluye iframes)
        page.on("request", lambda request: (
            print(f"📡 Petición: {request.url[:120]}") if ".m3u8" in request.url or ".mpd" in request.url else None,
            # Guardamos la URL si aún no tenemos una
            setattr(asyncio.get_event_loop(), '__m3u8', request.url) if (".m3u8" in request.url or ".mpd" in request.url) and not m3u8_encontrado else None
        ))
        # Nota: el truco con get_event_loop no es seguro; mejor usar una variable externa
        # Pero como estamos en async, podemos usar una variable mutable (lista)

        m3u8_capturado = []

        async def interceptar(request):
            if ".m3u8" in request.url or ".mpd" in request.url:
                print(f"📡 Stream candidato interceptado: {request.url[:120]}")
                m3u8_capturado.append(request.url)

        page.on("request", interceptar)

        try:
            print(f"Cargando página principal: {PAGINA_PRINCIPAL}")
            # Usamos 'domcontentloaded' para no esperar a que todos los anuncios carguen, pero debemos esperar un poco más
            await page.goto(PAGINA_PRINCIPAL, wait_until="domcontentloaded", timeout=60000)
            print("Página principal cargada (DOM). Esperando a que el iframe del reproductor aparezca...")

            # Esperar a que el iframe con name="player" esté presente y tenga un src
            try:
                await page.wait_for_selector('iframe[name="player"]', timeout=15000)
                print("Iframe del reproductor encontrado.")
            except:
                print("No se encontró el iframe 'player'. Continuando...")

            # Obtener el frame del iframe (puede que aún no haya cargado)
            # Damos tiempo para que cargue
            await asyncio.sleep(3)

            # Intentar acceder al frame
            frame = None
            for f in page.frames:
                if f.name == "player":
                    frame = f
                    break
            if not frame:
                print("No se pudo obtener el frame 'player'. Intentando extraer de la página principal...")
            else:
                print("Frame 'player' obtenido. Esperando a que el reproductor cargue...")
                # Dentro del frame, esperar por un elemento de reproductor
                try:
                    await frame.wait_for_selector("video, .jwplayer, .video-js", timeout=15000)
                    print("Reproductor detectado dentro del iframe.")
                except:
                    print("No se detectó reproductor visual en el iframe, pero continuamos.")

                # Simular interacción para forzar reproducción
                await frame.click("body", timeout=2000)
                # Intentar clic en botón play
                selectores_play = [
                    '.jw-icon-playback', '.jw-icon-display', '.vjs-big-play-button',
                    'button[aria-label="Play"]', '.play-button', '.fp-play',
                    'video', '.jwplayer'
                ]
                for sel in selectores_play:
                    try:
                        el = await frame.query_selector(sel)
                        if el:
                            await el.click()
                            print(f"Click en {sel} dentro del iframe")
                            break
                    except:
                        continue

            # Esperar un buen rato mientras se generan peticiones
            print("Esperando hasta 60 segundos a que aparezca un stream...")
            for i in range(12):
                await asyncio.sleep(5)
                # Intentar extraer con JS desde el frame si aún no tenemos stream
                if not m3u8_capturado and frame:
                    js_result = await frame.evaluate("""
                        (() => {
                            try { if (typeof jwplayer !== 'undefined') { const pl = jwplayer().getPlaylist(); if (pl && pl[0]) return pl[0].file; } } catch(e) {}
                            try { if (typeof videojs !== 'undefined') { return videojs('player').currentSource().src; } } catch(e) {}
                            try { const v = document.querySelector('video'); if (v && v.src) return v.src; } catch(e) {}
                            return null;
                        })()
                    """)
                    if js_result and ("m3u8" in js_result or "mpd" in js_result):
                        print(f"✅ Stream obtenido por JS: {js_result[:120]}")
                        m3u8_capturado.append(js_result)
                        break
                if m3u8_capturado:
                    break

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

        if m3u8_capturado:
            return m3u8_capturado[0]
        return None


def actualizar_animal_planet():
    print("\n🔎 Buscando señal de ANIMAL PLANET (desde la página principal)...")
    link = asyncio.run(capturar_animal_planet())

    if link:
        print(f"¡LOGRADO! Link encontrado: {link}")
        try:
            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for canal in data:
                if "ANIMAL PLANET" in canal.get('nombre', '').upper():
                    canal['url'] = link
                    print("URL de Animal Planet actualizada en usa.json.")

            with open('usa.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar: {e}")
    else:
        print("No se encontró ningún link .m3u8 válido para Animal Planet.")


# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    actualizar_zaz()
    actualizar_animal_planet()
