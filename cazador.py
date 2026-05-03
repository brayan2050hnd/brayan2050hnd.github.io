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
# ANIMAL PLANET — VERSIÓN FINAL: ELIMINA ANUNCIO + JS PLAY
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
        m3u8_capturado = []

        # Interceptar peticiones de red
        page.on("request", lambda request: (
            print(f"📡 Petición: {request.url[:120]}") if ".m3u8" in request.url or ".mpd" in request.url else None,
            m3u8_capturado.append(request.url) if (".m3u8" in request.url or ".mpd" in request.url) else None
        ))

        try:
            print(f"Cargando página principal: {PAGINA_PRINCIPAL}")
            await page.goto(PAGINA_PRINCIPAL, wait_until="domcontentloaded", timeout=60000)
            print("Página principal cargada (DOM). Esperando iframe 'player'...")

            # Esperar a que aparezca el iframe con name="player"
            try:
                await page.wait_for_selector('iframe[name="player"]', timeout=15000)
                print("Iframe del reproductor presente.")
            except:
                print("No se encontró el iframe 'player'. Continuando con la página principal...")

            # Dar tiempo a que el iframe cargue
            await asyncio.sleep(5)

            # Obtener el frame "player"
            frame = None
            for f in page.frames:
                if f.name == "player":
                    frame = f
                    break

            if frame:
                print("Frame 'player' obtenido. Preparando reproducción...")

                # 1. Ocultar el anuncio que bloquea los clics (id="don'tfoid")
                try:
                    await frame.evaluate("""
                        const ad = document.getElementById('don\\'tfoid');
                        if (ad) ad.style.display = 'none';
                    """)
                    print("Anuncio bloqueante ocultado.")
                except Exception as e:
                    print(f"No se pudo ocultar el anuncio: {e}")

                # 2. Intentar iniciar la reproducción con JavaScript
                js_play = """
                (() => {
                    // Intentar con JW Player
                    try {
                        if (typeof jwplayer !== 'undefined') {
                            const playlist = jwplayer().getPlaylist();
                            if (playlist && playlist[0]) {
                                // Devolver directamente la URL del stream si está disponible
                                return playlist[0].file;
                            }
                            // O forzar play
                            jwplayer().play();
                        }
                    } catch(e) {}
                    // Intentar con VideoJS
                    try {
                        if (typeof videojs !== 'undefined') {
                            const player = videojs('player');
                            player.play();
                            const src = player.currentSource().src;
                            if (src) return src;
                        }
                    } catch(e) {}
                    // Intentar con elemento <video>
                    try {
                        const v = document.querySelector('video');
                        if (v) {
                            v.play();
                            return v.src;
                        }
                    } catch(e) {}
                    return null;
                })()
                """
                resultado_js = await frame.evaluate(js_play)
                if resultado_js and ("m3u8" in resultado_js or "mpd" in resultado_js):
                    print(f"✅ Stream obtenido por JS: {resultado_js[:120]}")
                    m3u8_capturado.append(resultado_js)
                else:
                    print("JS no devolvió stream, pero se inició la reproducción (si es posible).")

                # 3. Esperar a que aparezcan peticiones de red del stream
                print("Esperando hasta 45 segundos a que se genere el stream definitivo...")
                for i in range(9):
                    if len(m3u8_capturado) > 1:  # ya tenemos al menos un candidato después del inicial
                        # El primer elemento podría ser el de antes, nos interesa el último
                        break
                    await asyncio.sleep(5)

            else:
                # Si no hay frame, esperamos un poco más a ver si aparece
                print("Esperando stream desde la página principal...")
                await asyncio.sleep(30)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

        # Tomamos el último m3u8 capturado (el más reciente, que debería ser el definitivo)
        if m3u8_capturado:
            return m3u8_capturado[-1]
        return None


def actualizar_animal_planet():
    print("\n🔎 Buscando señal de ANIMAL PLANET...")
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
