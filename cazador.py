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
# ANIMAL PLANET — DIAGNÓSTICO + EXTRACCIÓN MEJORADA
# ============================================================
STEALTH_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
Object.defineProperty(navigator, 'languages', { get: () => ['es-HN', 'es'] });
window.chrome = { runtime: {} };
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications' ?
    Promise.resolve({ state: Notification.permission }) :
    originalQuery(parameters)
);
"""

URL_PRINCIPAL = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"
URL_PLAYER    = "https://www.tvporinternet2.com/live/animalplanet.php"
REFERER       = URL_PRINCIPAL

async def capturar_animal_planet():
    m3u8_encontrado = None
    todas_peticiones = []

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
                "Referer": REFERER,
                "Origin": "https://www.tvporinternet2.com"
            }
        )
        await context.add_init_script(STEALTH_SCRIPT)
        page = await context.new_page()

        # Interceptar peticiones de red para depuración y captura
        async def interceptar(request):
            url = request.url
            todas_peticiones.append(url)
            if ".m3u8" in url or ".mpd" in url:
                if not any(x in url.lower() for x in ['doubleclick', 'googleads', 'sharethis']):
                    print(f"📡 Stream candidato: {url[:120]}")
                    nonlocal m3u8_encontrado
                    if not m3u8_encontrado:
                        m3u8_encontrado = url
        page.on("request", interceptar)

        try:
            # ---------- PASO 1: Cargar la página del reproductor ----------
            print(f"Cargando reproductor: {URL_PLAYER}")
            await page.goto(URL_PLAYER, wait_until="load", timeout=60000)
            print("Página cargada (evento load).")

            # Esperar un poco para que se ejecute cualquier JS inicial
            await asyncio.sleep(5)

            # ---------- PASO 2: Obtener el HTML completo ----------
            html = await page.content()
            print("--- HTML DEL REPRODUCTOR (primeros 2000 caracteres) ---")
            print(html[:2000])

            # ---------- PASO 3: Buscar en el HTML patrones de stream o iframes ----------
            # Buscar URLs de iframes que no sean de sharethis ni vacíos
            iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)
            iframes_validos = [src for src in iframes if src and 'sharethis' not in src and not src.startswith('about:')]
            print(f"\nIframes encontrados en el HTML: {iframes_validos}")

            # Buscar cualquier URL que contenga "m3u8", "token=", "expires=", o la IP codificada
            patrones_stream = re.findall(r'(https?://[^\s"\']*?(?:m3u8|token=|expires=|MTgx)[^\s"\']*)', html)
            print(f"\nPosibles enlaces de stream en HTML: {patrones_stream}")

            # Si hay un iframe distinto, navegar a él
            stream_iframe = None
            for src in iframes_validos:
                if 'live' in src or 'player' in src or 'animal' in src:
                    stream_iframe = src
                    break
            if not stream_iframe and iframes_validos:
                stream_iframe = iframes_validos[0]  # tomar el primero

            if stream_iframe:
                print(f"\nNavegando a iframe interno: {stream_iframe}")
                await page.goto(stream_iframe, wait_until="load", timeout=60000)
                await asyncio.sleep(5)
                html_interno = await page.content()
                print("--- HTML del iframe interno (primeros 2000 caracteres) ---")
                print(html_interno[:2000])
                # Buscar de nuevo patrones
                patrones_stream2 = re.findall(r'(https?://[^\s"\']*?(?:m3u8|token=|expires=|MTgx)[^\s"\']*)', html_interno)
                print(f"Posibles enlaces en iframe interno: {patrones_stream2}")

            # ---------- PASO 4: Interacción simulada en la página actual ----------
            # Intentar varios clics y esperas
            await page.mouse.move(200, 400)
            await page.wait_for_timeout(500)
            await page.mouse.click(200, 400)
            print("Toque en el centro.")

            # Selectores de play típicos
            selectores_play = [
                '.jw-icon-playback', '.jw-icon-display', '.vjs-big-play-button',
                'button[aria-label="Play"]', '.play-button', '.fp-play',
                'video', '.jwplayer', '#player'
            ]
            for sel in selectores_play:
                try:
                    el = await page.query_selector(sel)
                    if el:
                        await el.click()
                        print(f"Click en {sel}")
                        break
                except:
                    continue

            # Esperar hasta 60 segundos para capturar petición de stream
            intentos = 0
            while not m3u8_encontrado and intentos < 12:
                print(f"Esperando stream... ({intentos+1}/12)")
                await asyncio.sleep(5)
                intentos += 1

            # Último intento con JS
            if not m3u8_encontrado:
                js = """
                (() => {
                    try { if (typeof jwplayer !== 'undefined') { const pl = jwplayer().getPlaylist(); if (pl && pl[0]) return pl[0].file; } } catch(e) {}
                    try { if (typeof videojs !== 'undefined') { return videojs('player').currentSource().src; } } catch(e) {}
                    try { const v = document.querySelector('video'); if (v && v.src) return v.src; } catch(e) {}
                    return null;
                })()
                """
                js_result = await page.evaluate(js)
                if js_result and ("m3u8" in js_result or "mpd" in js_result):
                    print(f"Extraído por JS: {js_result[:120]}")
                    m3u8_encontrado = js_result

        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Imprimir todas las peticiones de red (primeras 50)
            print("\n--- DEBUG: Primeras 50 peticiones de red ---")
            for u in todas_peticiones[:50]:
                print(u[:150])
            await browser.close()

    return m3u8_encontrado


def actualizar_animal_planet():
    print("\nBuscando señal de ANIMAL PLANET...")
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
