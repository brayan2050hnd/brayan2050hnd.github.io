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
# ANIMAL PLANET — NUEVA VERSIÓN ROBUSTA
# ============================================================
STEALTH_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'languages', { get: () => ['es-HN', 'es', 'en-US', 'en'] });
Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
window.chrome = { runtime: {} };
"""

URL_PRINCIPAL = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"

async def capturar_animal_planet():
    link_encontrado = None
    m3u8_candidatos = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="es-HN",
            timezone_id="America/Tegucigalpa",
        )
        await context.add_init_script(STEALTH_SCRIPT)

        page = await context.new_page()

        # Interceptar peticiones de red (respaldo)
        def interceptar(request):
            url = request.url
            if ".m3u8" in url or ".mpd" in url:
                if not any(x in url.lower() for x in ['ads', 'doubleclick', 'googlevideo']):
                    m3u8_candidatos.append(url)
        page.on("request", interceptar)

        try:
            print("Cargando página principal...")
            await page.goto(URL_PRINCIPAL, wait_until="networkidle", timeout=60000)
            print("Página cargada.")

            # Esperar a que el reproductor esté presente
            try:
                await page.wait_for_selector("iframe, video, .jwplayer, .video-js", timeout=10000)
            except:
                print("No se detectó un reproductor estándar, continuando...")

            # Intentar extraer con JavaScript (JW Player, VideoJS, etc.)
            js_extractores = [
                "(() => { try { return jwplayer().getPlaylist()[0].file; } catch(e) { return null; } })()",
                "(() => { try { return videojs('player').currentSource().src; } catch(e) { return null; } })()",
                "(() => { try { return document.querySelector('video').src; } catch(e) { return null; } })()",
                "(() => { try { return document.querySelector('iframe').src; } catch(e) { return null; } })()",
            ]
            for js in js_extractores:
                resultado = await page.evaluate(js)
                if resultado and (resultado.startswith("http") or resultado.startswith("//")):
                    if resultado.startswith("//"):
                        resultado = "https:" + resultado
                    print(f"Extraído por JS: {resultado[:100]}...")
                    link_encontrado = resultado
                    break

            # Si no se obtuvo, dar tiempo extra y usar candidatos de red
            if not link_encontrado:
                print("Esperando 10 segundos más para capturar peticiones...")
                await asyncio.sleep(10)
                if m3u8_candidatos:
                    link_encontrado = m3u8_candidatos[0]
                    print(f"Capturado de red: {link_encontrado[:80]}...")

        except Exception as e:
            print(f"Error durante la captura: {e}")
        finally:
            await browser.close()

    return link_encontrado


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
        print("No se encontró ningún link .m3u8 para Animal Planet.")


# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    actualizar_zaz()
    actualizar_animal_planet()
