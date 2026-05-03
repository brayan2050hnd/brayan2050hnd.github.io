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
# ANIMAL PLANET — EMULACIÓN COMPLETA DE WEB VIDEO CASTER
# ============================================================
STEALTH_SCRIPT = """
// Eliminar rastros de automatización
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
Object.defineProperty(navigator, 'languages', { get: () => ['es-HN', 'es'] });
window.chrome = { runtime: {} };
// Sobrescribir el permiso de notificaciones para evitar bloqueos
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications' ?
    Promise.resolve({ state: Notification.permission }) :
    originalQuery(parameters)
);
"""

URL_PLAYER = "https://www.tvporinternet2.com/live/animalplanet.php"
REFERER    = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"

async def capturar_animal_planet():
    m3u8_encontrado = None
    todas_peticiones = []  # para depuración

    async with async_playwright() as p:
        # Emular un Galaxy S9 (Android Chrome)
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-web-security",           # permite iframes cross-origin
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

        # Interceptar todas las peticiones de red y registrar las relevantes
        async def interceptar(request):
            url = request.url
            todas_peticiones.append(url)
            if ".m3u8" in url or ".mpd" in url:
                # Ignorar solo las de anuncios muy obvias (pero las guardamos igual en log)
                if not any(x in url.lower() for x in ['doubleclick', 'googleads', 'sharethis']):
                    print(f"📡 Stream candidato: {url[:120]}")
                    nonlocal m3u8_encontrado
                    if not m3u8_encontrado:
                        m3u8_encontrado = url
        page.on("request", interceptar)

        try:
            print(f"Cargando reproductor móvil: {URL_PLAYER}")
            # Usamos 'load' en lugar de 'networkidle' para que no se cuelgue con anuncios
            await page.goto(URL_PLAYER, wait_until="load", timeout=60000)
            print("Página del reproductor cargada (evento load).")

            # Esperar a que el reproductor se inicialice (JW Player, video, etc.)
            try:
                await page.wait_for_selector("video, .jwplayer, .video-js, iframe", timeout=10000)
                print("Elemento reproductor detectado.")
            except:
                print("No se detectó reproductor visual, continuando...")

            # Simular interacción humana: scroll, toque en el centro (play)
            await page.mouse.move(200, 400)
            await page.wait_for_timeout(500)
            await page.mouse.click(200, 400)
            print("Toque en el centro del reproductor.")

            # Intentar hacer clic en el botón de play con selectores habituales
            selectores_play = [
                '.jw-icon-playback', '.jw-icon-display', '.vjs-big-play-button',
                'button[aria-label="Play"]', '.play-button', '.fp-play',
                'video', '.jwplayer'
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

            # Esperar un buen rato a que se genere el stream (máximo 45 segundos)
            intentos = 0
            while not m3u8_encontrado and intentos < 9:
                print(f"Esperando stream... ({intentos+1}/9)")
                await asyncio.sleep(5)
                intentos += 1

            # Si aún no apareció, intentar extraer con JavaScript
            if not m3u8_encontrado:
                js = """
                (() => {
                    // JW Player
                    try { if (typeof jwplayer !== 'undefined') { const pl = jwplayer().getPlaylist(); if (pl && pl[0]) return pl[0].file; } } catch(e) {}
                    // VideoJS
                    try { if (typeof videojs !== 'undefined') { const src = videojs('player').currentSource().src; if (src) return src; } } catch(e) {}
                    // HTML5 video
                    try { const v = document.querySelector('video'); if (v && v.src) return v.src; } catch(e) {}
                    // Buscar en todos los iframes
                    const iframes = document.querySelectorAll('iframe');
                    for (const iframe of iframes) {
                        try {
                            const v = iframe.contentDocument.querySelector('video');
                            if (v && v.src) return v.src;
                        } catch(e) {}
                    }
                    return null;
                })()
                """
                js_result = await page.evaluate(js)
                if js_result and ("m3u8" in js_result or "mpd" in js_result):
                    print(f"Extraído por JS: {js_result[:120]}")
                    m3u8_encontrado = js_result

        except Exception as e:
            print(f"Error durante la carga: {e}")
        finally:
            # Guardar todas las peticiones capturadas para depuración
            print("--- DEBUG: Primeras 30 peticiones (URLs) ---")
            for u in todas_peticiones[:30]:
                print(u[:150])
            await browser.close()

    return m3u8_encontrado


def actualizar_animal_planet():
    print("\nBuscando señal de ANIMAL PLANET (emulando Web Video Caster)...")
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
